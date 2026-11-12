from ftplib import FTP
import paramiko
import os

def subir_archivo_ftp(host, usuario, password, ruta_local, ruta_remota):
    """Sube un archivo usando FTP tradicional."""
    try:
        with FTP(host, timeout=10) as ftp:
            ftp.login(user=usuario, passwd=password)
            with open(ruta_local, "rb") as archivo:
                ftp.storbinary(f"STOR {ruta_remota}", archivo)
        return True, f"Archivo {os.path.basename(ruta_local)} subido por FTP."
    except Exception as e:
        return False, f"Error FTP: {str(e)}"

def subir_archivo_sftp(host, puerto, usuario, password, ruta_local, ruta_remota):
    """Sube un archivo de forma segura usando Paramiko (SFTP)."""
    try:
        transporte = paramiko.Transport((host, puerto))
        transporte.connect(username=usuario, password=password)
        sftp = paramiko.SFTPClient.from_transport(transporte)
        
        sftp.put(ruta_local, ruta_remota)
        
        sftp.close()
        transporte.close()
        return True, f"Archivo {os.path.basename(ruta_local)} subido por SFTP."
    except Exception as e:
        return False, f"Error SFTP: {str(e)}"