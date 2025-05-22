# Configuration file for API keys and settings
import os

# Get GROQ API key from environment variable or set directly
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key-here")

# Other configurations
MAX_CRAWL_DEPTH = 1
REQUEST_TIMEOUT = 10