nombre_txt = "memoria.txt"  
respuestas = {}
with open(nombre_txt, "r", encoding="utf-8") as f: 
    lineas = f.readlines()
for i in range(0, len(lineas), 2):
    pregunta = lineas[i].replace("\n", "")
    respuesta = lineas[i+1].replace("\n", "")
    respuestas[pregunta] = respuesta
print("--- Chatbot con Memoria ---")
while True:
    usuario = input("Tú: ")
    if usuario == "salir": break
    if usuario in respuestas:
        print("Bot:", respuestas[usuario])
    else:
        print("Bot: No sé qué decir. ¿Cómo debería responder?")
        nuevaresp = input("Enséñame: ")
        if nuevaresp:
            respuestas[usuario] = nuevaresp
            with open(nombre_txt, "a", encoding="utf-8") as f:
                f.write(usuario + "\n")
                f.write(nuevaresp + "\n")
            print("Bot: ¡Gracias! Ya lo guardé.")