# Sistema de Gestión de Restaurante

**Estudiante:** Antony Jordano Defaz Diaz  
**Materia:** Programación Orientada a Objetos  
**Semestre:** Segundo Semestre - UEA Tecnologías de la Información  

---
# 🍽️ Restaurant App - Sistema de Gestión de Restaurante

**Restaurant App** es una aplicación de escritorio desarrollada en Python utilizando Tkinter para la interfaz gráfica (UI/UX) y un sistema de almacenamiento en archivos JSON locales. El sistema permite la administración integral de usuarios, catálogo de productos e historial de ventas con validación estricta de datos y control de roles.

---

## 🚀 Características y Funcionalidades

### 👤 Gestión de Usuarios
- **CRUD Completo:** Registro, consulta, actualización y eliminación de usuarios en tiempo real.
- **Control de Roles:** Asignación de roles permistidos (`Administrador`, `Empleado`, `Cliente`) validados mediante `@property` y `@setter`.
- **Validación Estricta y Sanitización:**
  - Evita errores de nombres mediante el filtrado automático de caracteres especiales (transformación automática de "ñ/Ñ" a "n/N").
  - Manejo seguro de contraseñas y prevención de campos vacíos.
- **Interacción Fluida:** Eventos de teclado (`Enter` para registrar, `Escape` para limpiar campos) y sincronización con el selector `Combobox`.

### 📦 Gestión de Productos y Ventas
- Registro y actualización de productos.
- Registro de transacciones e historial de ventas.
- Métricas en tiempo real visualizadas en la barra de estado inferior.

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.x
- **GUI:** Tkinter / ttk (`Treeview`, `Combobox`, `Formularios`)
- **Arquitectura:** Programación Orientada a Objetos (POO) estructurada en capas (`modelos`, `servicios`, `ui`).
- **Persistencia de Datos:** JSON local (`usuarios.json`, `productos.json`, `ventas.json`).

---

## 📂 Estructura del Proyecto

```text
restaurante_app/
│
├── datos/                  # Archivos de almacenamiento JSON
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
│
├── modelos/                # Clases del dominio (POO)
│   ├── producto.py
│   ├── usuario.py          # Definición de Usuario y validación de roles
│   └── venta.py
│
├── servicios/              # Lógica de negocio y persistencia
│   ├── archivo_servicio.py # Lectura y escritura de archivos JSON
│   └── restaurante.py      # Servicio principal RestauranteServicio
│
├── ui/                     # Interfaz Gráfica de Usuario (Tkinter)
│   ├── login_view.py
│   └── main_view.py        # Vistas de gestión, tablas y eventos
│
└── main.py                 # Punto de entrada principal de la aplicación# PROYECTOAPP
