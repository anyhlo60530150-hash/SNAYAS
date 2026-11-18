# device_view.py
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox
)
from PySide6.QtCore import Qt

# Importa tus otros módulos
from app.backend.workers import NetworkWorker
from app.backend.scanner import escanear_red


class DeviceView(QWidget):

    def __init__(self):
        super().__init__()
        self.worker = None  # Referencia para evitar que el hilo muera prematuramente
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        titulo = QLabel("Dispositivos Conectados")
        titulo.setObjectName("titulo")

        self.descripcion = QLabel(
            "Visualización de los dispositivos identificados en la red"
        )

        layout.addWidget(titulo)
        layout.addWidget(self.descripcion)

        # TABLA DE DISPOSITIVOS
        self.tabla_dispositivos = QTableWidget()
        self.tabla_dispositivos.setColumnCount(4)
        self.tabla_dispositivos.setHorizontalHeaderLabels([
            "Nombre",
            "Dirección IP",
            "Estado",
            "MAC / Tipo"  # Ajustado para mostrar la MAC obtenida por Scapy
        ])
        self.tabla_dispositivos.setRowCount(0)
        self.tabla_dispositivos.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.tabla_dispositivos.verticalHeader().setVisible(False)
        self.tabla_dispositivos.setAlternatingRowColors(True)
        # Evitar que el usuario edite las celdas manualmente
        self.tabla_dispositivos.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout.addWidget(self.tabla_dispositivos)

        # BOTONES INFERIORES
        botones_layout = QHBoxLayout()
        
        self.btn_escanear = QPushButton("Escanear Red")
        self.btn_escanear.clicked.connect(self.iniciar_escaneo)

        self.btn_volver = QPushButton("Volver al panel principal")

        botones_layout.addWidget(self.btn_escanear)
        botones_layout.addWidget(self.btn_volver)
        layout.addLayout(botones_layout)

    def iniciar_escaneo(self):
        """Lanza el worker en segundo plano."""
        # Evitar múltiples escaneos simultáneos
        if self.worker is not None and self.worker.isRunning():
            return

        # Actualizar estado visual de la UI
        self.btn_escanear.setEnabled(False)
        self.btn_escanear.setText("Escaneando...")
        self.descripcion.setText("Buscando dispositivos en la red local, por favor espera...")
        self.tabla_dispositivos.setRowCount(0)  # Limpiar tabla anterior

        # Instanciar el worker pasando la función y sus argumentos
        # Nota: Asegúrate de ajustar el rango_ip a tu red local (ej. 192.168.0.0/24)
        self.worker = NetworkWorker(escanear_red, rango_ip="192.168.1.0/24")

        # Conectar las señales del worker a los métodos de esta vista
        self.worker.resultado_listo.connect(self.mostrar_resultados)
        self.worker.error_ocurrido.connect(self.manejar_error)
        self.worker.finished.connect(self.finalizar_escaneo)

        # Iniciar el hilo
        self.worker.start()

    def mostrar_resultados(self, dispositivos):
        """Recibe la lista de diccionarios desde el worker y llena la tabla."""
        self.tabla_dispositivos.setRowCount(len(dispositivos))

        for fila, disp in enumerate(dispositivos):
            item_nombre = QTableWidgetItem(disp.get("nombre", "Desconocido"))
            item_ip = QTableWidgetItem(disp.get("ip", ""))
            item_estado = QTableWidgetItem(disp.get("estado", "Activo"))
            item_mac = QTableWidgetItem(disp.get("mac", "N/A"))

            # Centrar el texto de las columnas
            for item in (item_nombre, item_ip, item_estado, item_mac):
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            self.tabla_dispositivos.setItem(fila, 0, item_nombre)
            self.tabla_dispositivos.setItem(fila, 1, item_ip)
            self.tabla_dispositivos.setItem(fila, 2, item_estado)
            self.tabla_dispositivos.setItem(fila, 3, item_mac)

        self.descripcion.setText(f"Se encontraron {len(dispositivos)} dispositivos activos.")

    def manejar_error(self, mensaje_error):
        """Muestra una alerta si Scapy falla (ej. falta de permisos de administrador/root)."""
        self.descripcion.setText("Error durante el escaneo.")
        QMessageBox.critical(
            self,
            "Error de Red",
            f"No se pudo completar el escaneo:\n{mensaje_error}\n\n"
            "Nota: Scapy requiere permisos de Administrador / root y Npcap instalado (en Windows)."
        )

    def finalizar_escaneo(self):
        """Restaura los botones cuando el hilo termina (con éxito o con error)."""
        self.btn_escanear.setEnabled(True)
        self.btn_escanear.setText("Escanear Red")