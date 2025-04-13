import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models.paciente import (agregar_paciente, editar_paciente,
                             eliminar_paciente, obtener_pacientes)


def volver_al_menu():
    from views.dashboard import mostrar_menu

    mostrar_menu()


def ventana_pacientes():
    def cargar_pacientes():
        tabla.delete(*tabla.get_children())
        for p in obtener_pacientes():
            tabla.insert("", "end", values=p)

    def guardar():
        datos = obtener_datos_formulario()
        if not validar_datos(datos):
            return
        agregar_paciente(*datos)
        limpiar()
        cargar_pacientes()
        messagebox.showinfo("Guardado", "Paciente agregado correctamente.")

    def editar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Editar paciente", "Debes seleccionar un paciente.")
            return
        paciente = tabla.item(seleccionado)["values"]
        id_paciente = paciente[0]
        datos = obtener_datos_formulario()
        if not validar_datos(datos):
            return
        confirm = messagebox.askyesno(
            "Confirmar edición", f"¿Actualizar datos del paciente '{datos[0]}'?"
        )
        if confirm:
            editar_paciente(id_paciente, *datos)
            cargar_pacientes()
            limpiar()
            messagebox.showinfo(
                "Editado", f"Paciente '{datos[0]}' actualizado correctamente."
            )

    def eliminar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning(
                "Eliminar paciente", "Debes seleccionar un paciente."
            )
            return
        paciente = tabla.item(seleccionado)["values"]
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar a {paciente[1]}?")
        if confirm:
            eliminar_paciente(paciente[0])
            cargar_pacientes()
            limpiar()
            messagebox.showinfo("Eliminado", "Paciente eliminado correctamente.")

    def llenar_formulario(event):
        seleccionado = tabla.selection()
        if seleccionado:
            datos = tabla.item(seleccionado)["values"]
            entry_nombre.delete(0, tk.END)
            entry_nombre.insert(0, datos[1])
            entry_especie.delete(0, tk.END)
            entry_especie.insert(0, datos[2])
            entry_raza.delete(0, tk.END)
            entry_raza.insert(0, datos[3])
            entry_sexo.delete(0, tk.END)
            entry_sexo.insert(0, datos[4])
            entry_nacimiento.delete(0, tk.END)
            entry_nacimiento.insert(0, datos[5])
            entry_propietario.delete(0, tk.END)
            entry_propietario.insert(0, datos[6])
            entry_contacto.delete(0, tk.END)
            entry_contacto.insert(0, datos[7])

    def limpiar():
        for e in entradas:
            e.delete(0, tk.END)

    def obtener_datos_formulario():
        return (
            entry_nombre.get().strip(),
            entry_especie.get().strip(),
            entry_raza.get().strip(),
            entry_sexo.get().strip(),
            entry_nacimiento.get().strip(),
            entry_propietario.get().strip(),
            entry_contacto.get().strip(),
        )

    def validar_datos(datos):
        if not all(datos):
            messagebox.showwarning(
                "Campos incompletos", "Todos los campos son obligatorios."
            )
            return False
        return True

    # Ventana
    win = tk.Tk()
    win.title("VetSys - Pacientes")
    win.geometry("1100x650")
    win.configure(bg="#e8f0fe")

    # Estilo general
    style = ttk.Style()
    style.configure("Treeview", font=("Segoe UI", 10))
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    style.map("TButton", background=[("active", "#1976d2")])

    # Encabezado
    tk.Label(
        win,
        text="Gestión de Pacientes",
        font=("Segoe UI", 18, "bold"),
        bg="#e8f0fe",
        fg="#0d47a1",
    ).pack(pady=10)

    # Formulario
    form = tk.Frame(win, bg="#e8f0fe")
    form.pack(pady=10)

    labels = [
        "Nombre",
        "Especie",
        "Raza",
        "Sexo",
        "Nacimiento",
        "Propietario",
        "Contacto",
    ]
    entradas = []
    for idx, label in enumerate(labels):
        tk.Label(
            form, text=label, bg="#e8f0fe", fg="#1a237e", font=("Segoe UI", 10)
        ).grid(row=idx // 2, column=(idx % 2) * 2, padx=10, pady=8, sticky="e")
        entry = tk.Entry(form, width=30, font=("Segoe UI", 10))
        entry.grid(row=idx // 2, column=(idx % 2) * 2 + 1, padx=10)
        entradas.append(entry)

    (
        entry_nombre,
        entry_especie,
        entry_raza,
        entry_sexo,
        entry_nacimiento,
        entry_propietario,
        entry_contacto,
    ) = entradas

    # Botones
    btn_frame = tk.Frame(win, bg="#e8f0fe")
    btn_frame.pack(pady=15)

    ttk.Button(btn_frame, text="Agregar Paciente", command=guardar).pack(
        side=tk.LEFT, padx=10
    )
    ttk.Button(btn_frame, text="Editar Paciente", command=editar).pack(
        side=tk.LEFT, padx=10
    )
    ttk.Button(btn_frame, text="Eliminar Paciente", command=eliminar).pack(
        side=tk.LEFT, padx=10
    )
    ttk.Button(
        btn_frame,
        text="Volver al Menú",
        command=lambda: [win.destroy(), volver_al_menu()],
    ).pack(side=tk.LEFT, padx=10)

    # Separador visual
    ttk.Separator(win, orient="horizontal").pack(fill="x", pady=10)

    # Tabla
    tabla = ttk.Treeview(
        win,
        columns=(
            "ID",
            "Nombre",
            "Especie",
            "Raza",
            "Sexo",
            "Nacimiento",
            "Propietario",
            "Contacto",
        ),
        show="headings",
        height=12,
    )
    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, width=130 if col == "ID" else 140)
    tabla.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
    tabla.bind("<<TreeviewSelect>>", llenar_formulario)

    cargar_pacientes()
    win.mainloop()
