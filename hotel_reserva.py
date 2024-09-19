from datetime import datetime

class Habitacion:
    def __init__(self, id_habitacion, tipo, precio, caracteristicas):
        self.id_habitacion = id_habitacion
        self.tipo = tipo
        self.precio = precio
        self.caracteristicas = caracteristicas
        self.estado = 'Disponible'

    def consultar_disponibilidad(self):
        return self.estado == 'Disponible'

    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

    def actualizar_precio(self, nuevo_precio):
        self.precio = nuevo_precio

class Hotel:
    def __init__(self):
        self.habitaciones = [
            Habitacion(1, 'Individual', 50, 'Cama individual, Wi-Fi'),
            Habitacion(2, 'Individual', 50, 'Cama individual, Wi-Fi'),
            Habitacion(3, 'Doble', 80, 'Dos camas, TV, Wi-Fi'),
            Habitacion(4, 'Doble', 80, 'Dos camas, TV, Wi-Fi'),
            Habitacion(5, 'Suite', 150, 'Cama king, Jacuzzi, Wi-Fi'),
            Habitacion(6, 'Suite', 150, 'Cama king, Jacuzzi, Wi-Fi')
        ]
        self.historial_reservas = []

    def mostrar_habitaciones(self):
        print("\nHabitaciones disponibles en el hotel:")
        for habitacion in self.habitaciones:
            estado = habitacion.estado
            print(f"ID: {habitacion.id_habitacion} | Tipo: {habitacion.tipo} | Precio: {habitacion.precio} | "
                  f"Características: {habitacion.caracteristicas} | Estado: {estado}")

    def obtener_habitacion_por_id(self, id_habitacion):
        for habitacion in self.habitaciones:
            if habitacion.id_habitacion == id_habitacion:
                return habitacion
        return None

    def cambiar_precio(self):
        self.mostrar_habitaciones()
        id_habitacion = int(input("\nElige el ID de la habitación para cambiar el precio: "))
        habitacion = self.obtener_habitacion_por_id(id_habitacion)
        if habitacion:
            nuevo_precio = float(input(f"Ingresa el nuevo precio para la habitación {habitacion.tipo}: "))
            habitacion.actualizar_precio(nuevo_precio)
            print(f"Precio de la habitación {habitacion.tipo} actualizado a {nuevo_precio}.")
        else:
            print("ID de habitación no encontrado.")

    def agregar_reserva_al_historial(self, reserva):
        self.historial_reservas.append(reserva)

    def mostrar_historial_reservas(self):
        if not self.historial_reservas:
            print("\nNo hay reservas en el historial.")
        else:
            print("\nHistorial de reservas:")
            for reserva in self.historial_reservas:
                print(f"Usuario: {reserva.usuario.nombre} | Habitación: {reserva.habitacion.tipo} "
                      f"(ID: {reserva.habitacion.id_habitacion}) | Entrada: {reserva.fecha_entrada} | Salida: {reserva.fecha_salida}")

class Reserva:
    def __init__(self, habitacion, fecha_entrada, fecha_salida, usuario):
        self.habitacion = habitacion
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida
        self.usuario = usuario

    def confirmar_reserva(self):
        self.habitacion.actualizar_estado('Reservada')
        print(f"\n¡Reserva confirmada para {self.usuario.nombre}!")
        print(f"Habitación: {self.habitacion.tipo} (ID: {self.habitacion.id_habitacion})")
        print(f"Fecha de entrada: {self.fecha_entrada}")
        print(f"Fecha de salida: {self.fecha_salida}")
        print(f"Precio total: {self.calcular_precio()}")

    def calcular_precio(self):
        dias = (self.fecha_salida - self.fecha_entrada).days
        return dias * self.habitacion.precio

class Usuario:
    def __init__(self, nombre, correo, telefono):
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

def realizar_reserva(hotel):
    hotel.mostrar_habitaciones()

    id_habitacion = int(input("\nElige el ID de la habitación que deseas reservar: "))
    habitacion = hotel.obtener_habitacion_por_id(id_habitacion)

    if habitacion and habitacion.consultar_disponibilidad():
        nombre = input("Ingresa tu nombre: ")
        correo = input("Ingresa tu correo electrónico: ")
        telefono = input("Ingresa tu teléfono: ")
        usuario = Usuario(nombre, correo, telefono)

        fecha_entrada = datetime.strptime(input("Ingresa la fecha de entrada (YYYY-MM-DD): "), '%Y-%m-%d')
        fecha_salida = datetime.strptime(input("Ingresa la fecha de salida (YYYY-MM-DD): "), '%Y-%m-%d')

        reserva = Reserva(habitacion, fecha_entrada, fecha_salida, usuario)
        reserva.confirmar_reserva()

        hotel.agregar_reserva_al_historial(reserva)
    else:
        print("La habitación no está disponible o no existe.")

def menu_principal(hotel):
    while True:
        print("\n---- Menú Principal ----")
        print("1. Realizar reserva")
        print("2. Cambiar precio de habitación (Administrador)")
        print("3. Consultar historial de reservas")
        print("4. Salir")
        
        opcion = input("Elige una opción: ")

        if opcion == '1':
            realizar_reserva(hotel)
        elif opcion == '2':
            hotel.cambiar_precio()
        elif opcion == '3':
            hotel.mostrar_historial_reservas()
        elif opcion == '4':
            print("Saliendo del sistema de reservas.")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    hotel = Hotel()
    menu_principal(hotel)
