from enum import Enum


class PostBanner(Enum):
    FIRST_POST = "First Post"


class ModerationStatus(Enum):
    UNMODERATED = "Unmoderated"
    REJECTED = "Rejected"
    REVIEWED = "Reviewed"
    FLAGGED = "Flagged"
