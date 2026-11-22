#telnet_service.py
import socket
import time

IAC = 255   # 0xFF
DONT = 254  # 0xFE
DO = 253    # 0xFD
WONT = 252  # 0xFC
WILL = 251  # 0xFB


def _filtrar_y_responder_iac(sock: socket.socket, data: bytes) -> str:
    """Responde a negociaciones Telnet básicas y devuelve el texto limpio."""
    texto = bytearray()
    i = 0
    n = len(data)

    while i < n:
        b = data[i]
        if b == IAC and i + 2 < n:
            cmd = data[i + 1]
            opt = data[i + 2]
            try:
                if cmd in (DO, DONT):
                    sock.sendall(bytes([IAC, WONT, opt]))
                elif cmd in (WILL, WONT):
                    sock.sendall(bytes([IAC, DONT, opt]))
            except OSError:
                # Si el peer cerró/abortó la conexión, dejamos de responder IAC
                break
            i += 3
        elif b == IAC and i + 1 < n and data[i + 1] == IAC:
            texto.append(IAC)
            i += 2
        else:
            texto.append(b)
            i += 1

    return texto.decode("utf-8", errors="ignore")


def _leer_disponible(
    sock: socket.socket,
    espera_max: float = 1.5,
    silencio_seg: float = 0.4,
) -> str:
    """Lee datos disponibles hasta que deje de llegar tráfico o venza espera_max."""
    sock.settimeout(0.25)
    fin = time.monotonic() + espera_max
    partes = []

    while time.monotonic() < fin:
        try:
            chunk = sock.recv(4096)
            if not chunk:
                break
            limpio = _filtrar_y_responder_iac(sock, chunk)
            if limpio:
                partes.append(limpio)
            # Extiende la ventana mientras siga llegando salida (útil para running-config)
            fin = min(time.monotonic() + silencio_seg, fin + 0.5)
        except socket.timeout:
            if partes:
                break
        except ConnectionResetError as e:
            raise RuntimeError(f"El servidor cerró/reinició la conexión (10054): {e}") from e
        except ConnectionAbortedError as e:
            raise RuntimeError(f"Conexión anulada localmente/por el host (10053): {e}") from e

    return "".join(partes)


def ejecutar_telnet(
    host: str,
    puerto: int,
    usuario: str,
    password: str,
    comando: str,
) -> tuple[bool, str]:
    """Conecta por Telnet, autentica si aplica y ejecuta un comando."""
    try:
        with socket.create_connection((host, int(puerto)), timeout=10) as s:
            banner = _leer_disponible(s, espera_max=1.5, silencio_seg=0.35)

            # Solo enviar usuario si el servidor pide login o si se configuró y no hay error previo
            if usuario:
                s.sendall(usuario.encode("ascii", errors="ignore") + b"\r\n")
                _leer_disponible(s, espera_max=1.2, silencio_seg=0.35)

            if password:
                s.sendall(password.encode("ascii", errors="ignore") + b"\r\n")
                _leer_disponible(s, espera_max=1.2, silencio_seg=0.35)

            s.sendall(comando.encode("ascii", errors="ignore") + b"\r\n")
            # Comandos como 'show running-config' tardan más en volcar toda la salida
            respuesta = _leer_disponible(s, espera_max=8.0, silencio_seg=0.6)

            salida_total = (banner + "\n" + respuesta).strip()
            return True, salida_total if salida_total else "Comando enviado."
    except Exception as e:
        return False, f"Error Telnet: {type(e).__name__}: {e}"