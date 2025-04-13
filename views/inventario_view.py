"""Vista del módulo de inventario para VetSys."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from models.inventario import actualizar_articulo
from models.inventario import agregar_articulo as modelo_agregar_articulo
from models.inventario import eliminar_articulo as modelo_eliminar_articulo
from models.inventario import obtener_inventario


def ventana_inventario():
    """Abre la ventana de gestión del inventario."""

    def cargar_imagen():
        ruta = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif")]
        )
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
        from views.dashboard import mostrar_menu

        mostrar_menu()

    def limpiar_campos():
        for entry in entradas.values():
            entry.delete(0, tk.END)
        tabla.selection_remove(tabla.selection())

    def cargar_tabla():
        tabla.delete(*tabla.get_children())
        for art in obtener_inventario():
            tabla.insert("", tk.END, values=art)

    def agregar():
        try:
            datos = [
                entradas[campo].get()
                for campo in [
                    "artículo",
                    "marca",
                    "submarca",
                    "sku",
                    "código de barras",
                    "unidad",
                    "precio",
                    "categoria",
                    "subcategoria",
                    "descripcion",
                    "imagen",
                ]
            ]
            modelo_agregar_articulo(*datos)
            messagebox.showinfo("Éxito", "Artículo agregado correctamente.")
            cargar_tabla()
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar: {e}")

    def modificar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning(
                "Advertencia", "Selecciona un artículo para modificar."
            )
            return
        try:
            id_articulo = tabla.item(seleccionado)["values"][0]
            datos = [
                entradas[campo].get()
                for campo in [
                    "artículo",
                    "marca",
                    "submarca",
                    "sku",
                    "código de barras",
                    "unidad",
                    "precio",
                    "categoria",
                    "subcategoria",
                    "descripcion",
                    "imagen",
                ]
            ]
            actualizar_articulo(id_articulo, *datos)
            messagebox.showinfo("Éxito", "Artículo actualizado correctamente.")
            cargar_tabla()
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar: {e}")

    def eliminar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning(
                "Advertencia", "Selecciona un artículo para eliminar."
            )
            return
        try:
            id_articulo = tabla.item(seleccionado)["values"][0]
            modelo_eliminar_articulo(id_articulo)
            messagebox.showinfo("Éxito", "Artículo eliminado correctamente.")
            cargar_tabla()
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    subcategorias = {
        "Medicamentos": ["Antibióticos", "Vacunas", "Desparasitantes"],
        "Alimentos": ["Cachorro", "Adulto", "Geriátrico"],
        "Accesorios": ["Correas", "Juguetes", "Camas"],
        "Higiene": ["Shampoo", "Toallitas", "Desinfectantes"],
        "Servicios": ["Consulta", "Baño", "Corte de uñas"],
    }

    win = tk.Tk()
    win.title("VetSys - Inventario")
    win.geometry("1100x620")
    win.configure(bg="#f4f6f9")

    tk.Label(
        win,
        text="Gestión de Inventario",
        font=("Segoe UI", 18, "bold"),
        bg="#f4f6f9",
        fg="#0d47a1",
    ).pack(pady=10)

    form = tk.Frame(win, bg="#f4f6f9")
    form.pack(pady=5)

    campos = [
        ("Artículo", 0, 0),
        ("Marca", 0, 2),
        ("Submarca", 0, 4),
        ("SKU", 1, 0),
        ("Código de Barras", 1, 2),
        ("Unidad", 1, 4),
        ("Precio", 2, 0),
        ("Categoría", 2, 2),
        ("Subcategoría", 2, 4),
        ("Descripción", 3, 0),
        ("Imagen", 4, 0),
    ]

    entradas = {}

    for texto, fila, columna in campos:
        tk.Label(form, text=texto, bg="#f4f6f9").grid(
            row=fila, column=columna, padx=5, pady=4, sticky="e"
        )

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
            tk.Button(form, text="Cargar Imagen", command=cargar_imagen).grid(
                row=fila, column=5, padx=5
            )
            entradas["imagen"] = entry_img
        else:
            entry = tk.Entry(form, width=25)
            entry.grid(row=fila, column=columna + 1, padx=5, pady=4)
            entradas[texto.lower()] = entry

    # Tabla
    global tabla
    tabla = ttk.Treeview(
        win,
        columns=(
            "ID",
            "Artículo",
            "Marca",
            "Submarca",
            "SKU",
            "Código",
            "Unidad",
            "Precio",
            "Categoría",
            "Subcategoría",
            "Imagen",
        ),
        show="headings",
    )
    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)
    tabla.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Botones
    botones_frame = tk.Frame(win, bg="#f4f6f9")
    botones_frame.pack(pady=5)

    tk.Button(
        botones_frame,
        text="Agregar",
        width=15,
        bg="#00b894",
        fg="white",
        command=agregar,
    ).pack(side=tk.LEFT, padx=5)
    tk.Button(
        botones_frame,
        text="Modificar",
        width=15,
        bg="#0984e3",
        fg="white",
        command=modificar,
    ).pack(side=tk.LEFT, padx=5)
    tk.Button(
        botones_frame,
        text="Eliminar",
        width=15,
        bg="#d63031",
        fg="white",
        command=eliminar,
    ).pack(side=tk.LEFT, padx=5)
    tk.Button(
        botones_frame,
        text="Limpiar",
        width=15,
        bg="#636e72",
        fg="white",
        command=limpiar_campos,
    ).pack(side=tk.LEFT, padx=5)

    tk.Button(win, text="Volver al Menú", width=20, command=volver).pack(pady=10)

    cargar_tabla()
    win.mainloop()
