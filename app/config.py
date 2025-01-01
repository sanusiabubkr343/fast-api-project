import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgres://postgres:postgrespw@localhost:55000/blog")
