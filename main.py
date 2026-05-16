from abc import ABC, abstractmethod
from datetime import datetime
def registrar_log(mensaje):
 with open("logs.txt", "a", encoding="utf-8") as archivo:
 archivo.write(f"[{datetime.now()}] {mensaje}\n")
class ClienteError(Exception):
 pass
class ServicioError(Exception):
 pass
class ReservaError(Exception):
 pass
class Entidad(ABC):
 @abstractmethod
 def mostrar_info(self):
 pass
class Cliente(Entidad):
 def __init__(self, nombre, cedula, correo):
 self.__nombre = nombre
 self.__cedula = cedula
 self.__correo = correo
 self.validar_datos()
 @property
 def nombre(self):
 return self.__nombre
 @property
 def cedula(self):
 return self.__cedula
 @property
 def correo(self):
 return self.__correo
 def validar_datos(self):
 if not self.__nombre.strip():
 raise ClienteError("El nombre no puede estar vacío")
 if len(self.__cedula) < 5:
 raise ClienteError("La cédula es inválida")
 if "@" not in self.__correo:
 raise ClienteError("Correo electrónico inválido")
 def mostrar_info(self):
 return f"Cliente: {self.nombre} - CC: {self.cedula}"
class Servicio(ABC):
 def __init__(self, nombre, tarifa_base):
 if tarifa_base <= 0:
 raise ServicioError("La tarifa debe ser mayor a cero")
 self.nombre = nombre
 self.tarifa_base = tarifa_base
 @abstractmethod
 def calcular_costo(self, horas, descuento=0):
 pass
 @abstractmethod
 def descripcion(self):
 pass
class ReservaSala(Servicio):
 def __init__(self, capacidad, tarifa_base=50000):
 super().__init__("Reserva de Sala", tarifa_base)
 self.capacidad = capacidad
 def calcular_costo(self, horas, descuento=0):
 if horas <= 0:
 raise ServicioError("Las horas deben ser mayores a cero")
 total = self.tarifa_base * horas
 total -= total * descuento
 return total
 def descripcion(self):
 return f"Sala con capacidad para {self.capacidad} personas"
class AlquilerEquipo(Servicio):
 def __init__(self, tipo_equipo, tarifa_base=80000):
 super().__init__("Alquiler de Equipo", tarifa_base)
 self.tipo_equipo = tipo_equipo
 def calcular_costo(self, horas, descuento=0):
 if horas <= 0:
 raise ServicioError("Tiempo inválido")
 total = self.tarifa_base * horas
 total -= total * descuento
 return total
 def descripcion(self):
 return f"Equipo tecnológico tipo {self.tipo_equipo}"
class AsesoriaEspecializada(Servicio):
 def __init__(self, especialidad, tarifa_base=120000):
 super().__init__("Asesoría Especializada", tarifa_base)
 self.especialidad = especialidad
 def calcular_costo(self, horas, descuento=0):
 if horas <= 0:
 raise ServicioError("Horas inválidas")
 total = self.tarifa_base * horas
 impuesto = total * 0.19
 total += impuesto
 total -= total * descuento
 return total
 def descripcion(self):
 return f"Asesoría en {self.especialidad}"
class Reserva:
 def __init__(self, cliente, servicio, horas):
 if not isinstance(cliente, Cliente):
 raise ReservaError("Cliente inválido")
 if not isinstance(servicio, Servicio):
 raise ReservaError("Servicio inválido")
 if horas <= 0:
 raise ReservaError("Las horas deben ser mayores a cero")
 self.cliente = cliente
 self.servicio = servicio
 self.horas = horas
 self.estado = "Pendiente"
 def confirmar(self):
 self.estado = "Confirmada"
 registrar_log(
 f"Reserva confirmada para {self.cliente.nombre}"
 )
 def cancelar(self):
 self.estado = "Cancelada"
 registrar_log(
 f"Reserva cancelada para {self.cliente.nombre}"
 )
 def procesar(self):
 try:
 costo = self.servicio.calcular_costo(self.horas)
 except Exception as error:
 raise ReservaError(
 "No fue posible calcular el costo"
 ) from error
 else:
 self.confirmar()
 return costo
 finally:
 registrar_log(
 f"Reserva procesada para {self.cliente.nombre}"
 )
 def mostrar_reserva(self):
 return (
 f"Cliente: {self.cliente.nombre} | "
 f"Servicio: {self.servicio.nombre} | "
 f"Estado: {self.estado}"
 )
print("Sistema ejecutado correctamente")