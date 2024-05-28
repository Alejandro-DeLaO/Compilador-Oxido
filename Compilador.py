#Marlene Paola Avalos Lopez
#Alejandro de la O Ramirez

import pathlib
import sys

class Analizador:
    idx = 0
    rows = ""
    input = ""
    #estados error y aceptor
    ERR = -1
    ACP = 999
    #valores logicos
    bool = ["verdadero", "falso"]
    #palabras reservadas
    res = [
        "fn", "principal", "imprimeln", "imprimeln!", "entero", "const", 
        "decimal", "logico", "alfabetico", "sea", "si", "sino", "para", 
        "en", "mientras", "ciclo", "regresa","leer", "interrumpe","continua","mut", "testfor"]
    
    #operadores aritmeticos
    arith_op = ["+", "-", "*", "%", "^"]
    #operadores relacionales
    rel_op = ["<", ">"]
    #Delimitadores universales||secuencias de escape
    univer_dlm = [" ", "\t", "\n"]
    #delimitadores
    dlm = ["{", "}", "[", "]", "(", ")", ";", ",", ":", "."]
    #simbolos
    sym = ["#", "$", "¿", "?", "¡", "|", "`", "~", "\\", "@", "&"]
    #matriz de transicion
    matran = [
        [  1,   1,  22,   2,   7,   8,  10,  12,  16,  20,  18,  14,  21,   5],  # 0 nl, tab, space state
        [  1,   1, ACP,   1, ACP, ACP,   1, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 1 identifier name state
        [ACP, ACP,   3,   2, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 2 int state
        [ERR, ERR, ERR,   4, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR],  # 3 int. state
        [ACP, ACP, ACP,   4, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 4 decimal state
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,   6],  # 5 division operator state
        [  6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6],  # 6 comment state
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 7 math operators state
        [ERR, ERR, ERR, ERR, ERR,   9, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR],  # 8 & sym state
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 9 &&(and) state
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP,  11, ACP, ACP, ACP, ACP, ACP, ACP],  # 10 ! (negation) state
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 11 != (not equal) state
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP,  13, ACP, ACP, ACP, ACP, ACP, ACP],  # 12 = (assignation) state
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 13 == (equality) state
        [ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR,  15, ERR, ERR],  # 14 | sym state
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 15 || (or) state
        [ 16,  16,  16,  16,  16,  16,  16,  16,  17,  16,  16,  16,  16,  16],  # 16 string initial state "words
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 17 string closure state "
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP,  19, ACP, ACP, ACP, ACP, ACP, ACP],  # 18 greater than/ lower than state
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 19 greater or equal than/ lower or equal than state
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 20 delimiters state
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 21 symbols state
        [ERR, ERR,  23, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR],  # 22 . sym state
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 23 .. (range) state
    ]
    tok = ""
    lex = ""
    dim1 = 0
    dim2 = 0
    contador_dimension = 0;
    tab_sim = {}
    tabla_de_valores = {}
    pl0_program = []
    nombre_del_archivo = ""
    contador_codigo = 1
    contador_linea = 1
    contador_columna = 0
    contador_etiquetas = 0
    imprimir_y_linea = False

    # Inicializador de la clase
    def __init__(self, nombre_del_archivo, input, rows):
        self.nombre_del_archivo = nombre_del_archivo
        self.input = input
        self.rows = rows

    def insertar_codigo(self, contador_codigo, cPl0):
        self.pl0_program[contador_codigo] = cPl0 
        self.contador_codigo += 1

    def insertar_tabla_simbolos(self, key, colec):
        self.tab_sim[key] = colec

    def obtener_simbolo(self, key):
        return self.tab_sim[key]

    def insertar_tabla_de_valores(self, key, value):
        self.tabla_de_valores[key] = value
    
    def obtener_valor(self, key):
        return self.tabla_de_valores[key]
    
    def print_semicolon_newline_error(self, numero_de_linea_evaluada):
        linea_a_analizar = self.rows[numero_de_linea_evaluada - 1]
        longitud_de_linea = len(linea_a_analizar)
        idx = longitud_de_linea - 1
        while idx >= 0:
            if linea_a_analizar[idx] not in self.univer_dlm:
                idx += 1
                break
            idx -= 1
        print("\033[1;31mError de Sintaxis Se esperaba ;\x1b[0m")
        print("\033[1;31m" + "\n[" + str(numero_de_linea_evaluada) + "]" + " [" + str(idx) + "] \x1b[0m", end="")
        print(self.rows[numero_de_linea_evaluada - 1] + "\033[1;31m", end="")
        sangria = idx + len(str(numero_de_linea_evaluada)) + len(str(idx)) + 4 + 2 + 1

        print("^".rjust(sangria))
        print(";".rjust(sangria) + "\x1b[0m")
        sys.exit()

    def print_error_line(self, error_line_num, correction):
        print("\033[1;31m" + "\n[" + str(self.contador_linea) + "]" + " [" + str(self.contador_columna) + "] \x1b[0m", end="")
        print(self.rows[error_line_num] + "\033[1;31m", end="")
        i = 0
        highlight = ""
        while i < len(self.lex):
            highlight += "^"
            i += 1

        #el 4 por los [], el 2 por los espacios y el -1 porque cuando tokenizas te detienes en el siguiente idx
        sangria = self.contador_columna + len(str(self.contador_linea)) + len(str(self.contador_columna)) + 4 + 2 

        print(highlight.rjust(sangria) + "\x1b[0m")

    # Metodo para imprimir errores
    def print_error(self, type, message, correction):
        print("\033[1;31m"+type, message + "\x1b[0m")
        self.print_error_line(self.contador_linea-1, correction)
        sys.exit()


