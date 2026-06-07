#semana de informatica 2026
import re
import tkinter as tk
from tkinter import scrolledtext, simpledialog
TOKEN_RAYADOR = [ #arreglo de tokens
    #el + te dice que puede haber mas numeros o letras no solo 1
    #el e'' le dice Lee todo lo que está dentro de las comillas exactamente carácter por carácter"
    ('FLOT',       r'\d+ç\d+'),    #\d+ busca uno o más dígitos, luego busca la letra física ç, y finalmente \d+ busca otro grupo de uno o más dígitos (ejemplo: 5ç5 o 12ç50). # Decimal
    ('ENT',        r'\d+'),        #\d significa dígito y el + significa uno o más de forma seguida ejemplo: 20, 100. # Entero
    ('CADENA',     r'["“”].*?["“”]'), #["“”] le dice a Python que el texto puede empezar con comillas normales ", o las comillas inclinadas “ y ”. El .*? le dice que agarre todo lo que encuentre dentro hasta que toque la comilla de cierre. # Texto / String
    
    #\b es un limite para que la palabra termine ahi y no pongan tal vezi123
    ('TAL_VEZI',   r'tal vezi\b'), # IZQ: Identifica condicional secundario y DER: Busca texto 'tal vezi' # Else if
    ('VALIDA',     r'valida\b'),# If
    ('SINO',       r'sino\b'),# Else
    ('BUCLE',      r'bucle\b'),# For
    ('MIENTRA',    r'mientra\b'),# While
    ('ROMPE',      r'rompe\b'),# Break
    ('SIGUE',      r'sigue\b'),#COntinue
    ('NADA',       r'nada\b'),# Pass
    ('ENTREGA',    r'entrega\b'),#return
    ('APAGAR',     r'apagar\b'),# Exit
    ('PEG',        r'peg\b'), # printff   
    ('ESCANEA',    r'escanea\b'), # scanf     
    ('Y',          r'y\b'), #and
    ('O',          r'o\b'), #or
    ('SUMA',       r'suma\b'), #+
    ('REST',       r'rest\b'), #-
    ('MULT',       r'mult\b'), #*
    ('DIVS',       r'divs\b'), #/
    ('MODU',       r'modu\b'), #%
    ('POW',        r'pow\b'),  # ^ potencia
    ('MAYOR',      r'mayor\b'), # >
    ('MENOR',      r'menor\b'), # <
    
    ('TIPO_ENT',   r'ent\b'), #int
    ('TIPO_FLOT',  r'flot\b'), #float
    ('TIPO_DOBLE', r'doble\b'), #double
    ('TIPO_LARGO', r'largo\b'), #long
    
    ('ID_VAR',     r'@[vV]_[a-zA-Z0-9]+'), #exige que comience por @ seguido de ^[v o V] luego un guion bajo y despues[las letras o mayusculas o numeros de 0 a 9] como @v_cali @v_edad1 aparte 
    ('ID_NUM',     r'\bn_[0-9]+\b'),   #antes de la n_ no hay texto y despues de el hay [0 a 9]y el + que puede haber muchos mas numeros perooo el \b dice que no puede haber texto despues del numero   
    
    ('ASIGNADOR',  r'>>'),  # =           
    
    ('LLAVE_A',    r'\(\('), # \ dice que el siguiente caracter se va a usar osea ( luego el otro \ dice que el siguiente tambien se usa osea ((       #este es {
    ('LLAVE_C',    r'\)\)'), # \ dice que el siguiente caracter se va a usar osea ) luego el otro ) dice que el siguiente tambien se usa osea ))       #este es }  
    ('PAR_A',      r'\['),   # \ dice que el siguiente caracter se va a usar osea [       #este es (       
    ('PAR_C',      r'\]'),   # \ dice que el siguiente caracter se va a usar osea ]       #este es )         
    ('COR_A',      r'\bil\b'), # \b busc que antes de la palabra no haya texto y luego busca la palabra il y luego \b dice que despues de la palabra no haya texto  # este es [        
    ('COR_C',      r'\bli\b'),  # \b busc que antes de la palabra no haya texto y luego busca la palabra li y luego \b dice que despues de la palabra no haya texto  # este es ]       
    
    ('FIN',        r'~'), #busca el simbolo ~             
    ('ESPACIO',    r'[ \t\n]+'), #busca espacios, tabulaciones o saltos de línea y los ignora
    ('MISMATCH',   r'.'), #cualquier otro caracter que no coincida con los anteriores, lo marca como error léxico
]

