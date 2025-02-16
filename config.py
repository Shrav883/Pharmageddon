import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Config:
    username = "skardeka"
    password = "Shravani@83K"
    encoded_password = quote_plus(password)  # Encodes special characters

    MONGO_URI = os.getenv('MONGO_URI') or f'mongodb+srv://{username}:{encoded_password}@hacklahoma25.hxd1x.mongodb.net/'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
