"""Vista del módulo de inventario para VetSys."""

import tkinter as tk
from tkinter import ttk, filedialog


def ventana_inventario():
    """Abre la ventana de gestión del inventario."""

    def cargar_imagen():
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif")])
        if ruta:
            entradas["imagen"].delete(0, tk.END)
            entradas["imagen"].insert(0, ruta)

    def actualizar_subcategorias():
        categoria = entradas["categoria"].get()
        subcats = subcategorias.get(categoria, [])
        entradas["subcategoria"].config(values=subcats)
        if subcats:
            entradas["subcategoria"].current(0)

    def volver():
        win.destroy()
        from views.dashboard import mostrar_menu  # Importación diferida aquí
        mostrar_menu()

    # Subcategorías por tipo
    subcategorias = {
        "Medicamentos": ["Antibióticos", "Vacunas", "Desparasitantes"],
        "Alimentos": ["Cachorro", "Adulto", "Geriátrico"],
        "Accesorios": ["Correas", "Juguetes", "Camas"],
        "Higiene": ["Shampoo", "Toallitas", "Desinfectantes"],
        "Servicios": ["Consulta", "Baño", "Corte de uñas"]
    }

    win = tk.Tk()
    win.title("VetSys - Inventario")
    win.geometry("1100x620")
    win.configure(bg="#f4f6f9")

    tk.Label(win, text="Gestión de Inventario", font=("Segoe UI", 18, "bold"),
             bg="#f4f6f9", fg="#0d47a1").pack(pady=10)

    form = tk.Frame(win, bg="#f4f6f9")
    form.pack(pady=5)

    campos = [
        ("Artículo", 0, 0), ("Marca", 0, 2), ("Submarca", 0, 4),
        ("SKU", 1, 0), ("Código de Barras", 1, 2), ("Unidad", 1, 4),
        ("Precio", 2, 0), ("Categoría", 2, 2), ("Subcategoría", 2, 4),
        ("Descripción", 3, 0), ("Imagen", 4, 0)
    ]

    entradas = {}

    for texto, fila, columna in campos:
        tk.Label(form, text=texto, bg="#f4f6f9").grid(
            row=fila, column=columna, padx=5, pady=4, sticky="e")

        if texto == "Categoría":
            combo_cat = ttk.Combobox(form, width=22, values=list(subcategorias.keys()))
            combo_cat.grid(row=fila, column=columna + 1, padx=5, pady=4)
            combo_cat.bind("<<ComboboxSelected>>", lambda _: actualizar_subcategorias())
            entradas["categoria"] = combo_cat
        elif texto == "Subcategoría":
            combo_sub = ttk.Combobox(form, width=22)
            combo_sub.grid(row=fila, column=columna + 1, padx=5, pady=4)
            entradas["subcategoria"] = combo_sub
        elif texto == "Descripción":
            entry = tk.Entry(form, width=70)
            entry.grid(row=fila, column=1, columnspan=5, padx=5, pady=4)
            entradas["descripcion"] = entry
        elif texto == "Imagen":
            entry_img = tk.Entry(form, width=60)
            entry_img.grid(row=fila, column=1, columnspan=4, padx=5, pady=4)
            tk.Button(
                form, text="Cargar Imagen", command=cargar_imagen).grid(row=fila, column=5, padx=5)
            entradas["imagen"] = entry_img
        else:
            entry = tk.Entry(form, width=25)
            entry.grid(row=fila, column=columna + 1, padx=5, pady=4)
            entradas[texto.lower()] = entry

    # Tabla
    tabla = ttk.Treeview(
        win,
        columns=("ID", "Artículo", "Marca", "Submarca", "SKU", "Código", "Unidad",
                 "Precio", "Categoría", "Subcategoría", "Imagen"),
        show="headings"
    )
    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Botón volver
    tk.Button(win, text="Volver al menú", command=volver).pack(pady=10)

    win.mainloop()
