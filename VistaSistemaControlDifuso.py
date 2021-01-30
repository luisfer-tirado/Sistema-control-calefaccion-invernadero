# importar librería
from tkinter import *
from tkinter import messagebox

from SistemaControlDifuso import sistema_control_difuso

class vista_sistema_control_difuso():

    # método constructor
    def __init__(self):
        # crear la ventana
        self.root = Tk()
        self.root.title("Sistema de Control Difuso - IA")
        self.root.resizable(False, False)

        app_width = 1280
        app_height = 708

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)

        # centrar la ventana conforme al ancho y largo
        self.root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

        # crear el frame principal
        self.frame = Frame(self.root, width=app_width, height=app_height)
        self.frame.pack()

        # variables numéricas para operaciones
        self.temperatura = 0
        self.contador_temperatura = 0

        self.humedad = 0
        self.contador_humedad = 0

        self.variacion = 0

        # llamar al método gráfico
        self.initUI()
        # comenzar el ciclo de ejecución
        self.root.mainloop()

    # método gráfico de la GUI
    def initUI(self):
        # ------------------ Imagenes -----------------------------------------
        self.rama1 = PhotoImage(file="img/rama1.png")
        self.label_rama1 = Label(self.frame, image=self.rama1)
        self.label_rama1.place(x=0, y=0)

        self.maceta1 = PhotoImage(file="img/maceta1.png")
        self.label_maceta1 = Label(self.frame, image=self.maceta1)
        self.label_maceta1.place(x=240, y=30)

        '''self.maceta2 = PhotoImage(file="img/maceta2.png")
        self.label_maceta2 = Label(self.frame, image=self.maceta2)
        self.label_maceta2.place(x=1040, y=580)'''

        self.maceta3 = PhotoImage(file="img/maceta3.png")
        self.label_maceta3 = Label(self.frame, image=self.maceta3)
        self.label_maceta3.place(x=1040, y=30)

        self.temp = PhotoImage(file="img/temperatura.png")
        self.label_temp = Label(self.frame, image=self.temp)
        self.label_temp.place(x=540, y=180)

        self.celcius = PhotoImage(file="img/celcius.png")
        self.label_celcius = Label(self.frame, image=self.celcius)
        self.label_celcius.place(x=600, y=180)

        self.hum = PhotoImage(file="img/humedad.png")
        self.label_hum = Label(self.frame, image=self.hum)
        self.label_hum.place(x=560, y=300)

        # ------------------- Elementos GUI -----------------------------------
        # ------------------- Etiquetas ---------------------------------------
        self.label_titulo = Label(self.frame, text="Calefacción\n Invernadero", font=("Roboto", 28))
        self.label_titulo.place(x=550, y=40)

        self.label_temperatura = Label(self.frame, text="Temperatura: ", font=("Roboto", 15))
        self.label_temperatura.place(x=510, y=240)

        self.label_humedad = Label(self.frame, text="Humedad: ", font=("Roboto", 15))
        self.label_humedad.place(x=540, y=360)

        # ------------------- Cajas de texto ----------------------------------
        self.entry_temperatura = Entry(self.frame, fg="green", font=("Roboto", 14), justify="center", width=6)
        self.entry_temperatura.insert(0, "0.0")
        self.entry_temperatura.place(x=680, y=240)

        self.entry_humedad = Entry(self.frame, fg="green", font=("Roboto", 14), justify="center", width=6)
        self.entry_humedad.insert(0, "0.0")
        self.entry_humedad.place(x=680, y=360)

        self.text_datos = Text(self.frame, bg="white", fg="blue", width=30, height=7, font=("Roboto", 12))
        self.text_datos.insert(INSERT, "---- DATOS DEL CONTROLADOR ----")
        self.text_datos["state"] = DISABLED
        self.text_datos.place(x=540, y=510)

        # ------------------- Botones -----------------------------------------
        self.boton_calcular = Button(self.frame, text="Calcular", command=lambda:self.calcular(), font=("Roboto", 17), bg="#2E9AFE")
        self.boton_calcular.place(x=620, y=430)

        self.boton_temperatura_menos = Button(self.frame, text="-", font=("Roboto", 12), bg="blue", command=lambda:self.decrementar_temperatura())
        self.boton_temperatura_menos.place(x=648, y=238)
        self.boton_temperatura_mas = Button(self.frame, text="+", font=("Roboto", 12), bg="red", command=lambda:self.incrementar_temperatura())
        self.boton_temperatura_mas.place(x=751, y=238)

        self.boton_humedad_menos = Button(self.frame, text="-", font=("Roboto", 12), bg="blue", command=lambda:self.decrementar_humedad())
        self.boton_humedad_menos.place(x=648, y=358)
        self.boton_humedad_mas = Button(self.frame, text="+", font=("Roboto", 12), bg="red", command=lambda:self.incrementar_humedad())
        self.boton_humedad_mas.place(x=751, y=358)

    # método para calcular la variación
    def calcular(self):
        self.limpiar_salida()

        if self.verificar() == True:
            sistema = sistema_control_difuso()
            self.variacion = sistema.simulacion(float(self.temperatura), float(self.humedad))

            self.llenar_texto()
            self.limpiar_entradas()
        else:
            self.limpiar_entradas()
            self.text_datos.insert(INSERT, "---- DATOS DEL CONTROLADOR ----")
            self.aviso_datos_incorrectos()

    # método para decrementar la temperatura
    def decrementar_temperatura(self):
        try:
            self.contador_temperatura = float(self.entry_temperatura.get())
            if self.contador_temperatura > 0:
                self.entry_temperatura.delete('0', END)
                self.contador_temperatura -= 1
                self.entry_temperatura.insert(0, str(self.contador_temperatura))
        except:
            self.limpiar_entradas()
            #self.text_datos.insert(INSERT, "---- DATOS DEL CONTROLADOR ----")
            self.aviso_datos_incorrectos()

    # método para incrementar la temperatura
    def incrementar_temperatura(self):
        try:
            self.contador_temperatura = float(self.entry_temperatura.get())
            if self.contador_temperatura < 40:
                self.entry_temperatura.delete('0', END)
                self.contador_temperatura += 1
                self.entry_temperatura.insert(0, str(self.contador_temperatura))
        except:
            self.limpiar_entradas()
            #self.text_datos.insert(INSERT, "---- DATOS DEL CONTROLADOR ----")
            self.aviso_datos_incorrectos()

    # método para decrementar la humedad
    def decrementar_humedad(self):
        try:
            self.contador_humedad = float(self.entry_humedad.get())
            if self.contador_humedad > 0:
                self.entry_humedad.delete('0', END)
                self.contador_humedad -= 1
                self.entry_humedad.insert(0, str(self.contador_humedad))
        except:
            self.limpiar_entradas()
            #self.text_datos.insert(INSERT, "---- DATOS DEL CONTROLADOR ----")
            self.aviso_datos_incorrectos()

    # método para incrementar la humedad
    def incrementar_humedad(self):
        try:
            self.contador_humedad = float(self.entry_humedad.get())
            if self.contador_humedad < 100:
                self.entry_humedad.delete('0', END)
                self.contador_humedad += 1
                self.entry_humedad.insert(0, str(self.contador_humedad))
        except:
            self.limpiar_entradas()
            #self.text_datos.insert(INSERT, "---- DATOS DEL CONTROLADOR ----")
            self.aviso_datos_incorrectos()

    # método para desplegar una alerta en dado caso de error
    def aviso_datos_incorrectos(self):
        messagebox.showwarning("Aviso", "Los datos son incorrectos")

    # método para limpiar los elementos Entry()
    def limpiar_entradas(self):
        self.entry_temperatura.delete('0', END)
        self.entry_temperatura.insert(0, "0.0")

        self.entry_humedad.delete('0', END)
        self.entry_humedad.insert(0, "0.0")

    # método para limpiar el elemento Text()
    def limpiar_salida(self):
        self.text_datos["state"] = NORMAL
        self.text_datos.delete('1.0', END)

    # método para mostrar los resultados en el elemento Text()
    def llenar_texto(self):
        self.text_datos.insert(INSERT, "---- DATOS DEL CONTROLADOR ----\nTemperatura: " + str(self.temperatura) + "°C\nHumedad: " + str(self.humedad) + "%\nVariación: " + str(self.variacion) + "\n\nTemperatura modificada: \n" + str(self.temperatura+self.variacion))
        self.text_datos["state"] = DISABLED

    # método que verifica condiciones
    def verificar(self):
        try:
            self.temperatura = float(self.entry_temperatura.get())
            self.humedad = float(self.entry_humedad.get())

            if ((self.temperatura >= 0) and (self.temperatura <= 40)) and ((self.humedad >= 0) and (self.humedad <= 100)) :
                return True
            else:
                return False
        except:
            return False

# ejecución principal
if __name__ == "__main__":
    vista = vista_sistema_control_difuso()
