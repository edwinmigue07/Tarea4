from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva
from gestor import GestorFJ
from excepciones import ErrorSoftwareFJ

def main():
    print("=== INICIANDO SIMULACIÓN SOFTWARE FJ ===\n")
    gestor = GestorFJ()

    # ---------------------------------------------------------
    # 1. Operaciones Válidas (Clientes y Servicios)
    # ---------------------------------------------------------
    print("--- Registrando datos válidos ---")
    
    # Cliente válido
    cliente_valido = gestor.ejecutar(Cliente, "12345678", "Edwin Cordero", "edwin@unad.edu.co", "3001234567")
    if cliente_valido: 
        gestor.agregar_cliente(cliente_valido)
        print(f"✅ Cliente creado: {cliente_valido.nombre}")

    # Sala válida
    sala = gestor.ejecutar(ReservaSala, "Sala VIP", 50000, 10)
    if sala:
        gestor.agregar_servicio(sala)
        print(f"✅ Servicio creado: {sala.nombre}")

    # ---------------------------------------------------------
    # 2. Operaciones Inválidas (Manejo de errores)
    # ---------------------------------------------------------
    print("\n--- Probando manejo de errores ---")

    # Error FJ-101: Correo inválido
    print("Intentando crear cliente con correo inválido...")
    gestor.ejecutar(Cliente, "87654321", "Ana Perez", "correo-invalido", "3109876543")

    # Error FJ-201: Tarifa negativa
    print("Intentando crear sala con tarifa negativa...")
    gestor.ejecutar(ReservaSala, "Sala Error", -1000, 5)

    # Error inesperado: Parámetros faltantes (TypeError)
    print("Intentando crear asesoría sin todos los parámetros (TypeError)...")
    gestor.ejecutar(AsesoriaEspecializada, "Asesoría Python", 80000) # Faltan argumentos

    # ---------------------------------------------------------
    # 3. Simulación de Reservas (Éxitos y Fallos encadenados)
    # ---------------------------------------------------------
    print("\n--- Creando Reservas ---")
    
    if cliente_valido and sala:
        # Reserva válida
        reserva1 = gestor.ejecutar(Reserva, cliente_valido, sala, 4, 5)
        if reserva1:
            gestor.crear_reserva(reserva1)
            gestor.ejecutar(reserva1.confirmar)
            print("Reserva 1 confirmada.")
            # Procesar con descuento (PROMO10) e IVA
            gestor.ejecutar(reserva1.procesar, impuesto=0.19, descuento="PROMO10")
            print(f"✅ Reserva 1 procesada. Total: ${reserva1.costo_total}")

        # Error FJ-301 encadenado: Reserva con exceso de asistentes
        print("\nIntentando reserva con 40 asistentes en sala de capacidad 10...")
        gestor.ejecutar(Reserva, cliente_valido, sala, 2, 40)

        # Error FJ-302: Procesar sin confirmar
        print("\nIntentando procesar reserva no confirmada...")
        reserva2 = gestor.ejecutar(Reserva, cliente_valido, sala, 2, 5)
        if reserva2:
            gestor.ejecutar(reserva2.procesar) # Falla porque no se ha confirmado

        # Error FJ-401: Descuento inconsistente
        print("\nIntentando procesar con descuento del 90%...")
        reserva3 = gestor.ejecutar(Reserva, cliente_valido, sala, 2, 5)
        if reserva3:
            gestor.ejecutar(reserva3.confirmar)
            gestor.ejecutar(reserva3.procesar, descuento=0.90)

    print("\n=== SIMULACIÓN FINALIZADA SIN INTERRUPCIONES ===")
    print("Revisa la carpeta 'logs/' para ver el registro de eventos y errores.")

if __name__ == "__main__":
    main()
