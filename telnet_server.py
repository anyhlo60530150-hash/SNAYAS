import socket
import time
import sys

IAC, DO, DONT, WILL, WONT = 255, 253, 254, 251, 252
ECHO = 1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", 2323))
    srv.listen(1)
    print("Simulador Telnet realista en 127.0.0.1:2323...")

    while True:
        conn, addr = srv.accept()
        with conn:
            # Simula negociación Telnet (ej. el servidor dice WILL ECHO)
            conn.sendall(bytes([IAC, WILL, ECHO]))
            conn.sendall(b"\r\nEdge-R1 Telnet\r\nUsername: ")
            _ = conn.recv(1024)

            conn.sendall(b"Password: ")
            _ = conn.recv(1024)

            conn.sendall(b"\r\nEdge-R1# ")
            cmd = conn.recv(1024).decode("utf-8", errors="ignore").strip()

            if "running-config" in cmd:

                for i in range(1, 8):
                    bloque = f"! Linea de configuracion {i}\r\n".encode("utf-8")
                    conn.sendall(bloque)
                    time.sleep(0.25)
            else:
                conn.sendall(f"Respuesta simulada para: {cmd}\r\n".encode("utf-8"))

            conn.sendall(b"Edge-R1# ")