import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import socket
import os
import pandas as pd
import json
import tkinter as tk
from tkinter import messagebox, filedialog, PhotoImage
import hashlib

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Inventarios")
        self.inventory_file = "inventory_data.json"
        self.users_file = "users.json"
        self.load_users()

        # Datos del inventario
        self.inventory = []
        self.load_inventory()

        # Pantalla de inicio de sesión
        self.show_login_screen()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, "r", encoding="utf-8") as f:
                raw_users = json.load(f)
                self.users = {}
                for username, data in raw_users.items():
                    if isinstance(data, str):
                        # Convertir formato antiguo a nuevo
                        self.users[username] = {"password": data, "profile_image": ""}
                    else:
                        self.users[username] = data
        else:
            self.users = {
                "admin": {"password": self.hash_password("admin"), "profile_image": ""},
                "user": {"password": self.hash_password("user123"), "profile_image": ""}
            }
            self.save_users()

    def save_users(self):
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False, indent=4)

    def show_login_screen(self):
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(self.login_frame, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_user = ttk.Entry(self.login_frame, bootstyle=INFO)
        self.entry_user.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.login_frame, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_password = ttk.Entry(self.login_frame, show="*", bootstyle=INFO)
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.login_frame, text="Iniciar Sesión", command=self.authenticate_user, bootstyle=SUCCESS).grid(row=2, column=0, pady=10)
        ttk.Button(self.login_frame, text="Registrarse", command=self.show_register_screen, bootstyle=PRIMARY).grid(row=2, column=1, pady=10)

    def show_register_screen(self):
        self.login_frame.destroy()
        self.register_frame = ttk.Frame(self.root)
        self.register_frame.grid(row=0, column=0, padx=10, pady=10)

        ttk.Label(self.register_frame, text="Nuevo Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_new_user = ttk.Entry(self.register_frame, bootstyle=INFO)
        self.entry_new_user.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.register_frame, text="Nueva Contraseña:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_new_password = ttk.Entry(self.register_frame, show="*", bootstyle=INFO)
        self.entry_new_password.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.register_frame, text="Imagen de Perfil:").grid(row=2, column=0, padx=5, pady=5)
        self.profile_image_path = tk.StringVar()
        ttk.Entry(self.register_frame, textvariable=self.profile_image_path, bootstyle=INFO).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(self.register_frame, text="Seleccionar", command=self.select_profile_image, bootstyle=PRIMARY).grid(row=2, column=2, padx=5, pady=5)

        ttk.Button(self.register_frame, text="Registrar", command=self.register_user, bootstyle=SUCCESS).grid(row=3, column=0, pady=10)
        ttk.Button(self.register_frame, text="Volver", command=self.back_to_login, bootstyle=PRIMARY).grid(row=3, column=1, pady=10)

    def select_profile_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.profile_image_path.set(file_path)

    def register_user(self):
        new_user = self.entry_new_user.get()
        new_password = self.entry_new_password.get()
        profile_image = self.profile_image_path.get()

        if not new_user or not new_password:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if new_user in self.users:
            messagebox.showerror("Error", "El usuario ya existe")
            return

        self.users[new_user] = {
            "password": self.hash_password(new_password),
            "profile_image": profile_image
        }
        self.save_users()
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        self.back_to_login()

    def back_to_login(self):
        self.register_frame.destroy()
        self.show_login_screen()

    def authenticate_user(self):
        username = self.entry_user.get()
        password = self.entry_password.get()
        hashed_password = self.hash_password(password)

        if username in self.users and self.users[username]["password"] == hashed_password:
            self.current_user = username
            self.current_user_image = self.users[username]["profile_image"]
            self.login_frame.destroy()
            self.show_profile_image()
            self.setup_ui()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def show_profile_image(self):
        if self.current_user_image:
            try:
                img = PhotoImage(file=self.current_user_image)
                self.profile_image_label = ttk.Label(self.root, image=img)
                self.profile_image_label.image = img  # Guardar referencia para evitar que se recolecte como basura
                self.profile_image_label.grid(row=0, column=1, padx=10, pady=10)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar la imagen de perfil: {e}")

    def setup_ui(self):
        # Frame para agregar productos
        frame_add = ttk.LabelFrame(self.root, text="Agregar Producto", bootstyle=PRIMARY)
        frame_add.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(frame_add, text="ID:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_id = ttk.Entry(frame_add, bootstyle=INFO)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_add, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_name = ttk.Entry(frame_add, bootstyle=INFO)
        self.entry_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_add, text="Cantidad:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_quantity = ttk.Entry(frame_add, bootstyle=INFO)
        self.entry_quantity.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_add, text="Precio:").grid(row=3, column=0, padx=5, pady=5)
        self.entry_price = ttk.Entry(frame_add, bootstyle=INFO)
        self.entry_price.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(frame_add, text="Agregar", command=self.add_product, bootstyle=SUCCESS).grid(row=4, column=0, columnspan=2, pady=10)

        # Barra de búsqueda
        frame_search = ttk.LabelFrame(self.root, text="Buscar Producto", bootstyle=PRIMARY)
        frame_search.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(frame_search, text="Buscar por ID o Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_search = ttk.Entry(frame_search, bootstyle=INFO)
        self.entry_search.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_search, text="Buscar", command=self.search_product, bootstyle=SUCCESS).grid(row=0, column=2, padx=5, pady=5)

        # Tabla para mostrar el inventario
        self.tree = ttk.Treeview(self.root, columns=("ID", "Nombre", "Cantidad", "Precio"), show="headings", bootstyle=INFO)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.grid(row=2, column=0, padx=10, pady=10)

        # Botones para importar, exportar, enviar, recibir, chatear y cambiar contraseña
        frame_actions = ttk.Frame(self.root)
        frame_actions.grid(row=3, column=0, pady=10)

        ttk.Button(frame_actions, text="Importar desde Excel", command=self.import_from_excel, bootstyle=PRIMARY).grid(row=0, column=0, padx=5)
        ttk.Button(frame_actions, text="Importar desde JSON", command=self.import_from_json, bootstyle=PRIMARY).grid(row=0, column=1, padx=5)
        ttk.Button(frame_actions, text="Exportar a Excel", command=self.export_to_excel, bootstyle=PRIMARY).grid(row=0, column=2, padx=5)
        ttk.Button(frame_actions, text="Exportar a JSON", command=self.export_to_json, bootstyle=PRIMARY).grid(row=0, column=3, padx=5)
        ttk.Button(frame_actions, text="Enviar por Red", command=self.send_inventory, bootstyle=WARNING).grid(row=0, column=4, padx=5)
        ttk.Button(frame_actions, text="Recibir por Red", command=self.receive_inventory, bootstyle=WARNING).grid(row=0, column=5, padx=5)
        ttk.Button(frame_actions, text="Chatear", command=self.open_chat_window, bootstyle=INFO).grid(row=0, column=6, padx=5)
        ttk.Button(frame_actions, text="Cambiar Contraseña", command=self.show_change_password_screen, bootstyle=INFO).grid(row=0, column=7, padx=5)
        ttk.Button(frame_actions, text="Eliminar Seleccionados", command=self.delete_selected_products, bootstyle=DANGER).grid(row=0, column=8, padx=5)

        if self.current_user == "admin":
            ttk.Button(frame_actions, text="Borrar Usuario", command=self.show_delete_user_screen, bootstyle=DANGER).grid(row=0, column=9, padx=5)

    def show_delete_user_screen(self):
        self.delete_user_frame = ttk.Toplevel(self.root)
        self.delete_user_frame.title("Borrar Usuario")

        ttk.Label(self.delete_user_frame, text="Usuario a borrar:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_delete_user = ttk.Entry(self.delete_user_frame, bootstyle=INFO)
        self.entry_delete_user.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.delete_user_frame, text="Borrar", command=self.delete_user, bootstyle=DANGER).grid(row=1, column=0, columnspan=2, pady=10)

    def delete_user(self):
        user_to_delete = self.entry_delete_user.get()

        if user_to_delete == "admin":
            messagebox.showerror("Error", "No se puede borrar el usuario admin")
            return

        if user_to_delete in self.users:
            del self.users[user_to_delete]
            self.save_users()
            messagebox.showinfo("Éxito", f"Usuario '{user_to_delete}' borrado correctamente")
            self.delete_user_frame.destroy()
        else:
            messagebox.showerror("Error", "El usuario no existe")

    def open_chat_window(self):
        self.chat_window = tk.Toplevel(self.root)
        self.chat_window.title("Chat")

        self.chat_display = tk.Text(self.chat_window, state="disabled", width=50, height=20)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.chat_entry = ttk.Entry(self.chat_window, width=40)
        self.chat_entry.grid(row=1, column=0, padx=10, pady=10)

        ttk.Button(self.chat_window, text="Enviar", command=self.send_message, bootstyle=SUCCESS).grid(row=1, column=1, padx=10, pady=10)

        self.start_chat_server()

    def start_chat_server(self):
        def server_thread():
            self.chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.chat_socket.bind(("0.0.0.0", 12346))
            self.chat_socket.listen(1)
            self.chat_connection, _ = self.chat_socket.accept()
            self.receive_messages()

        import threading
        threading.Thread(target=server_thread, daemon=True).start()

    def send_message(self):
        if not hasattr(self, 'chat_connection') or self.chat_connection is None:
            messagebox.showerror("Error", "No hay conexión activa para enviar mensajes.")
            return

        message = self.chat_entry.get()
        if message:
            self.chat_connection.sendall(message.encode("utf-8"))
            self.display_message(f"Tú: {message}")
            self.chat_entry.delete(0, tk.END)

    def receive_messages(self):
        def listen_for_messages():
            while True:
                try:
                    message = self.chat_connection.recv(1024).decode("utf-8")
                    if message:
                        self.display_message(f"Otro: {message}")
                except Exception as e:
                    break

        import threading
        threading.Thread(target=listen_for_messages, daemon=True).start()

    def display_message(self, message):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state="disabled")

    def add_product(self):
        product_id = self.entry_id.get()
        name = self.entry_name.get()
        quantity = self.entry_quantity.get()
        price = self.entry_price.get()

        if not product_id or not name or not quantity or not price:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            quantity = int(quantity)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número entero y Precio un número decimal")
            return

        self.inventory.append({"ID": product_id, "Nombre": name, "Cantidad": quantity, "Precio": price})
        self.tree.insert("", "end", values=(product_id, name, quantity, price))
        self.save_inventory()

        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)

    def search_product(self):
        query = self.entry_search.get().strip().lower()

        # Limpiar la tabla antes de mostrar los resultados
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Filtrar productos por ID o Nombre
        for product in self.inventory:
            product_id = product.get("ID", "").lower()
            product_name = product.get("Nombre", "").lower()
            if query in product_id or query in product_name:
                self.tree.insert("", "end", values=(product.get("ID", ""), product.get("Nombre", ""), product.get("Cantidad", 0), product.get("Precio", 0.0)))

        # Mostrar mensaje si no se encuentran resultados
        if not self.tree.get_children():
            messagebox.showinfo("Sin resultados", "No se encontraron productos que coincidan con la búsqueda.")

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
                        self.tree.insert("", "end", values=(product["ID"], product["Nombre"], product["Cantidad"], product["Precio"]))
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
                    "ID": row["ID"],
                    "Nombre": row["Nombre"],
                    "Cantidad": int(row["Cantidad"]),
                    "Precio": float(row["Precio"])
                }
                self.inventory.append(product)
                self.tree.insert("", "end", values=(product["ID"], product["Nombre"], product["Cantidad"], product["Precio"]))
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
                    self.tree.insert("", "end", values=(product["ID"], product["Nombre"], product["Cantidad"], product["Precio"]))
            messagebox.showinfo("Éxito", "Inventario importado desde JSON correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo importar el archivo: {e}")

    def show_change_password_screen(self):
        self.change_password_frame = ttk.Toplevel(self.root)
        self.change_password_frame.title("Cambiar Contraseña")

        ttk.Label(self.change_password_frame, text="Contraseña Actual:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_current_password = ttk.Entry(self.change_password_frame, show="*", bootstyle=INFO)
        self.entry_current_password.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.change_password_frame, text="Nueva Contraseña:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_new_password = ttk.Entry(self.change_password_frame, show="*", bootstyle=INFO)
        self.entry_new_password.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.change_password_frame, text="Confirmar Contraseña:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_confirm_password = ttk.Entry(self.change_password_frame, show="*", bootstyle=INFO)
        self.entry_confirm_password.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.change_password_frame, text="Cambiar", command=self.change_password, bootstyle=SUCCESS).grid(row=3, column=0, columnspan=2, pady=10)

    def change_password(self):
        current_password = self.entry_current_password.get()
        new_password = self.entry_new_password.get()
        confirm_password = self.entry_confirm_password.get()

        if not current_password or not new_password or not confirm_password:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if self.hash_password(current_password) != self.users[self.current_user]["password"]:
            messagebox.showerror("Error", "La contraseña actual es incorrecta")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return

        self.users[self.current_user]["password"] = self.hash_password(new_password)
        self.save_users()
        messagebox.showinfo("Éxito", "Contraseña cambiada correctamente")
        self.change_password_frame.destroy()

    def delete_selected_products(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Error", "No hay elementos seleccionados para eliminar.")
            return

        for item in selected_items:
            values = self.tree.item(item, "values")
            self.inventory = [product for product in self.inventory if product.get("ID") != values[0]]
            self.tree.delete(item)

        self.save_inventory()
        messagebox.showinfo("Éxito", "Elementos seleccionados eliminados correctamente.")

if __name__ == "__main__":
    app = ttk.Window(themename="darkly")
    InventoryApp(app)
    app.mainloop()