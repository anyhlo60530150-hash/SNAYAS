import queue
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
        self.cola_voz = queue.Queue()
        self.engine = None  # Se inicializa dentro de run() para respetar el hilo

    def hablar(self, texto: str):
        """Encola un mensaje para que Jarvis lo diga sin bloquear la UI."""
        self.cola_voz.put(texto)

    def _procesar_cola_voz(self):
        """Reproduce todos los mensajes pendientes en la cola dentro del hilo del worker."""
        if self.engine is None:
            return
        while not self.cola_voz.empty():
            texto = self.cola_voz.get()
            self.estado_cambiado.emit(f"Jarvis: {texto}")
            self.engine.say(texto)
            self.engine.runAndWait()

    def run(self):
        # Inicializar motor de voz DENTRO del hilo secundario (Thread-Safe)
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 165)

        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            self.estado_cambiado.emit(f"Error al calibrar micrófono: {e}")
            return

        # Saludo al iniciar el programa
        self.hablar("Sistema Jarvis iniciado. Estoy escuchando")
        self._procesar_cola_voz()

        while self.activo:
            self._procesar_cola_voz()

            try:
                with mic as source:
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=6)

                # Si se detuvo mientras escuchaba, salir sin procesar
                if not self.activo:
                    break

                texto = recognizer.recognize_google(audio, language="es-ES").lower()

                if self.palabra_activacion in texto:
                    orden = texto.split(self.palabra_activacion, 1)[1].strip()
                    self.procesar_orden(orden)

            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                self.estado_cambiado.emit("Error: Sin conexión para reconocimiento de voz")
            except Exception as e:
                self.estado_cambiado.emit(f"Error de audio: {e}")

        # Despedida limpia dentro del mismo hilo al salir del bucle
        self.engine.say("Cerrando asistente Jarvis")
        self.engine.runAndWait()

    def procesar_orden(self, orden: str):
        if not orden:
            self.hablar("Te escucho, dime qué necesitas")
            self._procesar_cola_voz()
            return

        # --- NAVEGACIÓN ---
        if "panel principal" in orden or "inicio" in orden or "panel de red" in orden:
            self.hablar("Abriendo panel principal")
            self.comando_detectado.emit("cambiar_panel", {"indice": 0})

        elif "dispositivos" in orden and "escanear" not in orden and "buscar" not in orden:
            self.hablar("Accediendo al módulo de dispositivos")
            self.comando_detectado.emit("cambiar_panel", {"indice": 1})

        elif "ssh" in orden and "ejecutar" not in orden:
            self.hablar("Abriendo consola SSH")
            self.comando_detectado.emit("cambiar_panel", {"indice": 2})

        elif "telnet" in orden and "ejecutar" not in orden:
            self.hablar("Abriendo panel Telnet")
            self.comando_detectado.emit("cambiar_panel", {"indice": 3})

        elif ("ftp" in orden or "transferencia" in orden) and "subir" not in orden:
            self.hablar("Abriendo transferencia de archivos")
            self.comando_detectado.emit("cambiar_panel", {"indice": 4})

        # --- ACCIONES DE ESCANEO Y TRÁFICO ---
        elif "escanear" in orden or "buscar dispositivos" in orden or "reconocimiento" in orden:
            self.hablar("Iniciando reconocimiento de dispositivos")
            self.comando_detectado.emit("escanear_dispositivos", {})

        elif "iniciar tráfico" in orden or "capturar tráfico" in orden or "iniciar captura" in orden or "iniciar sniffer" in orden:
            self.hablar("Iniciando captura de tráfico de red")
            self.comando_detectado.emit("iniciar_sniffer", {})

        elif "detener tráfico" in orden or "detener captura" in orden or "detener escaneo" in orden or "parar" in orden:
            self.hablar("Captura de tráfico detenida")
            self.comando_detectado.emit("detener_sniffer", {})

        elif "limpiar tabla" in orden or "borrar tabla" in orden or "eliminar registros" in orden:
            self.hablar("Registros de la tabla eliminados")
            self.comando_detectado.emit("limpiar_tabla", {})

        # --- ACCIONES EN VISTAS REMOTAS ---
        elif "ejecutar ssh" in orden:
            self.hablar("Estableciendo operación SSH")
            self.comando_detectado.emit("ejecutar_ssh", {})

        elif "ejecutar telnet" in orden:
            self.hablar("Ejecutando operación Telnet")
            self.comando_detectado.emit("ejecutar_telnet", {})

        elif "subir archivo" in orden:
            self.hablar("Iniciando transferencia FTP")
            self.comando_detectado.emit("subir_ftp", {})

        # --- NO RECONOCE COMANDO ---
        else:
            self.hablar("No he entendido la instrucción. Inténtalo nuevamente")

        self._procesar_cola_voz()

    def detener(self):
        """Señaliza el fin del hilo sin bloquear la interfaz gráfica."""
        self.activo = False
        self.wait(2500)