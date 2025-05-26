import re
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class CommandParser:
    """Handles parsing and validation of bot commands"""
    
    # Common multi-word locations for better parsing
    COMMON_LOCATIONS = {
        'new york', 'los angeles', 'san francisco', 'las vegas', 'new delhi',
        'hong kong', 'cape town', 'buenos aires', 'rio de janeiro', 'costa rica',
        'puerto rico', 'new zealand', 'south africa', 'united kingdom', 'united states'
    }
    
    # Common single-word locations (cities/countries)
    COMMON_SINGLE_LOCATIONS = {
        'london', 'paris', 'berlin', 'tokyo', 'sydney', 'toronto', 'mumbai',
        'bangalore', 'delhi', 'chennai', 'hyderabad', 'pune', 'kolkata',
        'singapore', 'dubai', 'amsterdam', 'madrid', 'rome', 'vienna',
        'zurich', 'stockholm', 'oslo', 'copenhagen', 'helsinki', 'warsaw',
        'prague', 'budapest', 'athens', 'lisbon', 'dublin', 'edinburgh',
        'manchester', 'birmingham', 'glasgow', 'bristol', 'leeds', 'liverpool',
        'seattle', 'portland', 'denver', 'austin', 'dallas', 'houston',
        'miami', 'atlanta', 'chicago', 'boston', 'philadelphia', 'detroit',
        'phoenix', 'vegas', 'francisco', 'angeles', 'diego'
    }
    
    @staticmethod
    def _smart_split_role_location(content: str) -> Optional[Tuple[str, str]]:
        """
        Smart splitting of content into role and location
        
        Args:
            content: The content after command (e.g., "Data Scientist New York")
            
        Returns:
            Tuple[str, str]: (role, location) if successful, None otherwise
        """
        content_lower = content.lower().strip()
        words = content.split()
        
        if len(words) < 2:
            return None
        
        # Check for known multi-word locations first
        for location in CommandParser.COMMON_LOCATIONS:
            if content_lower.endswith(' ' + location):
                role = content[:-len(location)].strip()
                location_proper = content[-len(location):].strip()
                if role:
                    return (role, location_proper)
        
        # Check if last word is a known single-word location
        last_word = words[-1].lower()
        if last_word in CommandParser.COMMON_SINGLE_LOCATIONS:
            role = ' '.join(words[:-1])
            location = words[-1]
            if role:
                return (role, location)
        
        # If no known location found, try different splits
        # For "Data Scientist New York", try:
        # 1. "Data Scientist" + "New York" (last 2 words as location)
        # 2. "Data Scientist New" + "York" (last 1 word as location)
        
        if len(words) >= 3:
            # Try last 2 words as location
            role = ' '.join(words[:-2])
            location = ' '.join(words[-2:])
            if role and location:
                return (role, location)
        
        # Default: last word as location
        role = ' '.join(words[:-1])
        location = words[-1]
        if role and location:
            return (role, location)
        
        return None
    
    @staticmethod
    def parse_register_command(message: str) -> Optional[Tuple[str, str]]:
        """
        Parse register command: 'register <role> <location>'
        
        Args:
            message: The incoming message text
            
        Returns:
            Tuple[str, str]: (role, location) if valid, None if invalid
        """
        # Remove extra whitespace
        message = message.strip()
        
        # Match pattern: register followed by content
        pattern = r'^register\s+(.+)$'
        match = re.match(pattern, message, re.IGNORECASE)
        
        if match:
            content = match.group(1).strip()
            return CommandParser._smart_split_role_location(content)
        
        return None
    
    @staticmethod
    def parse_post_command(message: str) -> Optional[Tuple[str, str]]:
        """
        Parse post command: 'post <role> <location>'
        
        Args:
            message: The incoming message text
            
        Returns:
            Tuple[str, str]: (role, location) if valid, None if invalid
        """
        # Remove extra whitespace
        message = message.strip()
        
        # Match pattern: post followed by content
        pattern = r'^post\s+(.+)$'
        match = re.match(pattern, message, re.IGNORECASE)
        
        if match:
            content = match.group(1).strip()
            return CommandParser._smart_split_role_location(content)
        
        return None
    
    @staticmethod
    def is_help_command(message: str) -> bool:
        """Check if message is asking for help"""
        help_keywords = ['help', 'commands', 'how', 'what', 'start', 'hi', 'hello']
        message_lower = message.lower().strip()
        
        return any(keyword in message_lower for keyword in help_keywords)
    
    @staticmethod
    def get_help_message() -> str:
        """Get the help message with available commands"""
        return (
            "🤖 *Welcome to JobBot!*\n\n"
            "*Available Commands:*\n\n"
            "📝 *register <role> <location>*\n"
            "   Register as a job seeker\n"
            "   Example: `register developer london`\n\n"
            "💼 *post <role> <location>*\n"
            "   Post a job (for employers)\n"
            "   Example: `post developer london`\n\n"
            "❓ *help*\n"
            "   Show this help message\n\n"
            "_Note: Commands are case-insensitive_"
        )
    
    @staticmethod
    def get_invalid_command_message() -> str:
        """Get message for invalid commands"""
        return (
            "❌ *Invalid command format*\n\n"
            "Please use one of these formats:\n"
            "• `register <role> <location>`\n"
            "• `post <role> <location>`\n"
            "• `help`\n\n"
            "Type 'help' for more information."
        ) 