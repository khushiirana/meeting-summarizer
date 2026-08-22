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

  const done      = meetings.filter(m => m.status === "done").length;
  const inProgress = meetings.filter(m => ["pending","transcribing","summarizing"].includes(m.status)).length;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-violet-50/30">

      {/* ── Header ──────────────────────────────────── */}
      <header className="bg-white/80 backdrop-blur border-b border-slate-100 sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-violet-600 to-indigo-600 flex items-center justify-center text-lg shadow-sm">
              🎙️
            </div>
            <div>
              <h1 className="text-base font-bold text-slate-900 leading-tight">
                Meeting Summarizer
              </h1>
              <p className="text-xs text-slate-400 leading-tight">
                Transcribe & summarize with AI
              </p>
            </div>
          </div>

          {/* Stats chips */}
          <div className="hidden sm:flex items-center gap-2">
            {inProgress > 0 && (
              <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-amber-50 text-amber-600 text-xs font-semibold border border-amber-100">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse" />
                {inProgress} processing
              </span>
            )}
            <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-slate-50 text-slate-500 text-xs font-medium border border-slate-100">
              <span className="text-emerald-500">✓</span>
              {done} completed
            </span>
            <div className="flex items-center gap-1 pl-2 border-l border-slate-100">
              <span className="text-xs text-slate-400">Powered by</span>
              <span className="text-xs font-semibold text-violet-600">Groq AI</span>
            </div>
          </div>
        </div>
      </header>

      {/* ── Main ────────────────────────────────────── */}
      <main className="max-w-4xl mx-auto px-6 py-10">

        {/* Upload section */}
        <div className="mb-10">
          <div className="flex items-end justify-between mb-4">
            <div>
              <h2 className="text-xl font-bold text-slate-900">Upload Meeting Audio</h2>
              <p className="text-sm text-slate-400 mt-0.5">
                We'll transcribe and summarize it automatically
              </p>
            </div>
          </div>
          <AudioUploader onUploaded={handleUploaded} />
        </div>

        {/* Meetings section */}
        <div>
          <div className="flex items-center justify-between mb-5">
            <div className="flex items-center gap-2.5">
              <h2 className="text-xl font-bold text-slate-900">Recent Meetings</h2>
              {meetings.length > 0 && (
                <span className="px-2 py-0.5 rounded-full bg-slate-100 text-slate-500 text-xs font-semibold">
                  {meetings.length}
                </span>
              )}
            </div>
            <button
              onClick={fetchMeetings}
              className="
                inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg
                text-slate-500 hover:text-violet-600 hover:bg-violet-50
                text-xs font-medium border border-slate-200 hover:border-violet-200
                transition-all duration-150
              "
            >
              <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
              </svg>
              Refresh
            </button>
          </div>

          <MeetingList
            meetings={meetings}
            loading={loading}
            onDeleted={handleDeleted}
          />
        </div>
      </main>
    </div>
  );
}
