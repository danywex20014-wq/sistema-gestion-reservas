from abc import ABC, abstractmethod
from datetime import datetime
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageEnhance

DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))


def obtener_ruta_recurso(nombre_archivo):
    return os.path.join(DIRECTORIO_ACTUAL, nombre_archivo)


def registrar_log(mensaje):
    try:
        with open(
            obtener_ruta_recurso("logs.txt"), "a", encoding="utf-8"
        ) as archivo:
            archivo.write(f"[{datetime.now()}] {mensaje}\n")
    except IOError:
        pass


class ClienteError(Exception):
    pass


class ServicioError(Exception):
    pass


class ReservaError(Exception):
    pass


class Entidad(ABC):

    @abstractmethod
    def mostrar_info(self):
        pass


class Cliente(Entidad):

    def __init__(self, nombre, cedula, correo):
        self.__nombre = nombre
        self.__cedula = cedula
        self.__correo = correo
        self.validar_datos()

    @property
    def nombre(self):
        return self.__nombre

    def validar_datos(self):
        if not self.__nombre.strip():
            raise ClienteError("¡Oops! El nombre no puede estar vacío 🖤")
        if len(self.__cedula.strip()) < 5:
            raise ClienteError("¡Cuidado! La cédula es inválida 💀")
        if "@" not in self.__correo:
            raise ClienteError("¡Uh-oh! El correo electrónico es inválido ✉️")

    def mostrar_info(self):
        return f"{self.__nombre}"


class Servicio(ABC):

    def __init__(self, nombre, tarifa_base):
        if tarifa_base <= 0:
            raise ServicioError("Tarifa inválida")
        self.nombre = nombre
        self.tarifa_base = tarifa_base

    @abstractmethod
    def calcular_costo(self, horas, descuento=0):
        pass


class ReservaSala(Servicio):

    def __init__(self, capacidad):
        super().__init__("Reserva Sala", 50000)
        self.capacidad = capacidad

    def calcular_costo(self, horas, descuento=0):
        total = self.tarifa_base * horas
        total -= total * descuento
        return total


class AlquilerEquipo(Servicio):

    def __init__(self, tipo_equipo):
        super().__init__("Alquiler Equipo", 80000)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, horas, descuento=0):
        total = self.tarifa_base * horas
        total -= total * descuento
        return total


class AsesoriaEspecializada(Servicio):

    def __init__(self, specialty):
        super().__init__("Asesoría", 120000)
        self.especialidad = specialty

    def calcular_costo(self, horas, descuento=0):
        total = self.tarifa_base * horas
        total += total * 0.19
        total -= total * descuento
        return total


class Reserva:

    def __init__(self, cliente, servicio, horas):
        if horas <= 0:
            raise ReservaError("Las horas deben ser mayores a cero ⏳")
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "Pendiente"

    def procesar(self):
        try:
            total = self.servicio.calcular_costo(self.horas)
        except Exception as error:
            raise ReservaError("Error procesando la reserva 👿") from error
        else:
            self.estado = "Confirmada"
            registrar_log(f"Reserva confirmada para {self.cliente.nombre}")
            return total


clientes = []
reservas = []
textos_historial_canvas = []

ventana = tk.Tk()
ventana.title("😈 Sistema Kuromi - Reservas 😈")
ventana.geometry("850x700")
ventana.resizable(False, False)

canvas = tk.Canvas(ventana, width=850, height=700, bg="#dccdf2", highlightthickness=0)
canvas.pack(fill="both", expand=True)


def cargar_img(nombre_archivo, tam):
    try:
        ruta = obtener_ruta_recurso(nombre_archivo)
        if os.path.exists(ruta):
            img = Image.open(ruta)
            img = img.resize(tam, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        return None
    except Exception as ex:
        print(f"Error cargando {nombre_archivo}: {ex}")
        return None


def cargar_img_con_opacidad(nombre_archivo, tam, opacidad=0.25):
    try:
        ruta = obtener_ruta_recurso(nombre_archivo)
        if os.path.exists(ruta):
            img = Image.open(ruta).convert("RGBA")
            img = img.resize(tam, Image.Resampling.LANCZOS)

            alpha = img.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacidad)
            img.putalpha(alpha)

            return ImageTk.PhotoImage(img)
        return None
    except Exception as ex:
        print(f"Error aplicando opacidad a {nombre_archivo}: {ex}")
        return None


