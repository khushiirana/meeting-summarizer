import { useState, useEffect, useCallback } from "react";
import AudioUploader from "./components/AudioUploader";
import MeetingList from "./components/MeetingList";
import { listMeetings } from "./api/client";

const POLL_INTERVAL = 3000;

export default function App() {
  const [meetings, setMeetings] = useState([]);
  const [loading, setLoading]   = useState(true);

  const fetchMeetings = useCallback(async () => {
    try {
      const { data } = await listMeetings();
      setMeetings(data);
    } catch (err) {
      console.error("Failed to fetch meetings:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { fetchMeetings(); }, [fetchMeetings]);

  // Auto-poll only while something is in-progress
  useEffect(() => {
    const inProgress = meetings.some(m =>
      ["pending","transcribing","summarizing"].includes(m.status)
    );
    if (!inProgress) return;
    const t = setInterval(fetchMeetings, POLL_INTERVAL);
    return () => clearInterval(t);
  }, [meetings, fetchMeetings]);

  const handleUploaded = () => setTimeout(fetchMeetings, 800);
  const handleDeleted  = (id) => setMeetings(prev => prev.filter(m => m.id !== id));

  return (
    <div className="min-h-screen bg-dark-900 text-white selection:bg-accent-purple/30 selection:text-white">

      {/* ── Header ──────────────────────────────────── */}
      <header className="bg-dark-900/90 backdrop-blur-md border-b border-dark-700 sticky top-0 z-40 transition-colors duration-300">
        <div className="max-w-[1440px] mx-auto px-4 md:px-6 py-4 flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <h1 className="text-[20px] font-bold text-white tracking-tight flex items-center gap-2">
              <span className="text-xl">🎙️</span> Meeting Summarizer
            </h1>
          </div>

          {/* Right Link */}
          <a href="#" className="hidden sm:block text-sm font-medium text-white hover:text-accent-cyan transition-colors">
            Read Docs
          </a>
        </div>
      </header>

      {/* ── Main Layout ────────────────────────────────────── */}
      <main className="max-w-[1440px] mx-auto px-4 md:px-6 py-10 md:py-16 pb-24">
        
        <div className="max-w-[1200px] mx-auto">
          {/* Hero Section */}
          <div className="max-w-[600px] mx-auto text-center mb-12 animate-slide-up" style={{ animationDelay: '100ms' }}>
            <h2 className="text-3xl md:text-5xl font-bold text-white mb-4 leading-tight tracking-tight">
              Let's transform meetings from chaos into action.
            </h2>
            <p className="text-base text-gray-400">
              Upload your audio file. Instant transcription, summaries, and action items powered by AI.
            </p>
          </div>

          {/* Upload Dropzone */}
          <div className="max-w-[600px] mx-auto mb-16 animate-slide-up" style={{ animationDelay: '200ms' }}>
            <AudioUploader onUploaded={handleUploaded} />
          </div>

          {/* Meetings Section (Results Grid) */}
          <div className="w-full">
            <MeetingList
              meetings={meetings}
              loading={loading}
              onDeleted={handleDeleted}
            />
          </div>
        </div>
      </main>
      
      {/* Footer */}
      <footer className="border-t border-dark-700 py-8 text-center text-xs text-dark-700">
        <p className="text-gray-500">Powered by Groq</p>
      </footer>
    </div>
  );
}
