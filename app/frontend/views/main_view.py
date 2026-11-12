import threading

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QHeaderView,
    QFrame,
    QSizePolicy,
    QTableWidgetItem,
    QMessageBox
)
from PySide6.QtCore import Qt

from app.frontend.stylesheet.style import obtener_estilos
from app.backend.workers import NetworkWorker
from app.backend.sniffer import capturar_trafico_continuo


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Network Assistant & Alert Suite")
        self.resize(1100, 700)
        self.setMinimumSize(800, 550)

        # 1. Inicializar variables de estado que faltaban
        self.worker = None
        self.detener_evento = threading.Event()
        self.ips_detectadas = set()

        self.init_ui()
        self.setStyleSheet(obtener_estilos())

    def init_ui(self):
        # CONTENEDOR PRINCIPAL
        central = QWidget()
        self.setCentralWidget(central)

        principal = QHBoxLayout(central)
        principal.setContentsMargins(0, 0, 0, 0)
        principal.setSpacing(0)

        # MENU LATERAL
        menu = QFrame()
        menu.setObjectName("menu")
        menu.setFixedWidth(210)

        menu_layout = QVBoxLayout(menu)
        menu_layout.setContentsMargins(15, 25, 15, 20)
        menu_layout.setSpacing(15)

        logo = QLabel("SMART NETWORK")
        logo.setObjectName("logo")
        menu_layout.addWidget(logo)

        btn_dashboard = QPushButton("Panel de Control")
        btn_devices = QPushButton("Dispositivos")
        btn_alerts = QPushButton("Alertas")
        btn_analytics = QPushButton("Analisis")
        btn_settings = QPushButton("Configuracion")

        for boton in [
            btn_dashboard,
            btn_devices,
            btn_alerts,
            btn_analytics,
            btn_settings
        ]:
            boton.setObjectName("menuButton")
            boton.setCursor(Qt.CursorShape.PointingHandCursor)
            menu_layout.addWidget(boton)

        menu_layout.addStretch()

        version = QLabel("Version 1.0")
        version.setObjectName("version")
        menu_layout.addWidget(version)

        # CONTENIDO PRINCIPAL
        contenido = QWidget()
        contenido.setObjectName("contenido")

        contenido_layout = QVBoxLayout(contenido)
        contenido_layout.setContentsMargins(25, 25, 25, 25)
        contenido_layout.setSpacing(20)

        # ENCABEZADO
        encabezado = QHBoxLayout()

        titulo = QLabel("Panel de Red")
        titulo.setObjectName("titulo")

        estado = QLabel("● Sistema en linea")
        estado.setObjectName("estado")

        encabezado.addWidget(titulo)
        encabezado.addStretch()
        encabezado.addWidget(estado)

        contenido_layout.addLayout(encabezado)

        # TARJETAS DE INFORMACION
        tarjetas = QHBoxLayout()
        tarjetas.setSpacing(15)

        # PRIMERA TARJETA
        tarjeta1 = QFrame()
        tarjeta1.setObjectName("tarjeta")
        layout1 = QVBoxLayout(tarjeta1)
        texto1 = QLabel("Dispositivos Conectados")
        texto1.setObjectName("textoTarjeta")
        self.numero_dispositivos = QLabel("0")
        self.numero_dispositivos.setObjectName("numeroTarjeta")
        layout1.addWidget(texto1)
        layout1.addWidget(self.numero_dispositivos)

        # SEGUNDA TARJETA
        tarjeta2 = QFrame()
        tarjeta2.setObjectName("tarjeta")
        layout2 = QVBoxLayout(tarjeta2)
        texto2 = QLabel("Alertas Activas")
        texto2.setObjectName("textoTarjeta")
        self.numero_alertas = QLabel("0")
        self.numero_alertas.setObjectName("numeroTarjeta")
        layout2.addWidget(texto2)
        layout2.addWidget(self.numero_alertas)

        # TERCERA TARJETA
        tarjeta3 = QFrame()
        tarjeta3.setObjectName("tarjeta")
        layout3 = QVBoxLayout(tarjeta3)
        texto3 = QLabel("Estado De La Red")
        texto3.setObjectName("textoTarjeta")
        self.estado_red = QLabel("Esperando...")
        self.estado_red.setObjectName("numeroTarjeta")
        layout3.addWidget(texto3)
        layout3.addWidget(self.estado_red)

        tarjetas.addWidget(tarjeta1)
        tarjetas.addWidget(tarjeta2)
        tarjetas.addWidget(tarjeta3)
        contenido_layout.addLayout(tarjetas)

        # 2. Guardar titulo_tabla como atributo de clase (self)
        self.titulo_tabla = QLabel("Dispositivos de Red")
        self.titulo_tabla.setObjectName("subtitulo")
        contenido_layout.addWidget(self.titulo_tabla)

        # TABLA
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels([
            "Nombre del Dispositivo",
            "Direccion IP",
            "Estado",
            "Tipo"
        ])
        self.tabla.setRowCount(0)

        encabezado_tabla = self.tabla.horizontalHeader()
        encabezado_tabla.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        contenido_layout.addWidget(self.tabla)

        # 3. Guardar botones con self y conectar sus señales clicked
        botones = QHBoxLayout()

        self.btn_actualizar = QPushButton("Limpiar tabla")
        self.btn_actualizar.setObjectName("actualizar")
        self.btn_actualizar.clicked.connect(self.limpiar_tabla)

        self.btn_escanear = QPushButton("Escanear red")
        self.btn_escanear.setObjectName("escanear")
        self.btn_escanear.clicked.connect(self.alternar_sniffer)

        botones.addStretch()
        botones.addWidget(self.btn_actualizar)
        botones.addWidget(self.btn_escanear)

        contenido_layout.addLayout(botones)

        # AGREGAR MENU Y CONTENIDO
        principal.addWidget(menu)
        principal.addWidget(contenido, 1)

    # 4. Método al nivel correcto de indentación (fuera de init_ui)
    def alternar_sniffer(self):
        """Inicia o detiene el sniffer al pulsar el botón."""
        if self.worker is not None and self.worker.isRunning():
            self.detener_evento.set()
            self.btn_escanear.setEnabled(False)
            self.btn_escanear.setText("Deteniendo...")
            self.estado_red.setText("Deteniendo...")
        else:
            self.iniciar_sniffer()

    def iniciar_sniffer(self):
        self.detener_evento.clear()
        self.ips_detectadas.clear()

        self.titulo_tabla.setText("Tráfico de Red en Tiempo Real")
        self.tabla.setHorizontalHeaderLabels([
            "IP Origen", "IP Destino", "Protocolo", "Longitud (Bytes)"
        ])
        self.tabla.setRowCount(0)

        self.worker = NetworkWorker(
            capturar_trafico_continuo,
            detener_evento=self.detener_evento,
            interfaz=None,
            filtro="ip"
        )

        self.worker.kwargs["callback_paquete"] = self.worker.progreso_dato.emit

        self.worker.progreso_dato.connect(self.agregar_paquete_a_tabla)
        self.worker.error_ocurrido.connect(self.manejar_error_sniffer)
        self.worker.finished.connect(self.al_finalizar_sniffer)

        self.btn_escanear.setText("Detener escaneo")
        self.estado_red.setText("Capturando...")
        self.worker.start()

    def agregar_paquete_a_tabla(self, info: dict):
        """Se ejecuta en el hilo principal cada vez que Scapy captura un paquete."""
        self.tabla.insertRow(0)
        self.tabla.setItem(0, 0, QTableWidgetItem(info["origen"]))
        self.tabla.setItem(0, 1, QTableWidgetItem(info["destino"]))
        self.tabla.setItem(0, 2, QTableWidgetItem(info["protocolo"]))
        self.tabla.setItem(0, 3, QTableWidgetItem(info["longitud"]))

        if self.tabla.rowCount() > 500:
            self.tabla.removeRow(500)

        for ip in (info["origen"], info["destino"]):
            if ip != "N/A":
                self.ips_detectadas.add(ip)
        self.numero_dispositivos.setText(str(len(self.ips_detectadas)))

    def al_finalizar_sniffer(self):
        """Se ejecuta automáticamente cuando el QThread termina."""
        self.btn_escanear.setEnabled(True)
        self.btn_escanear.setText("Escanear red")
        self.estado_red.setText("Detenido")

    def manejar_error_sniffer(self, mensaje_error: str):
        """Muestra errores (por ejemplo, si falta ejecutar como Administrador/root)."""
        QMessageBox.critical(
            self,
            "Error de Captura",
            f"No se pudo iniciar el sniffer:\n{mensaje_error}\n\n"
            "Asegúrate de ejecutar el programa como Administrador/root y tener Npcap instalado."
        )

    def limpiar_tabla(self):
        self.tabla.setRowCount(0)
        self.ips_detectadas.clear()
        self.numero_dispositivos.setText("0")

    def closeEvent(self, event):
        """Si el usuario cierra la ventana mientras escanea, detiene el hilo limpiamente."""
        if self.worker is not None and self.worker.isRunning():
            self.detener_evento.set()
            self.worker.wait(1500)
        event.accept()