from scapy.all import ARP, Ether, srp

def escanear_red(rango_ip="192.168.1.0/24"):
    """
    Envía paquetes ARP a la subred y devuelve una lista de dispositivos activos.
    """
    dispositivos = []
    # Crear paquete Ethernet broadcast + solicitud ARP
    paquete = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=rango_ip)
    
    # Enviar y recibir respuestas (timeout de 2 segundos)
    respondidos, _ = srp(paquete, timeout=2, verbose=0)

    for enviado, recibido in respondidos:
        dispositivos.append({
            "ip": recibido.psrc,
            "mac": recibido.hwsrc
        })
    
    return dispositivos