from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os
import uuid
import traceback
from datetime import datetime

from database import SessionLocal, engine, Base
from models import Meeting, MeetingStatus
from services.transcription import transcribe_audio
from services.summarizer import summarize_transcript

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meeting Summarizer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".mp3", ".mp4", ".wav", ".m4a", ".ogg", ".flac", ".webm"}


def process_meeting(meeting_id: int, file_path: str):
    """Background task: transcribe + summarize and update DB."""
    db = SessionLocal()
    try:
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            return

        # Step 1: Transcription
        meeting.status = MeetingStatus.TRANSCRIBING
        db.commit()

        transcript = transcribe_audio(file_path)
        meeting.transcript = transcript
        meeting.status = MeetingStatus.SUMMARIZING
        db.commit()

        # Step 2: Summarization
        result = summarize_transcript(transcript)
        meeting.summary = result.get("summary", "")
        meeting.key_decisions = result.get("key_decisions", [])
        meeting.action_items = result.get("action_items", [])
        meeting.status = MeetingStatus.DONE
        db.commit()

    except Exception as e:
        print(f"\n{'='*60}")
        print(f"ERROR processing meeting {meeting_id}:")
        traceback.print_exc()
        print(f"{'='*60}\n")
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if meeting:
            meeting.status = MeetingStatus.ERROR
            meeting.error_message = f"{type(e).__name__}: {str(e)}"
            db.commit()
    finally:
        db.close()
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)


@app.get("/")
def root():
    return {"message": "Meeting Summarizer API is running 🎙️"}


@app.post("/upload", status_code=202)
async def upload_meeting(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    unique_name = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    db = SessionLocal()
    try:
        meeting = Meeting(
            filename=file.filename,
            status=MeetingStatus.PENDING,
            created_at=datetime.utcnow(),
        )
        db.add(meeting)
        db.commit()
        db.refresh(meeting)
        meeting_id = meeting.id
    finally:
        db.close()

    background_tasks.add_task(process_meeting, meeting_id, file_path)

    return {"id": meeting_id, "message": "File uploaded. Processing started."}


@app.get("/meetings")
def list_meetings():
    db = SessionLocal()
    try:
        meetings = db.query(Meeting).order_by(Meeting.created_at.desc()).all()
        return [m.to_dict() for m in meetings]
    finally:
        db.close()


@app.get("/meetings/{meeting_id}")
def get_meeting(meeting_id: int):
    db = SessionLocal()
    try:
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")
        return meeting.to_dict()
    finally:
        db.close()


@app.delete("/meetings/{meeting_id}")
def delete_meeting(meeting_id: int):
    db = SessionLocal()
    try:
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")
        db.delete(meeting)
        db.commit()
        return {"message": "Meeting deleted"}
    finally:
        db.close()
