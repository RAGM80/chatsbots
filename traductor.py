def LimonGPT():
    # cambios al chile le invete cosas raras atte limon pero hay que ir haciendo if y else en caso de que e usuario escriba algo y que le de esas respuestas
    print("Soy limongpt no se mucho pero aprendo xd")
    palabranueva = ""
    respuestanueva = ""
    while True:
        usuario = input(": ")
        if usuario == "hola":
            print("LimonGPT:Hola,¿que quieres saber el dia de hoy?")
        else:
            if usuario == "suma":
                n1 = float(input("dame el numero 1: "))
                n2 = float(input("dame el numero 2: "))
                print(n1 + n2)
            else:
                if usuario == "quien es rayador":
                    print("es el que raya las listas del profe alexis")
                else:
                    if usuario == "quien es limon":
                        print("LimonGPT:es el que huele a chetos del ilb")
                    else: 
                        if usuario == "clima":
                            print("LimonGPTt:esta bonito.")
                        #rafa estuvo aqui 
                        else:
                            if usuario == "adios":
                                print("LimonGPT: Nos vemos, me voy a jugar.")
                            else:
                                if usuario == "chiste":
                                    print("LimonGPT: ¿Por qué los programadores prefieren el frío? Porque odian los bugs.")
                                else:
                                    if usuario == "clash royale":
                                        print("LimonGPT: Jiji ja ja! Cuidado con ese montapuercos.")
                                    else:
                                        if usuario == "python":
                                            print("LimonGPT: El mejor lenguaje, pero me marean tantos ifs anidados.")
                                        else:
                                            if usuario == "java":
                                                print("LimonGPT: public static void main... ay no, qué flojera escribir tanto.")
                                            else:
                                                if usuario == "sql":
                                                    print("LimonGPT: DROP TABLE respuestas; ... es broma, no borré nada.")
                                                else:
                                                    if usuario == "github":
                                                        print("LimonGPT: Haz commit de esta escalera de ifs antes de que explote.")
                                                    else:
                                                        if usuario == "resta":
                                                            n1 = float(input("dame el numero 1: "))
                                                            n2 = float(input("dame el numero 2: "))
                                                            print(n1 - n2)
                                                        else:
                                                            if usuario == "multiplicacion":
                                                                n1 = float(input("dame el numero 1: "))
                                                                n2 = float(input("dame el numero 2: "))
                                                                print(n1 * n2)
                                                            else:
                                                                if usuario == "memorama":
                                                                    print("LimonGPT: Prefiero los juegos de voltear cartas en Python.")
                                                                else:
                                                                    if usuario == "capitan cambibara":
                                                                        print("LimonGPT: El superhéroe que esta ciudad necesita.")
                                                                    else:
                                                                        if usuario == "como se llama ese muchacho":
                                                                            print("LimonGPT: el que gopea maquinas?")
                                                                        else:
                                                                            if usuario == "estadistica":
                                                                                print("LimonGPT: Hay un 99.9% de probabilidad de que te falte un 'else' en algún lado.")
                                                                            else:
                                                                                if usuario == "matriz":
                                                                                    print("LimonGPT: No soy Neo, no sé salir de esta matriz de código.")
                                                                                else:
                                                                                    if usuario == "uml":
                                                                                        print("LimonGPT: Imagínate hacer el diagrama de este código, sería una locura.")
                                                                                    else:
                                                                                        if usuario == "rafa":
                                                                                            print("LimonGPT: Ah, el mero mero que está programando todo esto.")
                                                                                        else:
                                                                                            if usuario == "novia":
                                                                                                print("LimonGPT: algo que limon no conoce ")
                                                                                            else:
                                                                                                if usuario == "comida":
                                                                                                    print("LimonGPT: Unos buenos tacos de la CDMX no caerían mal.")
                                                                                                else:
                                                                                                    if usuario == "musica":
                                                                                                        print("LimonGPT: Pon algo chido para seguir tecleando.")
                                                                                                    else:
                                                                                                        if usuario == "como estas":
                                                                                                            print("LimonGPT: Sobreviviendo a la anidación extrema.")
                                                                                                        else:
                                                                                                            if usuario == "salir":
                                                                                                                break
                                                                                                            else:
                                                                                                                if usuario == palabranueva:
                                                                                                                    print("LimonGPT: " + respuestanueva)
                                                                                                                else:
                                                                                                                    print("No sé qué es eso. ¿Qué debería responder?")
                                                                                                                    palabranueva = usuario
                                                                                                                    respuestanueva = input("Dime la respuesta: ")
                                                                                                                    print("LimonGPT: a bueno ya se")
LimonGPT()