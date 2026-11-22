
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QTextEdit, QPushButton, QMessageBox
)

from app.backend.ssh_service import ejecutar_ssh
from app.backend.workers import NetworkWorker


class SSHView(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        titulo = QLabel("Conexión SSH")
        titulo.setObjectName("titulo")

        descripcion = QLabel(
            "Panel de administración y ejecución remota SSH"
        )

        layout.addWidget(titulo)
        layout.addWidget(descripcion)

        # IP y puerto
        fila_host = QHBoxLayout()

        self.ip = QLineEdit()
        self.ip.setPlaceholderText("Dirección IP (ej. 192.168.1.10)")

        self.puerto = QLineEdit("22")
        self.puerto.setFixedWidth(90)

        fila_host.addWidget(QLabel("IP:"))
        fila_host.addWidget(self.ip)
        fila_host.addWidget(QLabel("Puerto:"))
        fila_host.addWidget(self.puerto)

        layout.addLayout(fila_host)

        # Usuario y contraseña
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

        # Comando
        layout.addWidget(QLabel("Comando a ejecutar:"))

        fila_cmd = QHBoxLayout()

        self.comando = QLineEdit()
        self.comando.setPlaceholderText("Ej: ls -la /var/www")
        self.comando.returnPressed.connect(self.enviar_comando)

        self.btn_ejecutar = QPushButton("Ejecutar SSH")
        self.btn_ejecutar.clicked.connect(self.enviar_comando)

        fila_cmd.addWidget(self.comando)
        fila_cmd.addWidget(self.btn_ejecutar)

        layout.addLayout(fila_cmd)

        # Consola
        layout.addWidget(QLabel("Salida de consola:"))

        self.informacion = QTextEdit()
        self.informacion.setReadOnly(True)
        self.informacion.setPlaceholderText(
            "La respuesta del servidor aparecerá aquí..."
        )

        layout.addWidget(self.informacion)

        self.btn_volver = QPushButton("Volver al panel principal")
        layout.addWidget(self.btn_volver)

    def enviar_comando(self):

        if self.worker is not None and self.worker.isRunning():
            return

        host = self.ip.text().strip()
        puerto = self.puerto.text().strip() or "22"
        usuario = self.usuario.text().strip()
        password = self.password.text()
        cmd = self.comando.text().strip()

        if not all([host, usuario, cmd]):
            QMessageBox.warning(
                self,
                "Campos incompletos",
                "Ingresa IP, usuario y comando."
            )
            return

        if not puerto.isdigit() or not 1 <= int(puerto) <= 65535:
            QMessageBox.warning(
                self,
                "Puerto inválido",
                "Ingresa un puerto entre 1 y 65535."
            )
            return

        self.btn_ejecutar.setEnabled(False)

        self.informacion.append(
            f"$ {cmd}\nConectando a {host}:{puerto}..."
        )

        self.worker = NetworkWorker(
            ejecutar_ssh,
            host,
            int(puerto),
            usuario,
            password,
            cmd
        )

        self.worker.resultado_listo.connect(
            self.mostrar_resultado
        )

        self.worker.error_ocurrido.connect(
            self.mostrar_error
        )

        self.worker.finished.connect(
            self.finalizar_ejecucion
        )

        self.worker.start()

    def mostrar_resultado(self, resultado):

        if isinstance(resultado, tuple) and len(resultado) == 2:
            exito, mensaje = resultado
        else:
            exito = True
            mensaje = str(resultado)

        estado = "[OK]" if exito else "[ERROR]"

        self.informacion.append(
            f"{estado}\n{mensaje}\n" + "-" * 40
        )

    def mostrar_error(self, error):

        self.informacion.append(
            f"[ERROR]\n{error}\n" + "-" * 40
        )

    def finalizar_ejecucion(self):

        self.btn_ejecutar.setEnabled(True)
