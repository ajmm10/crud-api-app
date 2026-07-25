from fastapi import Depends, FastAPI, HTTPException, status

from app.models import Producto, ProductoCreate, ProductoUpdate
from app.security import verify_api_key

app = FastAPI(title="Fiestas Mexicanas - Productos API")

# Storage en memoria
db: dict[int, Producto] = {}
next_id = 1


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/productos", response_model=list[Producto], dependencies=[Depends(verify_api_key)])
def listar_productos():
    return list(db.values())


@app.get("/productos/{producto_id}", response_model=Producto, dependencies=[Depends(verify_api_key)])
def obtener_producto(producto_id: int):
    if producto_id not in db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db[producto_id]


@app.post("/productos", response_model=Producto, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_api_key)])
def crear_producto(producto: ProductoCreate):
    global next_id
    nuevo = Producto(id=next_id, **producto.model_dump())
    db[next_id] = nuevo
    next_id += 1
    return nuevo


@app.put("/productos/{producto_id}", response_model=Producto, dependencies=[Depends(verify_api_key)])
def actualizar_producto(producto_id: int, producto: ProductoUpdate):
    if producto_id not in db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    actual = db[producto_id]
    datos = producto.model_dump(exclude_unset=True)
    actualizado = actual.model_copy(update=datos)
    db[producto_id] = actualizado
    return actualizado


@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verify_api_key)])
def eliminar_producto(producto_id: int):
    if producto_id not in db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    del db[producto_id]