#################################
# Metodos del analizador Lexico #
#################################

    # Metodo para decidir la siguiente columna de la matriz de transicion
    def columna(self, c):
        if c.isalpha():          return 0
        elif c == "_":           return 1
        elif c == ".":           return 2
        elif c.isdigit():        return 3
        elif c in self.arith_op: return 4
        elif c == "&":           return 5
        elif c == "!":           return 6
        elif c == "=":           return 7
        elif c == '"':           return 8
        elif c in self.dlm:      return 9
        elif c in self.rel_op:   return 10
        elif c == "|":           return 11
        elif c in self.sym:      return 12
        elif c in "/":           return 13
        elif c in self.univer_dlm:      return 0
        else:
            self.print_error("Error Lexico ", str(c) + " No es valido en el alfabeto del lenguaje", "Invalido")
        return self.ERR

    # Inicia el analizador lexico
    def tokeniza(self):
        if self.idx >= len(self.input):
            return '', ''

        token = 'NtK'
        lexema = ''
        while (token in ['Com', 'NtK'] and self.idx < len(self.input)):
            token, lexema = self.analizador_lexico()
        
        return token, lexema

    #Analizador lexico
    def analizador_lexico(self):

        while self.idx < len(self.input):
            #Estado actual de la matriz de transicion?
            estado = 0
            #Estado anterior de la matriz de transicion?
            estAnt = 0
            #lexema
            lex = ""
            #token
            tok = ""

            #mientras el indice no sea el final, el estado no sea aceptor y el estado no sea error
            #este while termina, cuando se haya terminado de leer un lexema completo o cuando haya un error
            while (
                self.idx < len(self.input)
                and estado != self.ACP
                and estado != self.ERR
            ):
                #mientras el caracter actual este dentro de los delimitadores universales y el estado sea 0(0 es el inicio de nuevos lexemas)
                while self.idx < len(self.input) and self.input[self.idx] in [" ", "\n", "\t", ""] and estado == 0:

                    if self.input[self.idx] == "\n":
                        self.contador_linea += 1
                        self.contador_columna = 0
                    elif self.input[self.idx] == " ": self.contador_columna += 1
                    #elif self.input[self.idx] == "\t": self.contador_columna += 4
                    #sumamos 1 al indice hasta llegar a un lexema que no sea un tab, espacio o una nueva linea
                    self.idx += 1
                
                if self.idx >= len(self.input): break
                
                caracter = self.input[self.idx]


                if caracter == "." and estado == 3:
                    lex = lex[0:-1]
                    self.idx -= 1
                    estado = 2
                    break

                #(el estado 6 es el de comentarios)
                if estado == 6:
                    lex += caracter
                    #concatenamos los caracteres hasta terminar de formar el comentario
                    while (estado == 6 and caracter != "\n" and self.idx < len(self.input)):
                        caracter = self.input[self.idx]
                        lex += caracter
                        self.idx += 1

                    #cuando se haya terminado el comentario, salimos del segundo while
                    self.contador_linea += 1
                    self.contador_columna = 0
                    break
                    
                if estado == 1 and caracter.isalpha() != True and caracter.isdigit() != True and caracter != "_":
                    if lex == "o":
                        estado = self.ACP
                        estAnt = 15
                        break
                    elif lex == "y":
                        estado = self.ACP
                        estAnt = 9
                        break

                if estado == 1 and caracter in self.univer_dlm: 
                    estAnt = estado
                    estado = self.ACP

                if estado != 6 and estado != 16 and caracter in self.univer_dlm:
                    break
                
                self.idx += 1
                if caracter != '\t' and caracter != '\n' and caracter != '': self.contador_columna += 1 
                #if caracter == '\t': self.contador_columna += 4

                col = self.columna(caracter)

                if col >= 0 and col <= 13 and estado != self.ERR:
                    estAnt = estado
                    estado = self.matran[estado][col]
                    if estado != self.ACP and estado != self.ERR:
                        lex += caracter

                if estado == self.ACP or estado == self.ERR:
                    if caracter == "\n" and self.contador_columna < 2:
                        self.contador_linea -= 1
                        self.contador_columna = 1

                    self.idx -= 1
                    self.contador_columna -= 1
                    break


            if estado != self.ACP and estado != self.ERR: estAnt = estado

            if estado == 3:
                self.print_error("Error Lexico", lex + " decimal incompleto" , "")
            elif estAnt == 16:
                self.print_error('Error Lexico', 'Cte Alfabetica SIN cerrar '+lex, "")
            elif estAnt == 8:
                self.print_error('Error Lexico', 'Operador logico incompleto '+lex, "")   
            elif estAnt == 1:
                tok = "Ide"
                if lex in self.res:
                    tok = "Res"
                elif lex in self.bool:
                    tok = "CtL"
            elif estAnt == 2:
                tok = "Ent"
            elif estAnt == 4:
                tok = "Dec"
            elif estAnt == 5 or estAnt == 7:
                tok = "Opa"
            elif estAnt == 6:
                tok = "Com"
                
                lex = lex[0 : len(lex) - 1]
            elif estAnt == 9 or estAnt == 10 or estAnt == 15:
                tok = "OpL"
            elif estAnt == 11 or estAnt == 13 or estAnt == 18 or estAnt == 19:
                tok = "OpR"
            elif estAnt == 12:
                tok = "OpS"
            elif estAnt == 17:
                tok = "CtA"
            elif estAnt == 20:
                tok = "Del"
            elif estAnt == 21 or estAnt == 14 or estAnt == 8 or estAnt == 22:
                tok = "Sym"
            elif estAnt == 23:
                tok = "Ran"
            else:
                tok = "NtK"

            return tok, lex
    
    #Imprime todos los tokens
    def imprimir_tokens(self):
        self.idx = 0
        while self.idx < len(self.input):
            token, lexema = analizador.tokeniza()
            print(token, lexema)


#####################################
# Metodos del Analizador Sintactico #
#####################################

# Inicia el analizador sintactico
    def analizador_sintactico(self):
        self.tok, self.lex = self.tokeniza()
        self.global_scope()
        print(str("\033[1;32m" + self.nombre_del_archivo) + ' COMPILO con EXITO!!!\x1b[0m')

# Bloque global
    def global_scope(self):
        while True:
            linea_evaluada = self.contador_linea
            if self.lex == "sea":
                self.declaracion_variables()
                if self.lex != ";" or self.contador_linea != linea_evaluada:
                    if self.contador_linea != linea_evaluada:
                        self.print_semicolon_newline_error(linea_evaluada)
                    self.print_error('Error de Sintaxis',  'Se esperaba ;', ";")
                self.tok, self.lex = self.tokeniza()
            elif self.lex == "fn":
                self.funciones()
            elif self.idx >= len(self.input):
                break
            else:
                self.print_error('Error de Sintaxis', 'Lexema inesperado ' + self.lex, "")

