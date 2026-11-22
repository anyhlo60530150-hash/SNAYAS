import queue
import speech_recognition as sr
import pyttsx3
from PySide6.QtCore import QThread, Signal, Slot, Qt


class JarvisWorker(QThread):
    comando_detectado = Signal(str, dict)
    estado_cambiado = Signal(str)
    _texto_inyectado = Signal(str)

    def __init__(self, palabra_activacion="jarvis", escuchar_microfono=True):
        super().__init__()
        self.palabra_activacion = palabra_activacion.lower()
        self.escuchar_microfono = escuchar_microfono
        self.activo = True
        self.cola_voz = queue.Queue()
        self.engine = None

        self._texto_inyectado.connect(
            self._procesar_texto_crudo,
            Qt.ConnectionType.QueuedConnection,
        )

    @Slot(str)
    def inyectar_texto(self, texto: str):
        """Permite probar comandos enviando texto desde la UI o tests sin usar el micrófono."""
        if texto and texto.strip():
            self._texto_inyectado.emit(texto.strip().lower())

    def _procesar_texto_crudo(self, texto: str):
        """Procesa un texto como si viniera del reconocedor de voz."""
        self.estado_cambiado.emit(f'Texto recibido: "{texto}"')

        if self.palabra_activacion in texto:
            orden = texto.split(self.palabra_activacion, 1)[1].strip()
        else:
            orden = texto.strip()

        self.procesar_orden(orden)

    def hablar(self, texto: str):
        """Encola un mensaje para que Jarvis lo diga en su hilo sin bloquear la UI."""
        if texto and self.activo:
            self.cola_voz.put(texto)

    def _crear_motor_voz(self):
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 165)
            return engine
        except Exception as e:
            self.estado_cambiado.emit(f"Error al iniciar motor de voz: {e}")
            return None

    def _procesar_cola_voz(self):
        """Reproduce todos los mensajes pendientes en la cola dentro del hilo del worker."""
        while not self.cola_voz.empty() and self.activo:
            texto = self.cola_voz.get()
            self.estado_cambiado.emit(f"Jarvis: {texto}")

            if self.engine is None:
                self.engine = self._crear_motor_voz()

            if self.engine is None:
                continue

            try:
                self.engine.say(texto)
                self.engine.runAndWait()
            except Exception as e:
                self.estado_cambiado.emit(f"Error TTS: {e}")
                # Reintentar recrear el motor una vez si SAPI5 falló
                try:
                    self.engine.stop()
                except Exception:
                    pass
                self.engine = self._crear_motor_voz()
                if self.engine is not None:
                    try:
                        self.engine.say(texto)
                        self.engine.runAndWait()
                    except Exception as e2:
                        self.estado_cambiado.emit(f"Error TTS reintento: {e2}")

    def run(self):
        self.engine = self._crear_motor_voz()

        recognizer = sr.Recognizer()
        recognizer.pause_threshold = 0.6
        mic = None

        if self.escuchar_microfono:
            try:
                mic = sr.Microphone()
                with mic as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.8)
            except Exception as e:
                self.estado_cambiado.emit(f"Micrófono no disponible ({e}). Modo texto activo.")
                mic = None

        self.hablar("Sistema Jarvis iniciado. Estoy escuchando")
        self._procesar_cola_voz()

        while self.activo:
            self._procesar_cola_voz()

            if not self.activo:
                break

            if not self.escuchar_microfono or mic is None:
                self.msleep(100)
                continue

            try:
                with mic as source:
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)

                if not self.activo:
                    break

                self._procesar_cola_voz()
                if not self.activo:
                    break

                texto = recognizer.recognize_google(audio, language="es-ES").lower()

                if not self.activo:
                    break

                if self.palabra_activacion in texto:
                    orden = texto.split(self.palabra_activacion, 1)[1].strip()
                    self.procesar_orden(orden)
                    self._procesar_cola_voz()

            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                self.estado_cambiado.emit("Error: Sin conexión para reconocimiento de voz")
            except Exception as e:
                if self.activo:
                    self.estado_cambiado.emit(f"Error de audio: {e}")

        # Limpieza al salir del bucle
        if self.engine is not None:
            try:
                self.engine.stop()
            except Exception:
                pass
            self.engine = None

    def procesar_orden(self, orden: str):
        if not orden:
            self.hablar("Te escucho, dime qué necesitas")
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

    def detener(self):
        """Señaliza el fin del hilo y evita que quede colgado al cerrar la app."""
        self.activo = False
        with self.cola_voz.mutex:
            self.cola_voz.queue.clear()

        if self.engine is not None:
            try:
                self.engine.stop()
            except Exception:
                pass

        if not self.wait(1500):
            self.terminate()
            self.wait(500)