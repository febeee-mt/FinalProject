import tkinter as tk

def cambiar_estado(button, output_number):
    if button['text'] == 'NO':
        button.config(text='NC',)
    else:
        button.config(text='NO',)


root = tk.Tk()
root.title("Manual Control")
root.geometry("750x500")
root.configure(bd=5)

# Configurar el color de borde para las ventanas

frame_centro = tk.Frame(root)
frame_centro.pack(pady=20)

# Botón "Monitoring"
button_monitoring = tk.Button(frame_centro, text="Monitoring", font="Helvetica 15 bold", padx=50, pady=3, relief="solid", bd=2,)
button_monitoring.pack(side=tk.LEFT)

# Botón "Manual Control"
button_manual_control = tk.Button(frame_centro, text="Manual Control", font="Helvetica 15 bold", padx=50, pady=3, relief="solid", bd=2,)
button_manual_control.pack(side=tk.LEFT)

etiqueta0 = tk.Label(root, text="Outputs", font="Helvetica 20 bold", width=40, height=3, anchor="sw", relief="flat",)
etiqueta0.pack(fill=tk.X, pady=20)

for i in range(1, 5):
    frame = tk.Frame(root, width=30, height=2, relief=tk.RAISED)
    frame.pack(pady=5, anchor="w")
    label = tk.Label(frame, text=f"Output {i}", font="Helveltica 15", width=15, relief="solid", bd=3,)
    label.pack(side=tk.LEFT)
    button = tk.Button(frame, text="NO", relief="ridge")
    button.pack(side=tk.LEFT)
    button.config(command=lambda b=button, i=i: cambiar_estado(b, i))

root.mainloop()
