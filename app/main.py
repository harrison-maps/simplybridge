from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.models import user
from app.models import developer_profile
from app.models import project
from app.models import message
from app.routes.auth import router as auth_router
from app.routes.profile import router as profile_router
from app.routes.projects import router as projects_router
from app.routes.messages import router as messages_router
from app.core.config import settings
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
possible_paths = [
    os.path.join(BASE_DIR, "frontend"),
    os.path.join(os.path.dirname(BASE_DIR), "frontend"),
    os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), "frontend"),
]
FRONTEND_DIR = None
for path in possible_paths:
    if os.path.exists(path):
        FRONTEND_DIR = path
        break
if FRONTEND_DIR is None:
    FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

print(f"Frontend directory: {FRONTEND_DIR}")
print(f"Frontend exists: {os.path.exists(FRONTEND_DIR)}")

if os.path.exists(FRONTEND_DIR):
    print(f"Mounting static files from {FRONTEND_DIR}")
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

allowed_origins = ["http://localhost:3000", "http://localhost:8000"]
if settings.FRONTEND_URL:
    allowed_origins.append(settings.FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(profile_router, tags=["Profiles"])
app.include_router(projects_router, prefix="/api", tags=["Projects"])
app.include_router(messages_router, tags=["Messages"])
Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Root"])
def root():
    if FRONTEND_DIR and os.path.exists(os.path.join(FRONTEND_DIR, "landing_page.html")):
        return FileResponse(os.path.join(FRONTEND_DIR, "landing_page.html"))
    return {"message": "SimplyBridge API is running", "docs": "/docs"}


@app.get("/debug", tags=["Debug"])
def debug():
    return {"frontend_dir": FRONTEND_DIR, "exists": os.path.exists(FRONTEND_DIR) if FRONTEND_DIR else False}


@app.get("/landing_page", tags=["Frontend"])
async def serve_landing_page():
    """Serve landing page"""
    return FileResponse(os.path.join(FRONTEND_DIR, "landing_page.html"))

@app.get("/login", tags=["Frontend"])
async def serve_login():
    return FileResponse(os.path.join(FRONTEND_DIR, "login.html"))

@app.get("/register", tags=["Frontend"])
async def serve_register():
    return FileResponse(os.path.join(FRONTEND_DIR, "register.html"))

@app.get("/developer_dashboard", tags=["Frontend"])
async def serve_developer_dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "developer_dashboard.html"))

@app.get("/developer_profile", tags=["Frontend"])
async def serve_developer_profile():
    return FileResponse(os.path.join(FRONTEND_DIR, "developer_profile.html"))

@app.get("/developer_directory", tags=["Frontend"])
async def serve_developer_directory():
    return FileResponse(os.path.join(FRONTEND_DIR, "developer_directory.html"))


@app.get("/{page}", tags=["Frontend"])
async def serve_frontend_page_fallback(page: str):
    """Serve frontend HTML pages - fallback"""
    if page in ["docs", "openapi.json", "redoc", "debug"]:
        return {"error": "Not found"}
    if not FRONTEND_DIR or not os.path.exists(FRONTEND_DIR):
        return HTMLResponse(content=f"<h1>SimplyBridge</h1><p>Frontend not found</p>")
    
    for name in [page, f"{page}.html"]:
        page_path = os.path.join(FRONTEND_DIR, name)
        if os.path.exists(page_path) and os.path.isfile(page_path):
            return FileResponse(page_path)
    
    return FileResponse(os.path.join(FRONTEND_DIR, "landing_page.html"))
