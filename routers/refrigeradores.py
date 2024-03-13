from fastapi import APIRouter, status, Depends
from schema.userSchema import Token, TokenData

from sqlalchemy.orm import Session

from schema import userSchema
import crud
from starlette.exceptions import HTTPException as StarletteHTTPException
from dependencies import get_token_header, get_query_token
from database import SessionLocal


#patch y put no funcionan

router= APIRouter(
    tags=["refrigeradores"],
    dependencies=[Depends(get_query_token)]
)
#confirmar si deben o no deben ser function async


# Dependency, crea una sesion por cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#obtiene un refrigerador por id
@router.get("/refrs/{refr_id}", response_model= userSchema.Refrigerador)
def read_refr(refr_id: int, db: Session = Depends(get_db)):
    db_refr = crud.get_refrigerador(db, refr_id=refr_id)
    if db_refr is None:
        raise StarletteHTTPException(status_code= 404, detail= "Refrigerador no encontrado")
    return db_refr

#obtiene todos los refrigeradores
@router.get("/refrs/", response_model=list[userSchema.Refrigerador])
def read_refrs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    refrigeradores = crud.get_refrigeradores(db, skip=skip, limit=limit)
    return refrigeradores

#crea un nuevo refrigerador
@router.post("/refrs/", response_model=userSchema.Refrigerador, status_code= status.HTTP_201_CREATED)
def create_refr(refr: userSchema.RefrigeradorCreate, db: Session = Depends(get_db)):
    db_refr = crud.get_refrigerador_by_nombre(db, nombre=refr.nombre)
    if db_refr:
        raise  StarletteHTTPException(status_code=400, detail="Refrigerador ya está registrado")
    return crud.create_refrigerador(db=db, refr=refr) 


#borra un refrigerador
@router.delete("/refrs/{refr_id}", response_model=userSchema.Refrigerador)
def delete_refr(refr_id: int, db: Session = Depends(get_db)):
    db_refr = crud.get_refrigerador_by_id(db, refr_id= refr_id)
    if db_refr is None:
        raise StarletteHTTPException(status_code=404, detail="Refrigerador no encontrado")
    db.delete(db_refr)
    db.commit()
    return db_refr

#Desde un objeto Refrigerador, puede acceder al objeto Registro_temperatura asociado a través del atributo registros_temperatura.
@router.get("/refr_regs/", response_model=list[userSchema.RegistroTemp])
def read_refr_registros(refr_id: int ,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_refr_registros = crud.get_refr_registros(db, refr_id = refr_id)
    if db_refr_registros is None:
        raise StarletteHTTPException(status_code= 404, detail= "No se encuentran registros de este refrigerador")
    return db_refr_registros


#actualiza a un refrigerador.
#modificar que put no pueda modificar los campos unicos.
@router.put("/refrs/{refr_id}", response_model= userSchema.Refrigerador)
def update_refr_by_id(refr:userSchema.RefrigeradorUpdate ,refr_id: int, db: Session = Depends(get_db)):
    db_refr = crud.get_refr(db, refr_id=refr_id)
    if db_refr is None:
        raise StarletteHTTPException(status_code= 404, detail= "Refrigerador no encontrado")
    update_refr_encoded = jsonable_encoder(refr)
    for key, value in update_refr_encoded.items():
        setattr(db_refr, key, value)
    db.commit()
    return db_refr

#actualiza a un registro_temp.
@router.patch("/regs/{refr_id}", response_model=userSchema.Refrigerador)
def patch_refr(refr_id: int, refr: userSchema.RefrigeradorUpdate, db: Session = Depends(get_db)):
    db_refr = crud.get_refr(db, refr_id=refr_id)
    if db_refr is None:
        raise StarletteHTTPException(status_code=404, detail="Refrigerador no encontrado")

    for key, value in refr.model_dump(exclude_unset=True).items():
        setattr(db_refr, key, value)
    db.commit()
    db.refresh(db_refr)
    return db_refr




