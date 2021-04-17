from enum import Enum


class UserProviderChoices(Enum):
    # Name is stored, Value is Display
    SIGN_UP = "registration"
    GITHUB = "github"
    LINKEDIN = "linkedin"
