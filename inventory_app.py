import ttkbootstrap as ttk
# Explicitly import necessary constants instead of using *
from ttkbootstrap.constants import INFO, PRIMARY, SUCCESS, WARNING, DANGER
# Import Style for customization
from ttkbootstrap import Style
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
        self.root.title("🌸 Sistema de Gestión de Inventarios Kawaii 🌸") # Cute title
        self.inventory_file = "inventory_data.json"
        self.users_file = "users.json"
        # Ensure load_users is called *after* users_file is defined
        self.load_users()

        # Datos del inventario
        self.inventory = []
        self.load_inventory() # Ensure this is also defined

        # --- Style Customizations ---
        style = Style()
        # Try a cute, rounded font (if available on the system)
        try:
            # Increase font size slightly for better readability and cuter look
            style.configure('.', font=('Segoe Print', 12))
        except tk.TclError:
            print("Segoe Print font not found, using default.")
            try:
                style.configure('.', font=('Comic Sans MS', 12)) # Fallback font
            except tk.TclError:
                 print("Comic Sans MS font not found, using default system font.")
                 style.configure('.', font=('TkDefaultFont', 11)) # Generic fallback

        # Configure pastel colors (using hex codes)
        PASTEL_PINK = "#FFDFD3"  # Lighter pink
        LIGHT_LAVENDER = "#F2E6FF" # Very light lavender
        PALE_MINT = "#E0FFF0"    # Pale mint green

        # Apply a light lavender background to frames for a soft look
        style.configure('TFrame', background=LIGHT_LAVENDER)
        style.configure('TLabel', background=LIGHT_LAVENDER) # Match label background
        style.configure('TButton', font=('Segoe Print', 11, 'bold')) # Make buttons slightly bolder
        style.configure('Treeview.Heading', font=('Segoe Print', 12, 'bold')) # Style Treeview headings

        # Customize LabelFrame look
        style.configure('TLabelframe', background=LIGHT_LAVENDER, bordercolor=PASTEL_PINK, relief="raised")
        style.configure('TLabelframe.Label', background=PASTEL_PINK, foreground="#5C5C5C", font=('Segoe Print', 11, 'italic')) # Label part of the LabelFrame

        # Customize Entry widgets slightly
        style.configure('TEntry', fieldbackground=PALE_MINT, foreground="#333333")

        # --- End Style Customizations ---


        # Pantalla de inicio de sesión
        self.show_login_screen()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # --- Re-inserting load_users method ---
    def load_users(self):
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, "r", encoding="utf-8") as f:
                    raw_users = json.load(f)
                    self.users = {}
                    for username, data in raw_users.items():
                        if isinstance(data, str): # Handle old format
                            self.users[username] = {"password": data, "profile_image": ""}
                        elif isinstance(data, dict) and "password" in data: # Handle new format
                             self.users[username] = data
                        else:
                             print(f"Skipping invalid user data for {username}") # Log invalid entries
                # Ensure default admin exists if file is empty or corrupted after load
                if "admin" not in self.users:
                     print("Admin user not found after loading, creating default.")
                     self.users["admin"] = {"password": self.hash_password("admin"), "profile_image": ""}
                     self.save_users() # Save if we added admin

            except json.JSONDecodeError:
                print(f"Error decoding JSON from {self.users_file}. Initializing with default admin.")
                self.users = {"admin": {"password": self.hash_password("admin"), "profile_image": ""}}
                self.save_users()
            except Exception as e:
                 print(f"An error occurred loading users: {e}. Initializing with default admin.")
                 self.users = {"admin": {"password": self.hash_password("admin"), "profile_image": ""}}
                 self.save_users()

        else:
            print(f"{self.users_file} not found. Creating default users.")
            self.users = {
                "admin": {"password": self.hash_password("admin"), "profile_image": ""},
                # Add back default user if desired
                # "user": {"password": self.hash_password("user123"), "profile_image": ""}
            }
            self.save_users()
    # --- End re-inserting load_users method ---


    def save_users(self):
        try:
            with open(self.users_file, "w", encoding="utf-8") as f:
                json.dump(self.users, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving users to {self.users_file}: {e}")
            # Avoid showing messagebox here if it causes issues during init
            # messagebox.showerror("Error Guardando Usuarios", f"No se pudo guardar el archivo de usuarios: {e}")


    # --- Make sure load_inventory is also defined ---
    def load_inventory(self):
        if os.path.exists(self.inventory_file):
            try:
                with open(self.inventory_file, "r", encoding="utf-8") as f:
                    self.inventory = json.load(f)
                    # Basic validation: ensure it's a list
                    if not isinstance(self.inventory, list):
                        print(f"Inventory data in {self.inventory_file} is not a list. Initializing empty inventory.")
                        self.inventory = []
                        self.save_inventory() # Optionally overwrite corrupted file
            except json.JSONDecodeError:
                 print(f"Error decoding JSON from {self.inventory_file}. Initializing empty inventory.")
                 self.inventory = []
            except Exception as e:
                 print(f"An error occurred loading inventory: {e}. Initializing empty inventory.")
                 self.inventory = []
        else:
             print(f"{self.inventory_file} not found. Starting with empty inventory.")
             self.inventory = []
    # --- End load_inventory definition ---

    # ... (rest of the InventoryApp class methods like show_login_screen, setup_ui etc.) ...
    # Ensure all methods previously defined are still present and correctly indented
    # ...existing code...

    def show_login_screen(self):
        # Ensure the frame uses the new style
        self.login_frame = ttk.Frame(self.root, padding=(20, 10), style='TFrame')
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
        # Check if login_frame exists before destroying
        if hasattr(self, 'login_frame') and self.login_frame.winfo_exists():
            self.login_frame.destroy()
         # Ensure the frame uses the new style
        self.register_frame = ttk.Frame(self.root, padding=(20, 10), style='TFrame')
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
        file_path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif")]) # Added gif
        if file_path:
            self.profile_image_path.set(file_path)

    def register_user(self):
        new_user = self.entry_new_user.get()
        new_password = self.entry_new_password.get()
        profile_image = self.profile_image_path.get()

        if not new_user or not new_password:
            messagebox.showerror("Error", "Usuario y contraseña son obligatorios")
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
         # Check if register_frame exists before destroying
        if hasattr(self, 'register_frame') and self.register_frame.winfo_exists():
            self.register_frame.destroy()
        self.show_login_screen()

    def authenticate_user(self):
        username = self.entry_user.get()
        password = self.entry_password.get()
        hashed_password = self.hash_password(password)

        if username in self.users and self.users[username]["password"] == hashed_password:
            self.current_user = username
            self.current_user_image = self.users[username].get("profile_image", "") # Use .get for safety
            if hasattr(self, 'login_frame') and self.login_frame.winfo_exists():
                self.login_frame.destroy()
            # setup_ui now handles placing the profile image frame
            self.setup_ui()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def setup_ui(self):
        # Clear previous UI elements if they exist
        for widget in self.root.winfo_children():
             # Keep the main window, destroy frames if they exist from previous logins/screens
            if isinstance(widget, (ttk.Frame, ttk.LabelFrame)) and widget not in [self.profile_frame]: # Avoid destroying profile frame here
                 widget.destroy()

        # Recreate profile frame (or ensure it exists)
        if not hasattr(self, 'profile_frame') or not self.profile_frame.winfo_exists():
             self.profile_frame = ttk.Frame(self.root, style='TFrame')
        self.profile_frame.grid(row=0, column=0, pady=10, padx=10, sticky='ne') # Top right corner

        # Configure main frames with padding and style
        main_frame = ttk.Frame(self.root, padding=(10, 10), style='TFrame')
        main_frame.grid(row=1, column=0, sticky='nsew') # Changed grid row for profile image
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)


        # Frame para agregar productos
        frame_add = ttk.LabelFrame(main_frame, text="💖 Agregar Producto 💖", style='TLabelframe')
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
        frame_search = ttk.LabelFrame(main_frame, text="🔍 Buscar Producto 🔍", style='TLabelframe')
        frame_search.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(frame_search, text="Buscar por ID o Nombre:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_search = ttk.Entry(frame_search, bootstyle=INFO)
        self.entry_search.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(frame_search, text="Buscar", command=self.search_product, bootstyle=SUCCESS).grid(row=0, column=2, padx=5, pady=5)

        # Tabla para mostrar el inventario
        tree_frame = ttk.Frame(main_frame, style='TFrame') # Frame to hold treeview and scrollbar
        tree_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')
        main_frame.grid_rowconfigure(2, weight=1) # Allow treeview frame to expand
        main_frame.grid_columnconfigure(0, weight=1) # Allow treeview frame to expand

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Nombre", "Cantidad", "Precio"), show="headings", bootstyle=INFO)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Precio", text="Precio")
        self.tree.grid(row=0, column=0, sticky='nsew') # Grid within tree_frame
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Add scrollbar to Treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns')

        # Populate treeview after setting it up
        self.populate_treeview()


        # Botones para acciones
        frame_actions = ttk.Frame(main_frame, style='TFrame')
        frame_actions.grid(row=3, column=0, pady=10, sticky="ew")
        # Center buttons in the actions frame - adjust column weights as needed
        num_buttons_row1 = 5
        num_buttons_row2 = 4 if self.current_user != "admin" else 5
        for i in range(max(num_buttons_row1, num_buttons_row2)):
             frame_actions.grid_columnconfigure(i, weight=1)


        # Arrange buttons in two rows for better spacing if many buttons
        ttk.Button(frame_actions, text="📥 Importar Excel", command=self.import_from_excel, bootstyle=PRIMARY).grid(row=0, column=0, padx=5, pady=3, sticky='ew')
        ttk.Button(frame_actions, text="📥 Importar JSON", command=self.import_from_json, bootstyle=PRIMARY).grid(row=0, column=1, padx=5, pady=3, sticky='ew')
        ttk.Button(frame_actions, text="📤 Exportar Excel", command=self.export_to_excel, bootstyle=PRIMARY).grid(row=0, column=2, padx=5, pady=3, sticky='ew')
        ttk.Button(frame_actions, text="📤 Exportar JSON", command=self.export_to_json, bootstyle=PRIMARY).grid(row=0, column=3, padx=5, pady=3, sticky='ew')
        ttk.Button(frame_actions, text="💬 Chatear", command=self.open_chat_window, bootstyle=INFO).grid(row=0, column=4, padx=5, pady=3, sticky='ew') # Moved chat earlier

        ttk.Button(frame_actions, text="🔑 Cambiar Contraseña", command=self.show_change_password_screen, bootstyle=INFO).grid(row=1, column=0, padx=5, pady=3, sticky='ew')
        ttk.Button(frame_actions, text="🗑️ Eliminar Seleccionados", command=self.delete_selected_products, bootstyle=DANGER).grid(row=1, column=1, padx=5, pady=3, sticky='ew')
        # Network buttons might be less common, place them together
        ttk.Button(frame_actions, text="📡 Enviar por Red", command=self.send_inventory, bootstyle=WARNING).grid(row=1, column=2, padx=5, pady=3, sticky='ew')
        ttk.Button(frame_actions, text="🛰️ Recibir por Red", command=self.receive_inventory, bootstyle=WARNING).grid(row=1, column=3, padx=5, pady=3, sticky='ew')


        if self.current_user == "admin":
            ttk.Button(frame_actions, text="👤 Borrar Usuario", command=self.show_delete_user_screen, bootstyle=DANGER).grid(row=1, column=4, padx=5, pady=3, sticky='ew') # Place admin button last

        # Call show_profile_image to place it in the dedicated frame
        self.show_profile_image()

    def populate_treeview(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert items from inventory
        for product in self.inventory:
             # Use .get with defaults for safety
            pid = product.get("ID", "")
            name = product.get("Nombre", "")
            qty = product.get("Cantidad", 0)
            price = product.get("Precio", 0.0)
            self.tree.insert("", "end", values=(pid, name, qty, price))


    def show_profile_image(self):
        # Clear previous image if any
        if hasattr(self, 'profile_frame') and self.profile_frame.winfo_exists():
             for widget in self.profile_frame.winfo_children():
                 widget.destroy()
        else: # If frame doesn't exist, create it (should be created in setup_ui)
             self.profile_frame = ttk.Frame(self.root, style='TFrame')
             self.profile_frame.grid(row=0, column=0, pady=10, padx=10, sticky='ne')


        if hasattr(self, 'current_user_image') and self.current_user_image and os.path.exists(self.current_user_image):
            try:
                # Resize image to be smaller and cuter
                img_orig = PhotoImage(file=self.current_user_image)
                # Adjust subsample values to make the image smaller (e.g., 4x smaller)
                # Make subsample values configurable or calculated if needed
                subsample_x = 4
                subsample_y = 4
                img = img_orig.subsample(subsample_x, subsample_y) # Make image smaller
                self.profile_image_label = ttk.Label(self.profile_frame, image=img, background=LIGHT_LAVENDER) # Use frame background
                self.profile_image_label.image = img  # Keep reference!
                self.profile_image_label.pack(pady=5, padx=5) # Pack within the profile frame
            except tk.TclError as e: # Catch specific Tcl errors related to image formats
                 print(f"Error loading/resizing profile image (TclError): {e}. Is the image format supported (PNG, GIF)?")
                 # Optionally show a placeholder
                 self.profile_image_label = ttk.Label(self.profile_frame, text="🖼️?", font=("Segoe UI Emoji", 20), background=LIGHT_LAVENDER)
                 self.profile_image_label.pack(pady=5, padx=5)
            except Exception as e:
                print(f"Generic error loading/resizing profile image: {e}")
                # Optionally show a placeholder
                self.profile_image_label = ttk.Label(self.profile_frame, text="🖼️?", font=("Segoe UI Emoji", 20), background=LIGHT_LAVENDER)
                self.profile_image_label.pack(pady=5, padx=5)
        else: # Optional: Show placeholder even if no image is set or path is invalid
            if hasattr(self, 'current_user_image') and self.current_user_image and not os.path.exists(self.current_user_image):
                 print(f"Profile image path not found: {self.current_user_image}")
            # Default placeholder if no image or error
            self.profile_image_label = ttk.Label(self.profile_frame, text="👤", font=("Segoe UI Emoji", 20), background=LIGHT_LAVENDER)
            self.profile_image_label.pack(pady=5, padx=5)


    def add_product(self):
        product_id = self.entry_id.get()
        name = self.entry_name.get()
        quantity_str = self.entry_quantity.get()
        price_str = self.entry_price.get()

        if not product_id or not name or not quantity_str or not price_str:
            messagebox.showerror("Error 💖", "¡Todos los campos son necesarios!")
            return

        # Validate if product ID already exists
        if any(p.get("ID") == product_id for p in self.inventory):
             messagebox.showwarning("Aviso 🧸", f"¡El producto con ID '{product_id}' ya existe!")
             return

        try:
            quantity = int(quantity_str)
            price = float(price_str)
            if quantity < 0 or price < 0:
                 messagebox.showerror("Error 💖", "¡Cantidad y precio no pueden ser negativos!")
                 return
        except ValueError:
            messagebox.showerror("Error 💖", "Cantidad debe ser un número entero y Precio un número decimal")
            return

        product = {"ID": product_id, "Nombre": name, "Cantidad": quantity, "Precio": price}
        self.inventory.append(product)
        self.tree.insert("", "end", values=(product_id, name, quantity, price))
        self.save_inventory()

        # Clear entries after adding
        self.entry_id.delete(0, tk.END)
        self.entry_name.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        self.entry_price.delete(0, tk.END)
        messagebox.showinfo("Éxito ✨", "¡Producto agregado con éxito!")


    def search_product(self):
        query = self.entry_search.get().strip().lower()

        # Clear the table before showing results
        for item in self.tree.get_children():
            self.tree.delete(item)

        found = False
        # Filter products by ID or Name (case-insensitive)
        for product in self.inventory:
            product_id = str(product.get("ID", "")).lower() # Ensure ID is string for comparison
            product_name = product.get("Nombre", "").lower()
            if query in product_id or query in product_name:
                self.tree.insert("", "end", values=(product.get("ID", ""), product.get("Nombre", ""), product.get("Cantidad", 0), product.get("Precio", 0.0)))
                found = True

        # Show message if no results found
        if not found:
            messagebox.showinfo("Sin resultados ☁️", "No se encontraron productos que coincidan.")
            # Optionally repopulate with all items if search is cleared?
            # if not query: self.populate_treeview()


    def save_inventory(self):
        try:
            with open(self.inventory_file, "w", encoding="utf-8") as f:
                json.dump(self.inventory, f, ensure_ascii=False, indent=4)
        except Exception as e:
             print(f"Error saving inventory to {self.inventory_file}: {e}")
             messagebox.showerror("Error Guardando Inventario", f"No se pudo guardar el archivo de inventario: {e}")


    def send_inventory(self):
        # Simple placeholder for IP - ideally use a config or prompt
        host = simpledialog.askstring("Enviar Inventario", "Introduce la IP de destino:", parent=self.root)
        if not host: return # User cancelled
        port = 12345 # Keep port consistent

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5) # Add a timeout
                s.connect((host, port))
                data = json.dumps(self.inventory).encode("utf-8")
                s.sendall(data)
                messagebox.showinfo("Éxito ✨", f"Inventario enviado a {host}")
        except socket.timeout:
             messagebox.showerror("Error de Red 🔌", f"Tiempo de espera agotado al conectar con {host}")
        except Exception as e:
            messagebox.showerror("Error de Red 🔌", f"Error al enviar inventario a {host}: {e}")


    def receive_inventory(self):
        host = "0.0.0.0"  # Listen on all interfaces
        port = 12345

        # Run receiving part in a separate thread to avoid blocking UI
        def receive_thread():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((host, port))
                    s.listen(1)
                    print(f"Esperando conexión en el puerto {port}...") # Log to console
                    # Show non-blocking message
                    # messagebox.showinfo("Esperando...", f"Esperando conexión en el puerto {port}...", parent=self.root) # This might still block a bit

                    conn, addr = s.accept()
                    print(f"Conexión aceptada desde {addr}")
                    with conn:
                        data = b""
                        while True: # Loop to receive potentially large data
                            chunk = conn.recv(4096) # Receive in chunks
                            if not chunk:
                                break
                            data += chunk

                        if not data:
                             print("No data received.")
                             # Use thread-safe message box if needed, or update status bar
                             # messagebox.showwarning("Recepción", "No se recibieron datos.", parent=self.root)
                             return

                        received_inventory = json.loads(data.decode("utf-8"))
                        print(f"Inventario recibido: {len(received_inventory)} items.")

                        # Update inventory and UI (needs to be thread-safe if modifying UI directly)
                        # For simplicity, append and save, then refresh UI from main thread if needed
                        new_items_count = 0
                        for product in received_inventory:
                             # Basic validation of received product structure
                             if isinstance(product, dict) and "ID" in product and "Nombre" in product:
                                 # Optional: Check for duplicates or merge logic here
                                 self.inventory.append(product)
                                 new_items_count += 1
                             else:
                                 print(f"Skipping invalid product data received: {product}")

                        if new_items_count > 0:
                            self.save_inventory()
                            # Schedule UI update from the main thread
                            self.root.after(0, self.populate_treeview)
                            self.root.after(0, lambda: messagebox.showinfo("Éxito ✨", f"{new_items_count} productos recibidos correctamente.", parent=self.root))
                        else:
                             self.root.after(0, lambda: messagebox.showwarning("Recepción", "Se recibieron datos, pero no contenían productos válidos.", parent=self.root))


            except Exception as e:
                print(f"Error al recibir el inventario: {e}")
                # Schedule error message from the main thread
                self.root.after(0, lambda: messagebox.showerror("Error de Red 🔌", f"Error al recibir inventario: {e}", parent=self.root))

        import threading
        # Show immediate feedback that listening has started
        messagebox.showinfo("Recibiendo...", f"Escuchando en el puerto {port}...\nLa aplicación puede parecer no responder mientras espera.", parent=self.root)
        threading.Thread(target=receive_thread, daemon=True).start()


    def export_to_excel(self):
        if not self.inventory:
            messagebox.showwarning("Aviso 🧸", "¡El inventario está vacío, no hay nada que exportar!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos Excel", "*.xlsx")])
        if not file_path:
            return

        try:
            df = pd.DataFrame(self.inventory)
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Éxito ✨", "¡Inventario exportado a Excel!")
        except Exception as e:
             messagebox.showerror("Error Exportando 📄", f"No se pudo exportar a Excel: {e}")


    def export_to_json(self):
        if not self.inventory:
            messagebox.showwarning("Aviso 🧸", "¡El inventario está vacío, no hay nada que exportar!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Archivos JSON", "*.json")])
        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.inventory, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Éxito ✨", "¡Inventario exportado a JSON!")
        except Exception as e:
             messagebox.showerror("Error Exportando 📄", f"No se pudo exportar a JSON: {e}")


    def import_from_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx")])
        if not file_path:
            return

        try:
            df = pd.read_excel(file_path)
            imported_count = 0
            skipped_count = 0
            # Basic validation of columns
            required_cols = ["ID", "Nombre", "Cantidad", "Precio"]
            if not all(col in df.columns for col in required_cols):
                 messagebox.showerror("Error Importando 📄", f"El archivo Excel debe contener las columnas: {', '.join(required_cols)}")
                 return

            for _, row in df.iterrows():
                 # Check for NaN or missing values before conversion
                 if pd.isna(row["ID"]) or pd.isna(row["Nombre"]) or pd.isna(row["Cantidad"]) or pd.isna(row["Precio"]):
                     print(f"Skipping row due to missing data: {row.to_dict()}")
                     skipped_count += 1
                     continue

                 try:
                     product = {
                         "ID": str(row["ID"]), # Ensure ID is string
                         "Nombre": str(row["Nombre"]),
                         "Cantidad": int(row["Cantidad"]),
                         "Precio": float(row["Precio"])
                     }
                     # Optional: Add check for duplicates before appending
                     if not any(p.get("ID") == product["ID"] for p in self.inventory):
                         self.inventory.append(product)
                         self.tree.insert("", "end", values=(product["ID"], product["Nombre"], product["Cantidad"], product["Precio"]))
                         imported_count += 1
                     else:
                          print(f"Skipping duplicate ID from Excel: {product['ID']}")
                          skipped_count +=1

                 except ValueError:
                     print(f"Skipping row due to invalid data type (Cantidad/Precio): {row.to_dict()}")
                     skipped_count += 1
                     continue

            self.save_inventory() # Save after importing all valid rows
            info_message = f"¡{imported_count} productos importados desde Excel!"
            if skipped_count > 0:
                 info_message += f"\n({skipped_count} filas omitidas por datos faltantes, inválidos o duplicados)."
            messagebox.showinfo("Éxito ✨", info_message)

        except Exception as e:
            messagebox.showerror("Error Importando 📄", f"No se pudo importar el archivo Excel: {e}")


    def import_from_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                     messagebox.showerror("Error Importando 📄", "El archivo JSON debe contener una lista de productos.")
                     return

                imported_count = 0
                skipped_count = 0
                for product in data:
                    # Basic validation
                    if isinstance(product, dict) and "ID" in product and "Nombre" in product and "Cantidad" in product and "Precio" in product:
                         # Ensure types are correct if possible, or handle potential errors
                         try:
                             product["ID"] = str(product["ID"])
                             product["Cantidad"] = int(product["Cantidad"])
                             product["Precio"] = float(product["Precio"])

                             # Optional: Add check for duplicates before appending
                             if not any(p.get("ID") == product["ID"] for p in self.inventory):
                                 self.inventory.append(product)
                                 self.tree.insert("", "end", values=(product["ID"], product["Nombre"], product["Cantidad"], product["Precio"]))
                                 imported_count += 1
                             else:
                                 print(f"Skipping duplicate ID from JSON: {product['ID']}")
                                 skipped_count += 1
                         except (ValueError, TypeError) as type_err:
                              print(f"Skipping product due to invalid data type in JSON: {product} - {type_err}")
                              skipped_count += 1
                    else:
                         print(f"Skipping invalid product structure in JSON: {product}")
                         skipped_count += 1

            self.save_inventory() # Save after processing the file
            info_message = f"¡{imported_count} productos importados desde JSON!"
            if skipped_count > 0:
                 info_message += f"\n({skipped_count} productos omitidos por estructura inválida, tipos de datos incorrectos o duplicados)."
            messagebox.showinfo("Éxito ✨", info_message)

        except json.JSONDecodeError:
             messagebox.showerror("Error Importando 📄", "El archivo JSON no es válido.")
        except Exception as e:
            messagebox.showerror("Error Importando 📄", f"No se pudo importar el archivo JSON: {e}")


    def show_change_password_screen(self):
        # Use Toplevel for consistency
        self.change_password_window = ttk.Toplevel(self.root)
        self.change_password_window.title("🔑 Cambiar Contraseña")
        # Apply style to the frame within Toplevel
        self.change_password_frame = ttk.Frame(self.change_password_window, padding=(15, 10), style='TFrame')
        self.change_password_frame.pack(expand=True, fill=tk.BOTH) # Use pack or grid as appropriate

        ttk.Label(self.change_password_frame, text="Contraseña Actual:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_current_password = ttk.Entry(self.change_password_frame, show="*", bootstyle=INFO)
        self.entry_current_password.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.change_password_frame, text="Nueva Contraseña:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_new_password_change = ttk.Entry(self.change_password_frame, show="*", bootstyle=INFO) # Use different variable name
        self.entry_new_password_change.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.change_password_frame, text="Confirmar Contraseña:").grid(row=2, column=0, padx=5, pady=5)
        self.entry_confirm_password = ttk.Entry(self.change_password_frame, show="*", bootstyle=INFO)
        self.entry_confirm_password.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(self.change_password_frame, text="Cambiar", command=self.change_password, bootstyle=SUCCESS).grid(row=3, column=0, columnspan=2, pady=10)


    def change_password(self):
        current_password = self.entry_current_password.get()
        new_password = self.entry_new_password_change.get() # Use correct variable name
        confirm_password = self.entry_confirm_password.get()

        if not current_password or not new_password or not confirm_password:
            messagebox.showerror("Error 🔑", "¡Todos los campos son obligatorios!", parent=self.change_password_window)
            return

        if self.hash_password(current_password) != self.users[self.current_user]["password"]:
            messagebox.showerror("Error 🔑", "La contraseña actual es incorrecta", parent=self.change_password_window)
            return

        if new_password != confirm_password:
            messagebox.showerror("Error 🔑", "Las nuevas contraseñas no coinciden", parent=self.change_password_window)
            return

        # Optional: Add password strength check here

        self.users[self.current_user]["password"] = self.hash_password(new_password)
        self.save_users()
        messagebox.showinfo("Éxito ✨", "Contraseña cambiada correctamente", parent=self.change_password_window)
        self.change_password_window.destroy()


    def delete_selected_products(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Aviso 🧸", "¡Selecciona uno o más productos para eliminar!", parent=self.root)
            return

        confirm = messagebox.askyesno("Confirmar Eliminación 🗑️", f"¿Seguro que quieres eliminar {len(selected_items)} producto(s) seleccionados?", parent=self.root)
        if not confirm:
            return

        ids_to_delete = []
        for item in selected_items:
            values = self.tree.item(item, "values")
            if values: # Ensure values exist
                 ids_to_delete.append(values[0]) # Get the ID (first column)

        # Filter out the inventory based on IDs
        original_count = len(self.inventory)
        self.inventory = [product for product in self.inventory if product.get("ID") not in ids_to_delete]
        deleted_count = original_count - len(self.inventory)

        # Remove from treeview
        for item in selected_items:
            self.tree.delete(item)

        if deleted_count > 0:
            self.save_inventory()
            messagebox.showinfo("Éxito ✨", f"{deleted_count} producto(s) eliminado(s) correctamente.", parent=self.root)
        else:
             messagebox.showinfo("Info ☁️", "No se eliminaron productos (quizás ya no existían).", parent=self.root)


    def show_delete_user_screen(self):
        # Ensure only admin can access this
        if self.current_user != "admin":
             messagebox.showerror("Acceso Denegado 🚫", "Solo el administrador puede borrar usuarios.")
             return

        self.delete_user_window = ttk.Toplevel(self.root)
        self.delete_user_window.title("👤 Borrar Usuario")
        self.delete_user_frame = ttk.Frame(self.delete_user_window, padding=(15, 10), style='TFrame')
        self.delete_user_frame.pack(expand=True, fill=tk.BOTH)

        ttk.Label(self.delete_user_frame, text="Usuario a borrar:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_delete_user = ttk.Entry(self.delete_user_frame, bootstyle=INFO)
        self.entry_delete_user.grid(row=0, column=1, padx=5, pady=5)

        # Optional: Add a listbox or combobox to select user instead of typing?

        ttk.Button(self.delete_user_frame, text="Borrar", command=self.delete_user, bootstyle=DANGER).grid(row=1, column=0, columnspan=2, pady=10)


    def delete_user(self):
        user_to_delete = self.entry_delete_user.get()

        if not user_to_delete:
             messagebox.showerror("Error 👤", "Introduce el nombre de usuario a borrar.", parent=self.delete_user_window)
             return

        if user_to_delete == "admin":
            messagebox.showerror("Error 👤", "¡No puedes borrar al usuario administrador!", parent=self.delete_user_window)
            return

        if user_to_delete in self.users:
            confirm = messagebox.askyesno("Confirmar Borrado 👤", f"¿Estás seguro de que quieres borrar al usuario '{user_to_delete}'? Esta acción no se puede deshacer.", parent=self.delete_user_window)
            if confirm:
                del self.users[user_to_delete]
                self.save_users()
                messagebox.showinfo("Éxito ✨", f"Usuario '{user_to_delete}' borrado correctamente.", parent=self.delete_user_window)
                self.delete_user_window.destroy()
        else:
            messagebox.showerror("Error 👤", f"El usuario '{user_to_delete}' no existe.", parent=self.delete_user_window)


    def open_chat_window(self):
        self.chat_window = ttk.Toplevel(self.root)
        self.chat_window.title("💬 Chat Kawaii 💬")
        # Apply style to the main chat frame
        chat_main_frame = ttk.Frame(self.chat_window, padding=(10,10), style='TFrame')
        chat_main_frame.pack(expand=True, fill=tk.BOTH)
        self.chat_window.grid_rowconfigure(0, weight=1)
        self.chat_window.grid_columnconfigure(0, weight=1)
        chat_main_frame.grid_rowconfigure(0, weight=1) # Text display row
        chat_main_frame.grid_columnconfigure(0, weight=1) # Text display column span


        # Use ttk.Text if available and style it, otherwise tk.Text
        text_font = ('Segoe Print', 11) # Define font once
        try:
            # Style the text display area
            self.chat_display = ttk.Text(chat_main_frame, state="disabled", width=50, height=20, background=PALE_MINT, foreground="#333333", font=text_font, wrap=tk.WORD)
        except AttributeError: # ttk.Text might not exist in all versions or setups
             self.chat_display = tk.Text(chat_main_frame, state="disabled", width=50, height=20, background=PALE_MINT, foreground="#333333", font=text_font, wrap=tk.WORD)
        self.chat_display.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky='nsew')

        # Add scrollbar to chat display
        chat_scrollbar = ttk.Scrollbar(chat_main_frame, orient=tk.VERTICAL, command=self.chat_display.yview)
        self.chat_display['yscrollcommand'] = chat_scrollbar.set
        chat_scrollbar.grid(row=0, column=2, sticky='ns', pady=10, padx=(0,10))


        # Frame for entry and button
        entry_frame = ttk.Frame(chat_main_frame, style='TFrame')
        entry_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0,10), sticky='ew') # Span 2 columns, adjust padding
        # entry_frame.grid_columnconfigure(0, weight=1) # Make entry expand

        self.chat_entry = ttk.Entry(entry_frame, width=40, bootstyle=INFO, font=text_font) # Use bootstyle for consistency
        self.chat_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5)) # Pack entry to the left
        # Bind Enter key to send message
        self.chat_entry.bind("<Return>", self.send_message_event)


        ttk.Button(entry_frame, text="Enviar 💌", command=self.send_message, bootstyle=SUCCESS).pack(side=tk.LEFT) # Pack button next to it


        # Placeholder for connection status?
        # self.chat_status_label = ttk.Label(chat_main_frame, text="Estado: Desconectado", style='TLabel')
        # self.chat_status_label.grid(row=2, column=0, columnspan=2, sticky='w', padx=10)


        # Attempt to connect or start server
        self.initialize_chat_connection()


    def initialize_chat_connection(self):
         # Simple client/server decision - prompt user?
         # For now, try to connect as client first, if fails, start server.
         # This is a basic approach and might need refinement.
         import threading

         def connect_as_client():
             host = simpledialog.askstring("Conectar Chat", "Introduce la IP del otro usuario (deja vacío para esperar conexión):", parent=self.chat_window)
             if host: # User entered an IP, try to connect
                 port = 12346
                 try:
                     print(f"Intentando conectar a {host}:{port}...")
                     # self.update_chat_status("Intentando conectar...")
                     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                     client_socket.settimeout(5)
                     client_socket.connect((host, port))
                     self.chat_connection = client_socket
                     print("Conectado como cliente.")
                     # self.update_chat_status(f"Conectado a {host}")
                     # Start receiving messages in a separate thread
                     threading.Thread(target=self.receive_messages, daemon=True).start()
                 except socket.timeout:
                      print("Timeout al conectar como cliente.")
                      # self.update_chat_status("Error: Timeout")
                      messagebox.showerror("Error de Chat", "Tiempo de espera agotado al conectar.", parent=self.chat_window)
                      self.start_chat_server() # Fallback to server mode
                 except Exception as e:
                      print(f"Error al conectar como cliente: {e}")
                      # self.update_chat_status(f"Error: {e}")
                      messagebox.showerror("Error de Chat", f"No se pudo conectar: {e}", parent=self.chat_window)
                      self.start_chat_server() # Fallback to server mode
             else: # User didn't enter IP, start server
                 self.start_chat_server()

         # Run connection attempt in a thread to avoid blocking UI during prompt/connection
         threading.Thread(target=connect_as_client, daemon=True).start()


    def start_chat_server(self):
        def server_thread():
            host = "0.0.0.0"
            port = 12346
            self.chat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.chat_socket.bind((host, port))
                self.chat_socket.listen(1)
                print(f"Chat server escuchando en el puerto {port}...")
                # self.update_chat_status(f"Esperando conexión en puerto {port}...")
                # Accept connection - this blocks the server_thread
                conn, addr = self.chat_socket.accept()
                self.chat_connection = conn # Store the connection socket
                print(f"Chat conectado con {addr}")
                # self.update_chat_status(f"Conectado con {addr[0]}")
                # Now start listening for messages on this connection
                self.receive_messages() # This will run in the server_thread
            except OSError as e:
                 print(f"Error al iniciar el servidor de chat (¿Puerto en uso?): {e}")
                 # self.update_chat_status(f"Error al iniciar servidor: {e}")
                 # Schedule messagebox from main thread
                 self.root.after(0, lambda: messagebox.showerror("Error de Chat", f"No se pudo iniciar el servidor en el puerto {port}. ¿Ya está en uso?", parent=self.chat_window))
            except Exception as e:
                 print(f"Error inesperado en el servidor de chat: {e}")
                 # self.update_chat_status(f"Error de servidor: {e}")


        import threading
        # Only start server thread if no connection exists yet
        if not hasattr(self, 'chat_connection') or self.chat_connection is None:
             threading.Thread(target=server_thread, daemon=True).start()


    def send_message_event(self, event): # Handles Enter key press
        self.send_message()

    def send_message(self):
        if not hasattr(self, 'chat_connection') or self.chat_connection is None:
            messagebox.showwarning("Chat Desconectado ☁️", "No hay conexión activa para enviar mensajes.", parent=self.chat_window)
            return

        message = self.chat_entry.get()
        if message:
            try:
                full_message = f"{self.current_user}: {message}" # Prepend username
                self.chat_connection.sendall(full_message.encode("utf-8"))
                self.display_message(f"Tú: {message}") # Display locally without username prefix
                self.chat_entry.delete(0, tk.END)
            except BrokenPipeError: # Handle case where other side disconnected
                 print("Error al enviar: Conexión cerrada por el otro usuario.")
                 messagebox.showerror("Error de Chat 🔌", "La conexión se ha cerrado.", parent=self.chat_window)
                 self.close_chat_connection()
                 # self.update_chat_status("Desconectado")
            except Exception as e:
                 print(f"Error al enviar mensaje: {e}")
                 messagebox.showerror("Error de Chat 🔌", f"No se pudo enviar el mensaje: {e}", parent=self.chat_window)


    def receive_messages(self):
        # This function now runs in a dedicated thread (either client or server)
        while True:
            try:
                if not hasattr(self, 'chat_connection') or self.chat_connection is None:
                     break # Exit if connection is lost/closed

                message_bytes = self.chat_connection.recv(1024)
                if not message_bytes: # Empty bytes indicate disconnection
                    print("Chat desconectado (recv returned empty).")
                    self.close_chat_connection()
                    # Schedule UI update from main thread
                    self.root.after(0, lambda: messagebox.showinfo("Chat Desconectado ☁️", "El otro usuario se ha desconectado.", parent=self.chat_window))
                    # self.root.after(0, self.update_chat_status, "Desconectado")
                    break

                message = message_bytes.decode("utf-8")
                if message:
                    # Schedule display_message to run in the main UI thread
                    self.root.after(0, self.display_message, message) # Display full message with sender name

            except ConnectionResetError:
                 print("Chat desconectado (ConnectionResetError).")
                 self.close_chat_connection()
                 self.root.after(0, lambda: messagebox.showinfo("Chat Desconectado ☁️", "La conexión se ha reiniciado.", parent=self.chat_window))
                 # self.root.after(0, self.update_chat_status, "Desconectado")
                 break
            except Exception as e:
                print(f"Error al recibir mensajes: {e}")
                self.close_chat_connection()
                # self.root.after(0, self.update_chat_status, f"Error: {e}")
                break # Exit loop on error


    def display_message(self, message):
        if hasattr(self, 'chat_display') and self.chat_display.winfo_exists():
            self.chat_display.config(state="normal")
            self.chat_display.insert(tk.END, message + "\\n")
            self.chat_display.see(tk.END) # Scroll to the bottom
            self.chat_display.config(state="disabled")

    def close_chat_connection(self):
         if hasattr(self, 'chat_connection') and self.chat_connection:
             try:
                 self.chat_connection.close()
             except Exception as e:
                 print(f"Error al cerrar socket de chat: {e}")
             finally:
                  self.chat_connection = None
         if hasattr(self, 'chat_socket') and self.chat_socket: # Close server socket too if it exists
              try:
                  self.chat_socket.close()
              except Exception as e:
                  print(f"Error al cerrar socket servidor de chat: {e}")
              finally:
                   self.chat_socket = None
         print("Conexión de chat cerrada.")
         # self.update_chat_status("Desconectado") # Update status if using a label

    # def update_chat_status(self, status):
    #      if hasattr(self, 'chat_status_label') and self.chat_status_label.winfo_exists():
    #          self.chat_status_label.config(text=f"Estado: {status}")


if __name__ == "__main__":
    # Import simpledialog here if needed for chat IP
    from tkinter import simpledialog

    # Changed themename from "darkly" to "minty" for a lighter aesthetic
    app = ttk.Window(themename="minty") # Keep minty as base
    InventoryApp(app)
    app.mainloop()