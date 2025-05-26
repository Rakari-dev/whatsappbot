from datetime import datetime
from typing import Optional
import uuid

class Job:
    """Represents a job posting"""
    
    def __init__(self, employer_phone: str, role: str, location: str, description: Optional[str] = None):
        self.id = str(uuid.uuid4())[:8]  # Short unique ID
        self.employer_phone = employer_phone
        self.role = role.lower().strip()
        self.location = location.lower().strip()
        self.description = description or f"{role} position in {location}"
        self.created_at = datetime.now()
        self.is_active = True
    
    def to_dict(self) -> dict:
        """Convert job to dictionary representation"""
        return {
            'id': self.id,
            'employer_phone': self.employer_phone,
            'role': self.role,
            'location': self.location,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }
    
    def get_alert_message(self) -> str:
        """Generate alert message for job seekers"""
        return (
            f"🎯 *New Job Alert!*\n\n"
            f"*Role:* {self.role.title()}\n"
            f"*Location:* {self.location.title()}\n"
            f"*Description:* {self.description}\n"
            f"*Posted:* {self.created_at.strftime('%Y-%m-%d %H:%M')}\n\n"
            f"Interested? Contact the employer or reply for more info!"
        )
    
    def __str__(self) -> str:
        return f"Job({self.id}, {self.role}, {self.location})" 