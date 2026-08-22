import enum
import json
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from database import Base


class MeetingStatus(str, enum.Enum):
    PENDING = "pending"
    TRANSCRIBING = "transcribing"
    SUMMARIZING = "summarizing"
    DONE = "done"
    ERROR = "error"


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    status = Column(Enum(MeetingStatus), default=MeetingStatus.PENDING, nullable=False)
    transcript = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    # Stored as JSON strings
    _key_decisions = Column("key_decisions", Text, nullable=True)
    _action_items = Column("action_items", Text, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    @property
    def key_decisions(self):
        if self._key_decisions:
            return json.loads(self._key_decisions)
        return []

    @key_decisions.setter
    def key_decisions(self, value):
        self._key_decisions = json.dumps(value) if value else None

    @property
    def action_items(self):
        if self._action_items:
            return json.loads(self._action_items)
        return []

    @action_items.setter
    def action_items(self, value):
        self._action_items = json.dumps(value) if value else None

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "status": self.status.value if self.status else None,
            "transcript": self.transcript,
            "summary": self.summary,
            "key_decisions": self.key_decisions,
            "action_items": self.action_items,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
