from typing import Optional

from pydantic import BaseModel


class VideoCardBase(BaseModel):
    name: str
    manufacturer: str
    memory: int
    price: float
    description: Optional[str] = None


class VideoCardCreate(VideoCardBase):
    pass


class VideoCard(VideoCardBase):
    id: int

    class Config:
        orm_mode = True


class CPUBase(BaseModel):
    name: str
    manufacturer: str
    cores: int
    clock_speed: float
    price: float
    description: Optional[str] = None


class CPUCreate(CPUBase):
    pass


class CPU(CPUBase):
    id: int

    class Config:
        orm_mode = True

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True