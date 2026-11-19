# app/backend/jarvis.py
import speech_recognition as sr
import pyttsx3
from PySide6.QtCore import QThread, Signal


class JarvisWorker(QThread):
    
    comando_detectado = Signal(str, dict)
    estado_cambiado = Signal(str)         

    def __init__(self, palabra_activacion="jarvis"):
        super().__init__()
        self.palabra_activacion = palabra_activacion.lower()
        self.activo = True

        # Inicializar motor de voz (TTS)
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 165)

    def hablar(self, texto: str):
        """Hace que Jarvis responda por voz."""
        self.estado_cambiado.emit(f"Jarvis: {texto}")
        self.engine.say(texto)
        self.engine.runAndWait()

    def run(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)

        self.estado_cambiado.emit("Jarvis en espera...")

        while self.activo:
            try:
                with mic as source:
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=6)

                texto = recognizer.recognize_google(audio, language="es-ES").lower()

                # Solo actúa si escucha la palabra clave "jarvis"
                if self.palabra_activacion in texto:
                    orden = texto.split(self.palabra_activacion, 1)[1].strip()
                    self.procesar_orden(orden)

            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                self.estado_cambiado.emit(f"Error de audio: {e}")

    def procesar_orden(self, orden: str):
        """Interpreta la intención de voz y emite la señal correspondiente."""
        if not orden:
            self.hablar("Dime, ¿qué necesitas?")
            return

        # --- NAVEGACIÓN ENTRE PANELES ---
        if "panel principal" in orden or "inicio" in orden or "panel de red" in orden:
            self.hablar("Abriendo panel principal")
            self.comando_detectado.emit("cambiar_panel", {"indice": 0})

        elif "dispositivos" in orden:
            self.hablar("Mostrando dispositivos conectados")
            self.comando_detectado.emit("cambiar_panel", {"indice": 1})

        elif "ssh" in orden:
            self.hablar("Abriendo consola SSH")
            self.comando_detectado.emit("cambiar_panel", {"indice": 2})

        elif "telnet" in orden:
            self.hablar("Abriendo panel Telnet")
            self.comando_detectado.emit("cambiar_panel", {"indice": 3})

        elif "ftp" in orden or "transferencia" in orden:
            self.hablar("Abriendo transferencia de archivos")
            self.comando_detectado.emit("cambiar_panel", {"indice": 4})

        # --- ACCIONES DE ESCANEO Y TRÁFICO ---
        elif "escanear red" in orden or "escanea la red" in orden or "buscar dispositivos" in orden:
            self.hablar("Iniciando escaneo de dispositivos en la red")
            self.comando_detectado.emit("escanear_dispositivos", {})

        elif "iniciar tráfico" in orden or "capturar tráfico" in orden or "iniciar sniffer" in orden:
            self.hablar("Iniciando captura de tráfico en tiempo real")
            self.comando_detectado.emit("iniciar_sniffer", {})

        elif "detener tráfico" in orden or "detener escaneo" in orden or "parar sniffer" in orden:
            self.hablar("Deteniendo captura de tráfico")
            self.comando_detectado.emit("detener_sniffer", {})

        elif "limpiar tabla" in orden or "borrar tabla" in orden:
            self.hablar("Tabla limpiada")
            self.comando_detectado.emit("limpiar_tabla", {})

        # --- ACCIONES EN VISTAS REMOTAS ---
        elif "ejecutar ssh" in orden:
            self.hablar("Ejecutando comando SSH")
            self.comando_detectado.emit("ejecutar_ssh", {})

        elif "ejecutar telnet" in orden:
            self.hablar("Ejecutando comando Telnet")
            self.comando_detectado.emit("ejecutar_telnet", {})

        elif "subir archivo" in orden:
            self.hablar("Iniciando subida de archivo")
            self.comando_detectado.emit("subir_ftp", {})

        else:
            self.hablar("No reconocí ese comando de red")

    def detener(self):
        self.activo = False
        self.wait(1000)