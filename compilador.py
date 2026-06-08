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
            
        elif tipo == 'ESCANEA': #analiza si es un escanea osea un scanf
            self.consumir('ESCANEA')#valida que sea un escanea
            self.consumir('PAR_A')#valida que despues del escanea haya un [
            tipo_id, nombre_var = self.actual()#revisa que lo que este dentro del [] sea una variable valida
            if tipo_id == 'ID_VAR':#si es una variable valida entonces se consume y se guarda el nombre de la variable para que el interprete sepa a donde guardar el valor que el usuario ingrese
                self.consumir(tipo_id)#valida que sea un identificador de variable
            else:
                raise SyntaxError(f"escanea requiere una variable válida, encontré '{nombre_var}'")#si no es una variable valida, se detiene el programa y muestra un mensaje de error indicando que escanea requiere una variable válida
            self.consumir('PAR_C')#valida que cierre con un ]
            self.consumir('FIN')#valida que termine con un ~
            return ('leer', nombre_var)#le indica al interprete que esta es una instruccion de lectura y le da el nombre de la variable para que sepa donde guardar el valor que el usuario ingrese

        elif tipo == 'ID_VAR':#si la instruccion comienza con una variable entonces puede ser una asignacion de valor a esa variable
            nombre = self.consumir(tipo)#guarda el nombre de la variable para que el interprete sepa a cual variable le va a asignar el valor
            self.consumir('ASIGNADOR')#valida que despues de la variable haya un token de asignacion >>
            expr = self.parse_expr()#analiza la expresion que se encuentra a la derecha del token de asignacion, puede ser una operacion, un numero, un texto o incluso otra variable
            self.consumir('FIN')#valida que la instruccion termine con un ~
            return ('asignacion', nombre, expr)#si es una asignacion normal sin declaracion previa, entonces se le indica al interprete que esta es una instruccion de asignacion y se le da el nombre de la variable y la expresion que se va a evaluar para obtener el valor a asignar a esa variable
            
        return None#si no se reconoce el tipo de instruccion, devuelve None para que el parser principal pueda decidir si avanza al siguiente token o si muestra un error de sintaxis

    def parse_expr(self):#analiza las expresiones que pueden ser operaciones entre terminos o simplemente un termino solo, por ejemplo puede analizar algo como 5 suma 3 o @v_edad mult 2 o incluso una sola variable o numero o texto
        izq = self.parse_termino()#analiza el primer termino de la expresion, que puede ser un numero, un texto, una variable o incluso otra operacion si es que hay parentesis o corchetes para indicar precedencia
        tipo, valor = self.actual()#despues de analizar el primer termino, revisa si el siguiente token es un operador como suma, rest, mult, divs, etc para saber si tiene que analizar otra parte de la expresion o si simplemente devuelve el termino analizado
        if tipo in ('SUMA', 'REST', 'MULT', 'DIVS', 'MODU', 'POW', 'MAYOR', 'MENOR', 'Y', 'O'):#si el siguiente token es un operador entonces se analiza la parte derecha de la expresion para obtener el segundo termino y luego se devuelve una tupla que representa la operacion completa con su operador y sus operandos
            self.pos += 1#si es un operador valido entonces avanza al siguiente token para analizar el segundo termino de la operacion
            der = self.parse_termino()#analiza el segundo termino de la operacion, que puede ser un numero, un texto, una variable o incluso otra operacion si es que hay parentesis o corchetes para indicar precedencia
            return ('operacion', izq, valor.lower(), der)#devuelve una tupla que representa la operacion completa, donde 'operacion' es un identificador para que el interprete sepa que esto es una operacion, izq es el primer termino analizado, valor.lower() es el operador en minusculas para facilitar su manejo en el interprete, y der es el segundo termino analizado
        return izq#si no hay operador, simplemente devuelve el termino analizado como resultado de la expresion

    def parse_termino(self):#analiza un termino que puede ser un numero, un texto, una variable o incluso otra operacion si es que hay parentesis o corchetes para indicar precedencia
        tipo, valor = self.actual()#lee el tipo y valor del token actual para decidir qué tipo de termino es, por ejemplo si es un numero entero o flotante, un texto entre comillas, una variable que comienza con @v_, o incluso una operacion entre parentesis o corchetes
        if tipo == 'ENT':#si es un numero entero entonces devuelve una tupla con el tipo 'entero' y el valor convertido a int para que el interprete lo maneje como un numero entero
            self.pos += 1#si es un numero entero entonces avanza al siguiente token para seguir analizando la expresion
            return ('entero', int(valor))#devuelve una tupla que representa un numero entero, donde 'entero' es un identificador para que el interprete sepa que esto es un numero entero, y int(valor) es el valor del numero convertido a tipo entero para que el interprete lo maneje como un numero en lugar de una cadena de texto
        elif tipo == 'FLOT':#si es un numero flotante entonces devuelve una tupla con el tipo 'flotante' y el valor convertido a float para que el interprete lo maneje como un numero flotante
            self.pos += 1#si es un numero flotante entonces avanza al siguiente token para seguir analizando la expresion
            return ('flotante', float(valor.replace('ç', '.')))#devuelve una tupla que representa un numero flotante, donde 'flotante' es un identificador para que el interprete sepa que esto es un numero flotante, y float(valor.replace('ç', '.')) es el valor del numero convertido a tipo flotante para que el interprete lo maneje como un numero en lugar de una cadena de texto, además se reemplaza la letra  ç por un punto para que Python pueda reconocerlo como un número decimal
        elif tipo == 'CADENA':#si es un texto entre comillas entonces devuelve una tupla con el tipo 'cadena' y el valor sin las comillas para que el interprete lo maneje como un texto
            self.pos += 1#si es un texto entre comillas entonces avanza al siguiente token para seguir analizando la expresion
            return ('cadena', valor[1:-1]) #devuelve una tupla que representa un texto, donde 'cadena' es un identificador para que el interprete sepa que esto es un texto, y valor[1:-1] es el valor del texto sin las comillas al inicio y al final para que el interprete lo maneje como un texto 
        elif tipo == 'ID_VAR':#si es una variable que comienza con @v_ entonces devuelve una tupla con el tipo 'variable' y el nombre de la variable para que el interprete lo maneje como una variable y pueda buscar su valor en el diccionario de variables
            self.pos += 1#si es una variable que comienza con @v_ entonces avanza al siguiente token para seguir analizando la expresion
            return ('variable', valor)#devuelve una tupla que representa una variable, donde 'variable' es un identificador para que el interprete sepa que esto es una variable, y valor es el nombre de la variable tal como aparece en el código fuente para que el interprete lo maneje como una variable y pueda buscar su valor en el diccionario de variables usando ese nombre
        elif tipo == 'ID_NUM':#si es un numero que comienza con n_ entonces devuelve una tupla con el tipo 'entero' y el valor convertido a int para que el interprete lo maneje como un numero entero, esto se usa para los numeros que aparecen en las condiciones como n_5 o n_10 para que el usuario no tenga que escribir un numero literal y pueda usar esta forma de escribir numeros en las condiciones de if, elif, while, etc
            self.pos += 1#si es un numero que comienza con n_ entonces avanza al siguiente token para seguir analizando la expresion
            return ('entero', int(valor.split('_')[1]))#devuelve una tupla que representa un numero entero, donde 'entero' es un identificador para que el interprete sepa que esto es un numero entero, y int(valor.split('_')[1]) es el valor del numero convertido a tipo entero para que el interprete lo maneje como un numero en lugar de una cadena de texto, además se usa split('_')[1] para obtener solo la parte del numero después de n_ y convertirla a entero
        raise SyntaxError(f"Valor no reconocido en la operación: {valor}")#si el token no es un numero, ni un texto, ni una variable, ni un numero con n_, entonces se detiene el programa y muestra un mensaje de error indicando que el valor no es reconocido en la operación, esto ayuda a detectar errores como escribir mal un numero o una variable o usar un simbolo que no es válido en la expresión



