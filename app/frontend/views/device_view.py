
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QHeaderView
)


class DeviceView(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        titulo = QLabel("Dispositivos Conectados")
        titulo.setObjectName("titulo")

        descripcion = QLabel(
            "Visualizacion de los dispositivos identificados en la red"
        )

        layout.addWidget(titulo)
        layout.addWidget(descripcion)

        # TABLA DE DISPOSITIVOS
        self.tabla_dispositivos = QTableWidget()
        self.tabla_dispositivos.setColumnCount(4)

        self.tabla_dispositivos.setHorizontalHeaderLabels([
            "Nombre",
            "Direccion IP",
            "Estado",
            "Tipo"
        ])

        self.tabla_dispositivos.setRowCount(0)

        self.tabla_dispositivos.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tabla_dispositivos.verticalHeader().setVisible(False)
        self.tabla_dispositivos.setAlternatingRowColors(True)

        layout.addWidget(self.tabla_dispositivos)

        # BOTON VOLVER
        self.btn_volver = QPushButton(
            "Volver al panel principal"
        )

        layout.addWidget(self.btn_volver)
