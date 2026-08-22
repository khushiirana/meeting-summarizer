import MeetingCard from "./MeetingCard";

function SkeletonCard() {
  return (
    <div className="bg-white rounded-2xl border border-slate-100 p-5 animate-pulse">
      <div className="flex items-center gap-3 mb-3">
        <div className="h-4 bg-slate-100 rounded-full w-4" />
        <div className="h-4 bg-slate-100 rounded-full w-48" />
      </div>
      <div className="h-3 bg-slate-100 rounded-full w-28 mb-4" />
      <div className="h-2 bg-slate-100 rounded-full w-full mb-2" />
      <div className="h-2 bg-slate-100 rounded-full w-3/4" />
    </div>
  );
}

export default function MeetingList({ meetings, loading, onDeleted }) {
  if (loading) {
    return (
      <div className="space-y-3">
        <SkeletonCard />
        <SkeletonCard />
      </div>
    );
  }

  if (meetings.length === 0) {
    return (
      <div className="text-center py-20">
        <div className="w-20 h-20 mx-auto rounded-2xl bg-slate-100 flex items-center justify-center text-4xl mb-4">
          🎤
        </div>
        <p className="font-semibold text-slate-600 mb-1">No meetings yet</p>
        <p className="text-sm text-slate-400">Upload an audio file above to get started</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {meetings.map((m) => (
        <MeetingCard key={m.id} meeting={m} onDeleted={onDeleted} />
      ))}
    </div>
  );
}
