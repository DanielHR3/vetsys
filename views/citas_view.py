import tkinter as tk
from tkinter import messagebox, ttk

from tkcalendar import DateEntry

from models.cita import guardar_cita, obtener_citas
from models.paciente import obtener_pacientes
from utils.calendar_utils import generar_archivo_calendario
from utils.email_utils import enviar_correo


def volver_al_menu():
    from views.dashboard import mostrar_menu

    mostrar_menu()


def ventana_citas():
    def actualizar_tabla():
        for row in tabla.get_children():
            tabla.delete(row)
        for cita in obtener_citas():
            tabla.insert("", "end", values=cita)

    def guardar():
        if not combo_paciente.get() or not date_fecha.get() or not combo_hora.get():
            messagebox.showwarning("Faltan datos", "Completa todos los campos.")
            return

        paciente_nombre = combo_paciente.get()
        paciente_id = pacientes_dict[paciente_nombre]
        correo = entry_correo.get()

        guardar_cita(
            paciente_id, date_fecha.get(), combo_hora.get(), entry_motivo.get(), correo
        )
        actualizar_tabla()
        messagebox.showinfo("Cita guardada", "La cita fue registrada correctamente.")

    def enviar_email():
        paciente = combo_paciente.get()
        correo = entry_correo.get()
        fecha = date_fecha.get()
        hora = combo_hora.get()
        motivo = entry_motivo.get()

        archivo = generar_archivo_calendario(paciente, fecha, hora, motivo)

        if enviar_correo(correo, paciente, fecha, hora, motivo, archivo):
            messagebox.showinfo(
                "Correo enviado", "Se envió la confirmación con archivo adjunto."
            )
        else:
            messagebox.showerror("Error", "No se pudo enviar el correo.")

    def generar_calendario():
        paciente = combo_paciente.get()
        archivo = generar_archivo_calendario(
            paciente, date_fecha.get(), combo_hora.get(), entry_motivo.get()
        )
        messagebox.showinfo("Calendario", f"Archivo .ics generado: {archivo}")

    def cancelar():
        date_fecha.set_date("")
        combo_hora.set("")
        entry_motivo.delete(0, tk.END)
        entry_correo.delete(0, tk.END)
        combo_paciente.set("")

    win = tk.Tk()
    win.title("VetSys - Citas")
    win.geometry("880x550")
    win.configure(bg="#f4f6f9")

    title = tk.Label(
        win, text="Gestión de Citas", font=("Arial", 16, "bold"), bg="#f4f6f9"
    )
    title.pack(pady=10)

    form_frame = tk.Frame(win, bg="#f4f6f9")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Paciente", bg="#f4f6f9").grid(
        row=0, column=0, padx=10, pady=5
    )
    tk.Label(form_frame, text="Fecha", bg="#f4f6f9").grid(
        row=0, column=2, padx=10, pady=5
    )
    tk.Label(form_frame, text="Hora", bg="#f4f6f9").grid(
        row=1, column=0, padx=10, pady=5
    )
    tk.Label(form_frame, text="Motivo", bg="#f4f6f9").grid(
        row=1, column=2, padx=10, pady=5
    )
    tk.Label(form_frame, text="Correo", bg="#f4f6f9").grid(
        row=2, column=0, padx=10, pady=5
    )

    pacientes = obtener_pacientes()
    pacientes_dict = {f"{p[1]} (ID {p[0]})": p[0] for p in pacientes}
    combo_paciente = ttk.Combobox(
        form_frame, values=list(pacientes_dict.keys()), width=30
    )
    combo_paciente.grid(row=0, column=1)

    date_fecha = DateEntry(
        form_frame,
        width=12,
        background="darkblue",
        foreground="white",
        date_pattern="yyyy-mm-dd",
    )
    date_fecha.grid(row=0, column=3)

    horas = [f"{h:02d}:00" for h in range(8, 21)]  # 08:00 a 20:00
    combo_hora = ttk.Combobox(form_frame, values=horas, width=10)
    combo_hora.grid(row=1, column=1)

    entry_motivo = tk.Entry(form_frame, width=30)
    entry_motivo.grid(row=1, column=3)

    entry_correo = tk.Entry(form_frame, width=30)
    entry_correo.grid(row=2, column=1)

    # Botones
    btn_frame = tk.Frame(win, bg="#f4f6f9")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Guardar Cita", width=15, command=guardar).grid(
        row=0, column=0, padx=5
    )
    tk.Button(btn_frame, text="Enviar Correo", width=15, command=enviar_email).grid(
        row=0, column=1, padx=5
    )
    tk.Button(
        btn_frame, text="Generar .ics", width=15, command=generar_calendario
    ).grid(row=0, column=2, padx=5)
    tk.Button(btn_frame, text="Cancelar", width=15, command=cancelar).grid(
        row=0, column=3, padx=5
    )

    tk.Button(
        win,
        text="Volver al Menú",
        width=20,
        bg="#dfefff",
        command=lambda: [win.destroy(), volver_al_menu()],
    ).pack(pady=10)

    # Tabla
    tabla = ttk.Treeview(
        win, columns=("ID", "Paciente", "Fecha", "Hora", "Motivo"), show="headings"
    )
    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, width=150)
    tabla.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

    actualizar_tabla()
    win.mainloop()
