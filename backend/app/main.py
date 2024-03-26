from dotenv import load_dotenv

load_dotenv()

# imports app to be used by uvicorn/gunicorn
from app.rest.main import app
