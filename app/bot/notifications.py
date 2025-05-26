from typing import List
from app.models.user import User
from app.models.job import Job
from app.services.twilio_service import TwilioService
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class NotificationService:
    """Service for sending job notifications to users"""
    
    def __init__(self):
        self.twilio_service = TwilioService()
    
    def send_job_alerts(self, job: Job, matching_users: List[User]) -> dict:
        """
        Send job alerts to all matching users
        
        Args:
            job: The job posting
            matching_users: List of users to notify
            
        Returns:
            dict: Summary of notification results
        """
        if not matching_users:
            logger.info(f"No matching users found for job {job.id}")
            return {'sent': 0, 'failed': 0, 'total': 0}
        
        # Prepare the alert message
        alert_message = job.get_alert_message()
        
        # Get phone numbers of matching users
        phone_numbers = [user.phone_number for user in matching_users]
        
        logger.info(f"Sending job alerts for {job.id} to {len(phone_numbers)} users")
        
        # Send bulk messages
        results = self.twilio_service.send_bulk_messages(phone_numbers, alert_message)
        results['total'] = len(phone_numbers)
        
        logger.info(f"Job alert results: {results}")
        return results
    
    def send_registration_confirmation(self, user: User) -> bool:
        """
        Send confirmation message to newly registered user
        
        Args:
            user: The registered user
            
        Returns:
            bool: True if sent successfully
        """
        message = (
            f"✅ *Registration Successful!*\n\n"
            f"You're now registered for:\n"
            f"*Role:* {user.role.title()}\n"
            f"*Location:* {user.location.title()}\n\n"
            f"You'll receive alerts when matching jobs are posted!\n\n"
            f"To update your preferences, just register again with new details."
        )
        
        return self.twilio_service.send_message(user.phone_number, message)
    
    def send_job_posted_confirmation(self, employer_phone: str, job: Job, alert_count: int) -> bool:
        """
        Send confirmation to employer that job was posted
        
        Args:
            employer_phone: Employer's phone number
            job: The posted job
            alert_count: Number of users notified
            
        Returns:
            bool: True if sent successfully
        """
        message = (
            f"✅ *Job Posted Successfully!*\n\n"
            f"*Job ID:* {job.id}\n"
            f"*Role:* {job.role.title()}\n"
            f"*Location:* {job.location.title()}\n\n"
            f"📢 *{alert_count} job seekers* have been notified!\n\n"
            f"Your job is now active and visible to interested candidates."
        )
        
        return self.twilio_service.send_message(employer_phone, message)
    
    def send_error_message(self, phone_number: str, error_type: str = "general") -> bool:
        """
        Send error message to user
        
        Args:
            phone_number: User's phone number
            error_type: Type of error (registration, posting, general)
            
        Returns:
            bool: True if sent successfully
        """
        error_messages = {
            "registration": (
                "❌ *Registration Failed*\n\n"
                "There was an issue with your registration. "
                "Please try again or contact support."
            ),
            "posting": (
                "❌ *Job Posting Failed*\n\n"
                "There was an issue posting your job. "
                "Please try again or contact support."
            ),
            "general": (
                "❌ *Something went wrong*\n\n"
                "Please try again later or contact support if the issue persists."
            )
        }
        
        message = error_messages.get(error_type, error_messages["general"])
        return self.twilio_service.send_message(phone_number, message) 