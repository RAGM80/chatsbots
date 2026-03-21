def LimonGPT():### cambios al chile le invete cosas raras atte limon pero hay que ir haciendo if y else en caso de que e usuario escriba algo y que le de esas respuestas
    print("Soy limongpt no se mucho pero aprendo xd")
    palabranueva = ""
    respuestanueva = ""
    while True:
        usuario = input(": ")
        if usuario == "hola":
            print("LimonGPT:Hola,que quieres saber de mi sabiduria")
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
                        print("LimonGPT:es el mas crack del ilb")
                    else: 
                        if usuario == "clima":
                            print("LimonGPTt:esta bonito.")
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