def lexer(codigo):
    tokens = [] #guarda los tokens encontrados en el código fuente
    regex_completo = '|'.join(f'(?P<{nombre}>{patron})' for nombre, patron in TOKEN_RAYADOR)#junta todos los patrones de tokens en una sola expresión regular usando alternancia (|) y asigna un nombre a cada grupo para identificar el tipo de token encontrado
    for match in re.finditer(regex_completo, codigo):#lee hacia la derecha y busca si coincide,si lo hace lo agregam a la lista pero si no
        tipo = match.lastgroup #es el vaalor a la izquierda es decir su nombre  Mayor ,Menor, Suma
        valor = match.group(tipo) #es lo que escribio el usuario como n_5 o @v_cali
        if tipo == 'ESPACIO': continue #si se encuentra un espacio,se ignora y continua
        if tipo == 'MISMATCH': #palabra incorrecta pasa a raise que detiene el programa y muestra el error
            raise RuntimeError(f"Error Léxico: Símbolo inválido '{valor}'.")
        tokens.append((tipo, valor)) #si es valido se agrega
    tokens.append(('EOF', ''))#cuando se termina,Eof indica el fin para ya no seguir buscando
    return tokens #entrega


class Parser:
    def __init__(self, tokens): #Recibe la que generó el lexer por ejemplo: 'VALIDA', 'valida' o 'ID_VAR', '@v_edad'
        self.tokens = tokens #aqui se guarda los tokens
        self.pos = 0 #siempre comienza a contar desde el primer token

    def actual(self):
        return self.tokens[self.pos] #solo observa el tipo y valor sin avanzar ayuda a parse adecidir si hace un if o bucle etc etc

    def consumir(self, tipo_esperado):
        tipo, valor = self.actual() #espera el tipo y valor del token recibido
        if tipo == tipo_esperado: #Compara el token real que tiene enfrente contra el que se supone que debe ir ahí
            self.pos += 1 #si es bueno pasa al siguiente pa leerlo
            return valor #devuelve el valor
        if tipo_esperado == 'FIN':
            raise SyntaxError(f"Te faltó cerrar una instrucción con '~'")#por si no se cierra con ~ el programa se detiene y muestra el error
        raise SyntaxError(f"Error de Sintaxis: Se esperaba {tipo_esperado}, pero encontré '{valor}'")#si el token no es el esperado, se detiene el programa y muestra un mensaje de error indicando qué se esperaba y qué se encontró realmente

    def parse(self): #metodo maestro
        instrucciones = [] #aqui se guardan las instrucciones
        while self.actual()[0] != 'EOF': #mientras que no sea EOF sigue leyendo comenzande desde 0
            inst = self.parse_instruccion() #intenta adivinar que tipo de instruccion es por su inico por ejemplo @ es una  variable o valida es un if etc etc
            if inst: instrucciones.append(inst)#si paso se agrega a la lista de instrucciones 
            else: self.pos += 1 #avanza al siguiente token por si no pudo identificar la instruccion, para evitar un bucle infinito
        return instrucciones #devuelve la lista de instrucciones que se han parseado

    def parse_bloque(self):
        self.consumir('LLAVE_A') #espera qe para cada valida, tal vezi o sino haya un (( que es el inicio del bloque de instrucciones
        instrucciones = []
        while self.actual()[0] not in ('LLAVE_C', 'EOF'):#mantiene leyendo instrucciones hasta que encuentre el )) que es el fin del bloque o EOF por si no se cierra el bloque
            inst = self.parse_instruccion()
            if inst: instrucciones.append(inst)#si paso se agrega a la lista de instrucciones del bloque
        self.consumir('LLAVE_C')#espera que después de leer todas las instrucciones del bloque, encuentre el )) que es el fin del bloque
        return instrucciones#devuelve la lista de instrucciones que se encuentran dentro del bloque

    def parse_instruccion(self):
        tipo, valor = self.actual() #lee el tipo y valor del token actual para decidir qué tipo de instrucción es, por ejemplo si es VALIDA entonces es un if, si es TIPO_ENT entonces es una declaración de variable, etc
        
        if tipo == 'VALIDA': #if
            self.consumir('VALIDA')
            self.consumir('PAR_A')#si es valida entonces espera que sea PAR_A osea [luego la condicion
            condicion = self.parse_expr()#este guarda la condicion del if 
            self.consumir('PAR_C')#]
            bloque_if = self.parse_bloque()#si es espera a que este el bloque de instrucciones del if entre (( y )) 

            bloques_elif = [] #aqui se guardan los else if
            while self.actual()[0] == 'TAL_VEZI': #si crea mas de un talvezi entonces se lee por orden desde el primero hasta el ultimo o que llegue a sino o u fin
                self.consumir('TAL_VEZI')#revisa si es un talevezi 
                self.consumir('PAR_A')#luego de validar tambien espera que sea PAR_A osea [ y lego la condicion
                cond_elif = self.parse_expr()#aqui se guarda la condicion del else if
                self.consumir('PAR_C') #]
                bloque_elif = self.parse_bloque()#si es un talevezi entonces espera a que este el bloque de instrucciones del else if entre (( y ))
                bloques_elif.append((cond_elif, bloque_elif))#si hay otro talevezi se agrega a la lista de bloques elif junto con su condicion

            bloque_else = None #significa que no es necesario un bloue sino osea else
            if self.actual()[0] == 'SINO':#si encuentra un sino entoces comiensa a leer desde 0
                self.consumir('SINO')#al igual que if y elif revisa que sea un sino y luego espera que este
                bloque_else = self.parse_bloque()#si es sino entones espera a que este el bloque de instrucciones del else entre (( y ))

            return ('if', condicion, bloque_if, bloques_elif, bloque_else)#agrupa toda la info del if,elif y else en un sola cosa para que los interprete

        elif tipo in ('TIPO_ENT', 'TIPO_FLOT', 'TIPO_DOBLE', 'TIPO_LARGO'):#revisa si es una de estas palabras reservadas
            self.consumir(tipo) #valida si es una palabra reservada de tipo de dato
            tipo_id, nombre_var = self.actual()#dependiendo del tipo de dato que sea, espera que el siguiente token sea como su instruccion
            
            if tipo_id == 'ID_VAR':#el tipo de dato espera que sea esa variable que comienze con @v_
                self.consumir(tipo_id)#valida que sea tipo identificador de variable
            else:
                raise SyntaxError(f"Nombre inválido '{nombre_var}'. Debe iniciar con @v_")#en caso de que no sea una variable valida, se detiene el programa y muestra un mensaje de error indicando que el nombre es inválido y debe iniciar con @v_
            
            if self.actual()[0] == 'ASIGNADOR':#revisa que sea el token osea >> y si es asi comienza a leer desde 0
                self.consumir('ASIGNADOR')#valida que sea el token de asignacion >>
                expr = self.parse_expr()#analiza la expresion que se encuentra  la derecha
                self.consumir('FIN')#valida que la instruccion termine con ~
                return ('asignacion_decl', nombre_var, expr)#asignacion_decl significa la variable a la izquerda y nombre_var es el nombre

            else:#si no le dio un vaalor a una variable
                self.consumir('FIN')#exige el  fin de la instruccion con ~
                return ('declaracion', nombre_var)#si guarda una declaracion d evariable pero sin valor

        elif tipo == 'PEG':#analiza si es un pegoseaun pritf
            self.consumir('PEG')#valida que sea un peg 
            self.consumir('PAR_A')#valida que despues del peg haya un [
            expr = self.parse_expr()#analiza lo que seenncuentra dentro del [] que puede ser una operacion o una variable o un texto o un numero etc etc
            self.consumir('PAR_C')#despues valida que cierre con un ]
            self.consumir('FIN')#valida que termine con un 
            return ('imprimir', expr)#usa el imprimir  para que interprete que es la accion y usa el expr paa que sepa lo que va a imprimir
            
        elif tipo == 'ESCANEA':
            self.consumir('ESCANEA')
            self.consumir('PAR_A')
            tipo_id, nombre_var = self.actual()
            if tipo_id == 'ID_VAR':
                self.consumir(tipo_id)
            else:
                raise SyntaxError(f"escanea requiere una variable válida, encontré '{nombre_var}'")
            self.consumir('PAR_C')
            self.consumir('FIN')
            return ('leer', nombre_var)

        elif tipo == 'ID_VAR':
            nombre = self.consumir(tipo)
            self.consumir('ASIGNADOR')
            expr = self.parse_expr()
            self.consumir('FIN')
            return ('asignacion', nombre, expr)
            
        return None

    def parse_expr(self):
        izq = self.parse_termino()
        tipo, valor = self.actual()
        if tipo in ('SUMA', 'REST', 'MULT', 'DIVS', 'MODU', 'POW', 'MAYOR', 'MENOR', 'Y', 'O'):
            self.pos += 1
            der = self.parse_termino()
            return ('operacion', izq, valor.lower(), der)
        return izq

    def parse_termino(self):
        tipo, valor = self.actual()
        if tipo == 'ENT':
            self.pos += 1
            return ('entero', int(valor))
        elif tipo == 'FLOT':
            self.pos += 1
            return ('flotante', float(valor.replace('ç', '.')))
        elif tipo == 'CADENA':
            self.pos += 1
            return ('cadena', valor[1:-1]) 
        elif tipo == 'ID_VAR':
            self.pos += 1
            return ('variable', valor)
        elif tipo == 'ID_NUM':
            self.pos += 1
    
            return ('entero', int(valor.split('_')[1]))
        raise SyntaxError(f"Valor no reconocido en la operación: {valor}")



