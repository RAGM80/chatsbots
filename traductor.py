import tkinter as tk
from tkinter import scrolledtext
import os

carpeta_actual = os.path.dirname(os.path.abspath(__file__))#obtiene la ruta de la carpeta exacta donde está guardado este script de Python
nombretxt = os.path.join(carpeta_actual, "memoria.txt") #crea la ruta completa para el archivo de texto donde el chat guardará lo que aprenda
respuestas = {}#diccionario vacío que usaremos para cargar las preguntas y respuestas en la memoria RAM

if not os.path.exists(nombretxt):#si el archivo memoria.txt no existe todavía, lo crea vacío para evitar que el programa truene
    with open(nombretxt, "w", encoding="utf-8") as f:
        pass

with open(nombretxt, "r", encoding="utf-8") as f: #abre el archivo en modo lectura para cargar los conocimientos previos que ya tiene guardados
    lineas = [linea.strip() for linea in f.readlines() if linea.strip()]#lee todas las líneas, les quita los espacios sueltos (\n) y descarta las líneas que estén vacías
    
    for i in range(0, len(lineas) - 1, 2): #recorre la lista de dos en dos ,una línea es pregunta, la siguiente es respuesta
        pregunta = lineas[i].lower()#convierte la pregunta a minúsculas para que sea fácil de buscar
        respuesta = lineas[i+1]#agarra la respuesta tal cual
        respuestas[pregunta] = respuesta#las empareja dentro del diccionario




#variables de control para saber si el usuario le está enseñando algo nuevo al bot
estado_aprendizaje = False#si es True, significa que el próximo mensaje que mandes será una respuesta nueva
pregunta_pendiente = ""#guarda temporalmente la frase que el bot no entendió

def procesar_mensaje(event=None):
    global estado_aprendizaje, pregunta_pendiente
    
   
    usuario = entrada_texto.get().strip()#obtiene el texto que el usuario escribió en la cajita de entrada y le quita espacios vacíos
    if not usuario:
        return #si el usuario no escribió nada, ignora el clic o el Enter
    
    chat_area.config(state=tk.NORMAL)#desbloquea temporalmente la pantalla del chat para poder escribir en ella
    chat_area.insert(tk.END, "Tú: " + usuario + "\n")#pinta en la pantalla lo que tú acabas de escribir
    entrada_texto.delete(0, tk.END) #borra el texto de la cajita de entrada para dejarla limpia para el siguiente mensaje
    if usuario.lower() == "salir":
        ventana.quit()
        return#si escribes la palabra  "salir", cierra la interfaz gráfica por completo
    #estado 1
    if estado_aprendizaje:#el bot estaba esperando que le enseñaras la respuesta a una pregunta pasada
        nuevaresp = usuario#el mensaje actual se convierte en la nueva respuesta aprendida
        respuestas[pregunta_pendiente.lower()] = nuevaresp#guarda la respuesta en la RAM
        
        with open(nombretxt, "a", encoding="utf-8") as f:#abre el archivo txt en modo "append" osea añadir al final para grabar la nueva respuesta permanentemente
            f.write(pregunta_pendiente + "\n")#escribe la pregunta en una línea
            f.write(nuevaresp + "\n")#escribe la respuesta en la siguiente línea
        
        chat_area.insert(tk.END, "ChatLaimon: ya aprendi algo nuevo SISISISISISI.\n\n")#le avisa al usuario con emoción que ya se lo aprendió
        
        estado_aprendizaje = False#apaga el modo aprendizaje y limpia la variable temporal
        pregunta_pendiente = ""
    #estado 0
    else:
        usuario_minuscula = usuario.lower()#si es una conversación normal, busca si lo que escribiste ya está en sus datos
        for signo_espacio in [",", ".", ";", ":"]:
            usuario_minuscula = usuario_minuscula.replace(signo_espacio, " ")
        for signo in ["?", "!", "¿", "¡"]:# borramos por completo los signos de apertura y de lo que quede
            usuario_minuscula = usuario_minuscula.replace(signo, "")
        encontrado = False
        if usuario_minuscula in respuestas:#prioridad 1: coincidencia exacta completa
            chat_area.insert(tk.END, "ChatLaimon: " + respuestas[usuario_minuscula] + "\n\n")
            encontrado = True
        if not encontrado:#prioridad 2: validación inteligente por longitud de lista
            palabras_lista = usuario_minuscula.split()
            
            
            if len(palabras_lista) == 1:#caso a: si el usuario escribió una sola palabra suelta como holaaaaaaaa
                palabra_unica = palabras_lista[0]
                for pregunta_guardada, respuesta_guardada in respuestas.items():
                    if pregunta_guardada in palabra_unica:
                        chat_area.insert(tk.END, "ChatLaimon: " + respuesta_guardada + "\n\n")
                        encontrado = True
                        break
            else:#caso b: si escribió más de una palabra, no adivina para respetar el contexto largo
                pass
        if not encontrado:#si terminó de buscar en toda la memoria y no tuvo ni una coincidencia
            chat_area.insert(tk.END, "ChatLaimon: No sé qué decir. ¿qué te digo? (Escribe la respuesta para enseñarme)\n\n")#mensaje al mandar
            estado_aprendizaje = True#activa el modo aprendizaje para procesar tu siguiente mensaje
            pregunta_pendiente = usuario#registra qué frase fue la que causó la duda
    
   
    chat_area.yview(tk.END)
    chat_area.config(state=tk.DISABLED)
ventana = tk.Tk()
ventana.title("ChatLaimon (EL MEJOR CHAT DEL MUNDO ;) )")
ventana.geometry("450x550")
ventana.config(bg="#f0f0f0")
chat_area = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, font=("Consolas", 11))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_area.insert(tk.END, "ChatLaimon INICIANDO,DIME TUS MAS OSCUROS SECRETOS...\n\n")
chat_area.config(state=tk.DISABLED) 

frame_inferior = tk.Frame(ventana, bg="#f0f0f0")
frame_inferior.pack(padx=10, pady=(0, 10), fill=tk.X)
entrada_texto = tk.Entry(frame_inferior, font=("Arial", 12))
entrada_texto.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
entrada_texto.bind("<Return>", procesar_mensaje) 

boton_enviar = tk.Button(frame_inferior, text="Enviar", command=procesar_mensaje, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
boton_enviar.pack(side=tk.RIGHT)
entrada_texto.focus() 
ventana.mainloop()