patron_tk = cargar_img("Fondo con Patrón.png", (150, 150))
img_titulo = cargar_img("La que va al lado del título.png", (65, 65))
img_kuromi_btn = cargar_img("Kuromi decorativa (Junto al botón).png", (110, 120))
img_calavera = cargar_img("Iconos de los campos (Nombre, Cédula, etc.).png", (38, 38))

img_fondo_interno = cargar_img_con_opacidad(
    "fondo de los cuadrados internos.png", (45, 45), opacidad=0.25
)

if patron_tk:
    for x in range(0, 850, 150):
        for y in range(0, 700, 150):
            canvas.create_image(x, y, image=patron_tk, anchor="nw")


def crear_rectangulo_redondeado(canvas_obj, x1, y1, x2, y2, radio, **kwargs):
    puntos = [
        x1 + radio, y1, x1 + radio, y1,
        x2 - radio, y1, x2 - radio, y1,
        x2, y1, x2, y1 + radio, x2, y1 + radio,
        x2, y2 - radio, x2, y2 - radio, x2, y2,
        x2 - radio, y2, x2 - radio, y2,
        x1 + radio, y2, x1 + radio, y2,
        x1, y2, x1, y2 - radio, x1, y2 - radio,
        x1, y1 + radio, x1, y1 + radio, x1, y1
    ]
    return canvas_obj.create_polygon(puntos, **kwargs, smooth=True)


crear_rectangulo_redondeado(
    canvas, 100, 20, 750, 420, radio=25, fill="#e8b5d5", outline="#e8b5d5"
)
crear_rectangulo_redondeado(
    canvas, 106, 26, 744, 414, radio=22, fill="#c0aae4", outline="#2b1331", width=3
)

if img_fondo_interno:
    for x in range(125, 710, 70):
        for y in range(45, 380, 65):
            canvas.create_image(x, y, image=img_fondo_interno, anchor="nw")

canvas.create_text(
    425,
    65,
    text="Sistema Kuromi - Reservas",
    fill="#2b1331",
    font=("Century Gothic", 24, "bold"),
)

if img_titulo:
    canvas.create_image(140, 32, image=img_titulo, anchor="nw")
    canvas.create_image(640, 32, image=img_titulo, anchor="nw")

estilo_label = {
    "bg": "#c0aae4",
    "fg": "#2b1331",
    "font": ("Century Gothic", 14, "bold"),
    "anchor": "w",
}


def crear_campo_formulario(y_pos, etiqueta):
    if img_calavera:
        canvas.create_image(190, y_pos - 8, image=img_calavera, anchor="nw")

    lbl = tk.Label(ventana, text=etiqueta, **estilo_label)
    canvas.create_window(245, y_pos - 4, window=lbl, anchor="nw")

    crear_rectangulo_redondeado(
        canvas, 370, y_pos - 3, 610, y_pos + 25, radio=10, fill="#ffffff", outline="#2b1331", width=1
    )

    entry = tk.Entry(
        ventana, bg="#ffffff", fg="#000000", font=("Century Gothic", 11, "bold"), relief="flat", bd=0
    )
    canvas.create_window(
        380, y_pos + 1, window=entry, width=220, height=20, anchor="nw"
    )
    return entry


entry_nombre = crear_campo_formulario(120, "Nombre")
entry_cedula = crear_campo_formulario(170, "Cédula")
entry_correo = crear_campo_formulario(220, "Correo")

if img_calavera:
    canvas.create_image(190, 261, image=img_calavera, anchor="nw")
lbl_serv = tk.Label(ventana, text="Servicio", **estilo_label)
canvas.create_window(245, 266, window=lbl_serv, anchor="nw")

crear_rectangulo_redondeado(
    canvas, 370, 267, 610, 295, radio=10, fill="#ffffff", outline="#2b1331", width=1
)

estilo_combo = ttk.Style()
estilo_combo.theme_use("clam")
estilo_combo.configure(
    "TCombobox",
    fieldbackground="#ffffff",
    background="#e063a9",
    foreground="#000000",
    darkcolor="#c0aae4",
    arrowcolor="#ffffff",
)

combo_servicio = ttk.Combobox(
    ventana,
    values=["Reserva Sala", "Alquiler Equipo", "Asesoría"],
    font=("Century Gothic", 10, "bold"),
    state="readonly",
    justify="left",
)
canvas.create_window(
    378, 270, window=combo_servicio, width=224, height=22, anchor="nw"
)
combo_servicio.current(0)

