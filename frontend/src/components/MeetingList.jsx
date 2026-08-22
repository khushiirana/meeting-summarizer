import MeetingCard from "./MeetingCard";

function SkeletonCard() {
  return (
    <div className="bg-dark-800 rounded-xl border border-dark-700 p-6 shadow-glow animate-pulse-soft relative overflow-hidden">
      <div className="absolute left-0 top-0 bottom-0 w-1 bg-dark-700" />
      <div className="flex justify-between items-center mb-6">
        <div className="h-5 bg-dark-700 rounded-full w-48" />
        <div className="h-6 bg-dark-700 rounded-full w-24" />
      </div>
      <div className="space-y-3">
        <div className="h-3 bg-dark-700 rounded-full w-3/4" />
        <div className="h-3 bg-dark-700 rounded-full w-1/2" />
        <div className="h-3 bg-dark-700 rounded-full w-5/6" />
      </div>
    </div>
  );
}

export default function MeetingList({ meetings, loading, onDeleted }) {
  if (loading) {
    return (
      <div className="space-y-6">
        <SkeletonCard />
        <SkeletonCard />
        <SkeletonCard />
      </div>
    );
  }

  if (meetings.length === 0) {
    return (
      <div className="text-center py-24 bg-dark-800/30 rounded-xl border border-dark-700/50 backdrop-blur-sm">
        <div className="w-16 h-16 mx-auto bg-dark-700/50 rounded-2xl flex items-center justify-center text-3xl mb-4 border border-dark-700">
          📁
        </div>
        <p className="text-lg font-bold text-white mb-2">No meetings yet</p>
        <p className="text-gray-400">Upload your first audio file above to see the magic.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
      {meetings.map((m, idx) => (
        <MeetingCard 
          key={m.id} 
          meeting={m} 
          onDeleted={onDeleted} 
          delay={idx * 150} // For staggered entrance
        />
      ))}
    </div>
  );
}
