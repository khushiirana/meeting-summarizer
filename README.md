# 🎙️ Meeting Summarizer


> **Transform meeting chaos into actionable insights** — Automatically transcribe and summarize your meetings with AI-powered precision.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18%2B-brightgreen?style=flat-square&logo=node.js)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.100%2B-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18%2B-61dafb?style=flat-square&logo=react)](https://react.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

---

## 🎥 Project Demonstration

Watch the complete project demonstration video to see Meeting Summarizer in action!

https://github.com/khushiirana/meeting-summarizer/raw/main/demo.mp4

**Alternative Links:**
- [☁️ Watch on Google Drive (Recommended)](https://drive.google.com/file/d/16nh91Pv5UcTfKH08XtGs552v8p77aIoq/view?usp=sharing)
- [⬇️ Download Video](./demo.mp4)

## 📌 About

Meeting Summarizer is a full-stack web application designed to eliminate the friction of capturing meeting outcomes. Upload an audio file, and let AI handle the rest—**transcription, summarization, key decision extraction, and action item tracking**—all in seconds.

Built by **Khushi** as part of the **Unthinkable Internship** at VIT CDC, this project demonstrates practical applications of modern AI APIs in real-world productivity workflows.

**[View on GitHub](https://github.com/khushiirana/meeting-summarizer)**

---

## ✨ Core Features

| Feature | Details |
|---------|---------|
| 🎙️ **Multi-Format Audio Support** | MP3, WAV, MP4, M4A, OGG, FLAC, WEBM |
| 🔊 **OpenAI Whisper Integration** | Industry-grade transcription with `whisper-1` |
| 🤖 **GPT-4o Summarization** | Structured JSON output with key decisions & action items |
| 💾 **Persistent Storage** | SQLite database for all meeting history |
| ⚡ **Real-Time Updates** | Live status polling with automatic UI refresh |
| 📋 **Transcript Viewer** | Toggle full transcripts for every meeting |
| 🗑️ **Session Management** | Delete meetings with one click |
| 🎨 **Responsive UI** | Mobile-friendly design with Tailwind CSS |

---

## 🛠️ Tech Stack

### **Frontend**
- **React 18** + Vite (lightning-fast dev experience)
- **Tailwind CSS** (utility-first styling)
- **Axios** (HTTP client for API communication)

### **Backend**
- **FastAPI** (modern, async Python framework)
- **Uvicorn** (production-ready ASGI server)
- **SQLAlchemy** (ORM for database management)
- **SQLite** (lightweight, zero-configuration database)

### **AI Services**
- **OpenAI Whisper API** → Transcription
- **OpenAI GPT-4o** → Summarization & NLP

---

## 📁 Project Structure

```
meeting-summarizer/
├── 📂 backend/
│   ├── main.py                      # FastAPI application & endpoints
│   ├── database.py                  # SQLAlchemy engine & session setup
│   ├── models.py                    # Meeting SQLAlchemy model
│   ├── 📂 services/
│   │   ├── transcription.py         # Whisper API client
│   │   └── summarizer.py            # GPT-4o summarization logic
│   ├── requirements.txt             # Python dependencies
│   └── .env.example                 # Environment template
│
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── 📂 api/
│   │   │   └── client.js            # Axios API client instance
│   │   ├── 📂 components/
│   │   │   ├── AudioUploader.jsx    # File upload handler
│   │   │   ├── MeetingCard.jsx      # Individual meeting display
│   │   │   └── MeetingList.jsx      # Meeting list container
│   │   ├── App.jsx                  # Root component
│   │   └── index.css                # Global styles
│   ├── tailwind.config.js           # Tailwind configuration
│   ├── vite.config.js               # Vite bundler config
│   └── package.json                 # Node dependencies
│
├── .gitignore
├── README.md                        # This file
└── LICENSE                          # MIT License
```

---

## 🚀 Quick Start

### Prerequisites
- **Python** 3.9 or higher
- **Node.js** 18 or higher  
- **OpenAI API Key** ([Get one free](https://platform.openai.com/account/api-keys))

### 1️⃣ Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here
```

**Start the server:**
```bash
uvicorn main:app --reload --port 8000
```

✅ Backend running at: **http://localhost:8000**  
📚 API Documentation: **http://localhost:8000/docs** (Interactive Swagger UI)

---

### 2️⃣ Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start development server
npm run dev
```

✅ Frontend running at: **http://localhost:5173**

---

## 📡 API Endpoints

All endpoints are documented in the **Swagger UI** at `http://localhost:8000/docs`

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `POST` | `/upload` | Upload and process audio file | `multipart/form-data` (audio file) |
| `GET` | `/meetings` | Retrieve all processed meetings | — |
| `GET` | `/meetings/{id}` | Get specific meeting details | — |
| `DELETE` | `/meetings/{id}` | Remove a meeting | — |

### Example: Upload a Meeting

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@meeting.mp3"
```

**Response:**
```json
{
  "id": "uuid-here",
  "filename": "meeting.mp3",
  "status": "PENDING",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## 🤖 How It Works

### 1. **Upload** 📤
User uploads an audio file (any supported format)

### 2. **Transcribe** 🔊
OpenAI Whisper API converts audio → accurate text transcription

### 3. **Summarize** 🧠
GPT-4o processes the transcript and outputs:
- **Summary** — 2-4 sentence overview
- **Key Decisions** — Critical outcomes from the meeting
- **Action Items** — Tasks with assigned owners

### 4. **Store** 💾
Meeting record persisted in SQLite with full transcript & summary

### 5. **Display** 📊
Frontend renders results with toggleable transcript view

---

## 📊 Meeting Status States

```
┌─────────┐    ┌──────────────┐    ┌────────────┐    ┌──────┐
│ PENDING │───▶│ TRANSCRIBING │───▶│ SUMMARIZING│───▶│ DONE │
└─────────┘    └──────────────┘    └────────────┘    └──────┘
                                            │
                                            └─────▶ ERROR
```

---

## 🎙️ Supported Audio Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| MP3 | `.mp3` | Most common format |
| WAV | `.wav` | Uncompressed audio |
| MPEG-4 | `.mp4`, `.m4a` | Video files & audio containers |
| OGG | `.ogg` | Open-source format |
| FLAC | `.flac` | Lossless compression |
| WebM | `.webm` | Web media format |

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Required: Your OpenAI API key
OPENAI_API_KEY=sk-your-api-key-here

# Optional: Database path (defaults to ./meetings.db)
DATABASE_URL=sqlite:///./meetings.db

# Optional: API port
API_PORT=8000

# Optional: CORS origins
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 🧪 Testing

### Test the API
```bash
# Using curl
curl -X GET "http://localhost:8000/meetings" \
  -H "Content-Type: application/json"

# Using Python
import requests
response = requests.get("http://localhost:8000/meetings")
print(response.json())
```

### Test Audio Upload
```bash
# Upload a test MP3 file
curl -X POST "http://localhost:8000/upload" \
  -F "file=@test-meeting.mp3"
```

---

## 📦 Dependencies

### Backend (`requirements.txt`)
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
openai==1.3.0
python-multipart==0.0.6
python-dotenv==1.0.0
```

### Frontend (`package.json`)
```
"react": "^18.2.0"
"vite": "^5.0.0"
"axios": "^1.6.0"
"tailwindcss": "^3.3.0"
```

---

## 🚨 Troubleshooting

### Issue: "OpenAI API Key not found"
**Solution:** Ensure `.env` file exists in `backend/` with `OPENAI_API_KEY=sk-...`

### Issue: CORS error when uploading files
**Solution:** Check that frontend URL is in `CORS_ORIGINS` in `.env`

### Issue: Audio file upload fails
**Solution:** 
- Verify file format is supported
- Check file size is reasonable (< 25MB recommended)
- Ensure backend is running (`uvicorn main:app --reload`)

### Issue: "Port 8000 already in use"
**Solution:** Use a different port:
```bash
uvicorn main:app --reload --port 8001
```

### Issue: Slow transcription
**Solution:**
- Smaller files transcribe faster
- Split long meetings into chunks
- Whisper API processes up to 25MB files

---

## 💡 Features Roadmap

- [ ] **Batch Processing** — Upload multiple files simultaneously
- [ ] **Speaker Diarization** — Identify who said what
- [ ] **Custom Summaries** — User-configurable summary length & style
- [ ] **Export Formats** — PDF, DOCX, Markdown outputs
- [ ] **Real-Time Transcription** — Live meeting transcription
- [ ] **Meeting Insights** — Sentiment analysis, meeting duration metrics
- [ ] **Team Collaboration** — Share meetings and summaries with teams
- [ ] **Webhook Integrations** — Sync with Slack, Microsoft Teams, Notion

---

## 🤝 Contributing

Contributions are welcome! Whether it's bug fixes, feature requests, or improvements—let's build together.

### Steps to Contribute:
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines:
- Follow **PEP 8** for Python code
- Use **ESLint** for JavaScript/React
- Write **descriptive commit messages**
- Test your changes before submitting

---

## 📋 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

Free to use for personal, academic, and commercial purposes.

---

## 👋 About the Author

**Khushi** (ID: 25MCA0075)  
**VIT Chennai — Center for Development of Computing (CDC)**  
**Unthinkable Internship Program**

💼 Building practical AI applications that solve real problems.

---

## 📧 Support & Questions

Have questions or found a bug? Here are your options:

- 📂 **GitHub Issues** — [Submit an issue](https://github.com/khushiirana/meeting-summarizer/issues)
- 💬 **Discussions** — [Join the discussion](https://github.com/khushiirana/meeting-summarizer/discussions)
- 🐛 **Bug Reports** — Please include:
  - Python/Node version
  - Error message & stack trace
  - Steps to reproduce
  - Operating system

---

## 🙏 Acknowledgments

- **OpenAI** — Whisper & GPT-4o APIs
- **VIT CDC** — Project guidance & mentorship
- **FastAPI & React Communities** — Amazing tools & documentation

---

<div align="center">

**Made with ❤️ by Khushi**

If you found this project helpful, please consider giving it a ⭐

[GitHub](https://github.com/khushiirana/meeting-summarizer) • [Report Bug](https://github.com/khushiirana/meeting-summarizer/issues) • [Request Feature](https://github.com/khushiirana/meeting-summarizer/issues)

</div>
