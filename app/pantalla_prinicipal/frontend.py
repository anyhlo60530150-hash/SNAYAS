import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFrame,
    QSizePolicy
)

from PySide6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart Network Assistant & Alert Suite")
        self.resize(1100, 700)
        self.setMinimumSize(800, 550)

        self.init_ui()
        self.setStyleSheet(self.estilos())

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

        # TITULO DE LA TABLA
        titulo_tabla = QLabel("Dispositivos de Red")
        titulo_tabla.setObjectName("subtitulo")

        contenido_layout.addWidget(titulo_tabla)

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
        #Aqui van los dispositivos conectados

        self.tabla.setRowCount(0)

        # ADAPTAR COLUMNAS AL ANCHO DE LA TABLA
        encabezado_tabla = self.tabla.horizontalHeader()

        encabezado_tabla.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tabla.verticalHeader().setVisible(False)

        self.tabla.setAlternatingRowColors(True)
        self.tabla.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        contenido_layout.addWidget(self.tabla)

        # BOTONES INFERIORES
        botones = QHBoxLayout()

        actualizar = QPushButton("Actualizar")
        actualizar.setObjectName("actualizar")

        escanear = QPushButton("Escanear red")
        escanear.setObjectName("escanear")

        botones.addStretch()
        botones.addWidget(actualizar)
        botones.addWidget(escanear)

        contenido_layout.addLayout(botones)

        # AGREGAR MENU Y CONTENIDO
        principal.addWidget(menu)
        principal.addWidget(contenido, 1)

    # ESTILOS QSS
    def estilos(self):

        return """

        QWidget {
            font-family: Arial;
            color: #E5E7EB;
        }

        QMainWindow {
            background-color: #111827;
        }

        #menu {
            background-color: #0B1220;
        }

        #logo {
            color: #38BDF8;
            font-size: 19px;
            font-weight: bold;
            padding-bottom: 25px;
        }

        #menuButton {
            background-color: transparent;
            color: #AAB4C5;
            border: none;
            padding: 13px;
            text-align: left;
            border-radius: 7px;
            font-size: 14px;
        }

        #menuButton:hover {
            background-color: #1E293B;
            color: #38BDF8;
        }

        #version {
            color: #64748B;
            font-size: 11px;
        }

        #contenido {
            background-color: #111827;
        }

        #titulo {
            font-size: 25px;
            font-weight: bold;
            color: white;
        }

        #estado {
            color: #4ADE80;
            font-size: 13px;
        }

        #tarjeta {
            background-color: #1E293B;
            border: 1px solid #334155;
            border-radius: 10px;
        }

        #textoTarjeta {
            color: #94A3B8;
            font-size: 12px;
        }

        #numeroTarjeta {
            color: #38BDF8;
            font-size: 25px;
            font-weight: bold;
        }

        #subtitulo {
            font-size: 18px;
            font-weight: bold;
            color: white;
        }

        QTableWidget {
            background-color: #1E293B;
            alternate-background-color: #253449;
            color: #E5E7EB;
            border: 1px solid #334155;
            border-radius: 8px;
            gridline-color: #334155;
            selection-background-color: #075985;
            selection-color: white;
        }

        QHeaderView::section {
            background-color: #0F172A;
            color: #38BDF8;
            padding: 12px;
            border: none;
            font-weight: bold;
        }

        QTableWidget::item {
            padding: 10px;
        }

        #actualizar, #escanear {
            background-color: #1E293B;
            color: #38BDF8;
            border: 1px solid #38BDF8;
            border-radius: 7px;
            padding: 10px 20px;
        }

        #actualizar:hover, #escanear:hover {
            background-color: #075985;
            color: white;
        }

        QPushButton {
            font-size: 13px;
        }

        """


if __name__ == "__main__":

    app = QApplication(sys.argv)

    ventana = MainWindow()
    ventana.show()

    sys.exit(app.exec())