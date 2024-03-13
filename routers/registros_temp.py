from fastapi import APIRouter, status, Depends, Path
from schema.userSchema import Token, TokenData

from sqlalchemy.orm import Session

from schema import userSchema
import crud
from starlette.exceptions import HTTPException as StarletteHTTPException
from dependencies import get_token_header, get_query_token
from database import SessionLocal
from datetime import date

#todo bien, falta ver los put y patch nomas

#bien todos los get y delete y post. Implementar tbn un get por turno de ingreso

router= APIRouter(
    tags=["registros_temperaturas"],
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

#obtiene un registro por id
@router.get("/regs/{reg_id}", response_model= userSchema.RegistroTemp)
def read_refr(reg_id: int, db: Session = Depends(get_db)):
    db_registro = crud.get_registroTemp(db, reg_id=reg_id) #crear get_registroTemp
    if db_registro is None:
        raise StarletteHTTPException(status_code= 404, detail= "Registro no encontrado")
    return db_registro

#obtiene todos los registros
@router.get("/regs/", response_model=list[userSchema.RegistroTemp])
def read_registros(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    registrosTemp = crud.get_registrosTemp(db, skip=skip, limit=limit)
    return registrosTemp

#crea un nuevo registro
#que no se puedan crear dos registros para el mismo refigerador con un mismo turno de registro en la misma fecha
@router.post("/regs/", response_model=userSchema.RegistroTemp, status_code= status.HTTP_201_CREATED)
def create_registro(reg: userSchema.RegistroTempCreate, db: Session = Depends(get_db)):
    return crud.create_registroTemp(db=db, reg=reg) #crear func create_emp

#borra un registro
@router.delete("/regs/{reg_id}", response_model=userSchema.RegistroTemp)
def delete_reg(reg_id: int, db: Session = Depends(get_db)):
    db_reg = crud.get_registroTemp(db, reg_id= reg_id)
    if db_reg is None:
        raise StarletteHTTPException(status_code=404, detail="Registro no encontrado")
    db.delete(db_reg)
    db.commit()
    return db_reg


@router.get("/regs_dia/{fecha_dia}", response_model=list[userSchema.RegistroTemp])
def read_refr_registros(fecha_dia: date = Path(..., title="Fecha del día", description="Fecha en formato YYYY-MM-DD"),
                        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    print(fecha_dia)
    print(type(fecha_dia))
    db_regs_dia = crud.get_reg_dia(db, fecha_dia=fecha_dia)
    if db_regs_dia is None:
        raise StarletteHTTPException(status_code=404, detail="No se encuentran registros de este día")
    return db_regs_dia

@router.get("/regs_turno/{turno}", response_model=list[userSchema.RegistroTemp])
def read_refr_registros(turno: int = Path(..., title="Turno del día", description="Puede ser turnos: 1,2,3 o 4"),
                        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_regs_turno = crud.get_reg_turno(db, turno=turno)
    if db_regs_turno is None:
        raise StarletteHTTPException(status_code=404, detail="No se encuentran registros de este turno")
    return db_regs_turno


#Luego manejar excepciones de crear un registro con un id_emp que no existe o con un id_refr que no existe.
#actualiza a un registro_temp.
#modificar que put no pueda modificar los campos unicos.
@router.put("/regs/{reg_id}", response_model= userSchema.RegistroTemp)
def update_reg_by_id(reg:userSchema.RegistroUpdate ,reg_id: int, db: Session = Depends(get_db)):
    db_reg = crud.get_reg(db, reg_id=reg_id)
    if db_reg is None:
        raise StarletteHTTPException(status_code= 404, detail= "Registro no encontrado")
    update_reg_encoded = jsonable_encoder(reg)
    for key, value in update_reg_encoded.items():
        setattr(db_reg, key, value)
    db.commit()
    return db_reg

#actualiza a un registro_temp.
@router.patch("/regs/{reg_id}", response_model=userSchema.RegistroTemp)
def patch_reg(reg_id: int, reg: userSchema.RegistroUpdate, db: Session = Depends(get_db)):
    db_reg = crud.get_reg(db, reg_id=reg_id)
    if db_reg is None:
        raise StarletteHTTPException(status_code=404, detail="Registro no encontrado")

    for key, value in reg.model_dump(exclude_unset=True).items():
        setattr(db_reg, key, value)
    db.commit()
    db.refresh(db_reg)
    return db_reg




