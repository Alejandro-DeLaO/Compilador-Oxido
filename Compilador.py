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
        [  1,   1,  21,   2,   7,   8,  10,  12,  16,  20,  18,  14,  21,   5],  # 0
        [  1,   1, ACP,   1, ACP, ACP,   1, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 1
        [ACP, ACP,   3,   2, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 2
        [ERR, ERR, ERR,   4, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR],  # 3
        [ACP, ACP, ACP,   4, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 4
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP,   6],  # 5
        [  6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6],  # 6
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 7
        [ERR, ERR, ERR, ERR, ERR,   9, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR],  # 8
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 9
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP,  11, ACP, ACP, ACP, ACP, ACP, ACP],  # 10
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 11
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP,  13, ACP, ACP, ACP, ACP, ACP, ACP],  # 12
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 13
        [ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR, ERR,  15, ERR, ERR],  # 14
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 15
        [ 16,  16,  16,  16,  16,  16,  16,  16,  17,  16,  16,  16,  16,  16],  # 16
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 17
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP,  19, ACP, ACP, ACP, ACP, ACP, ACP],  # 18
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 19
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 20
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 21
        [ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP, ACP],  # 22
    ]
    tok = ""
    lex = ""
    dim1 = 0
    dim2 = 0
    contador_dimension = 0;
    tab_sim = {}
    pl0_program = []
    nombre_del_archivo = ""
    contador_codigo = 1
    contador_linea = 1
    contador_columna = 0
    contador_etiquetas = 0
    imprimir_y_linea = False

    #inicializador de la clase
    def __init__(self, nombre_del_archivo, input, rows):
        self.nombre_del_archivo = nombre_del_archivo
        self.input = input
        self.rows = rows

    def insertar_codigo(self, contador_codigo, cPl0):
        self.pl0_program[contador_codigo] = cPl0 

    def insertar_tabla_simbolos(self, key, colec):
        self.tab_sim[key] = colec

    def obtener_simbolo(self, key):
        return self.tab_sim[key]

    def print_error_line(self,  error_lex):
        print("\n"+self.rows[self.contador_linea-1],end="")
        print("^".rjust(self.contador_columna))
        print(error_lex.rjust(self.contador_columna))

    #metodo para imprimir errores
    def print_error(self, type, message):
        print("[" + str(self.contador_linea) + "]", "[" + str(self.contador_columna) + "]", type, message)
        self.print_error_line(";")
        sys.exit()

    #metodo para decidir la siguiente columna de la matriz de transicion
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
            self.print_error("Error Lexico ", str(c) + " No es valido en el alfabeto del lenguaje")
        return self.ERR

    #Inicia el programa
    def init_program(self):
        for i in range(0, 10000):
            self.pl0_program.append([])
    
    def analizador_sintactico(self):
        self.tok, self.lex = self.tokeniza()
        while True:
            self.variables()
            self.funciones()
            if self.idx >= len(self.input):
                break
        print(self.nombre_del_archivo, 'COMPILO con EXITO!!!')

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

                self.idx += 1
                
                if caracter != '\t' and caracter != '\n' and caracter != '': self.contador_columna += 1 
                #if caracter == '\t': self.contador_columna += 4


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
                    break

                if estado == 1 and caracter in [":", "=", " ", "[", "("]:
                    if lex == "o":
                        estado = self.ACP
                        estAnt = 15
                        break
                    elif lex == "y":
                        estado = self.ACP
                        estAnt = 9
                        break
                if estado != 6 and estado != 16 and caracter in self.univer_dlm:
                    if caracter == "\n":
                        self.contador_linea += 1
                        self.contador_columna = 0
                    break

                if estado == 1 and caracter in self.univer_dlm: 
                    estAnt = estado
                    estado = self.ACP
                    break

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
                self.print_error("Error Lexico", lex + " decimal incompleto")
            elif estAnt == 16:
                self.print_error('Error Lexico', 'Cte Alfabetica SIN cerrar '+lex)
            elif estAnt == 8:
                self.print_error('Error Lexico', 'Operador logico incompleto '+lex)   
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
            elif estAnt == 21 or estAnt == 14 or estAnt == 8:
                tok = "Sym"
            else:
                tok = "NtK"

            return tok, lex
    
    #Imprime todos los tokens
    def imprimir_tokens(self):
        self.idx = 0
        while self.idx < len(self.input):
            token, lexema = analizador.tokeniza()
            print(token, lexema)

    def construir_archivo_PL0(self):
        self.idx = 0
        if len(self.input) > 0:
            self.init_program()
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

    def llamada_funcion(self):
        lexema_anterior = ""
        while True:
            lexema_anterior = self.lex
            self.tok, self.lex = self.tokeniza()
            if self.lex == ")" and lexema_anterior == "(":
                break
            if self.lex == "," and (lexema_anterior == "," or lexema_anterior == "("):
                self.print_error('Error de Sintaxis', 'Se esperaba PARAMETRO y llego '+ self.lex)
                break
            self.expr()
            if self.lex != ",":
                break
        if self.lex != ")":
            self.print_error('Error de Sintaxis', 'Se esperaba ) y llego '+ self.lex)
        self.tok, self.lex = self.tokeniza()

    def termino(self):
        nombre_identificador = ""
        is_function = False
        if self.lex == '(':
            self.tok, self.lex = self.tokeniza()
            self.expr()
            if self.lex != ')':
                self.print_error('Error de Sintaxis', 'Se esperaba ) y llego '+ self.lex)
        if self.tok in ['Ent', 'Dec', 'CtA', 'CtL']:
            if self.tok in ['Ent', 'Dec', 'CtA']:
                self.insertar_codigo(self.contador_codigo, ['LIT', self.lex, '0'])
            elif self.lex == 'verdadero':
                self.insertar_codigo(self.contador_codigo, ['LIT', 'V', '0'])
            elif self.lex == 'falso':
             self.insertar_codigo(self.contador_codigo, ['LIT', 'F', '0'])
            self.contador_codigo +=  1
        if self.tok == 'Ide':
            nombre_identificador = self.lex


        self.tok, self.lex = self.tokeniza()

        if self.lex == "(" and nombre_identificador != "":
            self.llamada_funcion()

        if self.lex == "[" and  nombre_identificador != "" and not is_function:
            while True:
                self.tok, self.lex = self.tokeniza()
                self.expr()
                if self.lex != "]": self.print_error('Error de Sintaxis', 'Se esperaba ] y llego '+ self.lex)
                self.tok, self.lex = self.tokeniza()
                if self.lex != "[":
                    break
        if nombre_identificador != "":
            self.insertar_codigo(self.contador_codigo, ['LOD', nombre_identificador, '0'])
            self.contador_codigo += 1

    def operador_menos_unitario(self):
        operador = ""
        if self.lex == "-":
            operador = self.lex
            self.tok, self.lex = self.tokeniza()
        
        self.termino()
        
        if operador == "-":
            self.insertar_codigo(self.contador_codigo, ["OPR", "0", "8"])
            self.contador_codigo += 1


    def operador_multiplicar(self):
        operador = ""
        while True:
            if self.lex in ["*", "/", "%"]:
                operador = self.lex
                self.tok, self.lex = self.tokeniza()

            self.operador_menos_unitario()

            if operador == "*":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "4"])
                self.contador_codigo += 1
            elif operador == "/":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "5"])
                self.contador_codigo += 1
            elif operador == "%":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "6"])
                self.contador_codigo += 1


            if self.lex not in ["*", "/", "%"]:
                break


    def operador_suma(self):
        operador = ""
        bin = False

        while True:
            if (self.lex == "+" or self.lex == "-") and bin:
                operador = self.lex
                self.tok, self.lex = self.tokeniza()
            self.operador_multiplicar()

            if operador == "+":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "2"])
                self.contador_codigo += 1
            elif operador == "-":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "3"])
                self.contador_codigo += 1

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
                self.contador_codigo += 1
            elif operador == ">":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "10"])
                self.contador_codigo += 1
            elif operador == "<=":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "11"])
                self.contador_codigo += 1
            elif operador == ">=":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "12"])
                self.contador_codigo += 1
            elif operador == "!=":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "13"])
                self.contador_codigo += 1
            elif operador == "==":
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "14"])
                self.contador_codigo += 1

    def operador_not(self):
        operador = ""
        if self.lex == "!":
            operador = self.lex
            self.tok, self.lex = self.tokeniza()
        self.operador_relacional()

        if operador == "!":
            self.insertar_codigo(self.contador_codigo, ["OPR", "0", "17"])
            self.contador_codigo += 1

    def operador_and(self):
        operador = ""
        while True:
            if self.lex == "&&" or self.lex == "y":
                operador = self.lex
                self.tok, self.lex = self.tokeniza()
            self.operador_not()

            if operador == "&&" or operador == "y": 
                self.insertar_codigo(self.contador_codigo, ["OPR", "0", "15"])
                self.contador_codigo += 1

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
                self.contador_codigo += 1

            #esto es para simular el do while
            if self.lex != "||" and self.lex != "o":
                break

    def imprimenl(self):
        self.tok, self.lex = self.tokeniza()
        if self.lex != '(':
            self.print_error('Error de Sintaxis', 'Se esperaba ( y llego '+ self.lex)
        self.tok, self.lex = self.tokeniza()
        if self.lex == ')':
            self.insertar_codigo(self.contador_codigo, ['LIT', '""', '0'])
            self.contador_codigo += 1
        elif self.lex != ')':
            sep = ','
            while sep == ',':
                sep = ''
                self.expr() 
                sep = self.lex
                if self.lex != ')': self.tok, self.lex = self.tokeniza()
                if sep == ',':
                    self.insertar_codigo(self.contador_codigo, ['OPR', '0', '20'])
                    self.contador_codigo += 1           

        if self.lex != ')': self.tok, self.lex = self.tokeniza()
        if self.lex != ')':
            self.print_error('Error de Sintaxis', 'Se esperaba ) y llego '+ self.lex)
        else:
            if self.imprimir_y_linea == False:
                self.insertar_codigo(self.contador_codigo, ['OPR', '0', '21'])
            if self.imprimir_y_linea == True:
                self.insertar_codigo(self.contador_codigo, ['OPR', '0', '20'])
            self.contador_codigo += 1           
        
        self.tok, self.lex = self.tokeniza()
        if self.lex != ';':
            self.print_error('Error de Sintaxis', 'se esperaba ; y llego '+ self.lex)

    def leer(self):  #Comando leer Oxido
        self.tok, self.lex = self.tokeniza()
        nombre_identificador = ''
        if self.lex != '(':
            self.print_error('Error de Sintaxis', 'Se esperaba ( y llego '+ self.lex)
        self.tok, self.lex = self.tokeniza()
        if self.tok != 'Ide':
            self.print_error('Error de Sintaxis', 'Se esperaba Identificador y llego '+ self.lex)
        else:
            nombre_identificador = self.lex
            self.tok, self.lex = self.tokeniza()
            if self.lex == '[':
                self.udim(nombre_identificador, 0, 0)
        if self.lex == ')':
            self.insertar_codigo(self.contador_codigo, ['OPR', nombre_identificador, '19'])
            self.contador_codigo += 1
        else:
            self.print_error('Error de Sintaxis', 'Se esperaba ")" y llego '+ self.lex)
        
        self.tok, self.lex = self.tokeniza()
        if self.lex != ';':
            self.print_error('Error de Sintaxis', 'se esperaba ; y llego '+ self.lex)


    def comando(self): 
        if self.lex == 'imprimeln!': self.imprimenl()
        elif self.lex == 'imprimeln': 
            self.imprimir_y_linea = True
            self.imprimenl();
            self.imprimir_y_linea = False
        elif self.lex == 'lmp': 
            self.insertar_codigo(self.contador_codigo, ['OPR', '0', '18'])
            self.contador_codigo += 1
            self.tok, self.lex = self.tokeniza()
            if self.lex != ';':
                self.print_error('Error de Sintaxis', 'se esperaba ; y llego '+ self.lex)
        elif self.lex == 'leer': self.leer()

    def asigna(self, nombre_variable):
        if self.lex != "=" and self.lex != "[" and self.tok not in ["Ent", "Dec","CtL", "CtA"]:
            self.print_error('Error de Sintaxis', 'se esperaba = o POSICION EN ARREGLO y llego '+ self.lex)
            return
        if self.lex == "[":
            self.tok, self.lex = self.tokeniza()
            while True:
                self.expr()
                if self.lex != "]":
                    self.print_error('Error de Sintaxis', 'se esperaba ] y llego '+ self.lex)
                self.tok, self.lex = self.tokeniza()
                if self.lex != "[":
                    break
            if self.lex != "=":
                self.print_error('Error de Sintaxis', 'se esperaba = y llego '+ self.lex)

        if self.lex == "=":
            self.tok, self.lex = self.tokeniza()
        if self.lex == "[":
            self.udim(nombre_variable, 0, 0)
            return


        self.expr()
        self.insertar_codigo(self.contador_codigo, ["STO", "0",  nombre_variable])
        self.contador_codigo += 1


    def estatutos(self):
        separador = ';'
        while separador == ';':
            separador = '*'
            if self.lex == ';':
                self.tok, self.lex = self.tokeniza()
            if self.lex == '}': break

            self.variables()

            self.comando()
            
            
            if self.lex == ';': separador = self.lex

            if self.tok == "Ide":
                nombre_variable = self.lex
                self.tok, self.lex = self.tokeniza()
                if self.lex == "(":
                    self.llamada_funcion()
                    separador = ";"

                elif self.lex == "=" or self.lex == "[":
                    self.asigna(nombre_variable)
                    if self.lex == ";":
                        separador = ";"
                    else: 
                        self.print_error('Error de Sintaxis', 'se esperaba ; y llego '+ self.lex)
                elif self.lex == ";":
                    separador = ";"
                elif self.tok == "Ide":
                    self.contador_linea -= 2
                    self.contador_columna = len(self.rows[self.contador_linea])
                    self.print_error('Error de Sintaxis', 'se esperaba ; y llego '+ self.lex)

            elif self.lex == "si":
                self.sentencia_si()
                separador = ";"
            elif self.lex == "para":
                self.bucle_para()
                separador = ";"
            elif self.lex == "ciclo":
                self.bucle_ciclo_mientras()
                separador = ";"
            elif self.lex == "mientras":
                self.bucle_mientras()
                separador = ";"
            elif self.lex == "testfor":
                self.bucle_for_prueba()
                separador = ";"
            elif self.lex == "regresa":
                self.regresa()
                separador = ";"

            

            
    

    def dimens(self):
        while True:
            self.tok, self.lex = self.tokeniza()
            if self.tok == "Ide":
                if self.obtener_simbolo(self.lex)[1] != "E":
                    self.print_error("Error de Sintaxis", "se esperaba ENTERO y llego " + self.lex)
                    break
                self.expr()
            elif self.tok != "Ent":
                self.print_error("Error de Sintaxis", "se esperaba ENTERO y llego " + self.lex)
            else:
                self.contador_dimension += 1
                if self.contador_dimension == 1: self.dim1 = self.lex
                elif self.contador_dimension == 2: self.dim2 = self.lex
                self.tok, self.lex = self.tokeniza()
            
            if self.lex != "]": self.print_error("Error de Sintaxis", "se esperaba ] y llego " + self.lex)
            self.tok, self.lex = self.tokeniza()
            if self.lex != "[": break
    
    def udim(self, nombre_identificador, profundidad, indice):
        contador_indice_arreglo = 0

        while True:
            self.tok, self.lex = self.tokeniza()
            if self.lex == "[":
                self.udim(nombre_identificador, 1, contador_indice_arreglo)
                contador_indice_arreglo += 1
            else:
                if profundidad > 0:
                    self.insertar_codigo(self.contador_codigo, ['LIT', str(indice), '0'])
                    self.contador_codigo += 1
                self.insertar_codigo(self.contador_codigo, ['LIT', str(contador_indice_arreglo), '0'])
                self.contador_codigo += 1
                contador_indice_arreglo += 1
                self.expr()
                
                self.insertar_codigo(self.contador_codigo, ['STO', '0', nombre_identificador])
                self.contador_codigo += 1
            if self.lex != ",":
                break

        if self.lex != "]":
            self.print_error("Error de Sintaxis", "se esperaba ] y llego " + self.lex)

        self.tok, self.lex = self.tokeniza()

    def variables(self):
        self.dim1 = 0
        self.dim2 = 0
        self.contador_dimension = 0
        nombre_variables = []
        tipo_de_dato = ''
        clase_de_variable = ''
        valor = ''
        while self.lex == 'sea':
            self.tok, self.lex = self.tokeniza()
            if self.lex == 'mut': 
                clase_de_variable = 'V'
                self.tok, self.lex = self.tokeniza()
            else: 
                clase_de_variable = 'C'
            while self.tok == 'Ide':
                nombre_del_indentificador = self.lex
                self.tok, self.lex = self.tokeniza()
                if self.lex == '[': self.dimens()
                nombre_variables.append(nombre_del_indentificador)
                if self.lex == ',':
                    self.tok, self.lex = self.tokeniza()
            #if self.lex != ':':
            #    self.print_error('Error de Sintaxis', 'se esperaba : y llego '+ self.lex)
            #comenta este IF 
            if self.lex == "=":
                self.tok, self.lex = self.tokeniza()
                if self.tok == "Ent":
                    tipo_de_dato = 'L'
                    valor = 'F'
                elif self.tok == "Dec":
                    tipo_de_dato = 'D'
                    valor = '0.0'
                elif self.tok == "CtL":
                    tipo_de_dato = 'L'
                    valor = 'F'
                elif self.tok == "CtA":
                    tipo_de_dato = 'A'
                    valor = '""'
                else:
                    self.print_error('Error de Sintaxis', 'se esperaba un Valor y llego '+ self.lex)
                    break       
                self.asigna(nombre_del_indentificador)
                if self.lex == ";":
                    for nombre in nombre_variables:
                        self.insertar_codigo(self.contador_codigo, ['LIT', valor, '0'])
                        self.contador_codigo += 1
                        self.insertar_codigo(self.contador_codigo, ['STO', '0', nombre])
                        self.contador_codigo += 1

                for nombre in nombre_variables:
                    self.insertar_tabla_simbolos(nombre, [clase_de_variable, tipo_de_dato, str(self.dim1), str(self.dim2)])
                
                self.dim1 = 0
                self.dim2 = 0
                nombre_variables = []

            elif self.lex == ":":
                self.tok, self.lex = self.tokeniza()
                if self.lex == 'entero' : 
                    tipo_de_dato = 'E'
                    valor = '0'
                elif self.lex == 'decimal': 
                    tipo_de_dato = 'D'
                    valor = '0.0'
                elif self.lex == 'logico' : 
                    tipo_de_dato = 'L'
                    valor = 'F'
                elif self.lex == 'alfabetico': 
                    tipo_de_dato = 'A'
                    valor = '""'
                else:
                    self.print_error('Error de Sintaxis', 'se esperaba un TIPO DE VALOR y llego '+ self.lex)
                    break
                self.tok, self.lex = self.tokeniza()
                if self.lex == '=':
                    self.asigna(nombre_del_indentificador)

                elif self.lex == ";":
                    for nombre in nombre_variables:
                        self.insertar_codigo(self.contador_codigo, ['LIT', valor, '0'])
                        self.contador_codigo += 1
                        self.insertar_codigo(self.contador_codigo, ['STO', '0', nombre])
                        self.contador_codigo += 1

                for nombre in nombre_variables:
                    self.insertar_tabla_simbolos(nombre, [clase_de_variable, tipo_de_dato, str(self.dim1), str(self.dim2)])
                
                self.dim1 = 0
                self.dim2 = 0
                nombre_variables = []
            if self.lex != ';':
                self.tok, self.lex = self.tokeniza()
            if self.lex != ';':
                self.print_error('Error de Sintaxis', 'se esperaba ; y llego '+ self.lex)
            else:
                self.tok, self.lex = self.tokeniza()
                if self.lex == 'fn':
                    self.insertar_codigo(self.contador_codigo, ['JMP', '0', '_principal'])
                    self.contador_codigo += 1


    def params(self): 
        sec = ','
        while sec == ',':
            if self.tok != 'Ide': 
                self.print_error('Error de Sintaxis', 'Se esperaba Ide y llego '+ self.lex)
            self.tok, self.lex = self.tokeniza()
            if self.lex != ':':
                self.print_error('Error de Sintaxis', 'Se esperaba : y llego '+ self.lex)
            self.tipo()
            self.tok, self.lex = self.tokeniza()
            sec = self.lex
            if sec == ',':
                self.tok, self.lex = self.tokeniza()

    def tipo(self):
        self.tok, self.lex = self.tokeniza()
        if not(self.lex in ['entero', 'decimal', 'logico', 'palabra']):
            self.print_error('Error de Sintaxis', 'Se esperaba entero, decimal, logico o palabra y llego '+ self.lex)
            

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
                self.print_error('Error de Sintaxis', 'Se esperaba Ide o principal y llego '+ self.lex)
            self.tok, self.lex = self.tokeniza();
            if self.lex != '(': 
                self.print_error('Error de Sintaxis', 'Se esperaba ( y llego '+ self.lex)
            self.tok, self.lex = self.tokeniza();
            if self.lex != ')': self.params()
            if self.lex != ')':
                self.print_error('Error de Sintaxis', 'Se esperaba ) y llego '+ self.lex)
            self.tok, self.lex = self.tokeniza();
            if self.lex == '-':
                self.tok, self.lex = self.tokeniza()
                if self.lex != '>':
                    self.print_error('Error de Sintaxis', 'Se esperaba > y llego '+ self.lex)
                self.tipo()
                self.tok, self.lex = self.tokeniza()

            if self.lex != '{':
                self.print_error('Error de Sintaxis', 'Se esperaba { y llego '+ self.lex)
            if self.lex != '}': self.block()

            if nombre_de_funcion == 'principal':
                self.insertar_codigo(self.contador_codigo, ['OPR', '0', '0'])
                self.contador_codigo += 1                  

        

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
        self.contador_codigo += 1

        if self.lex != "sino":
            self.block()

        if self.lex == "sino":
            self.contador_etiquetas += 1
            numero_de_etiqueta = str(self.contador_etiquetas)
            numero_de_etiqueta = "_E" + numero_de_etiqueta
            etiqueta_y = numero_de_etiqueta
            self.insertar_codigo(self.contador_codigo, ["JMP", "0", etiqueta_y])
            self.contador_codigo += 1
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
                            self.print_error('Error de Sintaxis', 'Se esperaba EXPRESION y llego '+ self.lex)
                        self.expr()
                        if self.lex != "," :
                            break
                    if self.lex != "]":
                        self.print_error('Error de Sintaxis', 'Se esperaba ] y llego '+ self.lex)
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
                                    self.print_error('Error de Sintaxis', 'Se esperaba ENTERO y llego '+ self.lex) 
                            else:
                                if self.tok == "Ent":
                                    self.tok, self.lex = self.tokeniza()
                                elif self.tok == "Ide":
                                    self.tok, self.lex = self.tokeniza()
                                elif self.lex == '(':
                                    self.expr()
                                else:
                                    self.print_error('Error de Sintaxis', 'Se esperaba ENTERO y llego '+ self.lex) 
                            
                            if self.lex != "{":
                                self.print_error('Error de Sintaxis', 'Se esperaba { y llego '+ self.lex) 
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
                                    self.print_error('Error de Sintaxis', 'Se esperaba ENTERO y llego '+ self.lex) 
                            else:
                                if self.tok == "Ent":
                                    self.tok, self.lex = self.tokeniza()
                                elif self.tok == "Ide":
                                    self.tok, self.lex = self.tokeniza()
                                elif self.lex == '(':
                                    self.expr()
                                else:
                                    self.print_error('Error de Sintaxis', 'Se esperaba ENTERO y llego '+ self.lex) 
                            
                            if self.lex != "{":
                                self.print_error('Error de Sintaxis', 'Se esperaba { y llego '+ self.lex) 
                            else: 
                                self.block()
                else:
                    self.print_error('Error de Sintaxis', 'Se esperaba RANGO O ARREGO y llego '+ self.lex) 

    def bucle_ciclo_mientras(self):
        self.tok, self.lex = self.tokeniza()
        self.block()
        if self.lex != "mientras":
            self.print_error('Error de Sintaxis', 'Se esperaba MIENTRAS y llego '+ self.lex) 
        self.tok, self.lex = self.tokeniza()
        self.expr()
        if self.lex != ";":
            self.print_error('Error de Sintaxis', 'Se esperaba ; y llego '+ self.lex) 

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
        self.contador_codigo += 1
        numero_etiqueta = str(self.contador_etiquetas)
        self.contador_etiquetas += 1
        numero_etiqueta = "_E" + numero_etiqueta
        etiqueta_y = numero_etiqueta
        self.insertar_codigo(self.contador_codigo, ["JMP", "0", etiqueta_y])
        self.contador_codigo += 1
        

        if self.lex != "{":
            self.print_error('Error de Sintaxis', 'Se esperaba { y llego '+ self.lex)
        
        self.insertar_tabla_simbolos(etiqueta_y, ['I', 'I', str(self.contador_codigo), 0])
        self.block()
        self.insertar_codigo(self.contador_codigo, ["JMP", "0", str(direccion1)])
        self.contador_codigo += 1
        self.insertar_tabla_simbolos(etiqueta_x, ['I', 'I', str(self.contador_codigo), 0])

        
    def bucle_for_prueba(self):
        self.tok, self.lex = self.tokeniza()
        if self.lex != ";": self.estatutos()
        if self.lex != ";": self.print_error('Error de Sintaxis', 'Se esperaba ; y llego '+ self.lex)
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
            self.contador_codigo += 1
            numero_etiqueta = str(self.contador_etiquetas)
            self.contador_etiquetas += 1
            numero_etiqueta = "_E" + numero_etiqueta
            etiqueta_y = numero_etiqueta
            self.insertar_codigo(self.contador_codigo, ["JMP", "0", etiqueta_y])
            self.contador_codigo += 1
        
        if self.lex != ";" :
            self.print_error('Error de Sintaxis', 'Se esperaba ; y llego '+ self.lex)
        
        self.tok, self.lex = self.tokeniza()

        if self.lex != "{":
            direccion2 = self.contador_codigo
            self.estatutos()
            self.insertar_codigo(self.contador_codigo, ["JMP", "0", str(direccion1)])
            self.contador_codigo += 1
        
        self.insertar_tabla_simbolos(etiqueta_y, ['I', 'I', str(self.contador_codigo), 0])
        self.block()
        self.insertar_codigo(self.contador_codigo, ["JMP", "0", str(direccion2)])
        self.contador_codigo += 1
        self.insertar_tabla_simbolos(etiqueta_x, ['I', 'I', str(self.contador_codigo), 0])

    def block(self):
        if self.lex != "{":
            self.print_error('Error de Sintaxis', 'Se esperaba { y llego '+ self.lex)
        self.tok, self.lex = self.tokeniza()

        if self.lex != "}": self.estatutos()
        if self.lex != "}": self.print_error("Error de Sintaxis", "Se esperaba FIN DE BLOQUE y llego " + self.lex)
        self.tok, self.lex = self.tokeniza()

    def regresa(self):
        self.tok, self.lex = self.tokeniza()
        self.expr()
        if self.lex != ";":
            self.print_error('Error de Sintaxis', 'Se esperaba ; y llego '+ self.lex)


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
        