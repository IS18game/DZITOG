from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import SessionLocal, engine

from .routers import items

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items.router)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    return {"message": "Добро пожаловать в магазин комплектующих!"}


@app.post("/videocards/", response_model=schemas.VideoCard, summary="Создать новую видеокарту", tags=["Видеокарты"])
def create_videocard(videocard: schemas.VideoCardCreate, db: Session = Depends(get_db)):
    """
    Создает новую видеокарту в базе данных.

    - **name**: Название видеокарты (обязательно).
    - **manufacturer**: Производитель видеокарты (обязательно).
    - **memory**: Объем памяти видеокарты в GB (обязательно).
    - **price**: Цена видеокарты (обязательно).
    - **description**: Описание видеокарты (необязательно).
    """
    db_videocard = models.VideoCard(**videocard.dict())
    db.add(db_videocard)
    db.commit()
    db.refresh(db_videocard)
    return db_videocard


@app.get("/videocards/", response_model=List[schemas.VideoCard], summary="Получить список всех видеокарт", tags=["Видеокарты"])
def read_videocards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Возвращает список всех видеокарт из базы данных.

    - **skip**: Количество записей для пропуска (по умолчанию 0).
    - **limit**: Максимальное количество возвращаемых записей (по умолчанию 100).
    """
    videocards = db.query(models.VideoCard).offset(skip).limit(limit).all()
    return videocards


@app.get("/videocards/{videocard_id}", response_model=schemas.VideoCard, summary="Получить видеокарту по ID", tags=["Видеокарты"])
def read_videocard(videocard_id: int, db: Session = Depends(get_db)):
    """
    Возвращает видеокарту по указанному ID.

    - **videocard_id**: ID видеокарты.
    """
    db_videocard = db.query(models.VideoCard).filter(models.VideoCard.id == videocard_id).first()
    if db_videocard is None:
        raise HTTPException(status_code=404, detail="Видеокарта не найдена")
    return db_videocard


@app.post("/cpus/", response_model=schemas.CPU, summary="Создать новый процессор", tags=["Процессоры"])
def create_cpu(cpu: schemas.CPUCreate, db: Session = Depends(get_db)):
    """
    Создает новый процессор в базе данных.

    - **name**: Название процессора (обязательно).
    - **manufacturer**: Производитель процессора (обязательно).
    - **cores**: Количество ядер процессора (обязательно).
    - **clock_speed**: Тактовая частота процессора в GHz (обязательно).
    - **price**: Цена процессора (обязательно).
    - **description**: Описание процессора (необязательно).
    """
    db_cpu = models.CPU(**cpu.dict())
    db.add(db_cpu)
    db.commit()
    db.refresh(db_cpu)
    return db_cpu


@app.get("/cpus/", response_model=List[schemas.CPU], summary="Получить список всех процессоров", tags=["Процессоры"])
def read_cpus(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Возвращает список всех процессоров из базы данных.

    - **skip**: Количество записей для пропуска (по умолчанию 0).
    - **limit**: Максимальное количество возвращаемых записей (по умолчанию 100).
    """
    cpus = db.query(models.CPU).offset(skip).limit(limit).all()
    return cpus


@app.get("/cpus/{cpu_id}", response_model=schemas.CPU, summary="Получить процессор по ID", tags=["Процессоры"])
def read_cpu(cpu_id: int, db: Session = Depends(get_db)):
    """
    Возвращает процессор по указанному ID.

    - **cpu_id**: ID процессора.
    """
    db_cpu = db.query(models.CPU).filter(models.CPU.id == cpu_id).first()
    if db_cpu is None:
        raise HTTPException(status_code=404, detail="Процессор не найден")
    return db_cpu