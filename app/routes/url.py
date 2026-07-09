from fastapi import APIRouter, HTTPException , Depends
from app.utils import generate_short_code
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import URLCreate, URLResponse
from sqlalchemy.exc import IntegrityError
from app.models import UrlMapping
from datetime import datetime
from fastapi.responses import RedirectResponse



router = APIRouter()

MAX_RETRIES = 5 

@router.post("/shorten" , response_model=URLResponse)
def shorten_url(data: URLCreate, db: Session = Depends(get_db)):
    for _ in range(MAX_RETRIES):
        short_code = generate_short_code()
        new_url = UrlMapping(
            original_url = str(data.url),
            short_code = short_code,
        )
        
        try:
            db.add(new_url)
            db.commit()
            db.refresh(new_url)
            return new_url
        except IntegrityError: 
            db.rollback()
            continue
    
    raise HTTPException(
    status_code=500,
    detail="Could not generate a unique short code."
)
    
@router.get("/{short_code}")
def redirect_to_original_url(
    short_code: str,
    db: Session = Depends(get_db)
):
    # sanitize short_code: Swagger UI or callers may include surrounding quotes
    short_code = short_code.strip('"').strip("'")
    url_mapping = (
        db.query(UrlMapping)
        .filter(UrlMapping.short_code == short_code)
        .first()
    )

    if url_mapping is None:
        raise HTTPException(
            status_code=404,
            detail="Short code not found"
        )

    
    url_mapping.clicks += 1
    db.commit()

    
    return RedirectResponse(
        url=url_mapping.original_url,
        status_code=307
    )