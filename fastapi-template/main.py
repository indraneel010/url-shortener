from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import string
import random
import os
from models import URLCreate, URLResponse, URLStats

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./urls.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database model
class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    click_count = Column(Integer, default=0)
    last_accessed = Column(DateTime, nullable=True)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener",
    description="A simple and fast URL shortener service",
    version="1.0.0"
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_short_code(length: int = 6) -> str:
    """Generate a random short code"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def is_valid_url(url: str) -> bool:
    """Basic URL validation"""
    return url.startswith(('http://', 'https://'))

@app.get("/")
def root():
    return {
        "message": "URL Shortener API",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.post("/shorten", response_model=URLResponse)
def create_short_url(url_data: URLCreate, db: Session = Depends(get_db)):
    """Create a shortened URL"""
    if not is_valid_url(url_data.original_url):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    # Check if custom code is provided and available
    if url_data.custom_code:
        existing = db.query(URL).filter(URL.short_code == url_data.custom_code).first()
        if existing:
            raise HTTPException(status_code=400, detail="Custom code already exists")
        short_code = url_data.custom_code
    else:
        # Generate unique short code
        while True:
            short_code = generate_short_code()
            existing = db.query(URL).filter(URL.short_code == short_code).first()
            if not existing:
                break
    
    # Create new URL entry
    db_url = URL(
        original_url=url_data.original_url,
        short_code=short_code
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    
    return URLResponse(
        id=db_url.id,
        original_url=db_url.original_url,
        short_code=db_url.short_code,
        short_url=f"{base_url}/{db_url.short_code}",
        created_at=db_url.created_at,
        click_count=db_url.click_count
    )

@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    """Redirect to the original URL"""
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Update click count and last accessed
    db_url.click_count += 1
    db_url.last_accessed = datetime.utcnow()
    db.commit()
    
    return RedirectResponse(url=db_url.original_url, status_code=301)

@app.get("/stats/{short_code}", response_model=URLStats)
def get_url_stats(short_code: str, db: Session = Depends(get_db)):
    """Get statistics for a shortened URL"""
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    
    return URLStats(
        id=db_url.id,
        original_url=db_url.original_url,
        short_code=db_url.short_code,
        short_url=f"{base_url}/{db_url.short_code}",
        created_at=db_url.created_at,
        click_count=db_url.click_count,
        last_accessed=db_url.last_accessed
    )

@app.get("/api/urls", response_model=list[URLStats])
def list_urls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all URLs with pagination"""
    urls = db.query(URL).offset(skip).limit(limit).all()
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    
    return [
        URLStats(
            id=url.id,
            original_url=url.original_url,
            short_code=url.short_code,
            short_url=f"{base_url}/{url.short_code}",
            created_at=url.created_at,
            click_count=url.click_count,
            last_accessed=url.last_accessed
        )
        for url in urls
    ]
