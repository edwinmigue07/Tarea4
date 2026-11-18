import logging
import os

class GestorFJ:
    """
    Clase central que gestiona las listas de clientes, servicios y reservas.
    Captura cualquier error para evitar que el programa se detenga.
    """
    def __init__(self):
        # Listas internas (sin base de datos, como pide la guía)
        self.clientes = []
        self.servicios = []
        self.reservas = []
        
        # Configuración básica del Logger (Registro de eventos y errores)
        if not os.path.exists('logs'):
            os.makedirs('logs')
            
        logging.basicConfig(
            filename='logs/software_fj.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )
        self.logger = logging.getLogger(__name__)

    def agregar_cliente(self, cliente):
        self.clientes.append(cliente)
        self.logger.info(f"Cliente registrado exitosamente: {cliente.nombre}")

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)
        self.logger.info(f"Servicio registrado exitosamente: {servicio.nombre}")

    def crear_reserva(self, reserva):
        self.reservas.append(reserva)
        self.logger.info(f"Reserva creada para el cliente: {reserva.cliente.nombre}")

    def ejecutar(self, operacion, *args, **kwargs):
        """
        Método que envuelve la ejecución de cualquier operación.
        Captura tanto errores propios (ErrorSoftwareFJ) como inesperados (TypeError, etc.)
        """
        try:
            # Ejecuta la función que se le pase
            return operacion(*args, **kwargs)
            
        except Exception as e:
            # Aquí capturamos CUALQUIER error. 
            # Si es un error propio, tiene código. Si es inesperado (ej. TypeError), no.
            if hasattr(e, 'codigo'):
                mensaje_error = f"Error controlado [{e.codigo}]: {e.mensaje}"
                self.logger.error(mensaje_error)
                print(f"⚠️ {mensaje_error}")
            else:
                # Captura de errores inesperados (ej. fallas de parámetros)
                mensaje_error = f"Error inesperado ({type(e).__name__}): {str(e)}"
                self.logger.error(mensaje_error)
                print(f"❌ {mensaje_error}")
                
            # Retornamos None o False para indicar que la operación falló, pero el programa sigue vivo
            return None
