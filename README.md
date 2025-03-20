# 📦 Sistema de Gestión de Inventarios

¡Bienvenido al Sistema de Gestión de Inventarios! 🎉

Este proyecto es una aplicación sencilla para gestionar inventarios con una interfaz gráfica moderna. Permite agregar, importar, exportar y enviar datos del inventario a través de la red, además de guardar los datos localmente.

## 🚀 Características

- **Inicio de sesión**: Acceso seguro con usuarios y contraseñas almacenados en `users.json`. Incluye:
  - Usuario: `admin`, Contraseña: `admin`
  - Usuario: `user`, Contraseña: `user123`
- **Registro de nuevos usuarios**: Permite a nuevos usuarios registrarse con un nombre y contraseña.
- **Cambio de contraseña**: Los usuarios pueden cambiar su contraseña desde la interfaz.
- **Eliminación de usuarios**: Solo el usuario `admin` puede eliminar usuarios.
- **Agregar productos**: Registra productos con ID, nombre, cantidad y precio.
- **Buscar productos**: Filtra productos por ID o nombre mediante una barra de búsqueda.
- **Eliminar productos seleccionados**: Permite seleccionar y eliminar varios productos de la tabla.
- **Importar y exportar**: Maneja datos en formatos Excel y JSON.
- **Persistencia local**: Guarda automáticamente los datos en un archivo `inventory_data.json`.
- **Envío y recepción por red**: Comparte el inventario con otros usuarios en la misma red.
- **Chat en red**: Comunícate con otros usuarios en la misma red mediante una ventana de chat.
- **Interfaz moderna**: Diseñada con ttkbootstrap para una experiencia visual mejorada.

## 🛠️ Requisitos

- Python 3.8 o superior
- Dependencias:
  - `ttkbootstrap`
  - `pandas`

Instálalas con:
```bash
pip install ttkbootstrap pandas
```

## 📋 Uso

1. Ejecuta la aplicación:
   ```bash
   python inventory_app.py
   ```
2. Inicia sesión con uno de los usuarios por defecto o regístrate como un nuevo usuario.
3. Usa la interfaz para:
   - Agregar productos.
   - Buscar productos por ID o nombre.
   - Eliminar productos seleccionados.
   - Importar o exportar datos.
   - Enviar o recibir el inventario por red.
   - Abrir la ventana de chat para comunicarte con otros usuarios.
   - Cambiar tu contraseña.
   - (Solo admin) Eliminar usuarios.

## 📂 Estructura del proyecto

- `inventory_app.py`: Código principal de la aplicación.
- `inventory_data.json`: Archivo donde se guardan los datos del inventario.
- `users.json`: Archivo donde se almacenan los usuarios registrados.
- `README.md`: Documentación del proyecto.

## 💻 Captura de pantalla

✨ ¡Próximamente! ✨

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas o mejoras, no dudes en compartirlas.

## 📧 Contacto

Si tienes preguntas o sugerencias, contáctame en: [ibarrabelloalisha@gmail.com](mailto:ibarrabelloalisha@gmail.com)

---

¡Gracias por usar el Sistema de Gestión de Inventarios! 🎊