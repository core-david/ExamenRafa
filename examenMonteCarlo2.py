import random
import tkinter as tk
from tkinter import ttk
import pandas as pd

# Función que implementa la simulación de Montecarlo para estimar el valor de π
def estimar_pi(puntos):
    puntos_circulo = 0
    puntos_dentro = []
    puntos_fuera = []
    for _ in range(puntos):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        if x ** 2 + y ** 2 <= 1:
            puntos_circulo += 1
            puntos_dentro.append((x, y))
        else:
            puntos_fuera.append((x, y))
    return 4 * puntos_circulo / puntos, puntos_dentro, puntos_fuera

# Función que se ejecuta cuando el usuario hace clic en el botón "Calcular"
def calcular():
    puntos = int(entry_puntos.get())
    estimacion_pi, _, _ = estimar_pi(puntos)
    label_resultado["text"] = f"Estimación de π: {estimacion_pi}"

# Función que se ejecuta cuando el usuario hace clic en el botón "Generar Excel"
def generar_excel():
    puntos = int(entry_puntos.get())
    _, puntos_dentro, puntos_fuera = estimar_pi(puntos)
    
    df_dentro = pd.DataFrame(puntos_dentro, columns=["x", "y"])
    df_fuera = pd.DataFrame(puntos_fuera, columns=["x", "y"])
    
    with pd.ExcelWriter("puntos.xlsx") as writer:
        df_dentro.to_excel(writer, sheet_name="Dentro del círculo", index=False)
        df_fuera.to_excel(writer, sheet_name="Fuera del círculo", index=False)

# Creación y configuración de los elementos de la interfaz gráfica de usuario utilizando Tkinter
root = tk.Tk()
root.title("Estimación de π")

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

label_puntos = ttk.Label(frame,text="Puntos:")
label_puntos.grid(row=0,column=0)

entry_puntos = ttk.Entry(frame)
entry_puntos.grid(row=0,column=1)

button_calcular = ttk.Button(frame,text="Calcular",command=calcular)
button_calcular.grid(row=1,columnspan=2)

button_excel = ttk.Button(frame,text="Generar Excel",command=generar_excel)
button_excel.grid(row=2,columnspan=2)

label_resultado = ttk.Label(frame,text="")
label_resultado.grid(row=3,columnspan=2)

root.mainloop()