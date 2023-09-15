import tkinter as tk
from tkinter import ttk
import random
import pandas as pd
import os

# Función que implementa la simulación de Montecarlo para estimar el área bajo la curva de una función polinómica
def monte_carlo_polinomio(coeficientes, replicas, intervalo):
    a, b = intervalo
    valores_aleatorios = [random.uniform(a, b) for _ in range(replicas)]
    alturas = []
    for x in valores_aleatorios:
        altura = 0
        for i, coeficiente in enumerate(coeficientes):
            altura += coeficiente * (x ** i)
        alturas.append(altura)
    areas = [(b - a) / replicas * altura for altura in alturas]
    estimacion_integral = sum(areas)
    return valores_aleatorios, alturas, areas, estimacion_integral

# Función que implementa la simulación de Montecarlo para estimar el área bajo la curva de una función exponencial
def monte_carlo_exponencial(a, b, replicas, intervalo):
    c, d = intervalo
    valores_aleatorios = [random.uniform(c, d) for _ in range(replicas)]
    alturas = [a ** (b * x) for x in valores_aleatorios]
    areas = [(d - c) / replicas * altura for altura in alturas]
    estimacion_integral = sum(areas)
    return valores_aleatorios, alturas, areas, estimacion_integral

# Función que se ejecuta cuando el usuario hace clic en el botón "Calcular"
def calcular():
    #obtiene el valor seleccionado por el usuario en el menú desplegable “Función” y lo almacena en la variable funcion.
    funcion = combo_funcion.get()
    #obtiene el texto ingresado por el usuario en el campo “Parámetros” y lo almacena en la variable parametros.
    parametros = entry_parametros.get()
    #obtiene el texto ingresado por el usuario en el campo “Réplicas”, lo convierte a un número entero y lo almacena en la variable replicas
    replicas = int(entry_replicas.get())
    #obtiene el texto ingresado por el usuario en el campo “Intervalo” y lo almacena en la variable intervalo.
    intervalo = entry_intervalo.get()
    
    if funcion == "Polinómica":
        coeficientes = list(map(float, parametros.split(",")))
        a, b = map(float, intervalo.split(","))
        _, _, _, estimacion_integral = monte_carlo_polinomio(coeficientes, replicas, [a, b])
    elif funcion == "Exponencial":
        a, b = map(float, parametros.split(","))
        c, d = map(float, intervalo.split(","))
        _, _, _, estimacion_integral = monte_carlo_exponencial(a, b, replicas, [c, d])
    
    label_resultado["text"] = f"Estimación de la integral: {estimacion_integral}"

def generar_excel():
    funcion = combo_funcion.get()
    parametros = entry_parametros.get()
    replicas = int(entry_replicas.get())
    intervalo = entry_intervalo.get()
    
    if funcion == "Polinómica":
        coeficientes = list(map(float, parametros.split(",")))
        a, b = map(float, intervalo.split(","))
        valores_aleatorios, alturas, areas,_  = monte_carlo_polinomio(coeficientes, replicas, [a,b])
        
    elif funcion == "Exponencial":
        a,b  = map(float,parametros.split(","))
        c,d  = map(float,intervalo.split(","))
        valores_aleatorios ,alturas ,areas,_  = monte_carlo_exponencial(a,b ,replicas,[c,d])
        
    df=pd.DataFrame({"Valores Aleatorios":valores_aleatorios,"Alturas":alturas,"Áreas":areas})
    
    df.to_excel("montecarlo.xlsx",index=False)
    
    os.startfile("montecarlo.xlsx")
    
# Función que se ejecuta cuando el usuario selecciona una función en el menú desplegable "Función"
def actualizar_parametros(event):
    funcion=combo_funcion.get()
    
    if funcion=="Polinómica":
        label_parametros["text"]="Coeficientes (ingrese los coeficientes del menor grado al mayor separados por comas):"
        
    elif funcion=="Exponencial":
        label_parametros["text"]="Parámetros a,b (ingrese los parámetros separados por comas):"

# Creación y configuración de los elementos de la interfaz gráfica de usuario utilizando Tkinter

root=tk.Tk()
root.title("Simulación de Montecarlo")

frame=ttk.Frame(root)
frame.pack(padx=10,pady=10)

label_funcion=ttk.Label(frame,text="Función:")
label_funcion.grid(row=0,column=0)

combo_funcion=ttk.Combobox(frame)
combo_funcion["values"]=["Polinómica","Exponencial"]
combo_funcion.current(0)
combo_funcion.bind("<<ComboboxSelected>>",actualizar_parametros)
combo_funcion.grid(row=0,column=1)

label_parametros=ttk.Label(frame,text="Coeficientes (ingrese los coeficientes del menor grado al mayor separados por comas):")
label_parametros.grid(row=1,column=0)

entry_parametros=ttk.Entry(frame)
entry_parametros.grid(row=1,column=1)

label_replicas=ttk.Label(frame,text="Réplicas:")
label_replicas.grid(row=2,column=0)

entry_replicas=ttk.Entry(frame)
entry_replicas.grid(row=2,column=1)

label_intervalo=ttk.Label(frame,text="Intervalo (ingrese el intervalo separdo por comas)")
label_intervalo.grid(row=3,column=0)

entry_intervalo=ttk.Entry(frame)
entry_intervalo.grid(row=3,column=1)

button_calcular=ttk.Button(frame,text="Calcular",command=calcular)
button_calcular.grid(row=4,columnspan=2)

button_excel = ttk.Button(frame, text="Generar Excel", command=generar_excel)
button_excel.grid(row=5, columnspan=2)

label_resultado = ttk.Label(frame,text="")
label_resultado.grid(row=6,columnspan=2)

root.mainloop()