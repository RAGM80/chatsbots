nombretxt = "memoria.txt"  
respuestas = {}
with open(nombretxt, "r", encoding="utf-8") as f: 
    lineas = f.readlines()
for i in range(0, len(lineas), 2):
    pregunta = lineas[i].replace("\n", "")
    respuesta = lineas[i+1].replace("\n", "")
    respuestas[pregunta] = respuesta
print("Chatlaimon con Memoria")
while True:
    usuario = input("Tú: ")
    if usuario == "salir": break
    if usuario in respuestas:
        print("chatlaimon:", respuestas[usuario])
    else:
        print("chatlaimon: No sé qué decir. ¿qué te digo?")
        nuevaresp = input("Enséñame: ")
        if nuevaresp:
            respuestas[usuario] = nuevaresp
            with open(nombretxt, "a", encoding="utf-8") as f:
                f.write("n" +usuario + "\n")
                f.write(nuevaresp + "\n")
            print("chatlaimon: ¡Gracias! Ya lo guardé.")