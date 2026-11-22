import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QComboBox, QFileDialog, QMessageBox
)

from app.backend.workers import TaskWorker
from app.backend.ftp_transfer import ejecutar_transferencia


class FTPView(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        titulo = QLabel("Transferencia de Archivos (FTP / SFTP)")
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        # Protocolo, IP y Puerto
        fila_conn = QHBoxLayout()
        self.protocolo = QComboBox()
        self.protocolo.addItems(["SFTP (Seguro)", "FTP (Tradicional)"])
        self.protocolo.currentIndexChanged.connect(self.cambiar_puerto_defecto)

        self.ip = QLineEdit()
        self.ip.setPlaceholderText("Dirección IP o Host")
        self.puerto = QLineEdit("22")
        self.puerto.setFixedWidth(80)

        fila_conn.addWidget(QLabel("Protocolo:"))
        fila_conn.addWidget(self.protocolo)
        fila_conn.addWidget(QLabel("Host:"))
        fila_conn.addWidget(self.ip)
        fila_conn.addWidget(QLabel("Puerto:"))
        fila_conn.addWidget(self.puerto)
        layout.addLayout(fila_conn)

        # Credenciales
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

        # Archivo local
        layout.addWidget(QLabel("Archivo local:"))
        fila_local = QHBoxLayout()
        self.ruta_local = QLineEdit()
        self.ruta_local.setPlaceholderText("Selecciona un archivo de tu equipo...")
        btn_examinar = QPushButton("Examinar...")
        btn_examinar.clicked.connect(self.seleccionar_archivo)
        fila_local.addWidget(self.ruta_local)
        fila_local.addWidget(btn_examinar)
        layout.addLayout(fila_local)

        # Ruta remota
        layout.addWidget(QLabel("Ruta destino en el servidor:"))
        self.ruta_remota = QLineEdit()
        self.ruta_remota.setPlaceholderText("Ej: /home/usuario/archivo.txt")
        layout.addWidget(self.ruta_remota)

        self.btn_subir = QPushButton("Subir Archivo")
        self.btn_subir.clicked.connect(self.iniciar_subida)
        layout.addWidget(self.btn_subir)

        self.informacion = QTextEdit()
        self.informacion.setReadOnly(True)
        self.informacion.setPlaceholderText("Registro de transferencias...")
        layout.addWidget(self.informacion)

        self.btn_volver = QPushButton("Volver al panel principal")
        layout.addWidget(self.btn_volver)

    def cambiar_puerto_defecto(self, index):
        if index == 0:  # SFTP
            self.puerto.setText("22")
            self.puerto.setEnabled(True)
        else:  # FTP
            self.puerto.setText("21")
            self.puerto.setEnabled(True)

    def seleccionar_archivo(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo para subir")
        if ruta:
            self.ruta_local.setText(ruta)
            if not self.ruta_remota.text().strip():
                self.ruta_remota.setText(f"/{os.path.basename(ruta)}")

    def iniciar_subida(self):
        protocolo_idx = self.protocolo.currentIndex()
        host = self.ip.text().strip()
        puerto_texto = self.puerto.text().strip() or ("22" if protocolo_idx == 0 else "21")
        usuario = self.usuario.text().strip()
        password = self.password.text()
        local = self.ruta_local.text().strip()
        remota = self.ruta_remota.text().strip()

        if not all([host, usuario, local, remota]):
            QMessageBox.warning(self, "Faltan datos", "Completa host, usuario, archivo local y ruta remota.")
            return

        if not os.path.isfile(local):
            QMessageBox.warning(self, "Archivo no válido", "La ruta del archivo local no existe.")
            return

        try:
            puerto = int(puerto_texto)
            if not (1 <= puerto <= 65535):
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Puerto inválido", "El puerto debe ser un número entero entre 1 y 65535.")
            return

        if self.worker is not None and self.worker.isRunning():
            QMessageBox.information(self, "Transferencia en curso", "Ya hay una subida en progreso.")
            return

        nombre_protocolo = "SFTP" if protocolo_idx == 0 else "FTP"
        self.btn_subir.setEnabled(False)
        self.informacion.append(f"[{nombre_protocolo}] Subiendo '{os.path.basename(local)}' a {host}:{puerto}...")

        self.worker = TaskWorker(
            ejecutar_transferencia,
            protocolo_idx,
            host,
            puerto,
            usuario,
            password,
            local,
            remota
        )
        self.worker.tarea_completada.connect(self.mostrar_resultado)
        self.worker.finished.connect(self._limpiar_worker)
        self.worker.start()

    def _limpiar_worker(self):
        self.btn_subir.setEnabled(True)
        self.worker = None

    def mostrar_resultado(self, exito: bool, mensaje: str):
        self.btn_subir.setEnabled(True)
        estado = "[OK]" if exito else "[ERROR]"
        self.informacion.append(f"{estado} {mensaje}")