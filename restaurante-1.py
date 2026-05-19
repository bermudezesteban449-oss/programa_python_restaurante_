# ==========================================
# TRABAJO FINAL - PROGRAMACIÓN
# Problema 2: Promoción en menú restaurante
# ==========================================

from tkinter import *
from tkinter import ttk

menu = [
    ["Hamburguesa", "Comida Rapida", 25000],
    ["Pizza", "Comida Rapida", 32000],
    ["Ensalada Cesar", "Saludable", 18000],
    ["Sushi", "Marina", 45000],
    ["Pasta Alfredo", "Italiana", 38000],
    ["Tacos", "Mexicana", 22000]
]

categoria_objetivo = "Comida Rapida"
umbral_precio = 24000


# ==========================================
# FUNCIÓN PARA CALCULAR EL PRECIO FINAL
# ==========================================
def calcular_precio_final(categoria, precio_base):
    if categoria == categoria_objetivo and precio_base > umbral_precio:
        descuento = precio_base * 0.15
        precio_final = precio_base - descuento
    else:
        precio_final = precio_base
    return precio_final


# ==========================================
# MOSTRAR RESULTADOS EN CONSOLA
# ==========================================
print("===== MENÚ DEL RESTAURANTE =====\n")
for producto in menu:
    nombre, categoria, precio_base = producto
    precio_final = calcular_precio_final(categoria, precio_base)
    print("Producto:", nombre)
    print("Categoría:", categoria)
    print("Precio Base: $", precio_base)
    print("Precio Final: $", precio_final)
    print("-----------------------------------")


# ==========================================
# INTERFAZ GRÁFICA - ORGANIZADA POR CATEGORÍA
# ==========================================

# Colores por categoría
COLORES_CATEGORIA = {
    "Comida Rapida": "#E74C3C",
    "Saludable":     "#27AE60",
    "Marina":      "#21AAE9",
    "Italiana":      "#BCB90D",
    "Mexicana":      "#E67E22",
}
COLOR_DEFAULT = "#7F8C8D"

ventana = Tk()
ventana.title("MENÚ RESTAURANTE")
ventana.geometry("720x600")
ventana.config(bg="#1C1C2E")
ventana.resizable(True, True)

# ── Título principal ──────────────────────────────────────────
titulo = Label(
    ventana,
    text=" MENÚ DEL RESTAURANTE",
    font=("Georgia", 22, "bold"),
    bg="#1C1C2E",
    fg="#F0E6D3",
    pady=12
)
titulo.pack(fill=X)

# Línea separadora
Canvas(ventana, height=2, bg="#F0E6D3", bd=0, highlightthickness=0).pack(fill=X, padx=20)

# ── Frame con scroll ──────────────────────────────────────────
contenedor = Frame(ventana, bg="#1C1C2E")
contenedor.pack(fill=BOTH, expand=True, padx=20, pady=10)

canvas = Canvas(contenedor, bg="#1C1C2E", highlightthickness=0)
scrollbar = Scrollbar(contenedor, orient=VERTICAL, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side=RIGHT, fill=Y)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

frame_scroll = Frame(canvas, bg="#1C1C2E")
canvas.create_window((0, 0), window=frame_scroll, anchor="nw")

def actualizar_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame_scroll.bind("<Configure>", actualizar_scroll)

# ── Agrupar productos por categoría ───────────────────────────
categorias = {}
for producto in menu:
    nombre, categoria, precio = producto
    categorias.setdefault(categoria, []).append(producto)

# Anchos fijos de columna en píxeles
ANCHOS_COL = [220, 140, 120, 140]

# ── Renderizar cada categoría ─────────────────────────────────
for categoria, productos in categorias.items():
    color = COLORES_CATEGORIA.get(categoria, COLOR_DEFAULT)

    # Encabezado de categoría
    header_frame = Frame(frame_scroll, bg=color, pady=6, padx=12)
    header_frame.pack(fill=X, pady=(14, 0))
    Label(
        header_frame,
        text=f"  {categoria.upper()}",
        font=("Georgia", 13, "bold"),
        bg=color, fg="white", anchor="w"
    ).pack(fill=X)

    # Una sola línea para el encabezado de columnas y todas las filas
    tabla = Frame(frame_scroll, bg="#1E1E30")
    tabla.pack(fill=X)

    # Configurar anchos fijos de columna (minsize en píxeles)
    for col_idx, ancho in enumerate(ANCHOS_COL):
        tabla.columnconfigure(col_idx, minsize=ancho)

    # Fila 0: encabezados de columna
    encabezados = ["PRODUCTO", "PRECIO BASE", "DESCUENTO", "PRECIO FINAL"]
    for col_idx, texto in enumerate(encabezados):
        Label(
            tabla,
            text=texto,
            font=("Courier", 9, "bold"),
            bg="#2A2A3E",
            fg="#AAA8C2",
            anchor="w",
            padx=10,
            pady=4
        ).grid(row=0, column=col_idx, sticky="ew")

    # Filas de productos (row 1 en adelante)
    for i, prod in enumerate(productos):
        nombre, cat, precio_base = prod
        precio_final = calcular_precio_final(cat, precio_base)
        tiene_descuento = precio_final < precio_base

        fila_bg = "#1E1E30" if i % 2 == 0 else "#252538"
        fila = i + 1  # row en el grid (0 es el encabezado)

        # Nombre
        Label(tabla, text=nombre, font=("Helvetica", 11),
              bg=fila_bg, fg="#F0E6D3", anchor="w",
              padx=10, pady=6
        ).grid(row=fila, column=0, sticky="ew")

        # Precio base (tachado si hay descuento)
        estilo_base = ("Helvetica", 11, "overstrike") if tiene_descuento else ("Helvetica", 11)
        color_base  = "#888" if tiene_descuento else "#F0E6D3"
        Label(tabla, text=f"${precio_base:,.0f}",
              font=estilo_base, bg=fila_bg, fg=color_base,
              anchor="w", padx=10
        ).grid(row=fila, column=1, sticky="ew")

        # Descuento
        descuento_texto = "15% OFF 🏷" if tiene_descuento else "—"
        descuento_color = "#E01A10" if tiene_descuento else "#555"
        Label(tabla, text=descuento_texto,
              font=("Helvetica", 10, "bold"), bg=fila_bg, fg=descuento_color,
              anchor="w", padx=10
        ).grid(row=fila, column=2, sticky="ew")

        # Precio final
        color_final = "#2ECC71" if tiene_descuento else "#F0E6D3"
        Label(tabla, text=f"${precio_final:,.0f}",
              font=("Helvetica", 11, "bold"), bg=fila_bg, fg=color_final,
              anchor="w", padx=10
        ).grid(row=fila, column=3, sticky="ew")

# ── Leyenda al pie ─────────────────────────────────────────────
Canvas(ventana, height=2, bg="#F0E6D3", bd=0, highlightthickness=0).pack(fill=X, padx=20)
Label(
    ventana,
    text="- Descuento del 15% para Comida Rápida con precio mayor a $24.000",
    font=("Helvetica", 11, "italic"),
    bg="#1C1C2E",
    fg="#AAA8C2",
    pady=8
).pack()

ventana.mainloop()