class Interpreter:
    def __init__(self, consola_widget): 
        self.variables = {}
        self.consola = consola_widget

    def imprimir(self, texto):
        self.consola.insert(tk.END, str(texto) + "\n")

    def evaluar(self, nodo):
        tipo = nodo[0]
        if tipo == 'entero': return nodo[1]
        if tipo == 'flotante': return nodo[1]
        if tipo == 'cadena': return nodo[1]
        if tipo == 'variable': 
            if nodo[1] not in self.variables:
                raise RuntimeError(f"Error: La variable '{nodo[1]}' no tiene valor.")
            return self.variables[nodo[1]]
            
        if tipo == 'operacion':
            izq = self.evaluar(nodo[1])
            der = self.evaluar(nodo[3])
            op = nodo[2]
            
            if op == 'suma': return izq + der
            if op == 'rest': return izq - der
            if op == 'mult': return izq * der
            if op == 'divs': return izq / der
            if op == 'modu': return izq % der
            if op == 'pow': return izq ** der
            
            if op == 'mayor': return izq > der
            if op == 'menor': return izq < der
            if op == 'y': return izq and der
            if op == 'o': return izq or der

    def ejecutar(self, instrucciones):
        for inst in instrucciones:
            if inst[0] == 'declaracion':
                nombre = inst[1]
                self.variables[nombre] = 0 
            elif inst[0] in ('asignacion', 'asignacion_decl'):
                nombre = inst[1]
                valor = self.evaluar(inst[2])
                self.variables[nombre] = valor 
            elif inst[0] == 'imprimir':
                valor = self.evaluar(inst[1])
                self.imprimir(valor) 
            elif inst[0] == 'leer':
                nombre = inst[1]
                valor_str = simpledialog.askstring("Entrada de Datos", f"Ingresa valor para {nombre}:")
                if valor_str is None:
                    raise RuntimeError("Entrada cancelada.")
                try:
                    if 'ç' in valor_str:
                        valor = float(valor_str.replace('ç', '.'))
                    else:
                        valor = int(valor_str)
                except ValueError:
                    valor = valor_str 
                self.variables[nombre] = valor
            
            elif inst[0] == 'if':
                _, condicion, bloque_if, bloques_elif, bloque_else = inst
                
                if self.evaluar(condicion):
                    self.ejecutar(bloque_if)
                else:
                    evaluado = False
                    for cond_elif, block_elif in bloques_elif:
                        if self.evaluar(cond_elif):
                            self.ejecutar(block_elif)
                            evaluado = True
                            break
                    if not evaluado and bloque_else:
                        self.ejecutar(bloque_else)