# Define las funciones
    def funciones(self):
            self.lex
            self.tok

            if self.idx >= len(self.input): return
            nombre_de_funcion =''
            while self.idx < len(self.input) and self.lex == 'fn':
                self.tok, self.lex = self.tokeniza()
                if self.tok == 'Ide': nombre_de_funcion = self.lex
                if self.tok == 'Res' and self.lex == 'principal':
                        nombre_de_funcion = self.lex
                        self.insertar_tabla_simbolos('_principal', ['F', 'I', str(self.contador_codigo),'0'])
                        self.insertar_tabla_simbolos('_P',['I', 'I', 1, 0])
                elif self.tok != 'Ide':
                    self.print_error('Error de Sintaxis', 'Se esperaba Ide o principal y llego '+ self.lex , "Ide o principal")
                self.tok, self.lex = self.tokeniza();
                if self.lex != '(': 
                    self.print_error('Error de Sintaxis', 'Se esperaba ( y llego '+ self.lex, "")
                self.tok, self.lex = self.tokeniza();
                if self.lex != ')': self.definicion_de_parametros()
                if self.lex != ')':
                    self.print_error('Error de Sintaxis', 'Se esperaba ) y llego '+ self.lex, "")
                self.tok, self.lex = self.tokeniza();
                if self.lex == '-':
                    self.tok, self.lex = self.tokeniza()
                    if self.lex != '>':
                        self.print_error('Error de Sintaxis', 'Se esperaba > y llego '+ self.lex, "")
                    self.tipo()
                    self.tok, self.lex = self.tokeniza()

                if self.lex != '{':
                    self.print_error('Error de Sintaxis', 'Se esperaba { y llego '+ self.lex, "")
                if self.lex != '}': self.block()

                if nombre_de_funcion == 'principal':
                    self.insertar_codigo(self.contador_codigo, ['OPR', '0', '0'])

