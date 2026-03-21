traductor = {
    "hola": "sul sul",
    "adios": "dag dag", 
    "bebe": "nooboo", 
    "comida": "mnyum", "gracias": "wadliba", "perro": "woof", 
    "gato": "meow", "amor": "laba", "pizza": "chum cha", 
    "genial": "whipna choba dog", "baño": "pish", "dinero": "simoleons", 
    "fuego": "flarb", "cansado": "mishno", "si": "vway", 
    "no": "nee", "que pasa": "hooba noobie", "dulce": "ooboo", 
    "asqueroso": "eeew", "fiesta": "gerbit"
}
print("traductor simlish (sims)")
print("escribe varias palabras separadas por espacios ejemplo(pizza,hola,adios,gato etc).")
entrada = input("Escribe en español: ")
palabras_usuario = entrada.lower().split()
frase_traducida = []
for p in palabras_usuario:
    if p in traductor:
        frase_traducida.append(traductor[p])
    else:
        frase_traducida.append(f"[{p}?]")
resultado_final = " ".join(frase_traducida)
print("\nTraducción:")
print(resultado_final.upper())