entry_horas = crear_campo_formulario(320, "Horas")

crear_rectangulo_redondeado(
    canvas, 100, 450, 750, 670, radio=20, fill="#e8b5d5", outline="#e8b5d5"
)
crear_rectangulo_redondeado(
    canvas, 106, 456, 744, 664, radio=18, fill="#c0aae4", outline="#2b1331", width=2
)

if img_fondo_interno:
    for x in range(125, 710, 70):
        for y in range(470, 650, 55):
            canvas.create_image(x, y, image=img_fondo_interno, anchor="nw")


def actualizar_historial_en_canvas():
    for texto_id in textos_historial_canvas:
        canvas.delete(texto_id)
    textos_historial_canvas.clear()

    y_inicial = 475
    for i, res in enumerate(reservas[-6:]):
        total = res.servicio.calcular_costo(res.horas)

        if total >= 1000000:
            texto_total = f"${total / 1000000:.1f}M"
        else:
            texto_total = f"${total:,.0f}"

        linea_texto = (
            f" 🖤  Cliente: {res.cliente.nombre}  |  Servicio: {res.servicio.nombre}  "
            f"|  Total: {texto_total}  |  Estado: {res.estado}"
        )
        txt_id = canvas.create_text(
            135,
            y_inicial + (i * 26),
            text=linea_texto,
            fill="#2b1331",
            font=("Century Gothic", 10, "bold"),
            anchor="w",
        )
        textos_historial_canvas.append(txt_id)


def registrar_reserva(event=None):
    try:
        nombre = entry_nombre.get()
        cedula = entry_cedula.get()
        correo = entry_correo.get()
        horas_texto = entry_horas.get()

        if not horas_texto.isdigit():
            raise ReservaError("¡Por favor ingresa un número de horas válido!")

        horas = int(horas_texto)
        cliente = Cliente(nombre, cedula, correo)
        clientes.append(cliente)

        type_servicio = combo_servicio.get()
        if type_servicio == "Reserva Sala":
            servicio = ReservaSala(20)
        elif type_servicio == "Alquiler Equipo":
            servicio = AlquilerEquipo("Proyector")
        else:
            servicio = AsesoriaEspecializada("Ciberseguridad")

        reserva = Reserva(cliente, servicio, horas)
        reserva.procesar()
        reservas.append(reserva)

        actualizar_historial_en_canvas()
        limpiar_formulario()

        messagebox.showinfo(
            "🖤 ¡Éxito! 🖤", "¡Tu reserva de Kuromi ha sido procesada!"
        )

    except Exception as e:
        registrar_log(str(e))
        messagebox.showerror("👿 Error Kuromi 👿", str(e))


def limpiar_formulario():
    entry_nombre.delete(0, tk.END)
    entry_cedula.delete(0, tk.END)
    entry_correo.delete(0, tk.END)
    entry_horas.delete(0, tk.END)
    combo_servicio.current(0)


