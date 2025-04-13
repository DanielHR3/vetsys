import os
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

from tkcalendar import DateEntry

from models.paciente import obtener_pacientes
from models.receta import (editar_receta, eliminar_receta, guardar_receta,
                           obtener_recetas_por_paciente)
from utils.pdf_utils import generar_receta_pdf


def volver_al_menu():
    from views.dashboard import mostrar_menu

    mostrar_menu()


def ventana_recetas():
    receta_editando = {"id": None}

    def cargar_recetas():
        paciente_nombre = combo_paciente.get()
        if not paciente_nombre:
            return
        paciente_id = pacientes_dict[paciente_nombre]
        registros = obtener_recetas_por_paciente(paciente_id)

        tabla.delete(*tabla.get_children())
        for r in registros:
            tabla.insert("", "end", values=r)

    def guardar_o_actualizar():
        paciente_nombre = combo_paciente.get()
        if not paciente_nombre:
            messagebox.showwarning("Advertencia", "Debes seleccionar un paciente.")
            return

        paciente_id = pacientes_dict[paciente_nombre]
        fecha = date_fecha.get()
        diagnostico = entry_diagnostico.get()
        medicamentos = txt_medicamentos.get("1.0", tk.END).strip()
        instrucciones = txt_instrucciones.get("1.0", tk.END).strip()

        try:
            if receta_editando["id"]:
                editar_receta(
                    receta_editando["id"],
                    paciente_id,
                    fecha,
                    diagnostico,
                    medicamentos,
                    instrucciones,
                )
                messagebox.showinfo("Actualizado", "Receta actualizada correctamente.")
                btn_guardar.config(text="Guardar Receta")
                receta_editando["id"] = None
            else:
                guardar_receta(
                    paciente_id, fecha, diagnostico, medicamentos, instrucciones
                )
                messagebox.showinfo("Guardado", "Receta registrada correctamente.")

            limpiar_campos()
            cargar_recetas()

            ruta = generar_receta_pdf(
                paciente_nombre, fecha, diagnostico, medicamentos, instrucciones
            )
            messagebox.showinfo("PDF generado", f"Receta exportada:\n{ruta}")
            abrir_pdf(ruta)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la receta:\n{e}")

    def llenar_formulario(event):
        seleccionado = tabla.selection()
        if not seleccionado:
            return
        datos = tabla.item(seleccionado)["values"]
        receta_editando["id"] = datos[0]
        date_fecha.set_date(datos[1])
        entry_diagnostico.delete(0, tk.END)
        entry_diagnostico.insert(0, datos[2])
        txt_medicamentos.delete("1.0", tk.END)
        txt_medicamentos.insert("1.0", datos[3])
        txt_instrucciones.delete("1.0", tk.END)
        txt_instrucciones.insert("1.0", datos[4])
        btn_guardar.config(text="Actualizar Receta")

    def eliminar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning(
                "Selecciona una receta", "Debes seleccionar una receta."
            )
            return
        datos = tabla.item(seleccionado)["values"]
        confirm = messagebox.askyesno("Eliminar", "¿Eliminar esta receta?")
        if confirm:
            eliminar_receta(datos[0])
            cargar_recetas()
            limpiar_campos()
            messagebox.showinfo("Eliminado", "Receta eliminada correctamente.")

    def exportar_pdf():
        seleccionado = tabla.focus()
        if not seleccionado:
            messagebox.showwarning(
                "Selecciona una receta", "Debes seleccionar una receta."
            )
            return
        receta = tabla.item(seleccionado)["values"]
        if not receta:
            return

        paciente_nombre = combo_paciente.get()
        fecha, diagnostico, medicamentos, instrucciones = receta[1:5]
        try:
            ruta = generar_receta_pdf(
                paciente_nombre, fecha, diagnostico, medicamentos, instrucciones
            )
            messagebox.showinfo("PDF generado", f"Receta exportada:\n{ruta}")
            abrir_pdf(ruta)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF:\n{e}")

    def abrir_pdf(ruta):
        if platform.system() == "Windows":
            os.startfile(ruta)
        elif platform.system() == "Darwin":
            subprocess.call(["open", ruta])
        else:
            subprocess.call(["xdg-open", ruta])

    def limpiar_campos():
        entry_diagnostico.delete(0, tk.END)
        txt_medicamentos.delete("1.0", tk.END)
        txt_instrucciones.delete("1.0", tk.END)
        receta_editando["id"] = None
        btn_guardar.config(text="Guardar Receta")

    # VENTANA
    win = tk.Tk()
    win.title("VetSys - Recetas Médicas")
    win.geometry("980x600")
    win.configure(bg="#e8f0fe")

    tk.Label(
        win,
        text="Recetas Médicas",
        font=("Segoe UI", 18, "bold"),
        bg="#e8f0fe",
        fg="#0d47a1",
    ).pack(pady=10)

    form = tk.Frame(win, bg="#e8f0fe")
    form.pack(pady=10)

    pacientes = obtener_pacientes()
    pacientes_dict = {f"{p[1]} (ID {p[0]})": p[0] for p in pacientes}

    tk.Label(form, text="Paciente", bg="#e8f0fe").grid(row=0, column=0)
    combo_paciente = ttk.Combobox(form, values=list(pacientes_dict.keys()), width=30)
    combo_paciente.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form, text="Fecha", bg="#e8f0fe").grid(row=0, column=2)
    date_fecha = DateEntry(
        form,
        width=15,
        background="darkblue",
        foreground="white",
        date_pattern="yyyy-mm-dd",
    )
    date_fecha.grid(row=0, column=3)

    tk.Label(form, text="Diagnóstico", bg="#e8f0fe").grid(row=1, column=0, pady=5)
    entry_diagnostico = tk.Entry(form, width=60)
    entry_diagnostico.grid(row=1, column=1, columnspan=3, padx=5)

    tk.Label(form, text="Medicamentos", bg="#e8f0fe").grid(row=2, column=0, pady=5)
    txt_medicamentos = tk.Text(form, width=70, height=4)
    txt_medicamentos.grid(row=2, column=1, columnspan=3, padx=5)

    tk.Label(form, text="Instrucciones", bg="#e8f0fe").grid(row=3, column=0, pady=5)
    txt_instrucciones = tk.Text(form, width=70, height=4)
    txt_instrucciones.grid(row=3, column=1, columnspan=3, padx=5)

    # BOTONES
    btn_frame = tk.Frame(win, bg="#e8f0fe")
    btn_frame.pack(pady=10)

    btn_guardar = tk.Button(
        btn_frame, text="Guardar Receta", width=20, command=guardar_o_actualizar
    )
    btn_guardar.pack(side=tk.LEFT, padx=10)

    tk.Button(btn_frame, text="Eliminar", width=20, command=eliminar).pack(
        side=tk.LEFT, padx=10
    )
    tk.Button(btn_frame, text="Exportar a PDF", width=20, command=exportar_pdf).pack(
        side=tk.LEFT, padx=10
    )

    tk.Button(
        win,
        text="Volver al Menú",
        width=20,
        bg="#dfefff",
        command=lambda: [win.destroy(), volver_al_menu()],
    ).pack(pady=10)

    tabla = ttk.Treeview(
        win,
        columns=("ID", "Fecha", "Diagnóstico", "Medicamentos", "Instrucciones"),
        show="headings",
        height=10,
    )
    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
    tabla.bind("<<TreeviewSelect>>", llenar_formulario)

    combo_paciente.bind("<<ComboboxSelected>>", lambda e: cargar_recetas())
    win.mainloop()
