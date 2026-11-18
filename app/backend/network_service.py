import os
import socket
import time
from ftplib import FTP
import paramiko


def ejecutar_ssh(host, puerto, usuario, password, comando):
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        cliente.connect(
            hostname=host, port=int(puerto), username=usuario, password=password, timeout=10
        )
        stdin, stdout, stderr = cliente.exec_command(comando)
        salida = stdout.read().decode("utf-8", errors="ignore")
        error = stderr.read().decode("utf-8", errors="ignore")
        cliente.close()
        return True, salida if salida else (error if error else "Comando ejecutado sin salida.")
    except Exception as e:
        return False, f"Error SSH: {str(e)}"


def ejecutar_telnet(host, puerto, usuario, password, comando):
    try:
        with socket.create_connection((host, int(puerto)), timeout=10) as s:
            time.sleep(0.5)
            s.recv(1024)
            s.sendall(usuario.encode("ascii") + b"\n")
            time.sleep(0.5)
            s.recv(1024)
            s.sendall(password.encode("ascii") + b"\n")
            time.sleep(0.5)
            s.recv(1024)

            s.sendall(comando.encode("ascii") + b"\n")
            time.sleep(1)
            respuesta = s.recv(4096).decode("utf-8", errors="ignore")
            return True, respuesta if respuesta else "Comando enviado."
    except Exception as e:
        return False, f"Error Telnet: {str(e)}"


def subir_archivo_ftp(host, usuario, password, ruta_local, ruta_remota):
    try:
        with FTP(host, timeout=10) as ftp:
            ftp.login(user=usuario, passwd=password)
            with open(ruta_local, "rb") as archivo:
                ftp.storbinary(f"STOR {ruta_remota}", archivo)
        return True, f"Archivo '{os.path.basename(ruta_local)}' subido por FTP correctamente."
    except Exception as e:
        return False, f"Error FTP: {str(e)}"


def subir_archivo_sftp(host, puerto, usuario, password, ruta_local, ruta_remota):
    try:
        transporte = paramiko.Transport((host, int(puerto)))
        transporte.connect(username=usuario, password=password)
        sftp = paramiko.SFTPClient.from_transport(transporte)
        sftp.put(ruta_local, ruta_remota)
        sftp.close()
        transporte.close()
        return True, f"Archivo '{os.path.basename(ruta_local)}' subido por SFTP correctamente."
    except Exception as e:
        return False, f"Error SFTP: {str(e)}"