import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import socket
import os
import pandas as pd
import json

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Inventarios")
        self.inventory_file = "inventory_data.json"

        # Datos del inventario
        self.inventory = []
        self.load_inventory()

        # Configuración de la interfaz
        self.setup_ui()

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

        # Botones para importar, exportar y enviar
        frame_actions = ttk.Frame(self.root)
        frame_actions.grid(row=2, column=0, pady=10)

        ttk.Button(frame_actions, text="Importar desde Excel", command=self.import_from_excel, bootstyle=PRIMARY).grid(row=0, column=0, padx=5)
        ttk.Button(frame_actions, text="Importar desde JSON", command=self.import_from_json, bootstyle=PRIMARY).grid(row=0, column=1, padx=5)
        ttk.Button(frame_actions, text="Exportar a Excel", command=self.export_to_excel, bootstyle=PRIMARY).grid(row=0, column=2, padx=5)
        ttk.Button(frame_actions, text="Exportar a JSON", command=self.export_to_json, bootstyle=PRIMARY).grid(row=0, column=3, padx=5)
        ttk.Button(frame_actions, text="Enviar por Red", command=self.send_inventory, bootstyle=WARNING).grid(row=0, column=4, padx=5)

    def add_product(self):
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()

        if not name or not quantity or not price:
            ttk.Messagebox.show_error("Todos los campos son obligatorios", title="Error")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            ttk.Messagebox.show_error("Cantidad debe ser un número entero y Precio un número decimal", title="Error")
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
                ttk.Messagebox.show_info("Inventario enviado correctamente", title="Éxito")
        except Exception as e:
            ttk.Messagebox.show_error(f"Error al enviar el inventario: {e}", title="Error")

    def export_to_excel(self):
        if not self.inventory:
            ttk.Messagebox.show_error("El inventario está vacío", title="Error")
            return

        file_path = ttk.filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos Excel", "*.xlsx")])
        if not file_path:
            return

        df = pd.DataFrame(self.inventory)
        df.to_excel(file_path, index=False)
        ttk.Messagebox.show_info("Inventario exportado a Excel correctamente", title="Éxito")

    def export_to_json(self):
        if not self.inventory:
            ttk.Messagebox.show_error("El inventario está vacío", title="Error")
            return

        file_path = ttk.filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivos JSON", "*.json")])
        if not file_path:
            return

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.inventory, f, ensure_ascii=False, indent=4)
        ttk.Messagebox.show_info("Inventario exportado a JSON correctamente", title="Éxito")

    def import_from_excel(self):
        file_path = ttk.filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
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
            ttk.Messagebox.show_info("Inventario importado desde Excel correctamente", title="Éxito")
        except Exception as e:
            ttk.Messagebox.show_error(f"No se pudo importar el archivo: {e}", title="Error")

    def import_from_json(self):
        file_path = ttk.filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for product in data:
                    self.inventory.append(product)
                    self.tree.insert("", "end", values=(product["Nombre"], product["Cantidad"], product["Precio"]))
            ttk.Messagebox.show_info("Inventario importado desde JSON correctamente", title="Éxito")
        except Exception as e:
            ttk.Messagebox.show_error(f"No se pudo importar el archivo: {e}", title="Error")

if __name__ == "__main__":
    app = ttk.Window(themename="darkly")
    InventoryApp(app)
    app.mainloop()