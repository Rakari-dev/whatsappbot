from twilio.rest import Client
from config.config import Config
import logging

logger = logging.getLogger(__name__)

class TwilioService:
    """Service for sending WhatsApp messages via Twilio"""
    
    def __init__(self):
        self.client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
        self.from_number = f"whatsapp:{Config.TWILIO_PHONE_NUMBER}"
    
    def send_message(self, to_number: str, message: str) -> bool:
        """
        Send a WhatsApp message to a phone number
        
        Args:
            to_number: Phone number in format +1234567890
            message: Message content to send
            
        Returns:
            bool: True if message sent successfully, False otherwise
        """
        try:
            # Ensure phone number has whatsapp: prefix
            if not to_number.startswith('whatsapp:'):
                to_number = f"whatsapp:{to_number}"
            
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            logger.info(f"Message sent successfully. SID: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send message to {to_number}: {str(e)}")
            return False
    
    def send_bulk_messages(self, recipients: list, message: str) -> dict:
        """
        Send the same message to multiple recipients
        
        Args:
            recipients: List of phone numbers
            message: Message content to send
            
        Returns:
            dict: Summary of sent/failed messages
        """
        results = {'sent': 0, 'failed': 0, 'errors': []}
        
        for phone_number in recipients:
            if self.send_message(phone_number, message):
                results['sent'] += 1
            else:
                results['failed'] += 1
                results['errors'].append(phone_number)
        
        return results 