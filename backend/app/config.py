from pathlib import Path
from dotenv import load_dotenv
import os

base_dir = Path(__file__).resolve().parent.parent
load_dotenv(base_dir / '.env')

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./data.db')
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'gemma2-9b-it')
