from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/items",
    tags=["Items"],
    responses={404: {"description": "Не найдено"}},
)

@router.post("/", response_model=schemas.Item, summary="Создать новый товар", tags=["Товары"])
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Создает новый товар в базе данных.

    - **title**: Название товара (обязательно).
    - **description**: Описание товара (необязательно).
    """
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[schemas.Item], summary="Получить список всех товаров", tags=["Товары"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Возвращает список всех товаров из базы данных.

    - **skip**: Количество записей для пропуска (по умолчанию 0).
    - **limit**: Максимальное количество возвращаемых записей (по умолчанию 100).
    """
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items

@router.get("/{item_id}", response_model=schemas.Item, summary="Получить товар по ID", tags=["Товары"])
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
    Возвращает товар по указанному ID.

    - **item_id**: ID товара.
    """
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return db_item

# Mock Item Model for demonstration purposes.
class MockItem(Base):
    __tablename__ = "mock_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)