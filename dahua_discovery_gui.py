#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DAHUA Camera Discovery Tool - GUI Version
Grafično testiranje in odkrivanje DAHUA kamer v lokalni mreži
"""

import socket
import threading
import time
from datetime import datetime
import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import ipaddress

class DAHUADiscoveryGUI:
    """DAHUA camera discovery with GUI"""
    
    DAHUA_PORT = 37810
    DAHUA_HEADER = bytes([0xFF, 0x01, 0x00, 0x00])
    
    def __init__(self, root):
        """Initialize GUI"""
        self.root = root
        self.root.title("DAHUA Camera Discovery Tool")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.cameras = []
        self.discovering = False
        self.discovery_thread = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup user interface"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="DAHUA Camera Discovery Tool", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Nastavitve", padding="10")
        settings_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        settings_frame.columnconfigure(1, weight=1)
        
        # Broadcast address
        ttk.Label(settings_frame, text="Broadcast naslov:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.broadcast_var = tk.StringVar(value="255.255.255.255")
        broadcast_entry = ttk.Entry(settings_frame, textvariable=self.broadcast_var)
        broadcast_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Timeout
        ttk.Label(settings_frame, text="Timeout (sekunde):").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.timeout_var = tk.StringVar(value="5")
        timeout_entry = ttk.Entry(settings_frame, textvariable=self.timeout_var, width=10)
        timeout_entry.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.discover_btn = ttk.Button(button_frame, text="Začni odkrivanje", command=self.start_discovery)
        self.discover_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="Ustavi", command=self.stop_discovery, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Počisti", command=self.clear_results).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Shrani rezultate", command=self.save_results).pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Pripravljen")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="blue")
        status_label.grid(row=2, column=0, columnspan=3, sticky=tk.W, padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Rezultati", padding="10")
        results_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Treeview for cameras
        columns = ("IP Naslov", "Port", "Status", "Čas odkrivanja")
        self.tree = ttk.Treeview(results_frame, columns=columns, height=10)
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("IP Naslov", anchor=tk.W, width=150)
        self.tree.column("Port", anchor=tk.W, width=80)
        self.tree.column("Status", anchor=tk.W, width=100)
        self.tree.column("Čas odkrivanja", anchor=tk.W, width=200)
        
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("IP Naslov", text="IP Naslov", anchor=tk.W)
        self.tree.heading("Port", text="Port", anchor=tk.W)
        self.tree.heading("Status", text="Status", anchor=tk.W)
        self.tree.heading("Čas odkrivanja", text="Čas odkrivanja", anchor=tk.W)
        
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Log frame
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(main_frame, text="Statistika", padding="10")
        stats_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        stats_frame.columnconfigure(0, weight=1)
        
        self.stats_var = tk.StringVar(value="Найдено камер: 0")
        stats_label = ttk.Label(stats_frame, textvariable=self.stats_var, font=("Arial", 10))
        stats_label.pack(side=tk.LEFT)
    
    def log_message(self, message):
        """Log message to log text widget"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def start_discovery(self):
        """Start discovery in separate thread"""
        if self.discovering:
            messagebox.showwarning("Opozorilo", "Odkrivanje je že v teku")
            return
        
        try:
            timeout = int(self.timeout_var.get())
            if timeout < 1 or timeout > 60:
                raise ValueError("Timeout mora biti med 1 in 60 sekundami")
        except ValueError as e:
            messagebox.showerror("Napaka", f"Neveljaven timeout: {e}")
            return
        
        self.discovering = True
        self.discover_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.cameras = []
        self.tree.delete(*self.tree.get_children())
        
        self.status_var.set("Odkrivanje v teku...")
        self.log_message("Začeti odkrivanje DAHUA kamer...")
        
        self.discovery_thread = threading.Thread(target=self.discovery_worker, daemon=True)
        self.discovery_thread.start()
    
    def stop_discovery(self):
        """Stop discovery"""
        self.discovering = False
        self.status_var.set("Ustavljanje...")
        self.log_message("Ustavljanje odkrivanja...")
    
    def discovery_worker(self):
        """Discovery worker thread"""
        try:
            broadcast_addr = self.broadcast_var.get()
            timeout = int(self.timeout_var.get())
            
            # Validate broadcast address
            try:
                ipaddress.ip_address(broadcast_addr)
            except ValueError:
                self.log_message(f"[-] Neveljaven IP naslov: {broadcast_addr}")
                self.discovering = False
                self.discover_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
                self.status_var.set("Napaka - neveljaven IP naslov")
                return
            
            self.log_message(f"[*] Pošljem odkrivne pakete na {broadcast_addr}:{self.DAHUA_PORT}")
            
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('0.0.0.0', self.DAHUA_PORT))
            
            # Send discovery packet
            discovery_packet = self.DAHUA_HEADER + bytes(16)
            sock.sendto(discovery_packet, (broadcast_addr, self.DAHUA_PORT))
            
            # Receive responses
            sock.settimeout(timeout)
            start_time = time.time()
            
            self.log_message(f"[*] Čakam na odgovore ({timeout} sekund)...")
            
            while self.discovering and (time.time() - start_time) < timeout:
                try:
                    data, addr = sock.recvfrom(1024)
                    
                    if len(data) > 4 and data[:4] == self.DAHUA_HEADER:
                        camera_info = {
                            'ip': addr[0],
                            'port': self.DAHUA_PORT,
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'status': 'Aktivna'
                        }
                        
                        self.cameras.append(camera_info)
                        self.log_message(f"[+] Najdena kamera: {addr[0]}")
                        
                        # Update tree
                        self.tree.insert("", tk.END, values=(
                            camera_info['ip'],
                            camera_info['port'],
                            camera_info['status'],
                            camera_info['timestamp']
                        ))
                        
                        # Update statistics
                        self.stats_var.set(f"Найдено камер: {len(self.cameras)}")
                
                except socket.timeout:
                    continue
                except Exception as e:
                    self.log_message(f"[-] Napaka: {e}")
            
            sock.close()
            
            self.log_message(f"[+] Odkrivanje zaključeno. Найдено {len(self.cameras)} kamer(e)")
            self.status_var.set(f"Zaključeno - Найдено {len(self.cameras)} kamer(e)")
            
        except Exception as e:
            self.log_message(f"[-] Napaka pri odkrivanju: {e}")
            self.status_var.set(f"Napaka: {e}")
        
        finally:
            self.discovering = False
            self.discover_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
    
    def clear_results(self):
        """Clear results"""
        self.tree.delete(*self.tree.get_children())
        self.log_text.delete(1.0, tk.END)
        self.cameras = []
        self.stats_var.set("Найдено камер: 0")
        self.status_var.set("Rezultati očiščeni")
    
    def save_results(self):
        """Save results to JSON file"""
        if not self.cameras:
            messagebox.showwarning("Opozorilo", "Ni rezultatov za shranjevanje")
            return
        
        try:
            filename = f"dahua_cameras_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.cameras, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Uspešno", f"Rezultati shranjeni v {filename}")
            self.log_message(f"[+] Rezultati shranjeni v {filename}")
        except Exception as e:
            messagebox.showerror("Napaka", f"Napaka pri shranjevanju: {e}")
            self.log_message(f"[-] Napaka pri shranjevanju: {e}")


def main():
    """Main function"""
    root = tk.Tk()
    app = DAHUADiscoveryGUI(root)
    root.mainloop()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Napaka: {e}")
