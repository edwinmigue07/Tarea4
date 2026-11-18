from entidades import EntidadBase
from excepciones import ClienteInvalidoError
import re

class Cliente(EntidadBase):
    """
    Clase que representa a un cliente. Aplica encapsulación y validaciones.
    """
    def __init__(self, documento, nombre, correo, telefono):
        super().__init__()
        # Usamos setters para que se validen los datos desde el inicio
        self.documento = documento
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def documento(self):
        return self._documento

    @documento.setter
    def documento(self, valor):
        if not valor or not str(valor).strip():
            raise ClienteInvalidoError("El documento no puede estar vacío.")
        self._documento = str(valor).strip()

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(str(valor).strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = str(valor).strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        # Validación simple con expresión regular para correos
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not valor or not re.match(patron, str(valor)):
            raise ClienteInvalidoError(f"El correo '{valor}' no tiene un formato válido.")
        self._correo = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not valor or not str(valor).isdigit():
            raise ClienteInvalidoError("El teléfono debe contener solo números.")
        self._telefono = str(valor)

    def describir(self):
        """Implementación del método abstracto de EntidadBase."""
        return f"Cliente: {self.nombre} | Doc: {self.documento} | Correo: {self.correo} | Tel: {self.telefono}"
