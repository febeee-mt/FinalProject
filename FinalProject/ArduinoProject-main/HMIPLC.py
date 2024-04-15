import tkinter as tk
from tkinter import BooleanVar, IntVar, ttk

#funcion para la creacion de la ventana de manual control
def abrir_manual_control():
    manual_control = tk.Toplevel(root)
    manual_control.title("Manual Control")
    manual_control.geometry("700x500")
    
    #botones y label
    frame_centro = tk.Frame(manual_control)
    frame_centro.pack(pady=20)
    button_monitoring = tk.Button(frame_centro, text="Monitoring", font="Helvetica 15 bold", padx=50, pady=3, relief="solid", bd=2, command=close)
    button_monitoring.pack(side=tk.LEFT)
    button_manual_control = tk.Button(frame_centro, text="Manual Control", font="Helvetica 15 bold", padx=50, pady=3, relief="solid", bd=2)
    button_manual_control.pack(side=tk.LEFT)
    etiqueta0 = tk.Label(manual_control, text="Outputs", font="Helvetica 20 bold", width=40, height=3, anchor="sw", relief="flat",)
    etiqueta0.pack(fill=tk.X, pady=20)
    
    #labels con los framen y botones 
    for i in range(1, 5):
        frame = tk.Frame(manual_control, width=30, height=2, relief=tk.RAISED)
        frame.pack(pady=5, anchor="w")
        label = tk.Label(frame, text=f"Output {i}", font="Helveltica 15", width=15, relief="solid", bd=3,)
        label.pack(side=tk.LEFT)
        button = tk.Button(frame, text="NO", relief="ridge")
        button.pack(side=tk.LEFT)
        button.config(command=lambda b=button, i=i: cambiar_estado(b, i))

#función que actualiza el valor de los botones
def cambiar_estado(button, output_number):
    if button['text'] == 'NO':
        button.config(text='NC',)
    else:
        button.config(text='NO',)

def close():
    root.destroy()

root = tk.Tk()
root.title("Monitoring")
root.geometry("750x500")
root.resizable(0, 0)

#a frame to contain the buttons
button_frame = ttk.Frame(root)
button_frame.pack(pady=15)

#buttons
btn_mntr = ttk.Button(button_frame, text="Monitoring", width=15, command=close)
btn_mntr.pack(side=tk.LEFT)
btn_control = ttk.Button(button_frame, text="Manual Control", width=20, command=abrir_manual_control)
btn_control.pack(side=tk.LEFT)

btn_record = ttk.Button(root, text="Record")
btn_record.pack(padx=10, pady=10, side=tk.TOP, anchor=tk.W)

container = ttk.Frame(root)
container.pack(fill=tk.X, pady=40)

#a frame for the inputs
inputs_frame = ttk.Frame(container)
inputs_frame.pack(fill=tk.X)

#inputs
label_in = ttk.Label(inputs_frame, text="Inputs")
label_in.pack(side=tk.LEFT, anchor=tk.N, padx=10)

temp_frame = ttk.Frame(inputs_frame, relief="groove")
temp_frame.pack(side=tk.LEFT, pady=30, padx=10)
input1 = ttk.Entry(temp_frame, textvariable=IntVar())
input1.insert(0,"Input 1 - Temperature")
input1.bind("<Button-1>", lambda e: input1.delete(0, tk.END))
input1.pack(padx=10, pady=10, ipadx=20, ipady=5)

hum_frame = ttk.Frame(inputs_frame, relief="groove")
hum_frame.pack(side=tk.LEFT, pady=30, padx=10)
input2 = ttk.Entry(hum_frame, textvariable=IntVar())
input2.insert(0,"Input 2 - Humidity")
input2.bind("<Button-1>", lambda e: input2.delete(0, tk.END))
input2.pack(padx=10, pady=10, ipadx=20, ipady=5)

bool_frame = ttk.Frame(inputs_frame, relief="groove")
bool_frame.pack(side=tk.LEFT, pady=30, padx=10)
input3 = ttk.Entry(bool_frame, textvariable=BooleanVar())
input3.insert(0,"Input 3 - Boolean")
input3.bind("<Button-1>", lambda e: input3.delete(0, tk.END))
input3.pack(padx=10, pady=10, ipadx=20, ipady=5)

#separator line
separator = ttk.Separator(container, orient='horizontal')
separator.pack(fill=tk.X, padx=15, side=tk.TOP, anchor=tk.N)

#a frame for the outputs
outputs_frame = ttk.Frame(container)
outputs_frame.pack(fill=tk.X)

label_out = ttk.Label(outputs_frame, text="Outputs")
label_out.pack(side=tk.LEFT, anchor=tk.N, padx=10, pady=25)

#outputs
out1_frame = ttk.Frame(outputs_frame, relief="groove")
out1_frame.pack(side=tk.LEFT, pady=50, padx=10)
out1 = ttk.Label(out1_frame, text="Output 1", relief="groove")
out1.pack(padx=10, pady=10, ipady=5, ipadx=10)

out2_frame = ttk.Frame(outputs_frame, relief="groove")
out2_frame.pack(side=tk.LEFT, pady=50, padx=10)
out2 = ttk.Label(out2_frame, text="Output 2", relief="groove")
out2.pack(padx=10, pady=10, ipady=5, ipadx=10)

out3_frame = ttk.Frame(outputs_frame, relief="groove")
out3_frame.pack(side=tk.LEFT, pady=50, padx=10)
out3 = ttk.Label(out3_frame, text="Output 3", relief="groove")
out3.pack(padx=10, pady=10, ipady=5, ipadx=10)

out4_frame = ttk.Frame(outputs_frame, relief="groove")
out4_frame.pack(side=tk.LEFT, pady=50, padx=10)
out4 = ttk.Label(out4_frame, text="Output 4", relief="groove")
out4.pack(padx=10, pady=10, ipady=5, ipadx=10)

root.mainloop()
