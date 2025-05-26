from datetime import datetime
from typing import Optional

class User:
    """Represents a job seeker user"""
    
    def __init__(self, phone_number: str, role: str, location: str):
        self.phone_number = phone_number
        self.role = role.lower().strip()
        self.location = location.lower().strip()
        self.created_at = datetime.now()
        self.is_active = True
    
    def matches_job(self, job_role: str, job_location: str) -> bool:
        """Check if this user's preferences match a job posting"""
        return (
            self.role == job_role.lower().strip() and 
            self.location == job_location.lower().strip() and
            self.is_active
        )
    
    def to_dict(self) -> dict:
        """Convert user to dictionary representation"""
        return {
            'phone_number': self.phone_number,
            'role': self.role,
            'location': self.location,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }
    
    def __str__(self) -> str:
        return f"User({self.phone_number}, {self.role}, {self.location})" 