def solicitar_cancelacion_reserva(event=None):
    popup = tk.Toplevel(ventana)
    popup.title("👿 Confirmar Acción 👿")
    popup.geometry("350x160")
    popup.resizable(False, False)
    popup.configure(bg="#c0aae4")

    popup.transient(ventana)
    popup.grab_set()

    x_pop = ventana.winfo_x() + (ventana.winfo_width() // 2) - 175
    y_pop = ventana.winfo_y() + (ventana.winfo_height() // 2) - 80
    popup.geometry(f"+{x_pop}+{y_pop}")

    lbl_msg = tk.Label(
        popup,
        text="¿Deseas borrar la última reserva guardada\ny limpiar el formulario? 🖤",
        bg="#c0aae4",
        fg="#2b1331",
        font=("Century Gothic", 11, "bold"),
        justify="center"
    )
    lbl_msg.pack(pady=20)

    marco_botones = tk.Frame(popup, bg="#c0aae4")
    marco_botones.pack(fill="x", side="bottom", pady=15)

    def accion_borrar():
        if reservas:
            reservas.pop()
            actualizar_historial_en_canvas()
        limpiar_formulario()
        popup.destroy()
        messagebox.showinfo("🖤 Borrado 🖤", "Campos limpios y última reserva eliminada.")

    def accion_no():
        popup.destroy()

    btn_si = tk.Button(
        marco_botones,
        text="Sí, borrar",
        bg="#e063a9",
        fg="white",
        activebackground="#ffdef2",
        activeforeground="#2b1331",
        font=("Century Gothic", 10, "bold"),
        relief="ridge",
        bd=2,
        cursor="heart",
        command=accion_borrar
    )
    btn_si.pack(side="left", padx=35, ipadx=10)

    btn_no = tk.Button(
        marco_botones,
        text="No",
        bg="#2b1331",
        fg="white",
        activebackground="#ffdef2",
        activeforeground="#2b1331",
        font=("Century Gothic", 10, "bold"),
        relief="ridge",
        bd=2,
        cursor="heart",
        command=accion_no
    )
    btn_no.pack(side="right", padx=35, ipadx=20)


btn_forma = crear_rectangulo_redondeado(
    canvas, 310, 365, 590, 405, radio=15, fill="#e063a9", outline="#2b1331", width=1
)

btn_texto = canvas.create_text(
    450, 385,
    text="Registrar Reserva",
    fill="white",
    font=("Century Gothic", 12, "bold")
)

btn_cancelar_forma = crear_rectangulo_redondeado(
    canvas, 160, 365, 290, 405, radio=15, fill="#e063a9", outline="#2b1331", width=1
)

btn_cancelar_texto = canvas.create_text(
    225, 385,
    text="Cancelar",
    fill="white",
    font=("Century Gothic", 12, "bold")
)


def on_enter(event):
    canvas.itemconfig(btn_forma, fill="#ffdef2", outline="#2b1331")
    canvas.itemconfig(btn_texto, fill="#2b1331")
    canvas.config(cursor="heart")


def on_leave(event):
    canvas.itemconfig(btn_forma, fill="#e063a9", outline="#2b1331")
    canvas.itemconfig(btn_texto, fill="white")
    canvas.config(cursor="")


def on_enter_cancelar(event):
    canvas.itemconfig(btn_cancelar_forma, fill="#ffdef2", outline="#2b1331")
    canvas.itemconfig(btn_cancelar_texto, fill="#2b1331")
    canvas.config(cursor="heart")


def on_leave_cancelar(event):
    canvas.itemconfig(btn_cancelar_forma, fill="#e063a9", outline="#2b1331")
    canvas.itemconfig(btn_cancelar_texto, fill="white")
    canvas.config(cursor="")


for elemento in (btn_forma, btn_texto):
    canvas.tag_bind(elemento, "<Button-1>", registrar_reserva)
    canvas.tag_bind(elemento, "<Enter>", on_enter)
    canvas.tag_bind(elemento, "<Leave>", on_leave)

for elemento in (btn_cancelar_forma, btn_cancelar_texto):
    canvas.tag_bind(elemento, "<Button-1>", solicitar_cancelacion_reserva)
    canvas.tag_bind(elemento, "<Enter>", on_enter_cancelar)
    canvas.tag_bind(elemento, "<Leave>", on_leave_cancelar)


if img_kuromi_btn:
    canvas.create_image(565, 305, image=img_kuromi_btn, anchor="nw")


componentes_tooltip = []

texto_firma = canvas.create_text(
    830, 685,
    text="Daniela Niño",
    fill="#2b1331",
    font=("Century Gothic", 10, "italic bold"),
    anchor="se"
)


def mostrar_mensaje_agradecimiento(event):
    global componentes_tooltip
    canvas.config(cursor="heart")

    if componentes_tooltip:
        return

    x_fin = 830
    x_ini = 440
    y = 660
    mensaje_txt = "Gracias mi mejor intento de trabajo sola :3"

    fondo_tooltip = crear_rectangulo_redondeado(
        canvas, x_ini, y - 25, x_fin, y, radio=8, fill="#ffffff", outline="#2b1331", width=1
    )

    contenido_tooltip = canvas.create_text(
        (x_ini + x_fin) // 2, y - 12,
        text=mensaje_txt,
        fill="#2b1331",
        font=("Century Gothic", 9, "bold"),
        justify="center"
    )

    componentes_tooltip.extend([fondo_tooltip, contenido_tooltip])


def ocultar_mensaje_agradecimiento(event):
    global componentes_tooltip
    canvas.config(cursor="")

    for item in componentes_tooltip:
        canvas.delete(item)
    componentes_tooltip.clear()


canvas.tag_bind(texto_firma, "<Enter>", mostrar_mensaje_agradecimiento)
canvas.tag_bind(texto_firma, "<Leave>", ocultar_mensaje_agradecimiento)


ventana.mainloop()