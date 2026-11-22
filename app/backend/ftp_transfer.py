import os
from ftplib import FTP, error_perm, error_temp


def subir_archivo_ftp(host: str, puerto: int, usuario: str, password: str, ruta_local: str, ruta_remota: str, timeout: int = 15):
    """Sube un archivo local a un servidor FTP tradicional."""
    if not os.path.isfile(ruta_local):
        return False, f"El archivo local no existe: {ruta_local}"

    ftp = FTP(timeout=timeout)
    try:
        ftp.connect(host=host, port=puerto)
        ftp.login(user=usuario, passwd=password)
        ftp.set_pasv(True)

        with open(ruta_local, "rb") as archivo:
            ftp.storbinary(f"STOR {ruta_remota}", archivo)

        return True, f"Archivo subido por FTP a '{host}:{puerto}{ruta_remota}'."
    except (error_perm, error_temp) as e:
        return False, f"Error del servidor FTP: {e}"
    except OSError as e:
        return False, f"Error de conexión FTP: {e}"
    finally:
        try:
            ftp.quit()
        except Exception:
            try:
                ftp.close()
            except Exception:
                pass


def subir_archivo_sftp(host: str, puerto: int, usuario: str, password: str, ruta_local: str, ruta_remota: str, timeout: int = 15):
    """Sube un archivo local a un servidor SFTP usando Paramiko."""
    if not os.path.isfile(ruta_local):
        return False, f"El archivo local no existe: {ruta_local}"

    try:
        import paramiko
    except ImportError:
        return False, "Falta instalar 'paramiko' para SFTP (pip install paramiko)."

    transport = None
    sftp = None
    try:
        transport = paramiko.Transport((host, puerto))
        transport.connect(username=usuario, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)
        if sftp is None:
            return False, "No se pudo abrir el canal SFTP."

        sftp.put(ruta_local, ruta_remota)
        return True, f"Archivo subido por SFTP a '{host}:{puerto}:{ruta_remota}'."
    except paramiko.AuthenticationException:
        return False, "Error de autenticación SFTP: usuario o contraseña incorrectos."
    except paramiko.SSHException as e:
        return False, f"Error SSH/SFTP: {e}"
    except OSError as e:
        return False, f"Error de conexión o ruta SFTP: {e}"
    finally:
        if sftp is not None:
            try:
                sftp.close()
            except Exception:
                pass
        if transport is not None:
            try:
                transport.close()
            except Exception:
                pass


def ejecutar_transferencia(protocolo_idx: int, host: str, puerto: int, usuario: str, password: str, ruta_local: str, ruta_remota: str):
    """Selecciona FTP o SFTP según el índice del combo (0 = SFTP, 1 = FTP)."""
    if protocolo_idx == 0:
        return subir_archivo_sftp(host, puerto, usuario, password, ruta_local, ruta_remota)
    return subir_archivo_ftp(host, puerto, usuario, password, ruta_local, ruta_remota)