# sniffer.py
from scapy.all import sniff, IP, TCP, UDP

def capturar_trafico_continuo(callback_paquete, detener_evento, interfaz=None, filtro=""):
    def procesar(paquete):
        info = {
            "origen": paquete[IP].src if paquete.haslayer(IP) else "N/A",
            "destino": paquete[IP].dst if paquete.haslayer(IP) else "N/A",
            "protocolo": "TCP" if paquete.haslayer(TCP) else ("UDP" if paquete.haslayer(UDP) else "Otro"),
            "longitud": str(len(paquete))
        }
        callback_paquete(info)

    while not detener_evento.is_set():
        sniff(
            iface=interfaz,
            filter=filtro,
            prn=procesar,
            store=0,
            timeout=1,
            stop_filter=lambda _: detener_evento.is_set()
        )