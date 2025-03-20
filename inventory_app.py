import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import socket
import os
import pandas as pd
import json
import tkinter as tk
from tkinter import messagebox, filedialog
import hashlib

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Inventarios")
        self.inventory_file = "inventory_data.json"
        self.users = {"admin": self.hash_password("admin123"), "user": self.hash_password("user123")}

        # Datos del inventario
        self.inventory = []
        self.load_inventory()

        # Pantalla de inicio de sesión
        self.show_login_screen()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def show_login_screen(self):
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(self.login_frame, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_user = ttk.Entry(self.login_frame, bootstyle=INFO)
        self.entry_user.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.login_frame, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_password = ttk.Entry(self.login_frame, show="*", bootstyle=INFO)
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.login_frame, text="Iniciar Sesión", command=self.authenticate_user, bootstyle=SUCCESS).grid(row=2, column=0, columnspan=2, pady=10)

    def authenticate_user(self):
        username = self.entry_user.get()
        password = self.entry_password.get()
        hashed_password = self.hash_password(password)

        if username in self.users and self.users[username] == hashed_password:
            self.login_frame.destroy()
            self.setup_ui()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def setup_ui(self):
        # Frame para agregar productos
        frame_add = ttk.LabelFrame(self.root, text="Agregar Producto", bootstyle=PRIMARY)
        frame_add.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(frame_add, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = ttk.Entry(frame_add, bootstyle=INFO)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_add, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_quantity = ttk.Entry(frame_add, bootstyle=INFO)
        self.entry_quantity.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_add, text="Precio:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_price = ttk.Entry(frame_add, bootstyle=INFO)
        self.entry_price.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame_add, text="Agregar", command=self.add_product, bootstyle=SUCCESS).grid(row=3, column=0, columnspan=2, pady=10)

        # Tabla para mostrar el inventario
        self.tree = ttk.Treeview(self.root, columns=("Nombre", "Cantidad", "Precio"), show="headings", bootstyle=INFO)
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.grid(row=1, column=0, padx=10, pady=10)

        # Botones para importar, exportar, enviar y recibir
        frame_actions = ttk.Frame(self.root)
        frame_actions.grid(row=2, column=0, pady=10)

        ttk.Button(frame_actions, text="Importar desde Excel", command=self.import_from_excel, bootstyle=PRIMARY).grid(row=0, column=0, padx=5)
        ttk.Button(frame_actions, text="Importar desde JSON", command=self.import_from_json, bootstyle=PRIMARY).grid(row=0, column=1, padx=5)
        ttk.Button(frame_actions, text="Exportar a Excel", command=self.export_to_excel, bootstyle=PRIMARY).grid(row=0, column=2, padx=5)
        ttk.Button(frame_actions, text="Exportar a JSON", command=self.export_to_json, bootstyle=PRIMARY).grid(row=0, column=3, padx=5)
        ttk.Button(frame_actions, text="Enviar por Red", command=self.send_inventory, bootstyle=WARNING).grid(row=0, column=4, padx=5)
        ttk.Button(frame_actions, text="Recibir por Red", command=self.receive_inventory, bootstyle=WARNING).grid(row=0, column=5, padx=5)

    def add_product(self):
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()

        if not name or not quantity or not price:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número entero y Precio un número decimal")
            return

        self.inventory.append({"Nombre": name, "Cantidad": quantity, "Precio": price})
        self.tree.insert("", "end", values=(name, quantity, price))
        self.save_inventory()

        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)

    def save_inventory(self):
        with open(self.inventory_file, "w", encoding="utf-8") as f:
            json.dump(self.inventory, f, ensure_ascii=False, indent=4)

    def load_inventory(self):
        if os.path.exists(self.inventory_file):
            with open(self.inventory_file, "r", encoding="utf-8") as f:
                self.inventory = json.load(f)

    def send_inventory(self):
        host = "<IP_DESTINO>"  # Cambiar por la IP del destinatario
        port = 12345

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                data = json.dumps(self.inventory).encode("utf-8")
                s.sendall(data)
                messagebox.showinfo("Éxito", "Inventario enviado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al enviar el inventario: {e}")

    def receive_inventory(self):
        host = "0.0.0.0"  # Escuchar en todas las interfaces de red
        port = 12345

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, port))
                s.listen(1)
                messagebox.showinfo("Esperando conexión", f"Esperando conexión en el puerto {port}...")
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024 * 1024)  # Recibir hasta 1 MB de datos
                    received_inventory = json.loads(data.decode("utf-8"))
                    for product in received_inventory:
                        self.inventory.append(product)
                        self.tree.insert("", "end", values=(product["Nombre"], product["Cantidad"], product["Precio"]))
                    self.save_inventory()
                    messagebox.showinfo("Éxito", "Inventario recibido correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al recibir el inventario: {e}")

    def export_to_excel(self):
        if not self.inventory:
            messagebox.showerror("Error", "El inventario está vacío")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos Excel", "*.xlsx")])
        if not file_path:
            return

        df = pd.DataFrame(self.inventory)
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Éxito", "Inventario exportado a Excel correctamente")

    def export_to_json(self):
        if not self.inventory:
            messagebox.showerror("Error", "El inventario está vacío")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivos JSON", "*.json")])
        if not file_path:
            return

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.inventory, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Éxito", "Inventario exportado a JSON correctamente")

    def import_from_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)
            for _, row in df.iterrows():
                product = {
                    "Nombre": row["Nombre"],
                    "Cantidad": int(row["Cantidad"]),
                    "Precio": float(row["Precio"])
                }
                self.inventory.append(product)
                self.tree.insert("", "end", values=(product["Nombre"], product["Cantidad"], product["Precio"]))
            messagebox.showinfo("Éxito", "Inventario importado desde Excel correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo importar el archivo: {e}")

    def import_from_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for product in data:
                    self.inventory.append(product)
                    self.tree.insert("", "end", values=(product["Nombre"], product["Cantidad"], product["Precio"]))
            messagebox.showinfo("Éxito", "Inventario importado desde JSON correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo importar el archivo: {e}")

if __name__ == "__main__":
    app = ttk.Window(themename="darkly")
    InventoryApp(app)
    app.mainloop()