# Define los parametros de la funcion declarada
    def definicion_de_parametros(self): 
        sec = ','
        while sec == ',':
            if self.tok != 'Ide': 
                self.print_error('Error de Sintaxis', 'Se esperaba Ide y llego '+ self.lex, "Ide")
            self.tok, self.lex = self.tokeniza()
            if self.lex != ':':
                self.print_error('Error de Sintaxis', 'Se esperaba : y llego '+ self.lex, ":")
            self.tipo()
            self.tok, self.lex = self.tokeniza()
            sec = self.lex
            if sec == ',':
                self.tok, self.lex = self.tokeniza()


    def declaracion_multivariable(self):
        nombres_de_variables = []
        clase_de_variable = ""
        nombre_del_identificador = ""
        total_de_variables = 0
        while True:
            self.dim1 = 0
            self.dim2 = 0
            self.contador_dimension = 0
            self.tok, self.lex = self.tokeniza();
            if self.lex == "mut":
                clase_de_variable = 'V'
                self.tok, self.lex = self.tokeniza()
            elif self.tok == "Ide":
                clase_de_variable = 'C'
            else:
                self.print_error('Error de Sintaxis', 'Se esperaba mut o IDENTIFICADOR y llego ' + self.lex, "mut o IDENTIFICADOR")

            if self.tok == "Ide":
                nombre_del_identificador = self.lex 
                self.tok, self.lex = self.tokeniza()
            else:
                self.print_error('Error de Sintaxis', 'Se esperaba IDENTIFICADOR y llego ' + self.lex, "IDENTIFICADOR")

            if self.lex == "[":
                self.dimens()
            
            nombres_de_variables.append(nombre_del_identificador)
            self.insertar_tabla_simbolos(nombre_del_identificador, [clase_de_variable, "I", str(self.dim1), str(self.dim2)])

            if self.lex != ",":
                break

        if self.lex != ")":
            self.print_error('Error de Sintaxis', 'Se esperaba ) y llego ' + self.lex, "")

        total_de_variables = len(nombres_de_variables)
        self.tok, self.lex = self.tokeniza()

        if self.lex == ";":
            self.print_error('Error de Sintaxis', 'Se esperaba ETIQUETA DE TIPO o ASIGNACION y llego ' + self.lex, "ETIQUETA DE TIPO o ASIGNACION")

        if self.lex == ":":
            self.tok, self.lex = self.tokeniza()
            if total_de_variables == 1 and self.lex != "(":
                if self.lex in ["alfabetico", "logico", "entero", "decimal"]:
                    
                    tipo_de_dato = "I"
                    if self.lex == "alfabetico": tipo_de_dato = "A"
                    elif self.lex == "logico": tipo_de_dato = "L"
                    elif self.lex == "entero": tipo_de_dato = "E"
                    elif self.lex == "decimal": tipo_de_dato = "D"

                    #obtengo el unico nombre guardado, uso el nombre como llave para obtener la coleccion de la tabla de simbolos
                    #cambio el valor de la posicion 1 (el tipo de dato) al tipo correspondiente
                    self.tab_sim[nombres_de_variables[0]][1] = tipo_de_dato
                else:
                    self.print_error('Error de Sintaxis', 'Se esperaba TIPO DE DATO y llego ' + self.lex, "TIPO DE DATO")
            elif self.lex == "(":
                variable_actual = 0
                while True:
                    if variable_actual == total_de_variables:
                        self.print_error('Error de Semantica', 'Se intenta asignar mas tipos que variables' , "")
                    self.tok, self.lex = self.tokeniza()
                    if self.lex in ["alfabetico", "logico", "entero", "decimal"]:
                        tipo_de_dato = "I"
                        if self.lex == "alfabetico": tipo_de_dato = "A"
                        elif self.lex == "logico": tipo_de_dato = "L"
                        elif self.lex == "entero": tipo_de_dato = "E"
                        elif self.lex == "decimal": tipo_de_dato = "D"
                        self.tab_sim[nombres_de_variables[variable_actual]][1] = tipo_de_dato
                        variable_actual += 1
                        self.tok, self.lex = self.tokeniza()
                    else:
                        self.print_error('Error de Sintaxis', 'Se esperaba TIPO DE DATO y llego ' + self.lex, "TIPO DE DATO")
                    if self.lex != ",":
                        if variable_actual < total_de_variables:
                            self.print_error('Error de Semantica', 'Se intenta asignar menos tipos que variables', "")
                        break

                if self.lex != ")":
                    self.print_error('Error de Sintaxis', 'Se esperaba ) y llego ' + self.lex, "")
                self.tok, self.lex = self.tokeniza()
                if self.lex == ";" or self.lex != "=":
                    return
            else:
                self.print_error('Error de Sintaxis', 'Se esperaba ( y llego ' + self.lex, "")
        

        if self.lex == "=":
            self.tok, self.lex = self.tokeniza()
            if total_de_variables == 1 and self.lex != "(":
                self.asignar_valor(nombres_de_variables[0])
                return
            if self.lex != "(":
                self.print_error('Error de Sintaxis', 'Se esperaba ( y llego ' + self.lex, "")
            
            
            variable_actual = 0
            while True:
                if variable_actual == total_de_variables:
                    self.print_error('Error de Semantica', 'Se intenta asignar mas valores que variables', "")
                self.tok, self.lex = self.tokeniza()
                self.asignar_valor(nombres_de_variables[variable_actual])
                variable_actual += 1
                if self.lex != ",":
                    if variable_actual < total_de_variables:
                        self.print_error('Error de Semantica', 'Se intenta asignar menos valores que variables', "")
                    break

            if self.lex != ")":
                self.print_error('Error de Sintaxis', 'Se esperaba ) y llego ' + self.lex, "")
            self.tok, self.lex = self.tokeniza()
            return
        
        self.print_error('Error de Sintaxis', 'Lexema inesperado ' + self.lex, "")


    def declaracion_variables(self):
        self.dim1 = 0
        self.dim2 = 0
        self.contador_dimension = 0
        tipo_de_dato = 'I'
        clase_de_variable = ''
        valor = ''
        self.tok, self.lex = self.tokeniza();
        if self.lex == "(":
            self.declaracion_multivariable()
            return

        elif self.lex == "mut":
            clase_de_variable = 'V'
            self.tok, self.lex = self.tokeniza()
        elif self.tok == "Ide":
            clase_de_variable = 'C'
        else:
             self.print_error('Error de Sintaxis', 'Se esperaba mut, IDENTIFICADOR o ( y llego ' + self.lex, "mut, IDENTIFICADOR o (")

        if self.tok == "Ide":
            nombre_del_identificador = self.lex 
            self.tok, self.lex = self.tokeniza()
        else:
            self.print_error('Error de Sintaxis', 'Se esperaba IDENTIFICADOR y llego ' + self.lex, "IDENTIFICADOR")

        if self.lex == "=":
            self.insertar_tabla_de_valores(nombre_del_identificador, valor)
            self.insertar_tabla_simbolos(nombre_del_identificador, [clase_de_variable, tipo_de_dato, str(self.dim1), str(self.dim2)])
            self.tok, self.lex = self.tokeniza()
            self.asignar_valor(nombre_del_identificador)
            return

        if self.lex == "[":
            self.dimens()
            
        if self.lex == ":":
            self.tok, self.lex = self.tokeniza()
            if self.lex == 'entero' : 
                tipo_de_dato = 'E'
                if self.dim1 == 0:
                    valor = '0'
            elif self.lex == 'decimal': 
                tipo_de_dato = 'D'
                if self.dim1 == 0:
                    alor = '0.0'
            elif self.lex == 'logico' : 
                tipo_de_dato = 'L'
                if self.dim1 == 0:
                    valor = 'F'
            elif self.lex == 'alfabetico': 
                tipo_de_dato = 'A'
                if self.dim1 == 0:
                    valor = '""'
            else:
                self.print_error('Error de Sintaxis', 'se esperaba un TIPO DE VALOR y llego '+ self.lex, "TIPO DE VALOR")
            self.tok, self.lex = self.tokeniza()
        else:
            self.print_error('Error de Sintaxis', 'Se esperaba TIPO DE VALOR, ASIGNACION DE VALOR O DIMENSION DE ARREGLO y llego ' + self.lex, "TIPO DE VALOR, ASIGNACION DE VALOR O DIMENSION DE ARREGLO")

        if self.lex == ";":
            self.insertar_tabla_de_valores(nombre_del_identificador, valor)
            self.insertar_tabla_simbolos(nombre_del_identificador, [clase_de_variable, tipo_de_dato, str(self.dim1), str(self.dim2)])

            
            self.insertar_codigo(self.contador_codigo, ['LIT', valor, '0'])
            self.insertar_codigo(self.contador_codigo, ['STO', '0', nombre_del_identificador])
            return

        if self.lex == "=":
            self.insertar_tabla_de_valores(nombre_del_identificador, valor)
            self.insertar_tabla_simbolos(nombre_del_identificador, [clase_de_variable, tipo_de_dato, str(self.dim1), str(self.dim2)])
            self.tok, self.lex = self.tokeniza()
            self.asignar_valor(nombre_del_identificador)
            return
        self.print_error('Error de Sintaxis', 'Se esperaba ASIGNACION DE VALOR o ; y llego ' + self.lex, "ASIGNACION DE VALOR o ;")

            



    def asignar_valor(self, nombre_del_identificador):
        

        #checar si es un arreglo
        if self.lex == "[":
            #nombre de la variable, profundidad, indice
            self.asignacion_dimensionada(nombre_del_identificador, 0, 0)
        else:
            if self.lex not in ["(", "+", "-", "!"] and self.tok not in ['Ent', 'Dec', 'CtA', 'CtL', "Ide"]:
                self.print_error('Error de Sintaxis', 'Se esperaba expresion y llego ' + self.lex, "expresion")
            self.expr()



# Llama a las funciones
    def llamada_funcion(self):
        lexema_anterior = ""
        while True:
            lexema_anterior = self.lex
            self.tok, self.lex = self.tokeniza()
            if self.lex == ")" and lexema_anterior == "(":
                break
            if self.lex == "," and (lexema_anterior == "," or lexema_anterior == "("):
                self.print_error('Error de Sintaxis', 'Se esperaba PARAMETRO y llego '+ self.lex, "PARAMETRO")
                break
            self.expr()
            if self.lex != ",":
                break
        if self.lex != ")":
            self.print_error('Error de Sintaxis', 'Se esperaba ) y llego '+ self.lex, "")
        self.tok, self.lex = self.tokeniza()


    def cargar_variable_dimensionada(self, nombre_identificador):
        self.tok, self.lex = self.tokeniza()
        self.expr()
        if self.lex != "]":
            self.print_error('Error de Sintaxis', 'Se esperaba ] y llego '+ self.lex, "")
        self.tok, self.lex = self.tokeniza()

