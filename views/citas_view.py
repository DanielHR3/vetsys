import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.cita import guardar_cita, obtener_citas, editar_cita, eliminar_cita
from models.paciente import obtener_pacientes
from utils.calendar_utils import generar_archivo_calendario
from utils.email_utils import enviar_correo


def volver_al_menu():
    from views.dashboard import mostrar_menu
    mostrar_menu()


def ventana_citas():
    cita_editando = {"id": None}  # ID temporal para edición

    def actualizar_tabla():
        for row in tabla.get_children():
            tabla.delete(row)
        for cita in obtener_citas():
            tabla.insert("", "end", values=cita)

    def guardar_o_actualizar():
        if not combo_paciente.get() or not date_fecha.get() or not combo_hora.get():
            messagebox.showwarning("Faltan datos", "Completa todos los campos.")
            return

        paciente_nombre = combo_paciente.get()
        paciente_id = pacientes_dict[paciente_nombre]
        correo = entry_correo.get()
        fecha = date_fecha.get()
        hora = combo_hora.get()
        motivo = entry_motivo.get()

        if cita_editando["id"]:
            editar_cita(cita_editando["id"], paciente_id, fecha, hora, motivo)
            messagebox.showinfo("Cita actualizada", "La cita fue modificada correctamente.")
            btn_guardar.config(text="Guardar Cita")
            cita_editando["id"] = None
        else:
            guardar_cita(paciente_id, fecha, hora, motivo, correo)
            messagebox.showinfo("Cita guardada", "La cita fue registrada correctamente.")

        actualizar_tabla()
        cancelar()

    def llenar_formulario(event):
        seleccionado = tabla.selection()
        if not seleccionado:
            return
        datos = tabla.item(seleccionado)["values"]
        cita_editando["id"] = datos[0]
        combo_paciente.set(datos[1])
        date_fecha.set_date(datos[2])
        combo_hora.set(datos[3])
        entry_motivo.delete(0, tk.END)
        entry_motivo.insert(0, datos[4])
        btn_guardar.config(text="Actualizar Cita")

    def eliminar():
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Selecciona una cita", "Selecciona una cita para eliminar.")
            return
        datos = tabla.item(seleccionado)["values"]
        confirm = messagebox.askyesno("Eliminar", f"¿Eliminar la cita de {datos[1]} el {datos[2]}?")
        if confirm:
            eliminar_cita(datos[0])
            actualizar_tabla()
            cancelar()
            messagebox.showinfo("Eliminado", "La cita fue eliminada correctamente.")

    def enviar_email():
        paciente = combo_paciente.get()
        correo = entry_correo.get()
        fecha = date_fecha.get()
        hora = combo_hora.get()
        motivo = entry_motivo.get()
        archivo = generar_archivo_calendario(paciente, fecha, hora, motivo)
        if enviar_correo(correo, paciente, fecha, hora, motivo, archivo):
            messagebox.showinfo("Correo enviado", "Confirmación enviada con archivo .ics.")
        else:
            messagebox.showerror("Error", "No se pudo enviar el correo.")

    def generar_calendario():
        paciente = combo_paciente.get()
        archivo = generar_archivo_calendario(paciente, date_fecha.get(), combo_hora.get(), entry_motivo.get())
        messagebox.showinfo("Calendario", f"Archivo .ics generado: {archivo}")

    def cancelar():
        combo_paciente.set("")
        from datetime import datetime
        date_fecha.set_date(datetime.today())
        combo_hora.set("")
        entry_motivo.delete(0, tk.END)
        entry_correo.delete(0, tk.END)
        cita_editando["id"] = None
        btn_guardar.config(text="Guardar Cita")

    # Ventana principal
    win = tk.Tk()
    win.title("VetSys - Citas")
    win.geometry("980x600")
    win.configure(bg="#e8f0fe")

    ttk.Style().configure("TButton", padding=6, relief="flat", background="#1976d2", foreground="black")

    # Título
    tk.Label(win, text="Gestión de Citas", font=("Segoe UI", 18, "bold"), bg="#e8f0fe", fg="#0d47a1").pack(pady=10)

    # Formulario
    form_frame = tk.Frame(win, bg="#e8f0fe")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Paciente", bg="#e8f0fe").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    tk.Label(form_frame, text="Fecha", bg="#e8f0fe").grid(row=0, column=2, padx=10, pady=5, sticky="e")
    tk.Label(form_frame, text="Hora", bg="#e8f0fe").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    tk.Label(form_frame, text="Motivo", bg="#e8f0fe").grid(row=1, column=2, padx=10, pady=5, sticky="e")
    tk.Label(form_frame, text="Correo", bg="#e8f0fe").grid(row=2, column=0, padx=10, pady=5, sticky="e")

    pacientes = obtener_pacientes()
    pacientes_dict = {f"{p[1]} (ID {p[0]})": p[0] for p in pacientes}
    combo_paciente = ttk.Combobox(form_frame, values=list(pacientes_dict.keys()), width=30)
    combo_paciente.grid(row=0, column=1)

    date_fecha = DateEntry(form_frame, width=12, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
    date_fecha.grid(row=0, column=3)

    horas = [f"{h:02d}:00" for h in range(8, 21)]
    combo_hora = ttk.Combobox(form_frame, values=horas, width=10)
    combo_hora.grid(row=1, column=1)

    entry_motivo = tk.Entry(form_frame, width=30)
    entry_motivo.grid(row=1, column=3)

    entry_correo = tk.Entry(form_frame, width=30)
    entry_correo.grid(row=2, column=1)

    # Botones
    btn_frame = tk.Frame(win, bg="#e8f0fe")
    btn_frame.pack(pady=10)

    btn_guardar = tk.Button(btn_frame, text="Guardar Cita", width=15, command=guardar_o_actualizar)
    btn_guardar.grid(row=0, column=0, padx=5)

    tk.Button(btn_frame, text="Eliminar", width=15, command=eliminar).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Enviar Correo", width=15, command=enviar_email).grid(row=0, column=2, padx=5)
    tk.Button(btn_frame, text="Generar .ics", width=15, command=generar_calendario).grid(row=0, column=3, padx=5)
    tk.Button(btn_frame, text="Cancelar", width=15, command=cancelar).grid(row=0, column=4, padx=5)

    tk.Button(win, text="Volver al Menú", width=20, bg="#dfefff", command=lambda: [win.destroy(), volver_al_menu()]).pack(pady=10)

    # Tabla
    tabla = ttk.Treeview(win, columns=("ID", "Paciente", "Fecha", "Hora", "Motivo"), show="headings", height=10)
    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
    tabla.bind("<<TreeviewSelect>>", llenar_formulario)

    actualizar_tabla()
    win.mainloop()
