from fastapi import APIRouter, Depends, HTTPException
from .. import schemas, crud
from ..dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/links")

@router.post("/shorten", response_model=schemas.Link)
def create_short_link(link: schemas.LinkCreate, db: Session = Depends(get_db)):
    return crud.create_link(db, link)

@router.get("/{short_code}")
def redirect_link(short_code: str, db: Session = Depends(get_db)):
    link = crud.get_link_by_short_code(db, short_code)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    crud.update_link_clicks(db, link)
    return {"url": link.original_url}