# scanner.py
import socket
from scapy.all import ARP, Ether, srp

def escanear_red(rango_ip="192.168.1.0/24"):
    """
    Envía paquetes ARP a la subred y devuelve una lista de dispositivos activos.
    """
    dispositivos = []
    paquete = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=rango_ip)
    respondidos, _ = srp(paquete, timeout=2, verbose=0)

    for enviado, recibido in respondidos:
        ip = recibido.psrc
        mac = recibido.hwsrc
        
        # Intentar resolver el nombre del dispositivo (hostname)
        try:
            nombre = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            nombre = "Desconocido"

        dispositivos.append({
            "nombre": nombre,
            "ip": ip,
            "mac": mac,
            "estado": "Activo"
        })
    
    return dispositivos