def compilar_ejecutar():
    codigo = texto_codigo.get("1.0", tk.END)
    consola.config(state=tk.NORMAL)
    consola.delete("1.0", tk.END)
    
    try:
        tokens = lexer(codigo)
        parser = Parser(tokens)
        arbol = parser.parse()
        interprete = Interpreter(consola)
        interprete.ejecutar(arbol)
    except Exception as e:
        consola.insert(tk.END, f"Error: {str(e)}")
    finally:
        consola.config(state=tk.DISABLED)

root = tk.Tk()
root.title("IDE - Rayatronic Oficial")
root.geometry("650x550")

tk.Label(root, text="Código Fuente:").pack(anchor="w", padx=10)
texto_codigo = scrolledtext.ScrolledText(root, height=14, width=75, font=("Consolas", 11))
texto_codigo.pack(padx=10, pady=5)

#coigo prueba
codigo_prueba = """ent @v_calificacion ~

peg [ "=== SISTEMA DE CALIFICACIONES ===" ] ~
peg [ "Por favor, ingresa tu calificacion:" ] ~
escanea [ @v_calificacion ] ~

valida [ @v_calificacion mayor n_8 ] ((
    peg [ "¡Excelente! Pasaste la materia sin problemas." ] ~
))
tal vezi [ @v_calificacion mayor n_5 ] ((
    peg [ "Pasaste de panzazo. Apenas la libraste." ] ~
))
sino ((
    peg [ "Reprobado. Nos vemos en el extraordinario." ] ~
))
"""
texto_codigo.insert(tk.END, codigo_prueba)

btn_ejecutar = tk.Button(root, text="Ejecutar Código", command=compilar_ejecutar, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
btn_ejecutar.pack(pady=5)

tk.Label(root, text="Consola de Salida:").pack(anchor="w", padx=10)
consola = scrolledtext.ScrolledText(root, height=10, width=75, state=tk.DISABLED, bg="#000000", fg="#00FF00", font=("Consolas", 11))
consola.pack(padx=10, pady=5)

if __name__ == "__main__":
    root.mainloop() 