class Interpreter:#aqui se ejecutan las instrucciones parseadas por el parser, recibe la consola para poder imprimir los resultados de las instrucciones de impresión y para mostrar los errores que puedan ocurrir durante la ejecución
    def __init__(self, consola_widget): #inicializa el diccionario de variables para guardar los valores de las variables declaradas y asignadas durante la ejecución, y guarda la referencia al widget de consola para poder imprimir en él
        self.variables = {}#diccionario para guardar las variables y sus valores, por ejemplo {'@v_edad': 20, '@v_nombre': 'Limon'}
        self.consola = consola_widget#referencia al widget de consola para poder imprimir los resultados de las instrucciones de impresión y para mostrar los errores que puedan ocurrir durante la ejecución

    def imprimir(self, texto):#método para imprimir texto en la consola, recibe el texto a imprimir y lo inserta al final del widget de consola seguido de un salto de línea para que cada impresión aparezca en una nueva línea
        self.consola.insert(tk.END, str(texto) + "\n")#inserta el texto convertido a cadena en el widget de consola, seguido de un salto de línea para que cada impresión aparezca en una nueva línea

    def evaluar(self, nodo):#método para evaluar un nodo de la expresión, recibe un nodo que puede ser un numero, un texto, una variable o una operación, y devuelve el valor resultante de evaluar ese nodo, por ejemplo si el nodo es ('entero', 5) devuelve 5, si el nodo es ('variable', '@v_edad') busca el valor de @v_edad en el diccionario de variables y lo devuelve, si el nodo es una operación entonces evalua los operandos y aplica el operador para devolver el resultado de la operación
        tipo = nodo[0]#el tipo del nodo es el primer elemento de la tupla, por ejemplo 'entero', 'flotante', 'cadena', 'variable' o 'operacion'
        if tipo == 'entero': return nodo[1]#si el tipo del nodo es 'entero', devuelve el segundo elemento de la tupla que es el valor del numero entero, por ejemplo si el nodo es ('entero', 5) entonces devuelve 5
        if tipo == 'flotante': return nodo[1]#si el tipo del nodo es 'flotante', devuelve el segundo elemento de la tupla que es el valor del numero flotante, por ejemplo si el nodo es ('flotante', 3.14) entonces devuelve 3.14
        if tipo == 'cadena': return nodo[1]#si el tipo del nodo es 'cadena', devuelve el segundo elemento de la tupla que es el valor de la cadena, por ejemplo si el nodo es ('cadena', 'Hola, mundo!') entonces devuelve 'Hola, mundo!'
        if tipo == 'variable':#si el tipo del nodo es 'variable', busca el valor de la variable en el diccionario de variables usando el nombre de la variable que es el segundo elemento de la tupla, por ejemplo si el nodo es ('variable', '@v_edad') entonces busca el valor de @v_edad en el diccionario de variables y lo devuelve, si la variable no existe en el diccionario, se detiene el programa y muestra un mensaje de error indicando que la variable no tiene valor 
            if nodo[1] not in self.variables:#si el nombre de la variable que se quiere evaluar no existe en el diccionario de variables, entonces se detiene el programa y muestra un mensaje de error indicando que la variable no tiene valor, esto ayuda a detectar errores como usar una variable sin declararla o sin asignarle un valor antes de usarla
                raise RuntimeError(f"Error: La variable '{nodo[1]}' no tiene valor.")#si el nombre de la variable que se quiere evaluar no existe en el diccionario de variables, entonces se detiene el programa y muestra un mensaje de error indicando que la variable no tiene valor, esto ayuda a detectar errores como usar una variable sin declararla o sin asignarle un valor antes de usarla
            return self.variables[nodo[1]]#si el nombre de la variable que se quiere evaluar existe en el diccionario de variables, entonces devuelve su valor para que pueda ser usado en la expresión, por ejemplo si el nodo es ('variable', '@v_edad') y en el diccionario de variables tenemos {'@v_edad': 20}, entonces devuelve 20
            
        if tipo == 'operacion':#si el tipo del nodo es 'operacion', entonces se evalua la operación, para eso primero se evalua el operando izquierdo que es el segundo elemento de la tupla, luego se evalua el operando derecho que es el cuarto elemento de la tupla, y luego se aplica el operador que es el tercer elemento de la tupla para obtener el resultado de la operación, por ejemplo si el nodo es ('operacion', ('entero', 5), 'suma', ('entero', 3)) entonces primero se evalua ('entero', 5) que devuelve 5, luego se evalua ('entero', 3) que devuelve 3, y luego se aplica el operador 'suma' para obtener el resultado de 5 + 3 que es 8
            izq = self.evaluar(nodo[1])#evalua el operando izquierdo de la operación, que es el segundo elemento de la tupla,
            der = self.evaluar(nodo[3])#evalua el operando derecho de la operación, que es el cuarto elemento de la tupla,
            op = nodo[2]#obtiene el operador de la operación, que es el tercer elemento de la tupla, y lo convierte a minusculas para facilitar su manejo en el interprete, por ejemplo 'suma', 'rest', 'mult', 'divs', etc
            
            if op == 'suma': return izq + der#si el operador es 'suma', devuelve la suma del operando izquierdo y el operando derecho, por ejemplo si izq es 5 y der es 3, entonces devuelve 8
            if op == 'rest': return izq - der#si el operador es 'rest', devuelve la resta del operando izquierdo y el operando derecho, por ejemplo si izq es 5 y der es 3, entonces devuelve 2
            if op == 'mult': return izq * der#si el operador es 'mult', devuelve la multiplicación del operando izquierdo y el operando derecho, por ejemplo si izq es 5 y der es 3, entonces devuelve 15
            if op == 'divs': return izq / der#si el operador es 'divs', devuelve la división del operando izquierdo y el operando derecho, por ejemplo si izq es 5 y der es 3, entonces devuelve 1.666...
            if op == 'modu': return izq % der#si el operador es 'modu', devuelve el módulo del operando izquierdo y el operando derecho, por ejemplo si izq es 5 y der es 3, entonces devuelve 2
            if op == 'pow': return izq ** der#si el operador es 'pow', devuelve la potencia del operando izquierdo y el operando derecho, por ejemplo si izq es 5 y der es 3, entonces devuelve 125
            
            if op == 'mayor': return izq > der#si el operador es 'mayor', devuelve True si el operando izquierdo es mayor que el operando derecho, False en caso contrario, por ejemplo si izq es 5 y der es 3, entonces devuelve True
            if op == 'menor': return izq < der#si el operador es 'menor', devuelve True si el operando izquierdo es menor que el operando derecho, False en caso contrario, por ejemplo si izq es 5 y der es 3, entonces devuelve False
            if op == 'y': return izq and der#si el operador es 'y', devuelve True si ambos operandos son True, False en caso contrario, por ejemplo si izq es True y der es False, entonces devuelve False
            if op == 'o': return izq or der#si el operador es 'o', devuelve True si al menos uno de los operandos es True, False en caso contrario, por ejemplo si izq es True y der es False, entonces devuelve True

    def ejecutar(self, instrucciones):#método para ejecutar una lista de instrucciones parseadas por el parser, recibe una lista de instrucciones que pueden ser declaraciones de variables, asignaciones de valores a variables, instrucciones de impresión, instrucciones de lectura, o estructuras de control como if, elif y else, y ejecuta cada instruccion en orden para llevar a cabo la lógica del programa
        for inst in instrucciones:#recorre cada instruccion de la lista de instrucciones para ejecutarla, por ejemplo si la instruccion es una declaración de variable, entonces se agrega la variable al diccionario de variables con un valor inicial de 0, si la instruccion es una asignacion de valor a una variable, entonces se evalua la expresion del lado derecho y se asigna el resultado a la variable en el diccionario de variables, si la instruccion es una instruccion de impresión, entonces se evalua la expresion a imprimir y se muestra en la consola, si la instruccion es una instruccion de lectura, entonces se muestra un cuadro de diálogo para que el usuario ingrese un valor y se asigna ese valor a la variable correspondiente en el diccionario de variables, si la instruccion es una estructura de control como if, elif o else, entonces se evalua la condicion y se ejecuta el bloque de instrucciones correspondiente según el resultado de la condicion
            if inst[0] == 'declaracion':#si la instruccion es una declaración de variable sin asignación de valor, entonces se agrega la variable al diccionario de variables con un valor inicial de 0 para que el programa pueda seguir ejecutándose sin errores, aunque lo ideal sería que el usuario siempre asigne un valor a las variables para evitar confusiones
                nombre = inst[1]#el nombre de la variable es el segundo elemento de la tupla de la instruccion, por ejemplo si la instruccion es ('declaracion', '@v_edad') entonces el nombre de la variable es '@v_edad'
                self.variables[nombre] = 0 #se agrega la variable al diccionario de variables con un valor inicial de 0, por ejemplo si el nombre de la variable es '@v_edad', entonces se agrega '@v_edad': 0 al diccionario de variables
            elif inst[0] in ('asignacion', 'asignacion_decl'):#si la instruccion es una asignacion de valor a una variable, ya sea con declaración previa o sin ella, entonces se evalua la expresion del lado derecho para obtener el valor a asignar, y luego se asigna ese valor a la variable en el diccionario de variables, 
                nombre = inst[1]#el nombre de la variable a la que se le va a asignar el valor es el segundo elemento de la tupla de la instruccion, por ejemplo si la instruccion es ('asignacion', '@v_edad', expr) entonces el nombre de la variable es '@v_edad'
                valor = self.evaluar(inst[2])#se evalua la expresion que se encuentra a la derecha del token de asignacion para obtener el valor a asignar a la variable, por ejemplo si la instruccion es ('asignacion', '@v_edad', ('operacion', ('entero', 20), 'suma', ('entero', 5))) entonces se evalua la expresion ('operacion', ('entero', 20), 'suma', ('entero', 5)) que devuelve 25, y ese es el valor que se va a asignar a @v_edad
                self.variables[nombre] = valor #se asigna el valor obtenido al nombre de la variable en el diccionario de variables, por ejemplo si el nombre de la variable es '@v_edad' y el valor obtenido es 25, entonces se asigna '@v_edad': 25 en el diccionario de variables para que a partir de ese momento @v_edad tenga el valor de 25 cuando se evalue su nodo en la expresión
            elif inst[0] == 'imprimir':#si la instruccion es una instruccion de impresión, entonces se evalua la expresion que se encuentra dentro del peg para obtener el valor a imprimir, y luego se muestra ese valor en la consola usando el método imprimir, 
                self.imprimir(valor)#se evalua la expresion que se encuentra dentro del peg para obtener el valor a imprimir, 
                nombre = inst[1]#el valor a imprimir es el segundo elemento de la tupla de la instruccion, por ejemplo si la instruccion es ('imprimir', ('operacion', ('entero', 5), 'suma', ('entero', 3))) entonces el valor a imprimir es la expresion ('operacion', ('entero', 5), 'suma', ('entero', 3)) que se evalua para obtener el resultado de 8, y ese es el valor que se va a imprimir en la consola
                valor_str = simpledialog.askstring("Entrada de Datos", f"Ingresa valor para {nombre}:")#si la instruccion es una instruccion de lectura, entonces se muestra un cuadro de diálogo para que el usuario ingrese un valor, y ese valor se asigna a la variable correspondiente en el diccionario de variables, 
                if valor_str is None:#si el usuario cancela el cuadro de diálogo o no ingresa ningún valor, entonces se detiene el programa y muestra un mensaje de error indicando que la entrada fue cancelada, esto ayuda a evitar que el programa siga ejecutándose con un valor nulo o vacío que podría causar errores en las operaciones posteriores
                    raise RuntimeError("Entrada cancelada.")
                try:
                    if 'ç' in valor_str:#si el valor ingresado por el usuario contiene la letra ç
                        valor = int(valor_str)#enotnces se intenta convertir el valor ingresado a un número entero, esto es para permitir que el usuario ingrese números decimales usando la letra ç como separador decimal
                except ValueError:#si marca un error de valor entonces
                    valor = valor_str #si el valor ingresado no se puede convertir a un número entero, entonces se asume que es un texto y se asigna el valor ingresado como una cadena de texto, esto permite que el usuario ingrese tanto números como textos en las instrucciones de lectura sin causar errores de conversión
                self.variables[nombre] = valor#se asigna el valor ingresado por el usuario a la variable correspondiente en el diccionario de variables, 
            
            elif inst[0] == 'if':#si la instruccion es una estructura de control if, entonces se evalua la condicion del if para determinar si se ejecuta el bloque de instrucciones del if o si se evaluan las condiciones de los elif o si se ejecuta el bloque de instrucciones del else, dependiendo del resultado de las evaluaciones de las condiciones
                _, condicion, bloque_if, bloques_elif, bloque_else = inst
                
                if self.evaluar(condicion):#si la condicion del if se evalua como True, entonces se ejecuta el bloque de instrucciones del if usando el método ejecutar para ejecutar cada instruccion dentro del bloque, y luego se continúa con la siguiente instruccion después del if sin evaluar los elif ni el else
                    self.ejecutar(bloque_if)#se ejecuta 
                else:#pero si es false el if entonces
                    evaluado = False
                    for cond_elif, block_elif in bloques_elif:#entonces se evalua cada una de las condiciones de los elif en orden, y si alguna de las condiciones de los elif se evalua como True, entonces se ejecuta el bloque de instrucciones correspondiente a ese elif 
                            self.ejecutar(block_elif)#se ejecuta
                            evaluado = True
                            break
                    if not evaluado and bloque_else:#si ninguna de las condiciones de los elif se evaluó como True, y además existe un bloque de instrucciones para el else, entonces se ejecuta el bloque de instrucciones del else
                        self.ejecutar(bloque_else)#se ejecuta el bloque de instrucciones del else si ninguna de las condiciones anteriores se evaluó como True, 


