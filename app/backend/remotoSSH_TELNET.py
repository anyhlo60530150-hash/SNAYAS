import paramiko
import socket
import time

def ejecutar_ssh(host, puerto, usuario, password, comando):
    """Conecta por SSH, ejecuta un comando y retorna la salida."""
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        cliente.connect(hostname=host, port=puerto, username=usuario, password=password, timeout=10)
        stdin, stdout, stderr = cliente.exec_command(comando)
        salida = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        cliente.close()
        return True, salida if salida else error
    except Exception as e:
        return False, f"Error SSH: {str(e)}"

def ejecutar_telnet(host, puerto, usuario, password, comando):
    """Cliente Telnet ligero usando sockets (compatible con Python 3.13+)."""
    try:
        with socket.create_connection((host, puerto), timeout=10) as s:
            time.sleep(0.5)
            s.recv(1024) # Leer banner inicial
            s.sendall(usuario.encode('ascii') + b"\n")
            time.sleep(0.5)
            s.recv(1024)
            s.sendall(password.encode('ascii') + b"\n")
            time.sleep(0.5)
            s.recv(1024)
            
            s.sendall(comando.encode('ascii') + b"\n")
            time.sleep(1)
            respuesta = s.recv(4096).decode('utf-8', errors='ignore')
            return True, respuesta
    except Exception as e:
        return False, f"Error Telnet: {str(e)}"