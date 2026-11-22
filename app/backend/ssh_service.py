import paramiko


def ejecutar_ssh(host: str, puerto: int, usuario: str, password: str, comando: str) -> tuple[bool, str]:
    """Conecta por SSH, ejecuta un comando y retorna (exito, salida_o_error)."""
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        cliente.connect(
            hostname=host,
            port=int(puerto),
            username=usuario,
            password=password,
            timeout=10,
        )
        _, stdout, stderr = cliente.exec_command(comando)
        salida = stdout.read().decode("utf-8", errors="ignore").strip()
        error = stderr.read().decode("utf-8", errors="ignore").strip()

        if salida:
            return True, salida
        if error:
            return False, error
        return True, "Comando ejecutado sin salida."
    except Exception as e:
        return False, f"Error SSH: {str(e)}"
    finally:
        cliente.close()