from sqlalchemy.orm import Session
from model import usersModel
from schema import userSchema
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import SessionLocal
from datetime import datetime
from sqlalchemy import func



#funciones dedicadas a interactuar con la base de datos, independiente de las funciones del path

#hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)


#crud empleados
def get_emp(db: Session, emp_id: int):
    return db.query(usersModel.Empleado).filter(usersModel.Empleado.id == emp_id).first()

def get_emp_by_email(db: Session, email: str):
    return db.query(usersModel.Empleado).filter(usersModel.Empleado.email == email).first()

def get_emp_by_rut(db: Session, rut: str):
    return db.query(usersModel.Empleado).filter(usersModel.Empleado.rut == rut).first()

def get_emps(db: Session, skip: int = 0, limit: int = 100):
    return db.query(usersModel.Empleado).offset(skip).limit(limit).all()

def create_emp(db: Session, emp: userSchema.EmpleadoCreate):
    clave_hash = get_password_hash(emp.clave)
    db_emp = usersModel.Empleado(email=emp.email, nombre= emp.nombre, apellido= emp.apellido, usuario= emp.usuario, rut= emp.rut, clave=clave_hash)
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

#registros de un empleado:
def get_emp_registros(db: Session, emp_id: int):
    v_emp_id = db.query(usersModel.Empleado).filter(usersModel.Empleado.id == emp_id).first()
    if v_emp_id is None:
        return None
    db_emp_registros=db.query(usersModel.Registro_temperatura).filter(usersModel.Registro_temperatura.id_empleado == emp_id).all()
    return db_emp_registros



#crud refrigerador
def get_refrigerador(db: Session, refr_id: int):
    return db.query(usersModel.Refrigerador).filter(usersModel.Refrigerador.id == refr_id).first()

def get_refrigerador_by_nombre(db: Session, nombre: str):
    return db.query(usersModel.Refrigerador).filter(usersModel.Refrigerador.nombre == nombre).first()

def get_refrigeradores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(usersModel.Refrigerador).offset(skip).limit(limit).all()

def create_refrigerador(db: Session, refr: userSchema.RefrigeradorCreate):
    db_refr = usersModel.Refrigerador(nombre=refr.nombre, descripcion= refr.descripcion)
    db.add(db_refr)
    db.commit()
    db.refresh(db_refr)
    return db_refr

#registros de un refrigerador:
def get_refr_registros(db: Session, refr_id: int):
    v_refr_id = db.query(usersModel.Refrigerador).filter(usersModel.Refrigerador.id == refr_id).first()
    if v_refr_id is None:
        return None
    db_refr_registros=db.query(usersModel.Registro_temperatura).filter(usersModel.Registro_temperatura.id_refrigerador == refr_id).all()
    return db_refr_registros



#crud registros
def get_registroTemp(db: Session, reg_id: int):
    return db.query(usersModel.Registro_temperatura).filter(usersModel.Registro_temperatura.id == reg_id).first()

def get_registroTemp_by_id(db: Session, id_reg: str):
    return db.query(usersModel.Refrigerador).filter(usersModel.Refrigerador.id == id_reg).first()

def get_registrosTemp(db: Session, skip: int = 0, limit: int = 100):
    return db.query(usersModel.Registro_temperatura).offset(skip).limit(limit).all()

def create_registroTemp(db: Session, reg: userSchema.RegistroTempCreate):
    #fecha_actual = datetime.now().date().strftime("%Y-%m-%d")
    #hora_actual = datetime.now().time().strftime("%H:%M:%S")
    fecha_actual = datetime.now().date()
    hora_actual = datetime.now().time()
    print(type(fecha_actual)) #class 'str'
    print(type(hora_actual)) #class 'str'
    print(type(datetime.now().date())) #class 'datetime.date'
    print(type(datetime.now().time())) #class 'datetime.time'
    db_reg = usersModel.Registro_temperatura(fecha= fecha_actual, hora= hora_actual, temperatura= reg.temperatura, id_empleado = reg.id_empleado, id_refrigerador= reg.id_refrigerador, turno_registro= reg.turno_registro)
    db.add(db_reg)
    db.commit()
    db.refresh(db_reg)
    return db_reg

def get_reg_dia(db: Session, fecha_dia: datetime.date):
    v_reg_dia = db.query(usersModel.Registro_temperatura).filter(
        func.date(usersModel.Registro_temperatura.fecha) == fecha_dia
    ).all()
    if not v_reg_dia:
        return None
    return v_reg_dia

def get_reg_turno(db: Session, turno: int):
    v_reg_turno = db.query(usersModel.Registro_temperatura).filter(usersModel.Registro_temperatura.turno_registro == turno).all()
    if not v_reg_turno:
        return None
    return v_reg_turno