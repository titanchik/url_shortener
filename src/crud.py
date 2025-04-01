from sqlalchemy.orm import Session
from . import models, schemas
from .utils import generate_short_code

def get_link_by_short_code(db: Session, short_code: str):
    return db.query(models.Link).filter(models.Link.short_code == short_code).first()

def create_link(db: Session, link: schemas.LinkCreate, user_id: int = None):
    short_code = link.custom_alias or generate_short_code()
    db_link = models.Link(
        original_url=str(link.original_url),
        short_code=short_code,
        expires_at=link.expires_at,
        user_id=user_id
    )
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

def update_link_clicks(db: Session, link: models.Link):
    link.clicks += 1
    link.last_clicked_at = func.now()
    db.commit()
    db.refresh(link)
    return link