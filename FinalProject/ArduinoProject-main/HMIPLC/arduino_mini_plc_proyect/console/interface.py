import tkinter as tk
from tkinter import BooleanVar, ttk
from tkinter import IntVar
from arduino_connect.arduino_conn import ArduinoConnection
import json
import sqlite3
from datetime import datetime

ard = ArduinoConnection('rfc2217://localhost:4000', 9600, 10, 'URL')

#database connection
conn = sqlite3.connect('database.db')
c = conn.cursor()

#create database
c.execute('''CREATE TABLE IF NOT EXISTS arduino_data
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              temp REAL,
              hum REAL,
              boolean INTEGER,
              timestamp DATETIME)''')

conn.commit()

def handle_arduino_communication_async(data, callback):
    def inner_callback():
        try:
            response = ard.execute('r') 
            callback(str([x.decode("utf-8") for x in response]))
        except Exception as e:
            print("Error:", e)
            callback(None)
    try:
        print("HOLA: "+data)
        ard.execute('w', data)
        root.after(100, inner_callback)  # Esperar 100 ms antes de intentar leer la respuesta
    except Exception as e:
        print("Error:", e)
        callback(None)

def obtener_temperatura():
    handle_arduino_communication_async("temperatura", lambda response: print(f"Temperatura: {response}"))

def obtener_humedad():
    handle_arduino_communication_async("humedad", lambda response: print(f"Humedad: {response}"))

def cambiar_estado(button, output_number):
    handle_arduino_communication_async(f"input {output_number}", lambda response: print(f"Estado de salida {output_number}: {response}"))

def handle_input3():
    estado_actual = input3.cget("text")
    if estado_actual == "NO":
        input3.config(text="NC")
        handle_arduino_communication_async("input 3 no", lambda response: None)
    else:
        input3.config(text="NO")
        cambiar_estado(None, 3)
        
        
def actualizar_conexion():
    global ard
    ard = ArduinoConnection('rfc2217://localhost:4000', 9600, 10, 'URL')
    print("Conexión con Arduino actualizada")
    

def abrir_manual_control():
    manual_control = tk.Toplevel(root)
    manual_control.title("Manual Control")
    manual_control.geometry("750x500")
    
    button_frame = ttk.Frame(manual_control)
    button_frame.pack(pady=15)

    button_monitoring = ttk.Button(button_frame, text="Monitoring", width=15, command=close)
    button_monitoring.pack(side=tk.LEFT)
    button_manual_control = ttk.Button(button_frame, text="Manual Control", width=20,)
    button_manual_control.pack(side=tk.LEFT)
    
    button_refresh = ttk.Button(manual_control, text="Refresh", command=actualizar_conexion)
    button_refresh.pack(padx=10, pady=10, side=tk.TOP, anchor=tk.W)
    
    etiqueta0 = tk.Label(manual_control, text="Outputs", font="Helvetica 20 bold", width=40, height=3, anchor="sw", relief="flat",)
    etiqueta0.pack(fill=tk.X, pady=20)
    
    for i in range(1, 5):
        frame = ttk.Frame(manual_control, width=30, height=2, relief=tk.RAISED)
        frame.pack(pady=5, anchor="w", padx=10)
        label = tk.Label(frame, text=f"Output {i}")
        label.pack(side=tk.LEFT)
        button = tk.Button(frame, text="NO")
        button.pack(side=tk.LEFT)
        button.config(command=lambda b=button, i=i: cambiar_estado(b, i))

def close():
    root.destroy()

root = tk.Tk()
root.title("Monitoring")
root.geometry("750x500")

button_frame = ttk.Frame(root)
button_frame.pack(pady=15)

btn_mntr = ttk.Button(button_frame, text="Monitoring", width=15, command=close)
btn_mntr.pack(side=tk.LEFT)
btn_control = ttk.Button(button_frame, text="Manual Control ", width=20, command=abrir_manual_control)
btn_control.pack(side=tk.LEFT)

btn_record = ttk.Button(root, text="Record")
btn_record.pack(padx=10, pady=10, side=tk.TOP, anchor=tk.W)

btn_refresh = ttk.Button(root, text="Refresh", command=actualizar_conexion)
btn_refresh.pack(padx=10, pady=10, side=tk.TOP, anchor=tk.W)

container = ttk.Frame(root)
container.pack(fill=tk.X, pady=40)

inputs_frame = ttk.Frame(container)
inputs_frame.pack(fill=tk.X)

label_in = ttk.Label(inputs_frame, text="Inputs")
label_in.pack(side=tk.LEFT, anchor=tk.N, padx=10)

temp_frame = ttk.Frame(inputs_frame, relief="groove")
temp_frame.pack(side=tk.LEFT, pady=30, padx=10)
input1 = ttk.Entry(temp_frame, textvariable=tk.StringVar())
input1.insert(0, "Input 1 - Temperature")
input1.bind("<Button-1>", lambda e: input1.delete(0, tk.END))
input1.pack(padx=10, pady=10, ipadx=20, ipady=5)

hum_frame = ttk.Frame(inputs_frame, relief="groove")
hum_frame.pack(side=tk.LEFT, pady=30, padx=10)
input2 = ttk.Entry(hum_frame, textvariable=tk.StringVar())
input2.insert(0, "Input 2 - Humidity")
input2.bind("<Button-1>", lambda e: input2.delete(0, tk.END))
input2.pack(padx=10, pady=10, ipadx=20, ipady=5)

bool_frame = ttk.Frame(inputs_frame, relief="groove")
bool_frame.pack(side=tk.LEFT, pady=30, padx=10)
input3 = ttk.Label(bool_frame, text="Input 3 - Boolean")
input3.pack(padx=10, pady=10, ipadx=20, ipady=5)

button_bool = ttk.Button(bool_frame, text="NO", command=handle_input3)
button_bool.pack(side=tk.LEFT, padx=5)

separator = ttk.Separator(container, orient='horizontal')
separator.pack(fill=tk.X, padx=15, side=tk.TOP, anchor=tk.N)

outputs_frame = ttk.Frame(container)
outputs_frame.pack(fill=tk.X)

label_out = ttk.Label(outputs_frame, text="Outputs")
label_out.pack(side=tk.LEFT, anchor=tk.N, padx=10, pady=25)

for i in range(1, 5):
    frame = ttk.Frame(outputs_frame, width=30, height=2, relief=tk.RAISED)
    frame.pack(pady=5, anchor="w", side=tk.LEFT, padx=10)
    label = ttk.Label(frame, text=f"Output {i}")
    label.pack(side=tk.LEFT)
    button = tk.Button(frame, text="NO")
    button.pack(side=tk.LEFT)
    button.config(command=lambda b=button, i=i: cambiar_estado(b, i))

root.mainloop()
