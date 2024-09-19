from datetime import datetime

class Reserva:
    def _init_(self, numero_reserva, fecha_original, fecha_reserva):
        self.numero_reserva = numero_reserva
        self.fecha_original = fecha_original
        self.fecha_reserva = fecha_reserva

class SistemaDeReservas:
    def _init_(self):
        self.reservas = {}
        self.limite_modificacion = 2  # Los usuarios pueden modificar reservas hasta 2 días antes de la fecha original
        self.limite_cancelacion = 1  # Los usuarios pueden cancelar reservas hasta 1 día antes de la fecha original

    def agregar_reserva(self, reserva):
        self.reservas[reserva.numero_reserva] = reserva

    def modificar_reserva(self, numero_reserva, nueva_fecha):
        if numero_reserva not in self.reservas:
            return "Número de reserva no encontrado."

        reserva = self.reservas[numero_reserva]
        fecha_actual = datetime.now()

        if (reserva.fecha_original - fecha_actual).days > self.limite_modificacion:
            return "Modificación no permitida: superado el límite de tiempo para modificar."

        nueva_fecha_dt = datetime.strptime(nueva_fecha, "%Y-%m-%d")
        reserva.fecha_reserva = nueva_fecha_dt
        return f"Reserva modificada con éxito. Nueva fecha de reserva: {nueva_fecha_dt.strftime('%Y-%m-%d')}"

    def cancelar_reserva(self, numero_reserva):
        if numero_reserva not in self.reservas:
            return "Número de reserva no encontrado."

        reserva = self.reservas[numero_reserva]
        fecha_actual = datetime.now()

        if (reserva.fecha_original - fecha_actual).days > self.limite_cancelacion:
            return "Cancelación no permitida: superado el límite de tiempo para cancelar."

        del self.reservas[numero_reserva]
        return "Reserva cancelada con éxito."
    
    
    
from datetime import datetime, timedelta

class Usuario:
    def _init_(self, nombre, correo_electronico):
        self.nombre = nombre
        self.correo_electronico = correo_electronico

    def enviar_notificacion(self, mensaje):
        print(f"Enviando notificación a {self.correo_electronico}: {mensaje}")

class Reserva:
    def _init_(self, numero_reserva, usuario, fecha_original, fecha_reserva):
        self.numero_reserva = numero_reserva
        self.usuario = usuario
        self.fecha_original = fecha_original
        self.fecha_reserva = fecha_reserva

    def enviar_confirmacion(self):
        mensaje = f"Hola {self.usuario.nombre},\nTu reserva número {self.numero_reserva} ha sido confirmada para el {self.fecha_reserva.strftime('%Y-%m-%d')}."
        self.usuario.enviar_notificacion(mensaje)

    def enviar_recordatorio_check_in(self):
        mensaje = f"Hola {self.usuario.nombre},\nRecuerda que tu check-in para la reserva número {self.numero_reserva} es el {self.fecha_reserva.strftime('%Y-%m-%d')}."
        self.usuario.enviar_notificacion(mensaje)

    def enviar_recordatorio_check_out(self):
        fecha_check_out = self.fecha_reserva + timedelta(days=1)  # Supongamos que el check-out es al día siguiente
        mensaje = f"Hola {self.usuario.nombre},\nRecuerda que tu check-out para la reserva número {self.numero_reserva} es el {fecha_check_out.strftime('%Y-%m-%d')}."
        self.usuario.enviar_notificacion(mensaje)

class SistemaDeReservas:
    def _init_(self):
        self.reservas = {}
        
    def agregar_reserva(self, reserva):
        self.reservas[reserva.numero_reserva] = reserva
        reserva.enviar_confirmacion()

    def enviar_recordatorios(self):
        fecha_actual = datetime.now()
        for reserva in self.reservas.values():
            # Enviar recordatorio de check-in 1 día antes de la fecha de reserva
            if reserva.fecha_reserva - fecha_actual <= timedelta(days=1):
                reserva.enviar_recordatorio_check_in()
            # Enviar recordatorio de check-out 1 día después de la fecha de reserva
            if reserva.fecha_reserva + timedelta(days=1) - fecha_actual <= timedelta(days=1):
                reserva.enviar_recordatorio_check_out()    
                
                
                