# Resolucion de expresiones, calcula el resultado de la expresion
    def termino(self):
        nombre_identificador = ""
        is_function = False
        if self.lex == '(':
            self.tok, self.lex = self.tokeniza()
            self.expr()
            if self.lex != ')':
                self.print_error('Error de Sintaxis', 'Se esperaba ) y llego '+ self.lex, "")
            self.tok, self.lex = self.tokeniza()
        elif self.tok in ['Ent', 'Dec', 'CtA', 'CtL']:
            if self.tok in ['Ent', 'Dec', 'CtA']:
                self.insertar_codigo(self.contador_codigo, ['LIT', self.lex, '0'])
            elif self.lex == 'verdadero':
                self.insertar_codigo(self.contador_codigo, ['LIT', 'V', '0'])
            elif self.lex == 'falso':
                self.insertar_codigo(self.contador_codigo, ['LIT', 'F', '0'])
            self.tok, self.lex = self.tokeniza()
        elif self.tok == 'Ide':
            nombre_identificador = self.lex
            self.tok, self.lex = self.tokeniza()
            if self.lex == "(":
                etiqueta_x = "_E" + str(self.contador_etiquetas)
                self.contador_etiquetas += 1
                self.insertar_codigo(self.contador_codigo, ["LOD", etiqueta_x, "0"])
                self.llamada_funcion()
                self.insertar_codigo(self.contador_codigo, ["CAL", etiqueta_x, "0"])
                self.insertar_tabla_simbolos(etiqueta_x, ["I", "I", str(self.contador_codigo), "0"])
            elif self.lex == "[":
                self.cargar_variable_dimensionada(nombre_identificador)
            self.insertar_codigo(self.contador_codigo, ["LOD", nombre_identificador, "0"])

        else:
            self.print_error('Error de Sintaxis', 'Se esperaba expresion y llego '+ self.lex, "expresion")


    def operador_menos_unitario(self):
        operador = ""
        if self.lex == "-":
            operador = self.lex
            self.tok, self.lex = self.tokeniza()
        
        self.termino()
        
        if operador == "-":
            self.insertar_codigo(self.contador_codigo, ["OPR", "0", "8"])

    def operador_multiplicar(self):
        operador = ""
        while True:
            if self.lex in ["*", "/", "%"]:
                operador = self.lex
                self.tok, self.lex = self.tokeniza()

            self.operador_menos_unitario()

            if operador == "*":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "4"])
            elif operador == "/":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "5"])
            elif operador == "%":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "6"])


            if self.lex not in ["*", "/", "%"]:
                break

    def operador_suma(self):
        operador = ""
        bin = False

        while True:
            if (self.lex == "+" or self.lex == "-") and bin:
                operador = self.lex
                self.tok, self.lex = self.tokeniza()
                if self.lex != "(" and self.tok != "Ide" and self.tok not in ['Ent', 'Dec', 'CtA', 'CtL']:
                    if self.lex != "]": self.print_error('Error de Sintaxis', 'Se esperaba termino y llego '+ self.lex, "termino")
            self.operador_multiplicar()

            if operador == "+":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "2"])
            elif operador == "-":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "3"])

            if(self.lex == "+" or self.lex == "-"):
                bin = True

            if (self.lex != "+" and self.lex != "-"):
                break

    def operador_relacional(self):
        operador = ""
        self.operador_suma()
        if self.lex in ["<", ">", "<=", ">=", "!=", "=="]:
            operador = self.lex
            self.tok, self.lex = self.tokeniza()
            self.operador_suma()

            if operador == "<":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "9"])
            elif operador == ">":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "10"])
            elif operador == "<=":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "11"])
            elif operador == ">=":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "12"])
            elif operador == "!=":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "13"])
            elif operador == "==":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "14"])

    def operador_not(self):
        operador = ""
        if self.lex == "!":
            operador = self.lex
            self.tok, self.lex = self.tokeniza()
        self.operador_relacional()

        if operador == "!":
            self.insertar_codigo(self.contador_codigo, ["OPR", "0", "17"])

    def operador_and(self):
        operador = ""
        while True:
            if self.lex == "&&" or self.lex == "y":
                operador = self.lex
                self.tok, self.lex = self.tokeniza()
            self.operador_not()

            if operador == "&&" or operador == "y": 
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "15"])

            if self.lex != "&&" and self.lex != "y":
                break

    def expr(self):
        operador = ""
        while True:
            
            if self.lex == "||" or self.lex == "o":
                operador = self.lex
                self.tok, self.lex = self.tokeniza()
            self.operador_and()
            if operador == "||" or operador == "o":
                self.insertar_codigo(self.contador_codigo, ['OPR', "0", "16"])

            #esto es para simular el do while
            if self.lex != "||" and self.lex != "o":
                break


# Define un nuevo bloque donde poner estatutos y estructuras de control
    def block(self):
        if self.lex != "{":
            self.print_error('Error de Sintaxis', 'Se esperaba { y llego '+ self.lex, "")
        self.tok, self.lex = self.tokeniza()

        if self.lex != "}": self.estatutos()
        if self.idx >= len(self.input):
            self.rows.append("")
        if self.lex != "}": self.print_error("Error de Sintaxis", "Se esperaba FIN DE BLOQUE y llego " + self.lex , "")
        self.tok, self.lex = self.tokeniza()

