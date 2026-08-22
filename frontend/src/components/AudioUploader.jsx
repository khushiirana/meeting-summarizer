import { useState, useRef } from "react";
import { uploadMeeting } from "../api/client";

const ACCEPTED = ".mp3,.mp4,.wav,.m4a,.ogg,.flac,.webm";

export default function AudioUploader({ onUploaded }) {
  const [dragging, setDragging] = useState(false);
  const [progress, setProgress]   = useState(null);
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
    <div className="w-full relative">
      {/* Drop zone */}
      <div
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        className={`
          flex flex-col items-center justify-center p-12 rounded-xl border-2 text-center cursor-pointer
          transition-all duration-200 group
          ${dragging
            ? "border-solid border-accent-purple bg-accent-purple/15 scale-105"
            : "border-dashed border-accent-purple bg-accent-purple/5 hover:border-solid hover:bg-accent-purple/10 hover:scale-[1.02]"
          }
        `}
      >
        <div className="text-[50px] mb-4 transition-transform duration-200 group-hover:scale-110">
          🎙️
        </div>

        <p className="text-lg font-bold text-white mb-2">
          {dragging ? "Drop audio here" : "Drag audio here or click to browse"}
        </p>
        <p className="text-sm text-gray-400 mb-8 max-w-sm mx-auto">
          Accepted: .mp3 .wav .mp4 .m4a .ogg .flac .webm<br/>
          Max size: 25MB
        </p>

        <button
          type="button"
          onClick={(e) => { e.stopPropagation(); inputRef.current.click(); }}
          className="
            inline-flex items-center justify-center gap-2 px-10 py-4 rounded-lg
            bg-gradient-to-br from-accent-purple to-accent-pink
            text-white text-base font-bold
            transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]
            hover:shadow-glow-strong shadow-glow
          "
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
          </svg>
          Upload Audio
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
        <div className="absolute -bottom-16 left-0 right-0 bg-dark-800 border border-dark-700 rounded-xl p-4 shadow-lg animate-slide-up z-10">
          <div className="flex justify-between text-sm font-medium text-gray-300 mb-2">
            <span className="animate-pulse-soft">Uploading…</span>
            <span className="text-accent-cyan">{progress}%</span>
          </div>
          <div className="h-2 bg-dark-900 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-accent-purple to-accent-cyan rounded-full transition-all duration-300 shadow-glow"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="mt-6 flex items-center gap-3 p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-sm animate-slide-up">
          <span>⚠️</span>
          <span className="font-medium">{error}</span>
        </div>
      )}
    </div>
  );
}
