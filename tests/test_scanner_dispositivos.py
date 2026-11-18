import sys
from scapy.all import ARP, Ether, srp

def escanear_red(red):
    print("\n========================================")
    print("       ESCANER DE RED LOCAL")
    print("========================================")
    print(f"Red objetivo: {red}\n")

    paquete_arp = ARP(pdst=red)

    paquete_ethernet = Ether(dst="ff:ff:ff:ff:ff:ff")

    paquete = paquete_ethernet / paquete_arp

    print("[+] Escaneando dispositivos...\n")

    respuestas = srp(paquete, timeout=3, verbose=False)[0]


    print("{:<18} {:<20}".format("DIRECCION IP", "DIRECCION MAC"))
    print("-" * 40)

    for enviado, recibido in respuestas:
        print("{:<18} {:<20}".format(
            recibido.psrc,
            recibido.hwsrc
        ))

    print("\n[+] Total de dispositivos encontrados:",
          len(respuestas))


if __name__ == "__main__":
    # Cambiar por el rango de tu red local
    red_local = "192.168.1.0/24"

    try:
        escanear_red(red_local)
    except PermissionError:
        print("[-] Ejecuta el programa como administrador.")
    except Exception as error:
        print("[-] Error:", error)
