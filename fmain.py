from datetime import datetime

# Clase de Usuario
class Usuario:
    def __init__(self, nombre, correo_electronico, contraseña, es_admin=False):
        self.nombre = nombre
        self.correo_electronico = correo_electronico
        self.contraseña = contraseña
        self.es_admin = es_admin

    def enviar_notificacion(self, mensaje):
        print(f"Enviando notificación a {self.correo_electronico}: {mensaje}")

# Clase de Habitaciones
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

# Clase de Reserva
class Reserva:
    def __init__(self, numero_reserva, habitacion, usuario, fecha_entrada, fecha_salida):
        self.numero_reserva = numero_reserva
        self.habitacion = habitacion
        self.usuario = usuario
        self.fecha_entrada = fecha_entrada
        self.fecha_salida = fecha_salida

    def enviar_confirmacion(self):
        mensaje = f"Hola {self.usuario.nombre},\nTu reserva número {self.numero_reserva} ha sido confirmada para el {self.fecha_entrada.strftime('%Y-%m-%d')}."
        self.usuario.enviar_notificacion(mensaje)

    def enviar_recordatorio_check_in(self):
        mensaje = f"Hola {self.usuario.nombre},\nRecuerda que tu check-in para la reserva número {self.numero_reserva} es el {self.fecha_entrada.strftime('%Y-%m-%d')}."
        self.usuario.enviar_notificacion(mensaje)

    def enviar_recordatorio_check_out(self):
        fecha_check_out = self.fecha_salida  # Supongamos que el check-out es el último día de la estancia
        mensaje = f"Hola {self.usuario.nombre},\nRecuerda que tu check-out para la reserva número {self.numero_reserva} es el {fecha_check_out.strftime('%Y-%m-%d')}."
        self.usuario.enviar_notificacion(mensaje)

    def calcular_precio_total(self):
        dias_estancia = (self.fecha_salida - self.fecha_entrada).days
        total = dias_estancia * self.habitacion.precio
        return total

# Clase de Hotel con funcionalidades de reservas y cancelaciones
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
        self.reservas = {}
        self.contador_reservas = 1
        self.usuarios = [Usuario('admin', 'admin@hotel.com', 'admin123', es_admin=True)]

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

    def realizar_reserva(self, usuario):
        self.mostrar_habitaciones()

        id_habitacion = int(input("\nElige el ID de la habitación que deseas reservar (o 0 para salir al menú principal): "))
        if id_habitacion == 0:
            return

        habitacion = self.obtener_habitacion_por_id(id_habitacion)

        if habitacion and habitacion.consultar_disponibilidad():
            fecha_entrada = datetime.strptime(input("Ingresa la fecha de entrada (YYYY-MM-DD): "), '%Y-%m-%d')
            fecha_salida = datetime.strptime(input("Ingresa la fecha de salida (YYYY-MM-DD): "), '%Y-%m-%d')

            reserva = Reserva(self.contador_reservas, habitacion, usuario, fecha_entrada, fecha_salida)
            self.reservas[self.contador_reservas] = reserva
            self.contador_reservas += 1

            reserva.enviar_confirmacion()

            total_a_pagar = reserva.calcular_precio_total()
            print(f"Total a pagar por {habitacion.tipo}: {total_a_pagar} USD.")

            habitacion.actualizar_estado('Reservada')

        else:
            print("La habitación no está disponible o no existe.")

    def cancelar_reserva(self, usuario):
        numero_reserva = int(input("Ingresa el número de la reserva que deseas cancelar (o 0 para salir al menú principal): "))
        if numero_reserva == 0:
            return

        if numero_reserva in self.reservas:
            reserva = self.reservas[numero_reserva]
            if reserva.usuario.correo_electronico == usuario.correo_electronico or usuario.es_admin:
                reserva.habitacion.actualizar_estado('Disponible')
                del self.reservas[numero_reserva]
                print("Reserva cancelada con éxito.")
            else:
                print("No tienes permiso para cancelar esta reserva.")
        else:
            print("Número de reserva no encontrado.")

    def modificar_reserva(self, usuario):
        numero_reserva = int(input("Ingresa el número de la reserva que deseas modificar (o 0 para salir al menú principal): "))
        if numero_reserva == 0:
            return

        if numero_reserva in self.reservas:
            reserva = self.reservas[numero_reserva]
            if reserva.usuario.correo_electronico == usuario.correo_electronico or usuario.es_admin:
                nueva_fecha_entrada = datetime.strptime(input("Ingresa la nueva fecha de entrada (YYYY-MM-DD): "), '%Y-%m-%d')
                nueva_fecha_salida = datetime.strptime(input("Ingresa la nueva fecha de salida (YYYY-MM-DD): "), '%Y-%m-%d')
                reserva.fecha_entrada = nueva_fecha_entrada
                reserva.fecha_salida = nueva_fecha_salida
                print("Reserva modificada con éxito.")
            else:
                print("No tienes permiso para modificar esta reserva.")
        else:
            print("Número de reserva no encontrado.")

    def cambiar_precio(self):
        self.mostrar_habitaciones()
        id_habitacion = int(input("\nElige el ID de la habitación para cambiar el precio (o 0 para salir al menú principal): "))
        if id_habitacion == 0:
            return

        habitacion = self.obtener_habitacion_por_id(id_habitacion)
        if habitacion:
            nuevo_precio = float(input(f"Ingresa el nuevo precio para la habitación {habitacion.tipo}: "))
            habitacion.actualizar_precio(nuevo_precio)
            print(f"Precio de la habitación {habitacion.tipo} actualizado a {nuevo_precio} USD.")
        else:
            print("ID de habitación no encontrado.")

    def mostrar_historial_reservas(self):
        if not self.reservas:
            print("\nNo hay reservas en el historial.")
        else:
            print("\nHistorial de reservas:")
            for numero_reserva, reserva in self.reservas.items():
                print(f"Reserva {numero_reserva} | Usuario: {reserva.usuario.nombre} | Habitación: {reserva.habitacion.tipo} "
                      f"(ID: {reserva.habitacion.id_habitacion}) | Entrada: {reserva.fecha_entrada.strftime('%Y-%m-%d')} | "
                      f"Salida: {reserva.fecha_salida.strftime('%Y-%m-%d')}")

    def registrar_usuario(self):
        nombre = input("Ingresa tu nombre: ")
        correo = input("Ingresa tu correo electrónico: ")
        contraseña = input("Ingresa tu contraseña: ")
        if any(u.correo_electronico == correo for u in self.usuarios):
            print("Error: El usuario ya existe.")
        else:
            self.usuarios.append(Usuario(nombre, correo, contraseña))
            print("Usuario registrado con éxito.")

    def iniciar_sesion(self):
        correo = input("Correo electrónico: ")
        contraseña = input("Contraseña: ")
        for usuario in self.usuarios:
            if usuario.correo_electronico == correo and usuario.contraseña == contraseña:
                print(f"Acceso concedido. Bienvenido {usuario.nombre}.")
                return usuario
        print("Error: Correo o contraseña incorrectos.")
        return None

