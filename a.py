from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file
password = os.getenv('PASSWORD')
username = os.getenv('USERNAME')
print(password)
print(username)