# Analiza los estatutos de cada bloque
    def estatutos(self):

        while True:
            linea_evaluada = self.contador_linea
            if self.lex == '}': break

            elif self.lex == "sea":
                self.declaracion_variables()
                if self.lex != ";" or self.contador_linea != linea_evaluada:
                    if self.contador_linea != linea_evaluada:
                        self.print_semicolon_newline_error(linea_evaluada)
                    self.print_error('Error de Sintaxis',  'Se esperaba ;', ";")
                self.tok, self.lex = self.tokeniza()

            elif self.lex == 'imprimeln!': 
                self.imprimenl()
                if self.lex != ";" or self.contador_linea != linea_evaluada:
                    if self.contador_linea != linea_evaluada:
                        self.print_semicolon_newline_error(linea_evaluada)
                    self.print_error('Error de Sintaxis',  'Se esperaba ;', ";")
                self.tok, self.lex = self.tokeniza()
            
            elif self.lex == 'imprimeln': 
                self.imprimir_y_linea = True
                self.imprimenl();
                if self.lex != ";" or self.contador_linea != linea_evaluada:
                    if self.contador_linea != linea_evaluada:
                        self.print_semicolon_newline_error(linea_evaluada)
                    self.print_error('Error de Sintaxis',  'Se esperaba ;', ";")
                self.tok, self.lex = self.tokeniza()
                self.imprimir_y_linea = False
            
            elif self.lex == 'lmp': 
                self.insertar_codigo(self.contador_codigo, ['OPR', '0', '18'])
                self.tok, self.lex = self.tokeniza()
                if self.lex != ";" or self.contador_linea != linea_evaluada:
                    if self.contador_linea != linea_evaluada:
                        self.print_semicolon_newline_error(linea_evaluada)
                    self.print_error('Error de Sintaxis',  'Se esperaba ;', ";")
                self.tok, self.lex = self.tokeniza()
            
            elif self.lex == 'leer': 
                self.leer()
                if self.lex != ";" or self.contador_linea != linea_evaluada:
                    if self.contador_linea != linea_evaluada:
                        self.print_semicolon_newline_error(linea_evaluada)
                    self.print_error('Error de Sintaxis',  'Se esperaba ;', ";")
                self.tok, self.lex = self.tokeniza()
            
            elif self.tok == "Ide":
                nombre_identificador = self.lex
                self.tok, self.lex = self.tokeniza()
                if self.lex == "(":
                    self.llamada_funcion()
                elif self.lex == "[":
                    while True:
                        self.tok, self.lex = self.tokeniza()
                        self.expr()
                        if self.lex != "]":
                            self.print_error('Error de Sintaxis', 'se esperaba ] y llego '+ self.lex, "")
                        self.tok, self.lex = self.tokeniza()
                        if self.tok != "[":
                            break
                    if self.lex == "=":
                        self.tok, self.lex = self.tokeniza()
                        self.asignar_valor(nombre_identificador)
                        self.insertar_codigo(self.contador_codigo, ["STO", "0", nombre_identificador])
                elif self.lex == "=":
                    self.tok, self.lex = self.tokeniza()
                    self.asignar_valor(nombre_identificador)
                if self.lex != ";" or self.contador_linea != linea_evaluada:
                    if self.contador_linea != linea_evaluada:
                        self.print_semicolon_newline_error(linea_evaluada)
                    self.print_error('Error de Sintaxis',  'Se esperaba ;', ";")
                self.tok, self.lex = self.tokeniza()

            elif self.lex == "si":
                self.sentencia_si()
            
            elif self.lex == "para":
                self.bucle_para()
            
            elif self.lex == "ciclo":
                linea_evaluada = self.bucle_ciclo_mientras()
                if self.lex != ";" or self.contador_linea != linea_evaluada:
                    if self.contador_linea != linea_evaluada:
                        self.print_semicolon_newline_error(linea_evaluada)
                    self.print_error('Error de Sintaxis',  'Se esperaba ;', ";")
                self.tok, self.lex = self.tokeniza()
            
            elif self.lex == "mientras":
                self.bucle_mientras()
            
            elif self.lex == "testfor":
                self.bucle_for_prueba()
            
            elif self.lex == "regresa":
                self.regresa()
                if self.lex != ";" or self.contador_linea != linea_evaluada:
                    if self.contador_linea != linea_evaluada:
                        self.print_semicolon_newline_error(linea_evaluada)
                    self.print_error('Error de Sintaxis',  'Se esperaba ;', ";")
                self.tok, self.lex = self.tokeniza()
            elif self.idx >= len(self.input):
                break
            else:
                self.print_error('Error de Sintaxis', 'Lexema inesperado ' + self.lex, "")

# Definicion de los built-ins del lenguaje

    def imprimenl(self):
        self.tok, self.lex = self.tokeniza()
        if self.lex != '(':
            self.print_error('Error de Sintaxis', 'Se esperaba ( y llego '+ self.lex, "")
        self.tok, self.lex = self.tokeniza()
        if self.lex == ')':
            self.insertar_codigo(self.contador_codigo, ['LIT', '""', '0'])
        elif self.lex != ')':
            sep = ','
            while sep == ',':
                sep = ''
                self.expr() 
                sep = self.lex
                if self.lex != ')': self.tok, self.lex = self.tokeniza()
                if sep == ',':
                    self.insertar_codigo(self.contador_codigo, ['OPR', '0', '20'])

        if self.lex != ')': self.tok, self.lex = self.tokeniza()
        if self.lex != ')':
            self.print_error('Error de Sintaxis', 'Se esperaba ) y llego '+ self.lex, "")
        else:
            if self.imprimir_y_linea == False:
                self.insertar_codigo(self.contador_codigo, ['OPR', '0', '21'])
            if self.imprimir_y_linea == True:
                self.insertar_codigo(self.contador_codigo, ['OPR', '0', '20'])
        
        self.tok, self.lex = self.tokeniza()

    def leer(self):  #Comando leer Oxido
        self.tok, self.lex = self.tokeniza()
        nombre_identificador = ''
        if self.lex != '(':
            self.print_error('Error de Sintaxis', 'Se esperaba ( y llego '+ self.lex, "")
        self.tok, self.lex = self.tokeniza()
        if self.tok != 'Ide':
            self.print_error('Error de Sintaxis', 'Se esperaba Identificador y llego '+ self.lex, "Identificador")
        else:
            nombre_identificador = self.lex
            self.tok, self.lex = self.tokeniza()
            if self.lex == '[':
                self.asignacion_dimensionada(nombre_identificador, 0, 0)
        if self.lex == ')':
            self.insertar_codigo(self.contador_codigo, ['OPR', nombre_identificador, '19'])
        else:
            self.print_error('Error de Sintaxis', 'Se esperaba ")" y llego '+ self.lex, "")
        
        self.tok, self.lex = self.tokeniza()


    def dimens(self):
        while True:
            self.tok, self.lex = self.tokeniza()
            if self.tok == "Ide":
                if self.obtener_simbolo(self.lex)[1] != "E":
                    self.print_error("Error de Semantica", "se esperaba ENTERO y llego " + self.lex, "ENTERO")
                self.expr()
            else:
                self.expr()
                if self.lex != "]":
                    self.print_error("Error de Sintaxis", "se esperaba ] y llego " + self.lex, "")
            

            self.contador_dimension += 1
            if self.contador_dimension == 1: self.dim1 = self.lex
            elif self.contador_dimension == 2: self.dim2 = self.lex
            self.tok, self.lex = self.tokeniza()
            
            if self.lex != "[": break
    
    def asignacion_dimensionada(self, nombre_identificador, profundidad, indice):
        contador_indice_arreglo = 0

        while True:
            self.tok, self.lex = self.tokeniza()
            if self.lex == "[":
                self.asignacion_dimensionada(nombre_identificador, 1, contador_indice_arreglo)
                contador_indice_arreglo += 1
            else:
                if profundidad > 0:
                    self.insertar_codigo(self.contador_codigo, ['LIT', str(indice), '0'])
                self.insertar_codigo(self.contador_codigo, ['LIT', str(contador_indice_arreglo), '0'])
                contador_indice_arreglo += 1
                self.expr()
                
                self.insertar_codigo(self.contador_codigo, ['STO', '0', nombre_identificador])
            if self.lex != ",":
                break

        if self.lex != "]":
            self.print_error("Error de Sintaxis", "se esperaba ] y llego " + self.lex, "")

        self.tok, self.lex = self.tokeniza()


    def tipo(self):
        self.tok, self.lex = self.tokeniza()
        if not(self.lex in ['entero', 'decimal', 'logico', 'alfabetico']):
            self.print_error('Error de Sintaxis', 'Se esperaba entero, decimal, logico o alfabetico y llego '+ self.lex, "entero, decimal, logico o alfabetico")


