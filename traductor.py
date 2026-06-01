import tkinter as tk
from tkinter import scrolledtext
import os

nombretxt = "memoria.txt"  
respuestas = {}

if not os.path.exists(nombretxt):
    with open(nombretxt, "w", encoding="utf-8") as f:
        pass

with open(nombretxt, "r", encoding="utf-8") as f: 
    lineas = f.readlines()
    for i in range(0, len(lineas)-1, 2): 
        pregunta = lineas[i].replace("\n", "")
        respuesta = lineas[i+1].replace("\n", "")
        respuestas[pregunta] = respuesta

estado_aprendizaje = False
pregunta_pendiente = ""

def procesar_mensaje(event=None):
    global estado_aprendizaje, pregunta_pendiente
    
   
    usuario = entrada_texto.get().strip()
    if not usuario:
        return 
    
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "Tú: " + usuario + "\n")
    entrada_texto.delete(0, tk.END) 
    
    if usuario.lower() == "salir":
        ventana.quit()
        return

    if estado_aprendizaje:
        
        nuevaresp = usuario
        respuestas[pregunta_pendiente] = nuevaresp
        
        with open(nombretxt, "a", encoding="utf-8") as f:
            f.write(pregunta_pendiente + "\n")
            f.write(nuevaresp + "\n")
        
        chat_area.insert(tk.END, "ChatLaimon: ya aprendi algo nuevo SISISISISISI.\n\n")
        
        estado_aprendizaje = False
        pregunta_pendiente = ""
    else:
        if usuario in respuestas:
            chat_area.insert(tk.END, "ChatLaimon: " + respuestas[usuario] + "\n\n")
        else:
            chat_area.insert(tk.END, "ChatLaimon: No sé qué decir. ¿qué te digo? (Escribe la respuesta para enseñarme)\n\n")
          
            estado_aprendizaje = True
            pregunta_pendiente = usuario
    
   
    chat_area.yview(tk.END)
    chat_area.config(state=tk.DISABLED)

# Aqui se empezo a hacer la intefaz, estos son los cambios que se agregaron 
ventana = tk.Tk()
ventana.title("ChatLaimon (EL MEJOR CHAT DEL MUNDO ;) )")
ventana.geometry("450x550")
ventana.config(bg="#f0f0f0")

# este es el area del historial del chat 
chat_area = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, font=("Consolas", 11))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Mensaje inicial
chat_area.insert(tk.END, "ChatLaimon INICIANDO,DIME TUS MAS OSCUROS SECRETOS...\n\n")
chat_area.config(state=tk.DISABLED) # en esta parte se desactiva para que el usuario no escriba directamente ahí

# cuadro inferior para el input y el botón
frame_inferior = tk.Frame(ventana, bg="#f0f0f0")
frame_inferior.pack(padx=10, pady=(0, 10), fill=tk.X)

# Caja de texto para el usuario
entrada_texto = tk.Entry(frame_inferior, font=("Arial", 12))
entrada_texto.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entrada_texto.bind("<Return>", procesar_mensaje) # aqui esto se hizo para que se pueda enviar presionando la tecla Enter

# Botón de enviar
boton_enviar = tk.Button(frame_inferior, text="Enviar", command=procesar_mensaje, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
boton_enviar.pack(side=tk.RIGHT)

# Iniciar el ciclo de la ventana
entrada_texto.focus() # Poner el cursor automáticamente en la caja de texto
ventana.mainloop()
