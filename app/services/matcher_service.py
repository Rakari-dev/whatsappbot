from typing import List
from app.models.user import User
from app.models.job import Job
import logging

logger = logging.getLogger(__name__)

class MatcherService:
    """Service for matching jobs with interested users"""
    
    def __init__(self):
        # In-memory storage for MVP (replace with database later)
        self.users: List[User] = []
        self.jobs: List[Job] = []
    
    def register_user(self, phone_number: str, role: str, location: str) -> bool:
        """
        Register a new job seeker
        
        Args:
            phone_number: User's WhatsApp number
            role: Desired job role
            location: Preferred location
            
        Returns:
            bool: True if registration successful
        """
        try:
            # Check if user already exists
            existing_user = self.get_user_by_phone(phone_number)
            if existing_user:
                # Update existing user's preferences
                existing_user.role = role.lower().strip()
                existing_user.location = location.lower().strip()
                logger.info(f"Updated user preferences: {phone_number}")
            else:
                # Create new user
                new_user = User(phone_number, role, location)
                self.users.append(new_user)
                logger.info(f"Registered new user: {phone_number}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to register user {phone_number}: {str(e)}")
            return False
    
    def post_job(self, employer_phone: str, role: str, location: str) -> Job:
        """
        Post a new job and return it
        
        Args:
            employer_phone: Employer's WhatsApp number
            role: Job role
            location: Job location
            
        Returns:
            Job: The created job object
        """
        try:
            new_job = Job(employer_phone, role, location)
            self.jobs.append(new_job)
            logger.info(f"Posted new job: {new_job.id} - {role} in {location}")
            return new_job
            
        except Exception as e:
            logger.error(f"Failed to post job: {str(e)}")
            raise
    
    def find_matching_users(self, job: Job) -> List[User]:
        """
        Find all users that match a job posting
        
        Args:
            job: Job object to match against
            
        Returns:
            List[User]: List of matching users
        """
        matching_users = []
        
        for user in self.users:
            if user.matches_job(job.role, job.location):
                matching_users.append(user)
        
        logger.info(f"Found {len(matching_users)} matching users for job {job.id}")
        return matching_users
    
    def get_user_by_phone(self, phone_number: str) -> User:
        """Get user by phone number"""
        for user in self.users:
            if user.phone_number == phone_number:
                return user
        return None
    
    def get_user_stats(self) -> dict:
        """Get statistics about registered users"""
        active_users = [u for u in self.users if u.is_active]
        return {
            'total_users': len(self.users),
            'active_users': len(active_users),
            'total_jobs': len(self.jobs)
        }
    
    def get_jobs_by_criteria(self, role: str = None, location: str = None) -> List[Job]:
        """Get jobs filtered by criteria"""
        filtered_jobs = self.jobs
        
        if role:
            filtered_jobs = [j for j in filtered_jobs if j.role == role.lower().strip()]
        
        if location:
            filtered_jobs = [j for j in filtered_jobs if j.location == location.lower().strip()]
        
        return filtered_jobs 