# Estructuras de control del lenguaje           
    def sentencia_si(self):
        self.tok, self.lex = self.tokeniza()
        self.expr()

        self.contador_etiquetas += 1
        numero_de_etiqueta = str(self.contador_etiquetas)
        etiqueta_x = ""
        etiqueta_y = ""
        numero_de_etiqueta = "_E" + numero_de_etiqueta
        etiqueta_x = numero_de_etiqueta
        self.insertar_codigo(self.contador_codigo, ["JMC", "F", etiqueta_x])

        if self.lex != "sino":
            self.block()

        if self.lex == "sino":
            self.contador_etiquetas += 1
            numero_de_etiqueta = str(self.contador_etiquetas)
            numero_de_etiqueta = "_E" + numero_de_etiqueta
            etiqueta_y = numero_de_etiqueta
            self.insertar_codigo(self.contador_codigo, ["JMP", "0", etiqueta_y])
            self.insertar_tabla_simbolos(etiqueta_x, ['I', 'I', str(self.contador_codigo), 0])
            self.tok, self.lex = self.tokeniza()
            self.block()
            self.insertar_tabla_simbolos(etiqueta_y, ['I', 'I', str(self.contador_codigo), 0])

        else:
            self.insertar_tabla_simbolos(etiqueta_x, ['I', 'I', str(self.contador_codigo), 0])

    def bucle_para(self):
        self.tok, self.lex = self.tokeniza()
        if self.tok == "Ide":
            #self.insertar_tabla_simbolos(self.lex, ['V', 'I', 0, 0])
            self.tok, self.lex = self.tokeniza()
            if self.lex == "en":
                self.tok, self.lex = self.tokeniza()
                if self.lex == "[":
                    while True:
                        self.tok, self.lex = self.tokeniza()
                        if self.lex != ",":
                            self.print_error('Error de Sintaxis', 'Se esperaba EXPRESION y llego '+ self.lex, "EXPRESION")
                        self.expr()
                        if self.lex != "," :
                            break
                    if self.lex != "]":
                        self.print_error('Error de Sintaxis', 'Se esperaba ] y llego '+ self.lex, "")
                    self.tok, self.lex = self.tokeniza()
                    if self.lex == "{":
                        self.block()
                elif self.tok == "Ent":
                    self.tok, self.lex = self.tokeniza()
                    if self.lex == ".":
                        self.tok, self.lex = self.tokeniza()
                        if self.lex == ".":
                            self.tok, self.lex = self.tokeniza()
                            if self.lex == "=":
                                self.tok, self.lex = self.tokeniza()
                                if self.tok == "Ent":
                                    self.tok, self.lex = self.tokeniza()
                                elif self.tok == "Ide":
                                    self.tok, self.lex = self.tokeniza()
                                elif self.lex == "(":
                                    self.expr()
                                else:
                                    self.print_error('Error de Sintaxis', 'Se esperaba ENTERO y llego '+ self.lex, "ENTERO") 
                            else:
                                if self.tok == "Ent":
                                    self.tok, self.lex = self.tokeniza()
                                elif self.tok == "Ide":
                                    self.tok, self.lex = self.tokeniza()
                                elif self.lex == '(':
                                    self.expr()
                                else:
                                    self.print_error('Error de Sintaxis', 'Se esperaba ENTERO y llego '+ self.lex, "ENTERO")
                            
                            if self.lex != "{":
                                self.print_error('Error de Sintaxis', 'Se esperaba { y llego '+ self.lex, "") 
                            else: 
                                self.block()
                elif self.lex == "(":
                    self.expr()
                    if self.lex == ".":
                        self.tok, self.lex = self.tokeniza()
                        if self.lex == ".":
                            self.tok, self.lex = self.tokeniza()
                            if self.lex == "=":
                                self.tok, self.lex = self.tokeniza()
                                if self.tok == "Ent":
                                    self.tok, self.lex = self.tokeniza()
                                elif self.tok == "Ide":
                                    self.tok, self.lex = self.tokeniza()
                                elif self.lex == "(":
                                    self.expr()
                                else:
                                    self.print_error('Error de Sintaxis', 'Se esperaba ENTERO y llego '+ self.lex, "ENTERO")
                            else:
                                if self.tok == "Ent":
                                    self.tok, self.lex = self.tokeniza()
                                elif self.tok == "Ide":
                                    self.tok, self.lex = self.tokeniza()
                                elif self.lex == '(':
                                    self.expr()
                                else:
                                    self.print_error('Error de Sintaxis', 'Se esperaba ENTERO y llego '+ self.lex, "ENTERO")
                            
                            if self.lex != "{":
                                self.print_error('Error de Sintaxis', 'Se esperaba { y llego '+ self.lex, "") 
                            else: 
                                self.block()
                else:
                    self.print_error('Error de Sintaxis', 'Se esperaba RANGO O ARREGO y llego '+ self.lex, "RANGO O ARREGO") 

    def bucle_ciclo_mientras(self):
        numero_de_linea_del_mientras = self.contador_linea
        self.tok, self.lex = self.tokeniza()
        self.block()
        if self.lex != "mientras":
            self.print_error('Error de Sintaxis', 'Se esperaba MIENTRAS y llego '+ self.lex, "MIENTRAS") 
        numero_de_linea_del_mientras = self.contador_linea
        self.tok, self.lex = self.tokeniza()
        self.expr()
        return numero_de_linea_del_mientras

    def bucle_mientras(self):

        self.tok, self.lex = self.tokeniza()
        etiqueta_x = ""
        etiqueta_y = ""
        numero_etiqueta = str(self.contador_etiquetas)
        self.contador_etiquetas += 1
        direccion1 = self.contador_codigo

        self.expr()
        numero_etiqueta = "_E" + numero_etiqueta
        etiqueta_x = numero_etiqueta
        self.insertar_codigo(self.contador_codigo, ["JMC", "F", etiqueta_x])
        numero_etiqueta = str(self.contador_etiquetas)
        self.contador_etiquetas += 1
        numero_etiqueta = "_E" + numero_etiqueta
        etiqueta_y = numero_etiqueta
        self.insertar_codigo(self.contador_codigo, ["JMP", "0", etiqueta_y])
        

        if self.lex != "{":
            self.print_error('Error de Sintaxis', 'Se esperaba { y llego '+ self.lex, "")
        
        self.insertar_tabla_simbolos(etiqueta_y, ['I', 'I', str(self.contador_codigo), 0])
        self.block()
        self.insertar_codigo(self.contador_codigo, ["JMP", "0", str(direccion1)])
        self.insertar_tabla_simbolos(etiqueta_x, ['I', 'I', str(self.contador_codigo), 0])
   
    def bucle_for_prueba(self):
        self.tok, self.lex = self.tokeniza()
        if self.lex != ";": self.estatutos()
        if self.lex != ";": self.print_error('Error de Sintaxis', 'Se esperaba ; y llego '+ self.lex, ";")
        self.tok, self.lex = self.tokeniza()
        etiqueta_x = ""
        etiqueta_y = ""
        numero_etiqueta = str(self.contador_etiquetas)
        self.contador_etiquetas += 1
        direccion1 = 0
        direccion2 = 0
        if self.lex != ";":
            direccion1 = self.contador_codigo
            self.expr()
            numero_etiqueta = "_E" + numero_etiqueta
            etiqueta_x = numero_etiqueta
            self.insertar_codigo(self.contador_codigo, ["JMC", "F", etiqueta_x])
            numero_etiqueta = str(self.contador_etiquetas)
            self.contador_etiquetas += 1
            numero_etiqueta = "_E" + numero_etiqueta
            etiqueta_y = numero_etiqueta
            self.insertar_codigo(self.contador_codigo, ["JMP", "0", etiqueta_y])
        
        if self.lex != ";" :
            self.print_error('Error de Sintaxis', 'Se esperaba ; y llego '+ self.lex, ";")
        
        self.tok, self.lex = self.tokeniza()

        if self.lex != "{":
            direccion2 = self.contador_codigo
            self.estatutos()
            self.insertar_codigo(self.contador_codigo, ["JMP", "0", str(direccion1)])
        
        self.insertar_tabla_simbolos(etiqueta_y, ['I', 'I', str(self.contador_codigo), 0])
        self.block()
        self.insertar_codigo(self.contador_codigo, ["JMP", "0", str(direccion2)])
        self.insertar_tabla_simbolos(etiqueta_x, ['I', 'I', str(self.contador_codigo), 0])

    def regresa(self):
        self.tok, self.lex = self.tokeniza()
        self.expr()


