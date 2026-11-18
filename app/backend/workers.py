from PySide6.QtCore import QThread, Signal


class NetworkWorker(QThread):
    # Señales que usan tus vistas (main_view.py y device_view.py)
    progreso_dato = Signal(object)
    resultado_listo = Signal(object)
    error_ocurrido = Signal(str)

    def __init__(self, funcion, *args, **kwargs):
        super().__init__()
        self.funcion = funcion
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            resultado = self.funcion(*self.args, **self.kwargs)
            self.resultado_listo.emit(resultado)
        except Exception as e:
            self.error_ocurrido.emit(str(e))


class TaskWorker(QThread):
    tarea_completada = Signal(bool, str)

    def __init__(self, funcion, *args, **kwargs):
        super().__init__()
        self.funcion = funcion
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            exito, mensaje = self.funcion(*self.args, **self.kwargs)
            self.tarea_completada.emit(exito, mensaje)
        except Exception as e:
            self.tarea_completada.emit(False, f"Error inesperado: {str(e)}")