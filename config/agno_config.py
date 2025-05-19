
"""
Agno framework configuration for SEO InsightHub
"""
import os
from agno import configure_logging

def setup_agno_config():
    """Configure Agno framework settings"""
    
    # Configure logging
    configure_logging(
        level="INFO",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Environment-specific settings
    config = {
        "development": {
            "log_level": "DEBUG",
            "async_timeout": 30,
            "max_concurrent_agents": 5
        },
        "production": {
            "log_level": "INFO",
            "async_timeout": 60,
            "max_concurrent_agents": 10
        }
    }
    
    env = os.getenv("ENVIRONMENT", "development")
    return config.get(env, config["development"])