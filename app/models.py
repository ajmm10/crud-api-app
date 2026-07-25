
from pydantic import BaseModel


class ProductoBase(BaseModel):
    nombre: str
    categoria: str
    precio: float
    stock: int


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: str | None = None
    categoria: str | None = None
    precio: float | None = None
    stock: int | None = None


class Producto(ProductoBase):
    id: int
