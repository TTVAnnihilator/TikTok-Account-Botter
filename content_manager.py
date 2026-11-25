"""Local tiktok content preparation. No network or publishing."""
from datetime import datetime, timezone
from hashlib import sha256
from uuid import UUID
import json

from companion import prepare


def draft_content(caption: str, asset_id: str, scheduled_at: datetime, now: datetime | None = None):
    now = now or datetime.now(timezone.utc)
    if not isinstance(caption, str) or not 1 <= len(caption.strip()) <= 2200:
        raise ValueError("Invalid caption")
    if str(UUID(asset_id)) != asset_id:
        raise ValueError("Asset reference must be a canonical UUID")
    if scheduled_at.utcoffset() is None or now.utcoffset() is None or scheduled_at <= now:
        raise ValueError("A future timezone-aware schedule is required")
    draft = {"platform": "tiktok", "caption": caption.strip(),
             "asset_id": asset_id, "scheduled_at": scheduled_at.astimezone(timezone.utc).isoformat()}
    digest = sha256(json.dumps(draft, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"draft": draft, "draft_sha256": digest, "state": "review_required",
            "proposal": prepare("publish_proposal"), "published": False,
            "automatic_spending_authorized": False}


def analytics_preview():
    return {"platform": "tiktok", "views": None, "likes": None,
            "followers": None, "source_verified": False, "connected": False}
