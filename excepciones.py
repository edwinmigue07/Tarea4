# Módulo de excepciones personalizadas para el sistema Software FJ

class ErrorSoftwareFJ(Exception):
    """Clase base para todas las excepciones del sistema."""
    def __init__(self, mensaje, codigo="FJ-000"):
        self.mensaje = mensaje
        self.codigo = codigo
        super().__init__(f"[{self.codigo}] {self.mensaje}")

class ClienteInvalidoError(ErrorSoftwareFJ):
    """Excepción para datos inválidos de clientes."""
    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-101")

class ServicioInvalidoError(ErrorSoftwareFJ):
    """Excepción para datos inválidos en la creación de servicios."""
    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-201")

class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Excepción cuando se intenta usar un servicio desactivado."""
    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-202")

class ReservaInvalidaError(ErrorSoftwareFJ):
    """Excepción para errores en la creación o datos de reservas."""
    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-301")

class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Excepción para operaciones no permitidas (ej. procesar reserva no confirmada)."""
    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-302")

class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Excepción para errores en cálculos de costos (ej. descuentos inválidos)."""
    def __init__(self, mensaje):
        super().__init__(mensaje, "FJ-401")
