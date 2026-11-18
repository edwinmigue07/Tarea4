from abc import ABC, abstractmethod
import uuid

class EntidadBase(ABC):
    """
    Clase abstracta que representa una entidad general del sistema.
    Aplica el pilar de Abstracción.
    """
    def __init__(self):
        # Genera un identificador único de solo lectura usando UUID
        self._id = str(uuid.uuid4())

    @property
    def id(self):
        """Retorna el identificador único de la entidad."""
        return self._id

    @abstractmethod
    def describir(self):
        """
        Método abstracto que obliga a las clases hijas a implementar
        su propia forma de describirse.
        """
        pass
