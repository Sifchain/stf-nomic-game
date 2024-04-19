import os

from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from . import app
from .routes import router as api_router

# Load environment variables
load_dotenv()

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
