import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import requests

BASE_URL = 'https://api-test-obpj.onrender.com/api/alumnos'

class AlumnoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Alumnos")
        self.root.geometry("500x600")
        self.root.configure(bg="#f0f0f0")

        # Título
        self.title_label = tk.Label(root, text="Gestión de Alumnos", font=("Helvetica", 24), bg="#f0f0f0")
        self.title_label.pack(pady=20)

        # Frame para botones
        self.frame = tk.Frame(root, bg="#f0f0f0")
        self.frame.pack(pady=20)

        # Botones
        self.btn_get_all = tk.Button(self.frame, text="Obtener Todos los Alumnos", command=self.obtener_alumnos, width=30)
        self.btn_get_all.grid(row=0, column=0, pady=5)

        self.btn_get_one = tk.Button(self.frame, text="Obtener Alumno por no_control", command=self.obtener_alumno, width=30)
        self.btn_get_one.grid(row=1, column=0, pady=5)

        self.btn_create = tk.Button(self.frame, text="Crear Nuevo Alumno", command=self.crear_alumno, width=30)
        self.btn_create.grid(row=2, column=0, pady=5)

        self.btn_update = tk.Button(self.frame, text="Actualizar Alumno", command=self.actualizar_alumno, width=30)
        self.btn_update.grid(row=3, column=0, pady=5)

        self.btn_patch = tk.Button(self.frame, text="Actualizar Parcialmente Alumno", command=self.actualizar_parcialmente_alumno, width=30)
        self.btn_patch.grid(row=4, column=0, pady=5)

        self.btn_delete = tk.Button(self.frame, text="Eliminar Alumno", command=self.eliminar_alumno, width=30)
        self.btn_delete.grid(row=5, column=0, pady=5)

        # Área de texto para mostrar resultados
        self.text_area = tk.Text(root, height=15, width=60, wrap=tk.WORD)
        self.text_area.pack(pady=20)
        self.text_area.config(state=tk.DISABLED)

    def mostrar_mensaje(self, mensaje):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, mensaje)
        self.text_area.config(state=tk.DISABLED)

    def obtener_alumnos(self):
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            alumnos = response.json()
            mensaje = "\n".join([f"{alumno['no_control']}: {alumno['nombre']}" for alumno in alumnos])
            self.mostrar_mensaje(mensaje)
        else:
            self.mostrar_mensaje("Error al obtener alumnos.")

    def obtener_alumno(self):
        no_control = simpledialog.askstring("Input", "Introduce el no_control del alumno:")
        if no_control:
            response = requests.get(f"{BASE_URL}/{no_control}")
            if response.status_code == 200:
                alumno = response.json()
                # Mostrar todos los datos del alumno
                mensaje = (f"Alumno encontrado:\n"
                           f"No de control: {alumno['no_control']}\n"
                           f"Nombre: {alumno['nombre']}\n"
                           f"Apellido Paterno: {alumno['ap_paterno']}\n"
                           f"Apellido Materno: {alumno['ap_materno']}\n"
                           f"Semestre: {alumno['semestre']}")
                self.mostrar_mensaje(mensaje)
            else:
                self.mostrar_mensaje("Error al obtener el alumno.")

    def crear_alumno(self):
        no_control = simpledialog.askstring("Input", "Introduce el no_control:")
        nombre = simpledialog.askstring("Input", "Introduce el nombre:")
        ap_paterno = simpledialog.askstring("Input", "Introduce el apellido paterno:")
        ap_materno = simpledialog.askstring("Input", "Introduce el apellido materno:")
        semestre = simpledialog.askinteger("Input", "Introduce el semestre:")
        
        if no_control and nombre and ap_paterno and ap_materno and semestre is not None:
            nuevo_alumno = {
                "no_control": no_control,
                "nombre": nombre,
                "ap_paterno": ap_paterno,
                "ap_materno": ap_materno,
                "semestre": semestre
            }

            response = requests.post(BASE_URL, json=nuevo_alumno)
            if response.status_code == 201:
                self.mostrar_mensaje("Alumno creado exitosamente.")
            else:
                self.mostrar_mensaje("Error al crear el alumno.")
        else:
            self.mostrar_mensaje("Por favor, completa todos los campos.")

    def actualizar_alumno(self):
        no_control = simpledialog.askstring("Input", "Introduce el no_control del alumno a actualizar:")
        if no_control:
            alumno_actualizado = {}

            # Preguntar si se quiere cambiar el no_control
            cambiar_no_control = messagebox.askyesno("Actualizar no_control", "¿Deseas cambiar el no_control?")
            if cambiar_no_control:
                nuevo_no_control = simpledialog.askstring("Input", "Introduce el nuevo no_control:")
                if nuevo_no_control:
                    alumno_actualizado['no_control'] = nuevo_no_control

            nombre = simpledialog.askstring("Input", "Nuevo nombre (dejar en blanco para no cambiar):")
            if nombre:
                alumno_actualizado['nombre'] = nombre

            ap_paterno = simpledialog.askstring("Input", "Nuevo apellido paterno (dejar en blanco para no cambiar):")
            if ap_paterno:
                alumno_actualizado['ap_paterno'] = ap_paterno

            ap_materno = simpledialog.askstring("Input", "Nuevo apellido materno (dejar en blanco para no cambiar):")
            if ap_materno:
                alumno_actualizado['ap_materno'] = ap_materno

            semestre = simpledialog.askinteger("Input", "Nuevo semestre (dejar en blanco para no cambiar):")
            if semestre is not None:
                alumno_actualizado['semestre'] = semestre

            response = requests.put(f"{BASE_URL}/{no_control}", json=alumno_actualizado)
            if response.status_code == 204:
                self.mostrar_mensaje("Alumno actualizado exitosamente.")
            else:
                self.mostrar_mensaje("Error al actualizar el alumno.")

    def actualizar_parcialmente_alumno(self):
        no_control = simpledialog.askstring("Input", "Introduce el no_control del alumno a actualizar parcialmente:")
        if no_control:
            alumno_actualizado = {}

            nombre = simpledialog.askstring("Input", "Nuevo nombre (dejar en blanco para no cambiar):")
            if nombre:
                alumno_actualizado['nombre'] = nombre

            ap_paterno = simpledialog.askstring("Input", "Nuevo apellido paterno (dejar en blanco para no cambiar):")
            if ap_paterno:
                alumno_actualizado['ap_paterno'] = ap_paterno

            ap_materno = simpledialog.askstring("Input", "Nuevo apellido materno (dejar en blanco para no cambiar):")
            if ap_materno:
                alumno_actualizado['ap_materno'] = ap_materno

            semestre = simpledialog.askinteger("Input", "Nuevo semestre (dejar en blanco para no cambiar):")
            if semestre is not None:
                alumno_actualizado['semestre'] = semestre

            response = requests.patch(f"{BASE_URL}/{no_control}", json=alumno_actualizado)
            if response.status_code == 204:
                self.mostrar_mensaje("Alumno actualizado parcialmente.")
            else:
                self.mostrar_mensaje("Error al actualizar el alumno.")

    def eliminar_alumno(self):
        no_control = simpledialog.askstring("Input", "Introduce el no_control del alumno a eliminar:")
        if no_control:
            response = requests.delete(f"{BASE_URL}/{no_control}")
            if response.status_code == 204:
                self.mostrar_mensaje("Alumno eliminado exitosamente.")
            else:
                self.mostrar_mensaje("Error al eliminar el alumno.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AlumnoApp(root)
    root.mainloop()
