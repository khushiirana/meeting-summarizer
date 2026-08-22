import { useState, useRef } from "react";
import { uploadMeeting } from "../api/client";

const ACCEPTED = ".mp3,.mp4,.wav,.m4a,.ogg,.flac,.webm";

export default function AudioUploader({ onUploaded }) {
  const [dragging, setDragging] = useState(false);
  const [progress, setProgress]   = useState(null);   // 0-100 or null
  const [error, setError]         = useState(null);
  const inputRef = useRef();

  const handleFile = async (file) => {
    setError(null);
    setProgress(0);
    try {
      await uploadMeeting(file, (e) => {
        if (e.total) setProgress(Math.round((e.loaded / e.total) * 100));
      });
      setProgress(null);
      onUploaded();
    } catch (err) {
      setError(err?.response?.data?.detail || "Upload failed. Please try again.");
      setProgress(null);
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  return (
    <div className="mb-10">
      {/* Drop zone */}
      <div
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        className={`
          relative border-2 border-dashed rounded-2xl px-8 py-12 text-center cursor-pointer
          transition-all duration-200 group
          ${dragging
            ? "border-violet-500 bg-violet-50 scale-[1.01]"
            : "border-slate-200 hover:border-violet-400 hover:bg-violet-50/40 bg-white"
          }
        `}
      >
        {/* Icon */}
        <div className={`
          mx-auto w-16 h-16 rounded-2xl flex items-center justify-center text-3xl mb-4
          transition-colors duration-200
          ${dragging ? "bg-violet-100" : "bg-slate-100 group-hover:bg-violet-100"}
        `}>
          🎙️
        </div>

        <p className="text-base font-semibold text-slate-700 mb-1">
          {dragging ? "Drop your audio file here" : "Upload Meeting Audio"}
        </p>
        <p className="text-sm text-slate-400 mb-5">
          Drag & drop or click to browse — MP3, WAV, MP4, M4A, OGG, FLAC, WEBM
        </p>

        <button
          type="button"
          onClick={(e) => { e.stopPropagation(); inputRef.current.click(); }}
          className="
            inline-flex items-center gap-2 px-6 py-2.5 rounded-xl
            bg-violet-600 hover:bg-violet-700 active:bg-violet-800
            text-white text-sm font-semibold shadow-sm
            transition-colors duration-150
          "
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          Choose File
        </button>

        <input
          ref={inputRef}
          type="file"
          accept={ACCEPTED}
          className="hidden"
          onChange={(e) => { const f = e.target.files[0]; if (f) handleFile(f); e.target.value = ""; }}
        />
      </div>

      {/* Progress bar */}
      {progress !== null && (
        <div className="mt-4 bg-white border border-slate-100 rounded-xl p-4 shadow-sm">
          <div className="flex justify-between text-xs font-medium text-slate-500 mb-2">
            <span>Uploading…</span>
            <span>{progress}%</span>
          </div>
          <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-violet-500 to-indigo-500 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="mt-3 flex items-start gap-2 p-3 bg-red-50 border border-red-200 rounded-xl text-red-600 text-sm">
          <span className="mt-0.5">⚠️</span>
          <span>{error}</span>
        </div>
      )}
    </div>
  );
}
