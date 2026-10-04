from datetime import date 


from modelos.producto import Productos
from modelos.usuario import Usuario
from modelos.venta import Venta 

class RestauranteServicio:
    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio
        self.usuarios = []
        self.productos = []
        self.ventas = []  
        self.cargar_datos()

    def guardar_ventas(self):
        self.archivo_servicio.escribir_json(
            "ventas.json",
            [v.a_diccionario() for v in self.ventas]
        )

    def cargar_datos(self):
        # 1. Cargar Usuarios
        usuarios_json = self.archivo_servicio.leer_json("usuarios.json")
        productos_json = self.archivo_servicio.leer_json("productos.json")
        ventas_json = self.archivo_servicio.leer_json("ventas.json")

        self.usuarios = [
            Usuario(
                datos.get("identificador"),
                datos.get("nombre",),
                datos.get("usuario",),
                datos.get("contrasena") or datos.get("contrasena"),
                datos.get("rol", "Cliente"),
            )
            for datos in usuarios_json
        ]

        # 2. Cargar Productos
        self.productos = [
            Productos(
                datos.get("codigo",),
                datos.get("nombre",),
                datos.get("precio", 0.0)
            )
            for datos in productos_json
        ]

        # 3. Cargar Ventas desde el archivo JSON
        self.ventas= [
            Venta(
                datos.get("identificador",""),
                datos.get("usuario_id",""),
                datos.get("producto_codigo",""),
                datos.get("fecha","")
            )
            for datos in ventas_json
        ]
   
    def validar_acceso(self, usuario, contrasena):
        #Verificar si las credenciales coinciden con un usuario cargado.
        for usuario_registrado in self.usuarios:
            if(
                usuario_registrado.contrasena == contrasena
                and usuario_registrado.contrasena == contrasena

            ):
               return usuario_registrado
        
        return None
    
    def cantidad_usuarios(self):
        return len(self.usuarios)

    def cantidad_productos(self):
        return len(self.productos)

    def cantidad_ventas(self):
        return len(self.ventas)

    def listar_usuarios(self):
        # Entrega los usuarios cargados para mostrarlos en la interfaz.
        return self.usuarios
    def listar_productos(self):
        """Devuelve la lista de platillos/productos para el menú."""
        return self.productos
    
    def listar_ventas(self):
        """Devuelve la lista de ventas registradas."""
        return self.ventas
    
    def guardar_productos(self):
        datos = [
            {
                "codigo": producto.codigo,
                "nombre": producto.nombre,
                "precio": producto.precio,
            }
            for producto in self.productos
        ]
        self.archivo_servicio.escribir_json("productos.json", datos)
    def guardar_usuarios(self):
        datos = [
       {
               "identificador": usuario.identificador,
               "nombre": usuario.nombre,
               "usuario": usuario.usuario,
               "contrasena": usuario.contrasena,
               "rol": usuario.rol,
        }
        for usuario in self.usuarios
        ]
        self.archivo_servicio.escribir_json("usuarios.json", datos)

    def buscar_producto_por_codigo(self, codigo):
        codigo = codigo.strip()
        for producto in self.productos:
            if producto.codigo == codigo:
                return producto
        return None
    
    
    def buscar_usuario_por_identificador(self, identificador):
        for u in self.usuarios:
            if str(u.identificador) == str(identificador):
                return u
        return None

    def actualizar_usuario(self, identificador, nombre, usuario, contrasena, rol):
        u = self.buscar_usuario_por_identificador(identificador)
        if not u:
            raise ValueError("El usuario no existe.")

        # Actualiza las propiedades directamente
        u.nombre = nombre
        u.usuario = usuario.replace("ñ", "n").replace("Ñ", "N")
        u.rol = rol  # Se dispara el @rol.setter corregido

        # Solo actualiza la contraseña si el usuario escribió algo en la caja
        if contrasena and contrasena.strip():
            u.contrasena = contrasena

        self.guardar_datos()  # Re-escribe el archivo usuarios.json
    def buscar_usuario_por_nombre_usuario(self, usuario):
        """Busca un usuario por su nombre de usuario de login."""
        for u in self.obtener_usuarios():
            if u.usuario.lower() == usuario.lower():
                return u
        return None

    def generar_identificador_venta(self):
        siguiente = len(self.ventas) + 1
        return f"V{siguiente:03d}"

    def registrar_producto(self, codigo, nombre, precio):
        nuevo_producto = Productos(codigo, nombre, precio)

        if self.buscar_producto_por_codigo(nuevo_producto.codigo) is not None:
            raise ValueError("Ya existe un producto con ese codigo.")

        self.productos.append(nuevo_producto)
        self.guardar_productos()
        return nuevo_producto

    def actualizar_producto(self, codigo, nombre, precio):
        producto_actual = self.buscar_producto_por_codigo(codigo)

        if producto_actual is None:
            raise ValueError("No existe un producto con ese codigo.")

        datos_validados = Productos(codigo, nombre, precio)
        producto_actual.nombre = datos_validados.nombre
        producto_actual.precio = datos_validados.precio
        self.guardar_productos()
        return producto_actual

    def eliminar_producto(self, codigo):
        producto_actual = self.buscar_producto_por_codigo(codigo)

        if producto_actual is None:
            raise ValueError("No existe un producto con ese codigo.")

        self.productos.remove(producto_actual)
        self.guardar_productos()
        return producto_actual
    
    def obtener_usuarios(self):
        """Retorna la lista de usuarios cargados."""
        return self.usuarios

    
    
    def registrar_usuario(self, identificador, nombre, usuario, contrasena, rol):
        if self.buscar_usuario_por_nombre_usuario(usuario):
            raise ValueError(f"El usuario '{usuario}' ya se encuentra registrado.")

        # Crea la instancia de Usuario segun la estructura de tu modelo
        nuevo_usuario = Usuario(
            identificador=identificador,
            nombre=nombre,
            usuario=usuario,
            contrasena=contrasena,
            rol=rol
        )
        self.usuarios.append(nuevo_usuario)
        self.guardar_datos()  # O la funcion que guarda en el archivo JSON
    def actualizar_usuario(
        self,
        identificador,
        nombre,
        usuario,
        contrasena,
        rol,
        identificador_usuario_actual=None,
    ):
        usuario_actual = self.buscar_usuario_por_identificador(identificador)

        if usuario_actual is None:
            raise ValueError("No existe un usuario con ese identificador.")

        datos_validados = Usuario(identificador, nombre, usuario, contrasena, rol)
        usuario_con_mismo_login = self.buscar_usuario_por_nombre_usuario(datos_validados.usuario)
        if (
            usuario_con_mismo_login is not None
            and usuario_con_mismo_login.identificador != usuario_actual.identificador
        ):
            raise ValueError("Ya existe otro usuario con ese nombre de usuario.")

        if (
            identificador_usuario_actual == usuario_actual.identificador
            and usuario_actual.rol == "Administrador"
            and datos_validados.rol != "Administrador"
        ):
            raise ValueError("No puede cambiar el rol del administrador actual.")

        usuario_actual.nombre = datos_validados.nombre
        usuario_actual.usuario = datos_validados.usuario
        usuario_actual.contrasena = datos_validados.contrasena
        usuario_actual.rol = datos_validados.rol
        self.guardar_usuarios()
        return usuario_actual
    def eliminar_usuario(self, identificador, identificador_usuario_actual=None):
        usuario_actual = self.buscar_usuario_por_identificador(identificador)

        if usuario_actual is None:
            raise ValueError("No existe un usuario con ese identificador.")
        if usuario_actual.identificador == identificador_usuario_actual:
            raise ValueError("No puede eliminar el usuario actualmente autenticado.")

        self.usuarios.remove(usuario_actual)
        self.guardar_usuarios()
        return usuario_actual
    def guardar_ventas(self):
        datos = [
            {
                "identificador": venta.identificador,
                "usuario_id": venta.usuario_id,
                "producto_id": venta.producto_id,
                "fecha": venta.fecha,
            }
            for venta in self.ventas
        ]
        self.archivo_servicio.escribir_json("ventas.json", datos)


    def registrar_venta(self, usuario_id, producto_codigo):
        usuario_id = usuario_id.strip()
        producto_codigo = producto_codigo.strip()

        if not usuario_id:
            raise ValueError("Debe seleccionar un usuario.")
        if not producto_codigo:
            raise ValueError("Debe seleccionar un producto.")

        # --- CAMBIA ESTAS LÍNEAS DE BÚSQUEDA ---
        usuario_encontrado = next(
            (u for u in self.usuarios if u.identificador == usuario_id or u.usuario == usuario_id or u.nombre == usuario_id),
            None
        )
        if usuario_encontrado is None:
            raise ValueError("El usuario seleccionado no existe.")

        if self.buscar_producto_por_codigo(producto_codigo) is None:
            raise ValueError("El producto seleccionado no existe.")

        # Usamos el usuario encontrado para registrar
        nueva_venta = Venta(
            self.generar_identificador_venta(),
            usuario_encontrado.usuario,
            producto_codigo,
            date.today().isoformat(),
        )
        self.ventas.append(nueva_venta)
        self.guardar_ventas()
        return nueva_venta
    def listar_ventas(self):
        return self.ventas