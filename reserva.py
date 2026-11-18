import datetime
from entidades import EntidadBase
from excepciones import ReservaInvalidaError, ServicioInvalidoError, OperacionNoPermitidaError, CalculoInconsistenteError

class Reserva(EntidadBase):
    """
    Clase que integra un cliente, un servicio, la duración y el estado de la reserva.
    """
    # Estados posibles de la reserva
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    PROCESADA = "PROCESADA"
    CANCELADA = "CANCELADA"
    FALLIDA = "FALLIDA"

    def __init__(self, cliente, servicio, duracion_horas, asistentes=1):
        super().__init__()
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.asistentes = asistentes
        self.estado = self.PENDIENTE
        self.costo_total = 0.0
        self.fecha_creacion = datetime.datetime.now()

        # Validación inicial con encadenamiento de excepciones
        try:
            self.servicio.validar_parametros(self.asistentes)
        except ServicioInvalidoError as e:
            # Encadenamiento: Convertimos un error de servicio en un error de reserva
            raise ReservaInvalidaError(f"No se pudo crear la reserva para {self.cliente.nombre}. Motivo: {e.mensaje}") from e

    def confirmar(self):
        """Cambia el estado de la reserva a CONFIRMADA."""
        if self.estado != self.PENDIENTE:
            raise OperacionNoPermitidaError(f"Solo se pueden confirmar reservas en estado PENDIENTE. Estado actual: {self.estado}")
        
        # Verificamos que el servicio siga activo antes de confirmar
        self.servicio.verificar_disponibilidad()
        self.estado = self.CONFIRMADA

    def cancelar(self):
        """Cancela la reserva."""
        if self.estado == self.PROCESADA:
            raise OperacionNoPermitidaError("No se puede cancelar una reserva que ya fue procesada y pagada.")
        
        self.estado = self.CANCELADA

    def procesar(self, impuesto=0.0, descuento=0.0):
        """
        Procesa la reserva calculando el costo total.
        Aplica try/except/else/finally.
        """
        try:
            # 1. Verificamos reglas de negocio
            if self.estado != self.CONFIRMADA:
                raise OperacionNoPermitidaError(f"La reserva debe estar CONFIRMADA para procesarse. Estado actual: {self.estado}")
            
            # 2. Calculamos el costo (llamada al método sobrecargado del servicio)
            costo = self.servicio.calcular_costo(self.duracion_horas, impuesto, descuento)
            
            # 3. Verificamos consistencia del cálculo (simulando un posible error)
            if costo <= 0:
                raise CalculoInconsistenteError("El costo calculado es inconsistente (menor o igual a cero).")
                
        except (OperacionNoPermitidaError, CalculoInconsistenteError) as e:
            # Si hay error, la reserva falla y guardamos el estado
            self.estado = self.FALLIDA
            # Re-lanzamos la excepción para que el Gestor la capture y la registre
            raise e
        else:
            # Bloque ELSE: Se ejecuta SOLO si no hubo ninguna excepción en el TRY
            self.costo_total = costo
            self.estado = self.PROCESADA
        finally:
            # Bloque FINALLY: Se ejecuta SIEMPRE, haya error o no.
            # Ideal para registrar en logs (el gestor lo hará, pero aquí podríamos dejar rastro)
            pass

    def describir(self):
        """Implementación del método abstracto."""
        return (f"Reserva ID: {self.id[:8]} | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | Horas: {self.duracion_horas} | "
                f"Estado: {self.estado} | Total: ${self.costo_total}")
      
