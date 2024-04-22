import os

from dotenv import load_dotenv
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from starlette.middleware.base import BaseHTTPMiddleware

from . import app
from .database import SessionLocal, engine
from .routes import router as api_router

# Load environment variables
load_dotenv()


class DBConnectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = None
        try:
            # Attach a session to the request state for the lifespan of the request
            request.state.db = SessionLocal()
            # Use text() to safely execute the plain SQL command
            request.state.db.execute(text("SELECT 1"))
            response = await call_next(request)
        except OperationalError:
            # If an OperationalError occurs, attempt to dispose and reconnect
            engine.dispose()
            request.state.db = SessionLocal()
            # Ensure the reconnection is also wrapped in text()
            request.state.db.execute(text("SELECT 1"))
            response = await call_next(request)
        finally:
            # Close the session after request is handled
            request.state.db.close()
        return response


# Add db middleware to the application
app.add_middleware(DBConnectionMiddleware)

# Add CORS middleware
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    if os.getenv("DEBUG"):
        app.debug = True

    try:
        uvicorn.run("nomic:app", host="0.0.0.0", port=8000, reload=app.debug)
    except KeyboardInterrupt:
        print("Exiting...")
