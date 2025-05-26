import unittest
from unittest.mock import Mock, patch
from app.bot.commands import CommandParser
from app.models.user import User
from app.models.job import Job
from app.services.matcher_service import MatcherService

class TestCommandParser(unittest.TestCase):
    """Test cases for command parsing"""
    
    def test_parse_register_command_valid(self):
        """Test valid register command parsing"""
        result = CommandParser.parse_register_command("register developer london")
        self.assertEqual(result, ("developer", "london"))
        
        result = CommandParser.parse_register_command("REGISTER Data Scientist New York")
        self.assertEqual(result, ("Data Scientist", "New York"))
    
    def test_parse_register_command_invalid(self):
        """Test invalid register command parsing"""
        result = CommandParser.parse_register_command("register developer")
        self.assertIsNone(result)
        
        result = CommandParser.parse_register_command("register")
        self.assertIsNone(result)
        
        result = CommandParser.parse_register_command("invalid command")
        self.assertIsNone(result)
    
    def test_parse_post_command_valid(self):
        """Test valid post command parsing"""
        result = CommandParser.parse_post_command("post developer london")
        self.assertEqual(result, ("developer", "london"))
        
        result = CommandParser.parse_post_command("POST Marketing Manager Berlin")
        self.assertEqual(result, ("Marketing Manager", "Berlin"))
    
    def test_parse_post_command_invalid(self):
        """Test invalid post command parsing"""
        result = CommandParser.parse_post_command("post developer")
        self.assertIsNone(result)
        
        result = CommandParser.parse_post_command("post")
        self.assertIsNone(result)
    
    def test_is_help_command(self):
        """Test help command detection"""
        self.assertTrue(CommandParser.is_help_command("help"))
        self.assertTrue(CommandParser.is_help_command("HELP"))
        self.assertTrue(CommandParser.is_help_command("hi"))
        self.assertTrue(CommandParser.is_help_command("hello"))
        self.assertTrue(CommandParser.is_help_command("what can you do"))
        self.assertFalse(CommandParser.is_help_command("register developer london"))

class TestUser(unittest.TestCase):
    """Test cases for User model"""
    
    def test_user_creation(self):
        """Test user creation"""
        user = User("+1234567890", "Developer", "London")
        self.assertEqual(user.phone_number, "+1234567890")
        self.assertEqual(user.role, "developer")
        self.assertEqual(user.location, "london")
        self.assertTrue(user.is_active)
    
    def test_user_matches_job(self):
        """Test job matching logic"""
        user = User("+1234567890", "developer", "london")
        
        # Should match
        self.assertTrue(user.matches_job("Developer", "London"))
        self.assertTrue(user.matches_job("DEVELOPER", "LONDON"))
        
        # Should not match
        self.assertFalse(user.matches_job("designer", "london"))
        self.assertFalse(user.matches_job("developer", "paris"))

class TestJob(unittest.TestCase):
    """Test cases for Job model"""
    
    def test_job_creation(self):
        """Test job creation"""
        job = Job("+1234567890", "Developer", "London")
        self.assertEqual(job.employer_phone, "+1234567890")
        self.assertEqual(job.role, "developer")
        self.assertEqual(job.location, "london")
        self.assertTrue(job.is_active)
        self.assertIsNotNone(job.id)
    
    def test_job_alert_message(self):
        """Test job alert message generation"""
        job = Job("+1234567890", "Developer", "London")
        message = job.get_alert_message()
        self.assertIn("New Job Alert", message)
        self.assertIn("Developer", message)
        self.assertIn("London", message)

class TestMatcherService(unittest.TestCase):
    """Test cases for MatcherService"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.matcher = MatcherService()
    
    def test_register_user(self):
        """Test user registration"""
        result = self.matcher.register_user("+1234567890", "developer", "london")
        self.assertTrue(result)
        
        user = self.matcher.get_user_by_phone("+1234567890")
        self.assertIsNotNone(user)
        self.assertEqual(user.role, "developer")
        self.assertEqual(user.location, "london")
    
    def test_register_user_update(self):
        """Test updating existing user"""
        # Register user first time
        self.matcher.register_user("+1234567890", "developer", "london")
        
        # Update user preferences
        self.matcher.register_user("+1234567890", "designer", "paris")
        
        user = self.matcher.get_user_by_phone("+1234567890")
        self.assertEqual(user.role, "designer")
        self.assertEqual(user.location, "paris")
    
    def test_post_job(self):
        """Test job posting"""
        job = self.matcher.post_job("+1234567890", "developer", "london")
        self.assertIsNotNone(job)
        self.assertEqual(job.role, "developer")
        self.assertEqual(job.location, "london")
    
    def test_find_matching_users(self):
        """Test finding matching users for a job"""
        # Register some users
        self.matcher.register_user("+1111111111", "developer", "london")
        self.matcher.register_user("+2222222222", "designer", "london")
        self.matcher.register_user("+3333333333", "developer", "paris")
        
        # Post a job
        job = self.matcher.post_job("+9999999999", "developer", "london")
        
        # Find matches
        matches = self.matcher.find_matching_users(job)
        
        # Should only match the first user
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].phone_number, "+1111111111")
    
    def test_get_user_stats(self):
        """Test getting user statistics"""
        # Register some users
        self.matcher.register_user("+1111111111", "developer", "london")
        self.matcher.register_user("+2222222222", "designer", "london")
        
        # Post a job
        self.matcher.post_job("+9999999999", "developer", "london")
        
        stats = self.matcher.get_user_stats()
        self.assertEqual(stats['total_users'], 2)
        self.assertEqual(stats['active_users'], 2)
        self.assertEqual(stats['total_jobs'], 1)

if __name__ == '__main__':
    unittest.main() 