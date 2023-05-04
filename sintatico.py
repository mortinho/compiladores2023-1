from token import *

class Sintatico:

    def __init__(self,token,debug = False):
        self.a=0
        self.error = False
        self.t=token
        self.debug = debug
        self.programa()
        print("end")
        
    def d(self,string):
        if self.debug: print(string)
        
    def treatFinal(self,input):
        self.d("treating: "+input+" -> "+str(self.t[self.a]))
        if self.t[self.a].equals(input): self.a+=1
        else:
            print("error "+input+" "+str(self.t[self.a]))
            self.error=True
        
    def peek(self,input):
        self.d("peeking: "+input+" -> "+str(self.t[self.a]))
        if self.t[self.a].equals(input): return True
        else: return False
    
    #-------------------#
    
    def programa(self):
        self.d("[PROGRAMA]")
        self.declaracoes()
        self.principal()
        self.d("[\\PROGRAMA]")
        
    def principal(self):
        self.treatFinal("begin")
        self.comando()
        self.lista_com()
        self.treatFinal("end")
        
    def declaracoes(self):
        self.d("[DECLARAÇÕES]")
        self.def_const()
        self.def_tipos()
        self.def_var()
        self.def_func()
        self.d("[\\DECLARAÇÕES]")
        
    def def_const(self):
        self.d("[DEF_CONST]")
        if (self.constante()): self.def_const()
        self.d("[\\DEF_CONST]")
        
    def constante(self):
        if not self.peek("const"): return False
        self.d("[CONSTANTE]")
        self.treatFinal("const")
        self.id()
        self.treatFinal("equals")
        self.const_valor()
        self.treatFinal(";")
        self.d("[\\CONSTANTE]")
        return True
        
    def def_tipos(self):
        self.d("[DEF_TIPOS]")
        if self.tipo(): self.def_tipos()
        self.d("[\\DEF_TIPOS]")
        
    def tipo(self):
        if not self.peek("type"): return False
        self.d("[TIPO]")
        self.treatFinal("type")
        self.id()
        self.treatFinal("=")
        self.tipo_dado()
        self.treatFinal(";")
        self.d("[\\TIPO]")
        return  True
        
    def def_var(self):
        self.d("[DEF_VAR]")
        if self.variavel(): self.def_var()
        self.d("[\\DEF_VAR]")
        
    def variavel(self):
        if not self.peek("var"): return False
        self.d("[VARIAVEL]")
        self.treatFinal("var")
        self.id()
        self.lista_id()
        self.treatFinal(":")
        self.tipo_dado()
        self.treatFinal(";")
        self.d("[\\VARIAVEL]")
        return True
        
    def def_func(self):
        self.d("[DEF_FUNC]")
        if self.funcao(): self.def_func()
        self.d("[\\DEF_FUNC]")
        
    def funcao(self):
        if not self.peek("function"): return False
        self.d("[FUNCAO]")
        self.treatFinal("function")
        self.nome_funcao()
        self.bloco_funcao()
        self.d("[\\FUNCAO]")
        return True
        
    def nome_funcao(self):
        self.d("[NOME_FUNCAO]")
        self.id()
        self.param_func()
        self.treatFinal(":")
        self.tipo_dado()
        self.d("[\\NOME_FUNCAO]")
        
    def param_func(self):
        if not self.peek("("): return False
        self.d("[PARAM_FUNC]")
        self.treatFinal("(")
        self.campos()
        self.treatFinal(")")
        self.d("[\\PARAM_FUNC]")
        return True
        
    def bloco_funcao(self):
        self.d("[BLOCO_FUNCAO]")
        self.def_var()
        self.treatFinal("begin")
        self.comando()
        self.lista_com()
        self.treatFinal("end")
        self.d("[\\BLOCO_FUNCAO]")
        
    def comando(self):
        self.d("[COMANDO]")
        if self.peek("while"):
            self.treatFinal("while")
            self.exp_logica()
            self.bloco()
        elif self.peek("if"):
            self.treatFinal("if")
            self.exp_logica()
            self.treatFinal("then")
            self.bloco()
            self.elseB()            
        elif self.peek("write"):
            self.treatFinal("write")
            self.const_valor()
        elif self.peek("read"):
            self.treatFinal("read")
            self.id()
            self.nome()
        else:
            self.id()
            self.nome()
            self.treatFinal(":=")
            self.exp_mat()
        self.d("[\\COMANDO]")
        
    def lista_com(self):
        if not self.peek(";"): return False
        self.d("[LISTA_COM]")
        self.treatFinal(";")
        self.comando()
        self.lista_com()
        self.d("[\\LISTA_COM]")
        
    def bloco(self):
        self.d("[BLOCO]")
        if self.peek("begin"):
            self.treatFinal("begin")
            self.comando()
            self.lista_com()
            self.treatFinal("end")
        else: self.comando()
        self.d("[\\BLOCO]")
        
    def elseB(self):
        if self.peek("else"):
            self.d("[ELSE]")
            self.treatFinal("else")
            self.bloco()
            self.d("[\\ELSE]")
            return True
        else: return False
        
    def lista_param(self):
        if self.parametro():
            self.d("[LIST_PARAM]")
            if self.peek(","):
                self.treatFinal(",")
                self.lista_param()
            self.d("[\\LIST_PARAM]")
            return True
            
    def exp_logica(self):
        self.d("[EXP_LOGICA]")
        self.exp_mat()
        if self.op_logico():
            self.exp_logica()
        self.d("[\\EXP_LOGICA]")
            
    def op_logico(self):
        self.d("[OP_LOGICO]")
        ops = [ '>', '<', '=', '!']
        for op in ops:
            if self.peek(op):
                self.treatFinal(op)
                return True
        self.d("[\\OP_LOGICO]")
        return False
        
    def lista_id(self):
        if not self.peek(","): return False
        self.d("[LISTA_ID]")
        self.treatFinal(",")
        self.id()
        self.lista_id()
        self.d("[\\LISTA_ID]")
        return True
    
    def tipo_dado(self):
        self.d("[TIPO_DADO]")
        if self.peek("integer"): self.treatFinal("integer")
        elif self.peek("real"): self.treatFinal("real")
        elif self.peek("array"): 
            self.treatFinal("array")
            self.treatFinal("[")
            self.numero()
            self.treatFinal("]")
            self.treatFinal("of")
            self.tipo_dado()
        elif self.peek("record"):
            self.treatFinal("record")
            self.campos()
            self.treatFinal("end")
        else: self.id()
        self.d("[\\TIPO_DADO]")
    
    def campos(self):
        self.d("[CAMPOS]")
        self.id()
        self.treatFinal(":")
        self.tipo_dado()
        self.lista_campos()
        self.d("[\\CAMPOS]")
        
    def lista_campos(self):
        self.d("[LISTA_CAMPOS]")
        if(not self.peek(";")): return False
        self.treatFinal(";")
        self.campos()
        self.lista_campos()
        self.d("[\\LISTA_CAMPOS]")
        return True
     
    def numero(self):
        self.d("[NUMERO]")
        if(not self.peek("numeric")): return False
        self.treatFinal("numeric")
        self.d("[\\NUMERO]")
        return True
        
    def id(self):
        self.d("[ID]")
        if(not self.peek("alphanumeric")): return False
        self.treatFinal("alphanumeric")
        self.d("[\\ID]")
        return True
        
    def const_valor(self):
        self.d("[CONST_VALOR]")
        if self.peek("const_valor"): self.treatFinal("const_valor")
        else: self.exp_mat()
        self.d("[\\CONST_VALOR]")
        
    def exp_mat(self):
        self.d("[EXP_MAT]")
        self.parametro()
        if self.op_mat():
            self.exp_mat()
        self.d("[\\EXP_MAT]")
        
    def parametro(self):
        self.d("[PARAMETRO]")
        if self.numero():
            return True
        elif self.id():
            self.nome()
            return True
        return False
        self.d("[\\PARAMETRO]")
            
    def nome(self):
        self.d("[NOME]")
        if self.peek("."): 
            self.treatFinal(".")
            self.id()
            self.nome()
        elif self.peek("["):
            self.treatFinal("[")
            self.parametro()
            self.treatFinal("]")
        elif self.peek("("):
            self.treatFinal("(")
            self.lista_param()
            self.treatFinal(")")
        self.d("[\\NOME]")
            
    def op_mat(self):
        self.d("[OP_MAT]")
        ops = [ '+', '-', '*', '/']
        for op in ops:
            if self.peek(op):
                self.treatFinal(op)
                return True
        self.d("[\\OP_MAT]")
        return False
        
    