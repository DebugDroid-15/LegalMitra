"""
LegalMitra Conversation Store
Thread-safe SQLite store for user sessions and conversation persistence,
isolated completely from the immutable legal knowledge base.
Provides session-level ownership isolation and safe lifecycle management.
"""

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from legalmitra.core.logging import get_logger

logger = get_logger("conversation_store")


class ConversationStore:
    """Stores user chat sessions and legal answers separately from the verified legal corpus."""

    def __init__(self, db_path: str = "data/conversations.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_db()

    def _init_db(self) -> None:
        """Create conversation tables if they do not exist and apply schema migrations."""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    conversation_id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL DEFAULT 'anonymous',
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    is_bookmarked INTEGER NOT NULL DEFAULT 0
                );
            """)
            # Migration check: ensure session_id column exists
            cursor = self.conn.cursor()
            cursor.execute("PRAGMA table_info(conversations);")
            columns = [row[1] for row in cursor.fetchall()]
            if "session_id" not in columns:
                cursor.execute("ALTER TABLE conversations ADD COLUMN session_id TEXT NOT NULL DEFAULT 'anonymous';")

            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    message_id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL REFERENCES conversations(conversation_id) ON DELETE CASCADE,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    citations_json TEXT,
                    evidence_json TEXT,
                    model_used TEXT,
                    latency_seconds REAL,
                    created_at TEXT NOT NULL
                );
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    feedback_id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL,
                    session_id TEXT NOT NULL DEFAULT 'anonymous',
                    query TEXT NOT NULL,
                    is_helpful INTEGER NOT NULL,
                    feedback_text TEXT,
                    created_at TEXT NOT NULL
                );
            """)
            # Migration check: ensure session_id column exists in feedback
            cursor.execute("PRAGMA table_info(feedback);")
            fb_columns = [row[1] for row in cursor.fetchall()]
            if "session_id" not in fb_columns:
                cursor.execute("ALTER TABLE feedback ADD COLUMN session_id TEXT NOT NULL DEFAULT 'anonymous';")

            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_msg_conv ON messages(conversation_id);")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_conv_session ON conversations(session_id);")

    def create_conversation(self, session_id: str, title: str = "New Legal Consultation") -> str:
        """Create a new unique conversation session owned by session_id."""
        conv_id = f"conv_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc).isoformat()
        with self.conn:
            self.conn.execute(
                "INSERT INTO conversations (conversation_id, session_id, title, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (conv_id, session_id, title, now, now)
            )
        return conv_id

    def list_conversations(self, session_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """List recent conversations strictly scoped to the owner's session_id."""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT conversation_id, title, created_at, updated_at, is_bookmarked 
            FROM conversations 
            WHERE session_id = ? 
            ORDER BY updated_at DESC 
            LIMIT ?
            """,
            (session_id, limit)
        )
        return [dict(row) for row in cursor.fetchall()]

    def get_conversation_owner(self, conversation_id: str) -> Optional[str]:
        """Look up the owner session_id of a conversation."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT session_id FROM conversations WHERE conversation_id = ?", (conversation_id,))
        row = cursor.fetchone()
        return row[0] if row else None

    def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        citations: Optional[List[str]] = None,
        evidence: Optional[List[Dict[str, Any]]] = None,
        model_used: Optional[str] = None,
        latency_seconds: Optional[float] = None,
    ) -> str:
        """Record a chat message in the conversation thread."""
        msg_id = f"msg_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc).isoformat()

        with self.conn:
            if role == "user":
                cursor = self.conn.cursor()
                cursor.execute("SELECT count(*) FROM messages WHERE conversation_id = ?", (conversation_id,))
                msg_count = cursor.fetchone()[0]
                if msg_count == 0:
                    clean_title = content[:60].strip() + ("..." if len(content) > 60 else "")
                    self.conn.execute(
                        "UPDATE conversations SET title = ?, updated_at = ? WHERE conversation_id = ?",
                        (clean_title, now, conversation_id)
                    )
                else:
                    self.conn.execute(
                        "UPDATE conversations SET updated_at = ? WHERE conversation_id = ?",
                        (now, conversation_id)
                    )

            self.conn.execute(
                """
                INSERT INTO messages (
                    message_id, conversation_id, role, content,
                    citations_json, evidence_json, model_used, latency_seconds, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    msg_id,
                    conversation_id,
                    role,
                    content,
                    json.dumps(citations or []),
                    json.dumps(evidence or []),
                    model_used,
                    latency_seconds,
                    now,
                )
            )
        return msg_id

    def get_messages(self, conversation_id: str, session_id: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Retrieve messages for a conversation.
        If session_id is provided, enforces that the conversation belongs to that session.
        Returns None if unauthorized or conversation does not exist.
        """
        cursor = self.conn.cursor()
        if session_id is not None:
            cursor.execute("SELECT session_id FROM conversations WHERE conversation_id = ?", (conversation_id,))
            row = cursor.fetchone()
            if not row:
                return None
            if row[0] != session_id:
                logger.warning(f"Unauthorized conversation access attempt: session {session_id} on conv {conversation_id}")
                return None

        cursor.execute(
            """
            SELECT message_id, role, content, citations_json, evidence_json, model_used, latency_seconds, created_at
            FROM messages WHERE conversation_id = ? ORDER BY created_at ASC
            """,
            (conversation_id,)
        )
        results = []
        for row in cursor.fetchall():
            d = dict(row)
            d["citations"] = json.loads(d.pop("citations_json") or "[]")
            d["evidence"] = json.loads(d.pop("evidence_json") or "[]")
            results.append(d)
        return results

    def delete_conversation(self, conversation_id: str, session_id: str) -> bool:
        """Permanently delete a conversation and its messages if owned by session_id."""
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT session_id FROM conversations WHERE conversation_id = ?", (conversation_id,))
            row = cursor.fetchone()
            if not row or row[0] != session_id:
                return False
            cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))
            cursor.execute("DELETE FROM conversations WHERE conversation_id = ?", (conversation_id,))
            return True

    def record_feedback(
        self,
        conversation_id: str,
        query: str,
        is_helpful: bool,
        session_id: str = "anonymous",
        feedback_text: Optional[str] = None
    ) -> str:
        """Record user precision feedback scoped to the session."""
        fid = f"fb_{uuid.uuid4().hex[:12]}"
        now = datetime.now(timezone.utc).isoformat()
        with self.conn:
            self.conn.execute(
                """
                INSERT INTO feedback (feedback_id, conversation_id, session_id, query, is_helpful, feedback_text, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (fid, conversation_id, session_id, query, 1 if is_helpful else 0, feedback_text, now)
            )
        return fid
