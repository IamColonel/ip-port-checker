import socket
from datetime import datetime
import concurrent.futures
from colorama import Fore, Style

def check_ports(ip_address, ports):
    open_ports = []
    try:
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip_address, port))
            sock.close()

            if result == 0:
                open_ports.append(port)
    except socket.gaierror as e:
        print(f"Erreur lors de la résolution de l'adresse IP {ip_address}: {e}")
    
    return ip_address, open_ports

def process_ip(ip_address):
    print(f"Vérification des ports pour l'adresse IP : {ip_address}")
    ip_address, open_ports = check_ports(ip_address, [80, 443])
    if open_ports:
        # result_message = f"IP: {ip_address}, Ports ouverts: {', '.join(map(str, open_ports))}"
        with open(output_file_name, "a") as output_file:
            output_file.write(ip_address + '\n')

def main():
    global output_file_name
    input_file = input("Entrez le chemin du fichier contenant les adresses IP : ")
    output_file_name = f"CHECKED_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    print(f"Lecture des adresses IP depuis le fichier : {input_file}")
    with open(input_file, "r") as file:
        ip_addresses = file.read().splitlines()

    with concurrent.futures.ThreadPoolExecutor(max_workers=250) as executor:
        executor.map(process_ip, ip_addresses)

    print(f"Résultats enregistrés dans le fichier : {output_file_name}")

if __name__ == "__main__":
    main()
