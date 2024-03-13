from fastapi import APIRouter, status, Depends
from schema.userSchema import Token, TokenData

from sqlalchemy.orm import Session

from schema import userSchema
import crud
from starlette.exceptions import HTTPException as StarletteHTTPException
from dependencies import get_token_header, get_query_token
from database import SessionLocal
from fastapi.encoders import jsonable_encoder


#patch y put no funcionan.

router= APIRouter(
    tags=["empleados"],
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

#obtiene un empleado por id
@router.get("/emps/{emp_id}", response_model= userSchema.Empleado)
def read_emp(emp_id: int, db: Session = Depends(get_db)):
    db_emp = crud.get_emp(db, emp_id=emp_id) #crear func get_emp
    if db_emp is None:
        raise StarletteHTTPException(status_code= 404, detail= "Empleado no encontrado")
    return db_emp

#obtiene todos los empleados
@router.get("/emps/", response_model=list[userSchema.Empleado])
def read_emps(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    empleados = crud.get_emps(db, skip=skip, limit=limit) #crear func get_emps
    return empleados

#crea un nuevo empleado
@router.post("/emps/", response_model=userSchema.Empleado, status_code= status.HTTP_201_CREATED)
def create_emp(emp: userSchema.EmpleadoCreate, db: Session = Depends(get_db)):
    db_emp = crud.get_emp_by_email(db, email=emp.email) 
    if db_emp:
        raise  StarletteHTTPException(status_code=400, detail="Email ya está registrado")
    return crud.create_emp(db=db, emp=emp) 


#Desde un objeto Empleado, puede acceder al objeto Registro_temperatura asociado a través del atributo registros_temperatura.
@router.get("/emp_regs/", response_model=list[userSchema.RegistroTemp])
def read_emp_registros(emp_id: int ,skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_emp_registros = crud.get_emp_registros(db, emp_id = emp_id)
    if db_emp_registros is None:
        raise StarletteHTTPException(status_code= 404, detail= "No se encuentran registros de este empleado")
    return db_emp_registros

#borra un empleado
@router.delete("/emps/{emp_id}", response_model=userSchema.Empleado)
def delete_emp(emp_id: int, db: Session = Depends(get_db)):
    db_emp = crud.get_emp(db, emp_id= emp_id)
    if db_emp is None:
        raise StarletteHTTPException(status_code=404, detail="Empleado no encontrado")
    db.delete(db_emp)
    db.commit()
    return db_emp



#actualiza a un empleado.
#modificar que put no pueda modificar el rut ni el email ya que son unicos.
@router.put("/emps/{emp_id}", response_model= userSchema.Empleado)
def update_emp_by_id(emp:userSchema.EmpleadoUpdate ,emp_id: int, db: Session = Depends(get_db)):
    db_emp = crud.get_emp(db, emp_id=emp_id)
    if db_emp is None:
        raise StarletteHTTPException(status_code= 404, detail= "Empleado no encontrado")
    update_emp_encoded = jsonable_encoder(emp)
    for key, value in update_emp_encoded.items():
        setattr(db_emp, key, value)
    db.commit()
    return db_emp

#actualiza un empleado
@router.patch("/emps/{emp_id}", response_model=userSchema.Empleado)
def patch_emp(emp_id: int, emp: userSchema.EmpleadoUpdate, db: Session = Depends(get_db)):
    db_emp = crud.get_emp(db, emp_id=emp_id)
    if db_emp is None:
        raise StarletteHTTPException(status_code=404, detail="Empleado no encontrado")

    for key, value in emp.model_dump(exclude_unset=True).items():
        setattr(db_emp, key, value)
    db.commit()
    db.refresh(db_emp)
    return db_emp

