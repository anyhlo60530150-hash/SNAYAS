
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
    QMessageBox,
    QStackedWidget
)

from PySide6.QtCore import Qt

from app.frontend.stylesheet.style import obtener_estilos
from app.backend.workers import NetworkWorker
from app.backend.sniffer import capturar_trafico_continuo
from app.frontend.views.ssh_view import SSHView
from app.frontend.views.telnet_view import TelnetView
from app.frontend.views.device_view import DeviceView


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Network Assistant & Alert Suite")
        self.resize(1100, 700)
        self.setMinimumSize(800, 550)

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

        self.btn_red = QPushButton("Panel de Red")
        self.btn_devices = QPushButton("Dispositivos")
        self.btn_ssh = QPushButton("Conexion SSH")
        self.btn_telnet = QPushButton("Conexion TELNET")

        botones_menu = [
            self.btn_red,
            self.btn_devices,
            self.btn_ssh,
            self.btn_telnet
        ]

        for boton in botones_menu:
            boton.setObjectName("menuButton")
            boton.setCursor(Qt.CursorShape.PointingHandCursor)
            menu_layout.addWidget(boton)

        menu_layout.addStretch()

        version = QLabel("Version 1.0")
        version.setObjectName("version")
        menu_layout.addWidget(version)

        # PANELES DE NAVEGACION
        self.paneles = QStackedWidget()

        self.panel_red = self.crear_panel_red()
        self.panel_dispositivos = DeviceView()
        self.panel_ssh = SSHView()
        self.panel_telnet = TelnetView()
        self.panel_ssh.btn_volver.clicked.connect(
            lambda: self.cambiar_panel(0)
            )
            
        self.panel_telnet.btn_volver.clicked.connect(
            lambda: self.cambiar_panel(0)
            )
            
        self.panel_dispositivos.btn_volver.clicked.connect(
            lambda: self.cambiar_panel(0)
            )

        self.paneles.addWidget(self.panel_red)
        self.paneles.addWidget(self.panel_dispositivos)
        self.paneles.addWidget(self.panel_ssh)
        self.paneles.addWidget(self.panel_telnet)

        # CONECTAR BOTONES DEL MENU
        self.btn_red.clicked.connect(
            lambda: self.cambiar_panel(0)
        )

        self.btn_devices.clicked.connect(
            lambda: self.cambiar_panel(1)
        )

        self.btn_ssh.clicked.connect(
            lambda: self.cambiar_panel(2)
        )

        self.btn_telnet.clicked.connect(
            lambda: self.cambiar_panel(3)
        )

        # BOTONES VOLVER
        self.panel_ssh.btn_volver.clicked.connect(
            lambda: self.cambiar_panel(0)
        )

        self.panel_telnet.btn_volver.clicked.connect(
            lambda: self.cambiar_panel(0)
        )
        self.panel_dispositivos.btn_volver.clicked.connect(
            lambda: self.cambiar_panel(0)
        )

        # AGREGAR MENU Y PANELES
        principal.addWidget(menu)
        principal.addWidget(self.paneles, 1)

    # CAMBIAR ENTRE PANELES
    def cambiar_panel(self, indice):
        self.paneles.setCurrentIndex(indice)

    # PANEL PRINCIPAL DE RED
    def crear_panel_red(self):

        contenido = QWidget()
        contenido.setObjectName("contenido")

        layout = QVBoxLayout(contenido)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        encabezado = QHBoxLayout()

        titulo = QLabel("Panel de Red")
        titulo.setObjectName("titulo")

        estado = QLabel("● Sistema en linea")
        estado.setObjectName("estado")

        encabezado.addWidget(titulo)
        encabezado.addStretch()
        encabezado.addWidget(estado)

        layout.addLayout(encabezado)

        # TARJETAS
        tarjetas = QHBoxLayout()
        tarjetas.setSpacing(15)

        tarjeta1 = QFrame()
        tarjeta1.setObjectName("tarjeta")
        layout1 = QVBoxLayout(tarjeta1)

        texto1 = QLabel("Dispositivos Conectados")
        texto1.setObjectName("textoTarjeta")

        self.numero_dispositivos = QLabel("0")
        self.numero_dispositivos.setObjectName("numeroTarjeta")

        layout1.addWidget(texto1)
        layout1.addWidget(self.numero_dispositivos)

        tarjeta2 = QFrame()
        tarjeta2.setObjectName("tarjeta")
        layout2 = QVBoxLayout(tarjeta2)

        texto2 = QLabel("Alertas Activas")
        texto2.setObjectName("textoTarjeta")

        self.numero_alertas = QLabel("0")
        self.numero_alertas.setObjectName("numeroTarjeta")

        layout2.addWidget(texto2)
        layout2.addWidget(self.numero_alertas)

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

        layout.addLayout(tarjetas)

        self.titulo_tabla = QLabel("Dispositivos de Red")
        self.titulo_tabla.setObjectName("subtitulo")

        layout.addWidget(self.titulo_tabla)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)

        self.tabla.setHorizontalHeaderLabels([
            "Nombre del Dispositivo",
            "Direccion IP",
            "Estado",
            "Tipo"
        ])

        self.tabla.setRowCount(0)

        self.tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setAlternatingRowColors(True)

        self.tabla.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        layout.addWidget(self.tabla)

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

        layout.addLayout(botones)

        return contenido

    # ESCANEO DE RED
    def alternar_sniffer(self):

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

        self.titulo_tabla.setText(
            "Trafico de Red en Tiempo Real"
        )

        self.tabla.setHorizontalHeaderLabels([
            "IP Origen",
            "IP Destino",
            "Protocolo",
            "Longitud (Bytes)"
        ])

        self.tabla.setRowCount(0)

        self.worker = NetworkWorker(
            capturar_trafico_continuo,
            detener_evento=self.detener_evento,
            interfaz=None,
            filtro="ip"
        )

        self.worker.kwargs["callback_paquete"] = (
            self.worker.progreso_dato.emit
        )

        self.worker.progreso_dato.connect(
            self.agregar_paquete_a_tabla
        )

        self.worker.error_ocurrido.connect(
            self.manejar_error_sniffer
        )

        self.worker.finished.connect(
            self.al_finalizar_sniffer
        )

        self.btn_escanear.setText("Detener escaneo")
        self.estado_red.setText("Capturando...")

        self.worker.start()

    def agregar_paquete_a_tabla(self, info: dict):

        self.tabla.insertRow(0)

        self.tabla.setItem(
            0, 0, QTableWidgetItem(info["origen"])
        )

        self.tabla.setItem(
            0, 1, QTableWidgetItem(info["destino"])
        )

        self.tabla.setItem(
            0, 2, QTableWidgetItem(info["protocolo"])
        )

        self.tabla.setItem(
            0, 3, QTableWidgetItem(info["longitud"])
        )

        if self.tabla.rowCount() > 500:
            self.tabla.removeRow(500)

        for ip in (info["origen"], info["destino"]):

            if ip != "N/A":
                self.ips_detectadas.add(ip)

        self.numero_dispositivos.setText(
            str(len(self.ips_detectadas))
        )

    def al_finalizar_sniffer(self):

        self.btn_escanear.setEnabled(True)
        self.btn_escanear.setText("Escanear red")
        self.estado_red.setText("Detenido")

    def manejar_error_sniffer(self, mensaje_error: str):

        QMessageBox.critical(
            self,
            "Error de Captura",
            f"No se pudo iniciar el sniffer:\n{mensaje_error}\n\n"
            "Asegurate de ejecutar el programa como Administrador/root "
            "y tener Npcap instalado."
        )

    def limpiar_tabla(self):

        self.tabla.setRowCount(0)
        self.ips_detectadas.clear()
        self.numero_dispositivos.setText("0")

    def closeEvent(self, event):

        if self.worker is not None and self.worker.isRunning():

            self.detener_evento.set()
            self.worker.wait(1500)

        event.accept()
