#!/usr/bin/env python3
"""
WhatsApp Job Board Bot - Entry Point
"""

import logging
import os
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point for the application"""
    try:
        # Create Flask app
        app = create_app()
        
        # Get port from environment or default to 5000
        port = int(os.getenv('PORT', 5000))
        
        logger.info("Starting WhatsApp Job Board Bot...")
        logger.info(f"Server will run on port {port}")
        logger.info("Webhook endpoint: /webhook")
        logger.info("Status endpoint: /status")
        
        # Run the app
        app.run(
            host='0.0.0.0',
            port=port,
            debug=app.config.get('DEBUG', False)
        )
        
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise

if __name__ == '__main__':
    main() 