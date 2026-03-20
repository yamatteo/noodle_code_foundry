import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main() -> None:
    # Access environment variables
    database_url = os.getenv("DATABASE_URL")
    redis_url = os.getenv("REDIS_URL")
    mail_host = os.getenv("MAIL_HOST")
    
    print("Hello from noodle-code-foundry!")
    print(f"Database URL: {database_url}")
    print(f"Redis URL: {redis_url}")
    print(f"Mail Host: {mail_host}")