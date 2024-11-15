import requests
import random
import time
import paramiko
import os
import subprocess
import logging
from scapy.all import *
from termcolor import colored
from stem import Signal
from stem.control import Controller
#import socks
#import socket

logging.basicConfig(filename="reconDevils.log", level=logging.INFO)

def change_tor_identity():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password="your_password_here")
        controller.signal(Signal.NEWNYM)

def tor_proxy_setup():
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket
    print(colored("• Tor proxy ativado. Todo tráfego HTTP será roteado via Tor.", "green"))

def google_dork(domain):
    print(colored(f"[+] Iniciando Google Dorking para {domain}...", "yellow"))
    
    dorks = [
        f'site:{domain} intitle:"index of /"',
        f'site:{domain} ext:php OR ext:asp OR ext:aspx',
        f'site:{domain} inurl:admin OR inurl:login OR inurl:dashboard',
        f'site:{domain} filetype:sql OR filetype:log OR filetype:txt',
        f'site:{domain} inurl:wp- OR inurl:config OR inurl:db'
    ]
    
    for dork in dorks:
        print(colored(f"[+] Executando Dork: {dork}", "cyan"))
        time.sleep(random.uniform(1.5, 3.5))

    print(colored("\n[+] Dorking concluído. Retornando ao menu...", "cyan"))


def subdomain_scan_anon(domain, wordlist):
    print(f" • [Iniciando varredura de subdomínios Em: {domain}...] ")
    logging.info(f"• [Scan de subdomínios anônimo iniciado para {domain} ]")

    with open(wordlist, 'r', encoding='latin-1') as file:
        subdomains = file.read().splitlines()

    total_words = len(subdomains)
    print(f"/------------------------------------------------------------------------------------------------------------ ")
    print(f" [+] WORDLIST: {wordlist}                                                                                   ")
    print(f" [+] TOTAL DE PALAVRAS: {total_words}                                                                       ")
    print(f"|------------------------------------------------------------------------------------------------------------")
    print(f" • Varredura na URL: http://{domain}                                                                        ")
    print(f"\\------------------------------------------------------------------------------------------------------------")

    found_subdomains = []

    for subdomain in subdomains:
        url = f"http://{subdomain}.{domain}"
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(url, headers=headers, timeout=3)

            if response.status_code == 200 or response.status_code == 403:
                found_subdomains.append(f"{url} (CODE:{response.status_code}|SIZE:{len(response.content)})")
                print(colored(f"[+] Subdomínio encontrado: {url} (CODE:{response.status_code}|SIZE:{len(response.content)})", "green"))
                logging.info(f"• Subdomínio encontrado: {url} (CODE:{response.status_code}|SIZE:{len(response.content)})")

        except requests.exceptions.RequestException as e:
            logging.error(f"[!] Erro ao tentar {url}: {str(e)}")
            continue

    if found_subdomains:
        print(colored("\n[+] Subdomínios encontrados:", "green"))
        for sub in found_subdomains:
            print(sub)
    else:
        print(colored("\n[!] Nenhum subdomínio encontrado.", "red"))

    print(colored("\n[+] Varredura de subdomínios concluída. Retornando ao menu...", "cyan"))
    logging.info("[+] Varredura de subdomínios concluída.")


def directory_scan_anon(domain, wordlist):
    print(colored(f"[+] Iniciando varredura de diretórios anonimamente no {domain}...", "yellow"))
    logging.info(f"[+] Scan de diretórios anônimo iniciado para {domain}")
    with open(wordlist, 'r') as file:
        directories = file.read().splitlines()

    for directory in directories:
        url = f"http://{domain}/{directory}"
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
                'Referer': 'https://google.com'
            }
            response = requests.get(url, headers=headers, timeout=3)
            if response.status_code == 200:
                print(colored(f"[+] Diretório encontrado: {url}", "green"))
                logging.info(f"[+] Diretório encontrado: {url}")
            elif response.status_code == 403:
                print(colored(f"[!] Acesso negado: {url}", "yellow"))
                logging.warning(f"[!] Acesso negado no diretório: {url}")
            time.sleep(random.uniform(1.5, 4.5))
        except Exception as e:
            logging.error(f"[!] Erro no diretório {directory}: {str(e)}")
            continue

def main():
    print(colored("• Iniciando o Menu da Ferramenta ReconDevils...", "cyan"))
    print("/---------------------------------------------------\\ ")
    print("| [ 1 ] Pivot via SSH Tunnel                        |")
    print("| [ 2 ] Escanear Rede Interna                       |")
    print("| [ 3 ] Scan de Subdomínios                         |")
    print("| [ 4 ] Scan de Diretórios                          |")
    print("| [ 5 ] Google Dorking                              |")
    print("| [ 6 ] Habilitar Proxy Anônimo (Tor)               |")
    print("| [ 7 ] Scan de Subdomínios (Anonimamente via Tor)  |")
    print("| [ 8 ] Scan de Diretórios (Anonimamente via Tor)   |")
    print("|---------------------------------------------------|")
    print("|        [>_]  SEJA BEM-VINDO AO MENU [>_]          |")
    print("|             [Redes sociais & Github]              |")
    print("|      insta: @alaric0x15 - Git: @STAYLOVELY        |")
    print("\\---------------------------------------------------/ ")

    option = input("[+] Escolha uma opção: ")

    if option == "1":
        host = input("[+] Digite o IP do alvo: ")
        user = input("[+] Usuário SSH: ")
        password = input("[+] Senha SSH: ")
        ssh_tunnel(host, user, password)
    
    elif option == "2":
        scan_network()
    
    elif option == "3":
        domain = input("[+] Digite o domínio alvo: ")
        wordlist = input("[+] Digite o caminho do wordlist de subdomínios: ")
        subdomain_scan(domain, wordlist)
    
    elif option == "4":
        domain = input("[+] Digite o domínio alvo: ")
        wordlist = input("[+] Digite o caminho do wordlist de diretórios: ")
        directory_scan(domain, wordlist)
    
    elif option == "5":
        domain = input("[+] Digite o domínio alvo: ")
        google_dork(domain)
    
    elif option == "6":
        tor_proxy_setup()

    elif option == "7":
        domain = input("[+] Digite o domínio alvo: ")
        wordlist = input("[+] Digite o caminho do wordlist de subdomínios: ")
        subdomain_scan_anon(domain, wordlist)
    
    elif option == "8":
        domain = input("[+] Digite o domínio alvo: ")
        wordlist = input("[+] Digite o caminho do wordlist de diretórios: ")
        directory_scan_anon(domain, wordlist)
    
    else:
        print(colored("[!] Opa! Opção inválida...", "red"))

if __name__ == "__main__":
    main()
