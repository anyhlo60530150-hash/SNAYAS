from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QPushButton, QMessageBox
)
from app.backend.network_service import ejecutar_telnet
from app.backend.workers import NetworkWorker


class TelnetView(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        titulo = QLabel("Conexión TELNET")
        titulo.setObjectName("titulo")
        descripcion = QLabel("Panel de administración remota TELNET")

        layout.addWidget(titulo)
        layout.addWidget(descripcion)

        fila_host = QHBoxLayout()
        self.ip = QLineEdit()
        self.ip.setPlaceholderText("Dirección IP")
        self.puerto = QLineEdit("23")
        self.puerto.setFixedWidth(90)
        fila_host.addWidget(QLabel("IP:"))
        fila_host.addWidget(self.ip)
        fila_host.addWidget(QLabel("Puerto:"))
        fila_host.addWidget(self.puerto)
        layout.addLayout(fila_host)

        fila_auth = QHBoxLayout()
        self.usuario = QLineEdit()
        self.usuario.setPlaceholderText("Usuario")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Contraseña")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        fila_auth.addWidget(QLabel("Usuario:"))
        fila_auth.addWidget(self.usuario)
        fila_auth.addWidget(QLabel("Contraseña:"))
        fila_auth.addWidget(self.password)
        layout.addLayout(fila_auth)

        layout.addWidget(QLabel("Comando a ejecutar:"))
        fila_cmd = QHBoxLayout()
        self.comando = QLineEdit()
        self.comando.setPlaceholderText("Ej: show running-config")
        self.comando.returnPressed.connect(self.enviar_comando)
        self.btn_ejecutar = QPushButton("Ejecutar Telnet")
        self.btn_ejecutar.clicked.connect(self.enviar_comando)
        fila_cmd.addWidget(self.comando)
        fila_cmd.addWidget(self.btn_ejecutar)
        layout.addLayout(fila_cmd)

        layout.addWidget(QLabel("Información de conexión:"))
        self.informacion = QTextEdit()
        self.informacion.setReadOnly(True)
        self.informacion.setPlaceholderText("Salida de la sesión Telnet...")
        layout.addWidget(self.informacion)

        self.btn_volver = QPushButton("Volver al panel principal")
        layout.addWidget(self.btn_volver)

    def enviar_comando(self):
        host = self.ip.text().strip()
        puerto = self.puerto.text().strip() or "23"
        usuario = self.usuario.text().strip()
        password = self.password.text()
        cmd = self.comando.text().strip()

        if not all([host, usuario, cmd]):
            QMessageBox.warning(self, "Campos incompletos", "Ingresa IP, usuario y comando.")
            return

        self.btn_ejecutar.setEnabled(False)
        self.informacion.append(f"> {cmd}\nEnviando por Telnet a {host}...")

        self.worker = NetworkWorker(ejecutar_telnet, host, puerto, usuario, password, cmd)
        self.worker.resultado.connect(self.mostrar_resultado)
        self.worker.start()

    def mostrar_resultado(self, exito, mensaje):
        self.btn_ejecutar.setEnabled(True)
        estado = "[OK]" if exito else "[ERROR]"
        self.informacion.append(f"{estado}\n{mensaje}\n" + "-" * 40)