###############################################################################
# Inicia Analizadores, Crea arreglo del programa PL0 y escribe al archivo PL0 #
###############################################################################
    def construir_archivo_PL0(self):
        self.idx = 0
        if len(self.input) > 0:
            self.create_blank_PL0_array()
            self.analizador_sintactico()
            nombre_archivo_salida = self.nombre_del_archivo[0:len(self.nombre_del_archivo)-3] + 'eje'
            try:
                with open(str(pathlib.Path(__file__).parent.resolve()) + "/" + nombre_archivo_salida, 'w') as archivo_de_salida:
                    for x, y in self.tab_sim.items():
                        archivo_de_salida.write(x + ',')
                        archivo_de_salida.write(y[0]+',')
                        archivo_de_salida.write(y[1]+',')
                        archivo_de_salida.write(str(y[2])+',')
                        archivo_de_salida.write(str(y[3])+',')
                        archivo_de_salida.write('#,\n')
                    archivo_de_salida.write('@\n')
                    for i in range(1, self.contador_codigo):
                        archivo_de_salida.write(str(i) + ' ')
                        archivo_de_salida.write(self.pl0_program[i][0] + ' ')
                        archivo_de_salida.write(self.pl0_program[i][1] + ', ')
                        archivo_de_salida.write(self.pl0_program[i][2]  + '\n')
                archivo_de_salida.close()
            except FileNotFoundError:
                print(self.nombre_del_archivo, 'No exite volver a intentar')

    def create_blank_PL0_array(self):
        for i in range(0, 10000):
            self.pl0_program.append([])

###############################
# Funcion Main del compilador #
###############################
if __name__ == "__main__":
    #pedimos el nombre del archivo
    nombre_del_archivo = input("Ingresa el nombre del archivo (.icc) [.]=Salir: ")
    
    #nos aseguramos de que el archivo termine con .icc 
    #y de lo contrario seguimos pidiendo el nombre del archivo
    while not nombre_del_archivo.endswith(".icc"):
        if nombre_del_archivo == ".": sys.exit(0)
        nombre_del_archivo = input("Ingresa el nombre del archivo (.icc) [.]=Salir: ")

    #resolvemos el path del compilador con pathlib, le añadimos el nombre del archivo y lo abrimos en modo lectura
    with open(
        str(pathlib.Path(__file__).parent.resolve()) + "/" + nombre_del_archivo, "r"
    ) as file:
        #leemos todas las lineas del archivo y las guardamos en rows que es una lista con todas las lineas
        rows = file.readlines()
        #cerramos el archivo
        file.close()
        
        #inicializamos input con un string vacio
        input = ""
        #leemos toda la lista de lineas y las concatenamos a input
        for row in rows:
            input += row
        #inicializa la clase del analizador lexico
        analizador = Analizador(nombre_del_archivo, input, rows)

        #imprimimos todo el archivo introducido con la variable input
        print("\n" + input + "\n")

        #metemos todo el archivo al analizador lexico para tokenizar
        #analizador.imprimir_tokens()

        analizador.construir_archivo_PL0()
        