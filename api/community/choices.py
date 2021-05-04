from enum import Enum


class Banners(Enum):
    HIRING = "Hiring"
    NEW = "New"
    ACQUIRED = "Acquired"


class ModerationStatus(Enum):
    UNMODERATED = "Unmoderated"
    REJECTED = "Rejected"
    APPROVED = "Approved"
    FLAGGED = "Flagged"
