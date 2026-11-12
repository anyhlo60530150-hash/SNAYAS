
from scapy.all import IP, ICMP
from app.backend.sniffer import capturar_trafico_continuo


def recibir_paquete(info):
    print("Paquete recibido:")
    print(info)


paquete = (
    IP(
        src="192.168.1.10",
        dst="8.8.8.8"
    )
    / ICMP()
)

capturar_trafico_continuo(paquete, recibir_paquete)
