from flask import Blueprint, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from app.bot.commands import CommandParser
from app.bot.notifications import NotificationService
from app.services.matcher_service import MatcherService
import logging

logger = logging.getLogger(__name__)

# Create blueprint for webhook routes
webhook_bp = Blueprint('webhook', __name__)

# Initialize services (in production, use dependency injection)
matcher_service = MatcherService()
notification_service = NotificationService()
command_parser = CommandParser()

@webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    """
    Main webhook endpoint for receiving WhatsApp messages from Twilio
    """
    try:
        # Get incoming message data
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        
        # Remove 'whatsapp:' prefix if present
        if from_number.startswith('whatsapp:'):
            from_number = from_number[9:]
        
        logger.info(f"Received message from {from_number}: {incoming_msg}")
        
        # Create Twilio response object
        resp = MessagingResponse()
        
        # Process the message and get response
        response_message = process_message(incoming_msg, from_number)
        
        # Add response to Twilio response
        resp.message(response_message)
        
        return str(resp)
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        resp = MessagingResponse()
        resp.message("Sorry, something went wrong. Please try again later.")
        return str(resp)

def process_message(message: str, phone_number: str) -> str:
    """
    Process incoming message and return appropriate response
    
    Args:
        message: The incoming message text
        phone_number: Sender's phone number
        
    Returns:
        str: Response message to send back
    """
    try:
        # Check for help command
        if command_parser.is_help_command(message):
            return command_parser.get_help_message()
        
        # Try to parse register command
        register_params = command_parser.parse_register_command(message)
        if register_params:
            role, location = register_params
            return handle_register_command(phone_number, role, location)
        
        # Try to parse post command
        post_params = command_parser.parse_post_command(message)
        if post_params:
            role, location = post_params
            return handle_post_command(phone_number, role, location)
        
        # If no valid command found
        return command_parser.get_invalid_command_message()
        
    except Exception as e:
        logger.error(f"Error processing message from {phone_number}: {str(e)}")
        return "Sorry, something went wrong. Please try again later."

def handle_register_command(phone_number: str, role: str, location: str) -> str:
    """
    Handle user registration command
    
    Args:
        phone_number: User's phone number
        role: Desired job role
        location: Preferred location
        
    Returns:
        str: Response message
    """
    try:
        # Register user with matcher service
        success = matcher_service.register_user(phone_number, role, location)
        
        if success:
            # Get user object for confirmation
            user = matcher_service.get_user_by_phone(phone_number)
            
            # Send confirmation (this will be sent separately via Twilio)
            notification_service.send_registration_confirmation(user)
            
            # Return immediate response
            return (
                f"✅ *Registration Successful!*\n\n"
                f"You're now registered for:\n"
                f"*Role:* {role.title()}\n"
                f"*Location:* {location.title()}\n\n"
                f"You'll receive alerts when matching jobs are posted!"
            )
        else:
            return (
                "❌ *Registration Failed*\n\n"
                "There was an issue with your registration. Please try again."
            )
            
    except Exception as e:
        logger.error(f"Error in register command: {str(e)}")
        return "❌ Registration failed. Please try again later."

def handle_post_command(phone_number: str, role: str, location: str) -> str:
    """
    Handle job posting command
    
    Args:
        phone_number: Employer's phone number
        role: Job role
        location: Job location
        
    Returns:
        str: Response message
    """
    try:
        # Post the job
        job = matcher_service.post_job(phone_number, role, location)
        
        # Find matching users
        matching_users = matcher_service.find_matching_users(job)
        
        # Send alerts to matching users
        alert_results = notification_service.send_job_alerts(job, matching_users)
        
        # Send confirmation to employer
        notification_service.send_job_posted_confirmation(
            phone_number, job, alert_results['sent']
        )
        
        # Return immediate response
        return (
            f"✅ *Job Posted Successfully!*\n\n"
            f"*Job ID:* {job.id}\n"
            f"*Role:* {role.title()}\n"
            f"*Location:* {location.title()}\n\n"
            f"📢 *{alert_results['sent']} job seekers* have been notified!"
        )
        
    except Exception as e:
        logger.error(f"Error in post command: {str(e)}")
        return "❌ Job posting failed. Please try again later."

@webhook_bp.route('/status', methods=['GET'])
def status():
    """
    Health check endpoint
    """
    try:
        stats = matcher_service.get_user_stats()
        return jsonify({
            'status': 'healthy',
            'stats': stats
        })
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500