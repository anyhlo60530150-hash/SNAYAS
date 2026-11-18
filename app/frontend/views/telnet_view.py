
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton
)


class TelnetView(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        titulo = QLabel("Conexion TELNET")
        titulo.setObjectName("titulo")

        descripcion = QLabel(
            "Panel de administracion de conexiones TELNET"
        )

        layout.addWidget(titulo)
        layout.addWidget(descripcion)

        layout.addWidget(QLabel("Direccion IP:"))
        self.ip = QLineEdit()
        self.ip.setPlaceholderText("Direccion IP")
        layout.addWidget(self.ip)

        layout.addWidget(QLabel("Puerto:"))
        self.puerto = QLineEdit()
        self.puerto.setPlaceholderText("23")
        layout.addWidget(self.puerto)

        layout.addWidget(QLabel("Usuario:"))
        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText("Usuario")
        layout.addWidget(self.usuario)

        layout.addWidget(QLabel("Informacion de conexion:"))
        self.informacion = QTextEdit()
        self.informacion.setPlaceholderText(
            "Informacion de la conexion TELNET..."
        )
        layout.addWidget(self.informacion)

        self.btn_volver = QPushButton("Volver al panel principal")
        layout.addWidget(self.btn_volver)
