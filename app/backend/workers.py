# workers.py
from PySide6.QtCore import QThread, Signal

class NetworkWorker(QThread):
    # Señales para comunicarse de forma segura con la interfaz
    resultado_listo = Signal(object)   # Emite el retorno final (listas, tuplas, etc.)
    progreso_dato = Signal(object)     # Emite datos en vivo (ej. cada paquete del sniffer)
    error_ocurrido = Signal(str)

    def __init__(self, funcion, *args, **kwargs):
        super().__init__()
        self.funcion = funcion
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            # Ejecuta tu función de red en el hilo secundario
            resultado = self.funcion(*self.args, **self.kwargs)
            self.resultado_listo.emit(resultado)
        except Exception as e:
            self.error_ocurrido.emit(str(e))



 
