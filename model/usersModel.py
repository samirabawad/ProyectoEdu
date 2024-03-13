from database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# Modelos que migran a la base de datos: Empleado, Refrigerador y Registro_temperatura.

#t__tablename__ indica el nombre de la tabla en la base de datos.

class Empleado(Base):
    __tablename__="empleados"

    id = Column(Integer, primary_key=True) #identificador único autoincremental
    rut = Column(String(length=50), unique=True, index=True) #rut del empleado, con indice para facilitar búsqueda
    nombre = Column(String(length=50))
    apellido = Column(String(length=50))
    usuario = Column(String(length=50)) #nombre de usuario para autentificación
    clave = Column(String(length=100)) #clave para autentificación con hash 
    email = Column(String(length=50), unique=True, index=True)
    activo = Column(Boolean, default=True) #si el empleado está activo o inactivo


    registros_temperatura = relationship('Registro_temperatura', back_populates='empleado') #relación inversa
    #Desde un objeto Empleado, puedes acceder al objeto Registro_temperatura asociado a través del atributo registros_temperatura.


class Refrigerador(Base):
    __tablename__ = 'refrigeradores'
    
    id = Column(Integer, primary_key=True) #identificador único autoincremental.
    nombre = Column(String(length=100)) #nombre o ubicación del refrigerador.
    activo = Column(Boolean, default=True)
    descripcion = Column(String(length=300)) #descripción del refrigerador.
 

    registros_temperatura = relationship('Registro_temperatura', back_populates='refrigerador') #relación inversa
    #Desde un objeto Refrigerador, puedes acceder al objeto Registro_temperatura asociado a través del atributo registros_temperatura.


class Registro_temperatura(Base):
    __tablename__ = 'registros_temperatura'

    id = Column(Integer, primary_key=True) #identificador único autoincremental 
    fecha = Column(Date, nullable=False, default=func.now(), index=True) #hora del registro 
    hora = Column(Time, nullable=False, default=func.now()) #hora del registro
    turno_registro= Column(Integer, nullable=False, index=True) #turno del registro (1,2,3 o 4)
    temperatura = Column(Float, nullable=False) #temperatura registrada

    id_empleado = Column(Integer, ForeignKey("empleados.id"), nullable=False) #clave foránea que se vincula con campo ´id´ de tabla ´empleados´
    id_refrigerador = Column(Integer, ForeignKey("refrigeradores.id"), nullable=False) #clave foránea que se vincula con campo ´id´ de tabla ´refrigeradores´ 

    empleado = relationship("Empleado", back_populates='registros_temperatura') #relación inversa
    #Desde un objeto RegistroTemperatura, puedes acceder al objeto Empleado asociado a través del atributo empleado.
    
    refrigerador = relationship('Refrigerador', back_populates='registros_temperatura')
    #Desde un objeto RegistroTemperatura, puedes acceder al objeto Refrigerador asociado a través del atributo refrigerador.

