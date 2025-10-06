"""
Test Priority Enum
"""
from enum import Enum


class TestPriority(Enum):
    """Test priority enumeration"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"