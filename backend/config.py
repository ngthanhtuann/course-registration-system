import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

JWT_SECRET = os.getenv("JWT_SECRET", "")
if len(JWT_SECRET) < 32 or JWT_SECRET == "dev-secret-change-me":
    raise RuntimeError("Set JWT_SECRET to a random secret of at least 32 characters in backend/.env")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 8
