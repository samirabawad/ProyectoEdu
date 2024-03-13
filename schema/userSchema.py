
#Data enviada del cliente a la API
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from enum import Enum
from pydantic import BaseModel
from datetime import date, time
from typing import Optional


#modificaaaar los post, get, update, solo funciona empleado


#schema base de un registro de temperatura, del que se basan otros schemas.
class RegistroTempBase(BaseModel):
    temperatura: float
    id_empleado: int
    id_refrigerador: int
    turno_registro:  int #turno del registro (1,2,3 o 4)

#schema para que el usuario pueda crear los campos de un registro desde el frontend.
class RegistroTempCreate(RegistroTempBase):
    pass

#schema para leer los campos de registro guardado en la base de datos.
class RegistroTemp(RegistroTempBase):
    id: int
    fecha: date  # Cambiar esto según el formato deseado
    hora: time   # Cambiar esto según el formato deseado
    class Config:
        orm_mode = True

#schema para la actualización de un registro.
class RegistroUpdate(BaseModel):
    temperatura: Optional[float] = None
    id_empleado: Optional[int] = None
    id_refrigerador: Optional[int] = None
    turno_registro:  Optional[int] = None
    id: Optional[int] = None
    fecha: Optional[date] = None  # Cambiar esto según el formato deseado
    hora: Optional[time] = None  # Cambiar esto según el formato deseado
    class Config:
        orm_mode = True




#schema base de un empleado, del que se basan otros schemas.
class EmpleadoBase(BaseModel):
    rut: str
    nombre: str
    apellido: str
    usuario: str
    email: str #después cambiar a tipo email

#schema para que el usuario pueda crear los campos de un empleado desde el frontend.
class EmpleadoCreate(EmpleadoBase):
    clave: str

#schema para leer los campos de usuario guardado en la base de datos.
class Empleado(EmpleadoBase):
    id: int
    activo: bool
    #registros_temperatura: list[Registro_temperatura] = [] #los registros de temperatura a los que esta asociado el empleado
    class Config:
        orm_mode = True

#schema para la actualización de un empleado.
class EmpleadoUpdate(BaseModel):
    rut: Optional[str] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    usuario: Optional[str] = None
    email: Optional[str] = None
    clave: Optional[str] = None
    id: Optional[int] = None
    activo: Optional[bool] = None
    class Config:
        orm_mode = True


#modificaaaar los post, get, update, solo funciona empleado


#schema base de un refrigerador, del que se basan otros schemsas.
class RefrigeradorBase(BaseModel):
    nombre: str
    descripcion: str

#schema para que el usuario pueda crear los campos de un refrigerador desde el frontend.
class RefrigeradorCreate(RefrigeradorBase):
    pass

#schema para leer los campos de refrigerador guardado en la base de datos.
class Refrigerador(RefrigeradorBase):
    id: int
    activo: bool
    #registros_temperatura: list[Registro_temperatura] = [] #los registros de temperatura a los que esta asociado el empleado
    class Config:
        orm_mode = True

#schema para la actualización de un refrigerador.
class RefrigeradorUpdate(BaseModel):
    rut: Optional[str] = None
    descripcion: Optional[str] = None
    id: Optional[int] = None
    activo: Optional[bool] = None
    class Config:
        orm_mode = True




class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None





