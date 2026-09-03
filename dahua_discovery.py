#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DAHUA Camera Discovery Tool
Testiranje in odkrivanje DAHUA kamer v lokalni mreži
"""

import socket
import struct
import sys
import threading
import time
from datetime import datetime
import json

class DAHUADiscovery:
    """DAHUA camera discovery utility"""
    
    # DAHUA UDP discovery port
    DAHUA_PORT = 37810
    
    # DAHUA discovery protocol header
    DAHUA_HEADER = bytes([0xFF, 0x01, 0x00, 0x00])
    
    def __init__(self, timeout=3, broadcast_addr='255.255.255.255'):
        """
        Initialize DAHUA Discovery
        
        Args:
            timeout: Timeout za prijave v sekundah
            broadcast_addr: Broadcast naslov za pošiljanje
        """
        self.timeout = timeout
        self.broadcast_addr = broadcast_addr
        self.cameras = []
        self.lock = threading.Lock()
    
    def send_discovery_packet(self, sock):
        """Pošlji odkrivni paket na DAHUA kamere"""
        try:
            # DAHUA discovery packet
            discovery_packet = self.DAHUA_HEADER + bytes(16)  # Header + padding
            
            sock.sendto(discovery_packet, (self.broadcast_addr, self.DAHUA_PORT))
            print(f"[*] Pošljem odkrivni paket na {self.broadcast_addr}:{self.DAHUA_PORT}")
        except Exception as e:
            print(f"[-] Napaka pri pošiljanju paketa: {e}")
    
    def receive_responses(self, sock):
        """Prejmi odgovore od DAHUA kamer"""
        sock.settimeout(self.timeout)
        start_time = time.time()
        
        print("[*] Čakam na odgovore od kamer...")
        
        while time.time() - start_time < self.timeout:
            try:
                data, addr = sock.recvfrom(1024)
                
                # Preveri DAHUA header
                if len(data) > 4 and data[:4] == self.DAHUA_HEADER:
                    camera_info = self.parse_dahua_response(data, addr[0])
                    if camera_info:
                        with self.lock:
                            self.cameras.append(camera_info)
                        print(f"[+] Najdena kamera: {addr[0]}")
                
            except socket.timeout:
                continue
            except Exception as e:
                print(f"[-] Napaka pri prejemanju: {e}")
                continue
    
    def parse_dahua_response(self, data, ip):
        """Razčleni DAHUA odgovor"""
        try:
            camera_info = {
                'ip': ip,
                'timestamp': datetime.now().isoformat(),
                'port': self.DAHUA_PORT
            }
            
            # Skušaj ekstraktovati dodatne informacije
            if len(data) > 40:
                # Preostali podatki v paketu
                try:
                    info_str = data[4:].decode('utf-8', errors='ignore').strip('\x00')
                    if info_str:
                        camera_info['info'] = info_str
                except:
                    pass
            
            return camera_info
        except Exception as e:
            print(f"[-] Napaka pri razčlenjevanju: {e}")
            return None
    
    def discover(self):
        """Izvedite odkrivanje DAHUA kamer"""
        print("=" * 60)
        print("DAHUA Camera Discovery Tool")
        print("Testiranje in odkrivanje DAHUA kamer v lokalni mreži")
        print("=" * 60)
        print()
        
        try:
            # Kreiraj UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # Odpri socket za poslušanje
            sock.bind(('0.0.0.0', self.DAHUA_PORT))
            
            # Pošlji odkrivni paket
            self.send_discovery_packet(sock)
            
            # Prejmi odgovore
            self.receive_responses(sock)
            
            sock.close()
            
        except Exception as e:
            print(f"[-] Napaka: {e}")
            return False
        
        return True
    
    def display_results(self):
        """Prikaži rezultate odkrivanja"""
        print()
        print("=" * 60)
        print("REZULTATI ODKRIVANJA")
        print("=" * 60)
        
        if not self.cameras:
            print("[-] Nobena DAHUA kamera ni bila najdena")
            return
        
        print(f"[+] Najdeno {len(self.cameras)} kamere(e):\n")
        
        for idx, camera in enumerate(self.cameras, 1):
            print(f"Kamera {idx}:")
            print(f"  IP Naslov: {camera['ip']}")
            print(f"  Port: {camera['port']}")
            print(f"  Čas odkrivanja: {camera['timestamp']}")
            if 'info' in camera:
                print(f"  Informacije: {camera['info']}")
            print()
    
    def save_results(self, filename='dahua_cameras.json'):
        """Shrani rezultate v JSON datoteko"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.cameras, f, indent=2, ensure_ascii=False)
            print(f"[+] Rezultati shranjeni v {filename}")
        except Exception as e:
            print(f"[-] Napaka pri shranjevanju: {e}")


def main():
    """Glavna funkcija"""
    print()
    
    # Kreiraj discovery instance
    discovery = DAHUADiscovery(timeout=5)
    
    # Izvedite odkrivanje
    if discovery.discover():
        discovery.display_results()
        discovery.save_results()
    else:
        print("[-] Odkrivanje je bilo neuspešno")
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Prekinjeno s strani uporabnika")
        sys.exit(0)
    except Exception as e:
        print(f"[-] Napaka: {e}")
        sys.exit(1)
