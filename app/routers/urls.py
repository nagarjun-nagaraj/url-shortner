import random
import string
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app import models, schemas
from app.cache import get_cached_url, set_cached_url

router = APIRouter()


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


@router.post("/shorten", response_model=schemas.URLResponse)
def shorten_url(url: schemas.URLCreate, db: Session = Depends(get_db)):
    for _ in range(5):
        try:
            short_code = generate_short_code()
            db_url = models.URL(
                original_url=str(url.original_url),
                short_code=short_code
            )
            db.add(db_url)
            db.commit()
            db.refresh(db_url)
            return db_url
        except IntegrityError:
            db.rollback()
    raise HTTPException(status_code=500, detail="Could not generate unique code")


@router.get("/stats/{short_code}", response_model=schemas.URLStats)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="Short code not found")
    return db_url


@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    # check Redis first
    cached = get_cached_url(short_code)
    if cached:
        return RedirectResponse(url=cached.decode("utf-8"))

    # not in cache — hit the DB
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="Short code not found")

    db_url.clicks += 1
    db.commit()

    # save to cache for next time
    set_cached_url(short_code, db_url.original_url)

    return RedirectResponse(url=db_url.original_url)