def compilar_ejecutar():#esta función se llama cuando el usuario hace clic en el botón Ejecutar Código en la interfaz , y se encarga de tomar el código fuente escrito por el usuario en el widget de texto, pasarlo por el lexer para obtener los tokens, luego por el parser para obtener la estructura de instrucciones, y finalmente crear una instancia del interprete para ejecutar esas instrucciones y mostrar los resultados en la consola, además maneja cualquier error que pueda ocurrir durante este proceso y los muestra en la consola para que el usuario pueda corregir su código
    codigo = texto_codigo.get("1.0", tk.END)# Toma todo el texto que el usuario escribió en la caja de código, desde la primera línea hasta el final
    consola.config(state=tk.NORMAL)# Habilita temporalmente la consola de salida para poder escribir los resultados o errores
    consola.delete("1.0", tk.END)# Borra todo lo que tenía la consola antes para que no se amontone con la nueva ejecución
    
    try:#
        tokens = lexer(codigo)#Pasa el código texto por el lexer para romperlo y convertirlo en una lista de tokens
        parser = Parser(tokens)#Le entrega los tokens al Parser para acomodarlos en orden estructurado
        arbol = parser.parse()#El parser genera el "árbol" de instrucciones es decir la lista con la lógica organizada
        interprete = Interpreter(consola)#Crea el intérprete y le pasa la consola para saber dónde pintar los resultados
        interprete.ejecutar(arbol)#El intérprete lee el árbol y ejecuta las acciones una por una en la vida real
    except Exception as e:
        consola.insert(tk.END, f"Error: {str(e)}")# Si algo falla en el lexer, parser o intérprete, atrapa el error y lo pinta en la consola en color verde
    finally:
        consola.config(state=tk.DISABLED)# Pase lo que pase corra bien o con error, vuelve a bloquear la consola para que el usuario no pueda escribir en ella directamente

# Crea la ventana principal de la interfaz gráfica usando Tkinter
root = tk.Tk()
root.title("IDE - Rayatronic Oficial")#titulo
root.geometry("650x550")#tamaño

tk.Label(root, text="Código Fuente:").pack(anchor="w", padx=10)# Crea y acomoda la etiqueta (texto descriptivo) para el área de código fuente
texto_codigo = scrolledtext.ScrolledText(root, height=14, width=75, font=("Consolas", 11))# Crea la caja de texto grande con barra de desplazamiento  para escribir el código fuente
texto_codigo.pack(padx=10, pady=5)# Lo acomoda en la ventana dándole un margen

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