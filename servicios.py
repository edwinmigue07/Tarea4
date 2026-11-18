from abc import ABC, abstractmethod
from entidades import EntidadBase
from excepciones import ServicioInvalidoError, ServicioNoDisponibleError, CalculoInconsistenteError

class Servicio(EntidadBase, ABC):
    """
    Clase abstracta que representa un servicio general en Software FJ.
    """
    def __init__(self, nombre, tarifa_base):
        super().__init__()
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.activo = True

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor):
        if valor < 0:
            raise ServicioInvalidoError("La tarifa base no puede ser negativa.")
        self._tarifa_base = valor

    def activar(self):
        self.activo = True

    def desactivar(self):
        self.activo = False

    def verificar_disponibilidad(self):
        if not self.activo:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def validar_parametros(self, *args, **kwargs):
        pass

    # MÉTODO SOBRECARGADO (Simulado en Python usando *args y **kwargs)
    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        """
        Calcula el costo del servicio.
        Acepta variaciones: 
        - calcular_costo(horas)
        - calcular_costo(horas, impuesto)
        - calcular_costo(horas, impuesto, descuento_numerico)
        - calcular_costo(horas, impuesto, codigo_promocional_str)
        """
        self.verificar_disponibilidad()
        
        if horas <= 0:
            raise CalculoInconsistenteError("Las horas deben ser mayores a cero.")

        subtotal = self.tarifa_base * horas

        # Lógica para descuento (si es número o si es un código promocional)
        if isinstance(descuento, str):
            if descuento.upper() == "PROMO10":
                descuento = 0.10
            else:
                descuento = 0.0
                
        if descuento < 0 or descuento > 0.5:
            raise CalculoInconsistenteError("El descuento no puede ser negativo ni mayor al 50%.")

        costo_con_descuento = subtotal - (subtotal * descuento)
        total = costo_con_descuento + (costo_con_descuento * impuesto)
        
        return total


class ReservaSala(Servicio):
    def __init__(self, nombre, tarifa_base, capacidad_maxima):
        super().__init__(nombre, tarifa_base)
        self.capacidad_maxima = capacidad_maxima

    def describir(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"Sala: {self.nombre} | Capacidad: {self.capacidad_maxima} | Tarifa/h: ${self.tarifa_base} | Estado: {estado}"

    def validar_parametros(self, asistentes):
        if asistentes > self.capacidad_maxima:
            raise ServicioInvalidoError(f"La sala '{self.nombre}' tiene capacidad para {self.capacidad_maxima} personas, se intentaron registrar {asistentes}.")


class AlquilerEquipo(Servicio):
    def __init__(self, nombre, tarifa_base, tipo_equipo):
        super().__init__(nombre, tarifa_base)
        self.tipo_equipo = tipo_equipo

    def describir(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"Equipo: {self.nombre} | Tipo: {self.tipo_equipo} | Tarifa/h: ${self.tarifa_base} | Estado: {estado}"

    def validar_parametros(self, cantidad_equipos):
        if cantidad_equipos <= 0:
            raise ServicioInvalidoError("La cantidad de equipos debe ser mayor a cero.")


class AsesoriaEspecializada(Servicio):
    def __init__(self, nombre, tarifa_base, nivel_experto, modalidad):
        super().__init__(nombre, tarifa_base)
        self.nivel_experto = nivel_experto
        self.modalidad = modalidad

    def describir(self):
        estado = "Activo" if self.activo else "Inactivo"
        return f"Asesoría: {self.nombre} | Nivel: {self.nivel_experto} | Modalidad: {self.modalidad} | Tarifa/h: ${self.tarifa_base} | Estado: {estado}"

    def validar_parametros(self, nivel_solicitado):
        if nivel_solicitado.lower() != self.nivel_experto.lower():
            raise ServicioInvalidoError(f"El nivel solicitado '{nivel_solicitado}' no coincide con la asesoría '{self.nivel_experto}'.")