# Menú principal del sistema
def menu_principal(hotel):
    while True:
        print("\n---- Menú Principal ----")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            hotel.registrar_usuario()

        elif opcion == "2":
            usuario = hotel.iniciar_sesion()
            if usuario:
                if usuario.es_admin:
                    menu_administrador(hotel, usuario)
                else:
                    menu_usuario(hotel, usuario)

        elif opcion == "3":
            print("Gracias por usar el sistema de gestión del hotel.")
            break

        else:
            print("Opción inválida. Intenta de nuevo.")

# Menú para el usuario administrador
def menu_administrador(hotel, usuario):
    while True:
        print("\n---- Menú Administrador ----")
        print("1. Ver habitaciones")
        print("2. Ver historial de reservas")
        print("3. Modificar reserva")
        print("4. Cancelar reserva")
        print("5. Cambiar precio de una habitación")
        print("6. Cerrar sesión")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            hotel.mostrar_habitaciones()

        elif opcion == "2":
            hotel.mostrar_historial_reservas()

        elif opcion == "3":
            hotel.modificar_reserva(usuario)

        elif opcion == "4":
            hotel.cancelar_reserva(usuario)

        elif opcion == "5":
            hotel.cambiar_precio()

        elif opcion == "6":
            print("Sesión cerrada.")
            break

        else:
            print("Opción inválida. Intenta de nuevo.")

# Menú para el usuario estándar
def menu_usuario(hotel, usuario):
    while True:
        print(f"\n---- Menú Usuario: {usuario.nombre} ----")
        print("1. Ver habitaciones")
        print("2. Realizar reserva")
        print("3. Modificar reserva")
        print("4. Cancelar reserva")
        print("5. Ver historial de reservas")
        print("6. Cerrar sesión")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            hotel.mostrar_habitaciones()

        elif opcion == "2":
            hotel.realizar_reserva(usuario)

        elif opcion == "3":
            hotel.modificar_reserva(usuario)

        elif opcion == "4":
            hotel.cancelar_reserva(usuario)

        elif opcion == "5":
            hotel.mostrar_historial_reservas()

        elif opcion == "6":
            print("Sesión cerrada.")
            break

        else:
            print("Opción inválida. Intenta de nuevo.")

# Ejecutar el programa
if __name__ == "__main__":
    hotel = Hotel()
    menu_principal(hotel)
    
    
#Usuario: admin@hotel.com
#Contraseña: admin123   

