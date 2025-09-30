"""
Environment Enum
"""
from enum import Enum


class Environment(Enum):
    """Environment enumeration"""
    DEV = "dev"
    QA = "qa"
    STAGING = "staging"
    PROD = "prod"