from token import *
from tree import *
import sys

class Sintatico:

    def __init__(self,token,debug = False):
        self.a=0
        self.error = False
        self.t=token
        self.debug = debug
        self.sintTree = self.programa()
        print("end")
        self.sintTree.print()
        
    def d(self,string):
        if self.debug: print(string)
        
    def treatFinal(self,input):
        self.d("treating: "+input+" -> "+str(self.t[self.a]))
        if self.t[self.a].equals(input):
            f = self.t[self.a]
            self.a+=1
            return f
        else:
            t = self.t[self.a]
            print("error at "+str(t.line)+","+str(t.column)+": expected "+input+" but found "+t.id+": "+t.value )
            sys.exit()
        
    def peek(self,input):
        self.d("peeking: "+input+" -> "+str(self.t[self.a]))
        if self.t[self.a].equals(input): return True
        else: return False
    
    #-------------------#
    
    def programa(self):
        self.d("[PROGRAMA]")
        tree = Tree("PROGRAMA")
        tree.addChild(self.declaracoes())
        tree.addChild(self.principal())
        self.d("[\\PROGRAMA]")
        return tree
        
    def principal(self):
        self.d("[PRINCIPAL]")
        tree = Tree("PRINCIPAL")
        tree.addChild(self.treatFinal("begin"))
        tree.addChild(self.comando())
        tree.addChild(self.lista_com())
        tree.addChild(self.treatFinal("end"))
        self.d("[\\PRINCIPAL]")
        return tree
        
    def declaracoes(self):
        self.d("[DECLARAÇÕES]")
        tree = Tree("DECLARAÇÕES")
        tree.addChild(self.def_const())
        tree.addChild(self.def_tipos())
        tree.addChild(self.def_var())
        tree.addChild(self.def_func())
        self.d("[\\DECLARAÇÕES]")
        return tree
        
    def def_const(self):
        self.d("[DEF_CONST]")
        tree = Tree("DEF_CONST")
        if tree.addChild(self.constante()): 
            tree.addChild(self.def_const())
        self.d("[\\DEF_CONST]")
        return tree
        
    def constante(self):
        if not self.peek("const"): return False
        self.d("[CONSTANTE]")
        tree = Tree("CONSTANTE")
        tree.addChild(self.treatFinal("const"))
        tree.addChild(self.id())
        tree.addChild(self.treatFinal("equals"))
        tree.addChild(self.const_valor())
        tree.addChild(self.treatFinal(";"))
        self.d("[\\CONSTANTE]")
        return tree
        
    def def_tipos(self):
        self.d("[DEF_TIPOS]")
        tree = Tree("DEF_TIPOS")
        if tree.addChild(self.tipo()): 
            tree.addChild(self.def_tipos())
        self.d("[\\DEF_TIPOS]")
        return tree
        
    def tipo(self):
        if not self.peek("type"): return False
        self.d("[TIPO]")
        tree = Tree("TIPO")
        tree.addChild(self.treatFinal("type"))
        tree.addChild(self.id())
        tree.addChild(self.treatFinal("="))
        tree.addChild(self.tipo_dado())
        tree.addChild(self.treatFinal(";"))
        self.d("[\\TIPO]")
        return  tree
        
    def def_var(self):
        self.d("[DEF_VAR]")
        tree = Tree("DEF_VAR")
        if tree.addChild(self.variavel()):
            tree.addChild(self.def_var())
        self.d("[\\DEF_VAR]")
        return tree
        
    def variavel(self):
        if not self.peek("var"): return False
        self.d("[VARIAVEL]")
        tree = Tree("VARIAVEL")
        tree.addChild(self.treatFinal("var"))
        tree.addChild(self.id())
        tree.addChild(self.lista_id())
        tree.addChild(self.treatFinal(":"))
        tree.addChild(self.tipo_dado())
        tree.addChild(self.treatFinal(";"))
        self.d("[\\VARIAVEL]")
        return tree
        
    def def_func(self):
        self.d("[DEF_FUNC]")
        tree = Tree("DEF_FUNC")
        if tree.addChild(self.funcao()):
            tree.addChild(self.def_func())
        self.d("[\\DEF_FUNC]")
        return tree
        
    def funcao(self):
        if not self.peek("function"): return False
        self.d("[FUNCAO]")
        tree = Tree("FUNCAO")
        tree.addChild(self.treatFinal("function"))
        tree.addChild(self.nome_funcao())
        tree.addChild(self.bloco_funcao())
        self.d("[\\FUNCAO]")
        return tree
        
    def nome_funcao(self):
        self.d("[NOME_FUNCAO]")
        tree = Tree("NOME_FUNCAO")
        tree.addChild(self.id())
        tree.addChild(self.param_func())
        tree.addChild(self.treatFinal(":"))
        tree.addChild(self.tipo_dado())
        self.d("[\\NOME_FUNCAO]")
        return tree
        
    def param_func(self):
        if not self.peek("("): return False
        self.d("[PARAM_FUNC]")
        tree = Tree("PARAM_FUNC")
        tree.addChild(self.treatFinal("("))
        tree.addChild(self.campos())
        tree.addChild(self.treatFinal(")"))
        self.d("[\\PARAM_FUNC]")
        return tree
        
    def bloco_funcao(self):
        self.d("[BLOCO_FUNCAO]")
        tree = Tree("BLOCO_FUNCAO")
        tree.addChild(self.def_var())
        tree.addChild(self.treatFinal("begin"))
        tree.addChild(self.comando())
        tree.addChild(self.lista_com())
        tree.addChild(self.treatFinal("end"))
        self.d("[\\BLOCO_FUNCAO]")
        return tree
        
    def comando(self):
        self.d("[COMANDO]")
        tree = Tree("COMANDO")
        if self.peek("while"):
            tree.addChild(self.treatFinal("while"))
            tree.addChild(self.exp_logica())
            tree.addChild(self.bloco())
        elif self.peek("if"):
            tree.addChild(self.treatFinal("if"))
            tree.addChild(self.exp_logica())
            tree.addChild(self.treatFinal("then"))
            tree.addChild(self.bloco())
            tree.addChild(self.elseB())
        elif self.peek("write"):
            tree.addChild(self.treatFinal("write"))
            tree.addChild(self.const_valor())
        elif self.peek("read"):
            tree.addChild(self.treatFinal("read"))
            tree.addChild(self.id())
            tree.addChild(self.nome())
        else:
            tree.addChild(self.id())
            tree.addChild(self.nome())
            tree.addChild(self.treatFinal(":="))
            tree.addChild(self.exp_mat())
        self.d("[\\COMANDO]")
        return tree
        
    def lista_com(self):
        if not self.peek(";"): return False
        self.d("[LISTA_COM]")
        tree = Tree("LISTA_COM")
        tree.addChild(self.treatFinal(";"))
        tree.addChild(self.comando())
        tree.addChild(self.lista_com())
        self.d("[\\LISTA_COM]")
        return tree
        
    def bloco(self):
        self.d("[BLOCO]")
        tree = Tree("BLOCO")
        if self.peek("begin"):
            tree.addChild(self.treatFinal("begin"))
            tree.addChild(self.comando())
            tree.addChild(self.lista_com())
            tree.addChild(self.treatFinal("end"))
        else: tree.addChild(self.comando())
        self.d("[\\BLOCO]")
        return tree
        
    def elseB(self):
        if self.peek("else"):
            self.d("[ELSE]")
            tree = Tree("ELSE")
            tree.addChild(self.treatFinal("else"))
            tree.addChild(self.bloco())
            self.d("[\\ELSE]")
            return tree
        else: return False
        
    def lista_param(self):
        tree = Tree("LIST_PARAM")
        if tree.addChild(self.parametro()):
            self.d("[LIST_PARAM]")
            if self.peek(","):
                tree.addChild(self.treatFinal(","))
                tree.addChild(self.lista_param())
            self.d("[\\LIST_PARAM]")
            return tree
        else: return False
            
    def exp_logica(self):
        self.d("[EXP_LOGICA]")
        tree = Tree("EXP_LOGICA")
        tree.addChild(self.exp_mat())
        if tree.addChild(self.op_logico()):
            tree.addChild(self.exp_logica())
        self.d("[\\EXP_LOGICA]")
        return tree
        
    def op_logico(self):
        self.d("[OP_LOGICO]")
        tree = Tree("OP_LOGICO")
        ops = [ '>', '<', '=', '!']
        for op in ops:
            if self.peek(op):
                tree.addChild(self.treatFinal(op))
                return tree
        self.d("[\\OP_LOGICO]")
        return False
        
    def lista_id(self):
        if not self.peek(","): return False
        self.d("[LISTA_ID]")
        tree = Tree("LISTA_ID")
        tree.addChild(self.treatFinal(","))
        tree.addChild(self.id())
        tree.addChild(self.lista_id())
        self.d("[\\LISTA_ID]")
        return tree
    
    def tipo_dado(self):
        self.d("[TIPO_DADO]")
        tree = Tree("TIPO_DADO")
        if self.peek("integer"): tree.addChild(self.treatFinal("integer"))
        elif self.peek("real"): tree.addChild(self.treatFinal("real"))
        elif self.peek("array"):
            tree.addChild(self.treatFinal("array"))
            tree.addChild(self.treatFinal("["))
            tree.addChild(self.numero())
            tree.addChild(self.treatFinal("]"))
            tree.addChild(self.treatFinal("of"))
            tree.addChild(self.tipo_dado())
        elif self.peek("record"):
            tree.addChild(self.treatFinal("record"))
            tree.addChild(self.campos())
            tree.addChild(self.treatFinal("end"))
        else: tree.addChild(self.id())
        self.d("[\\TIPO_DADO]")
        return tree
        
    def campos(self):
        self.d("[CAMPOS]")
        tree = Tree("CAMPOS")
        tree.addChild(self.id())
        tree.addChild(self.treatFinal(":"))
        tree.addChild(self.tipo_dado())
        tree.addChild(self.lista_campos())
        self.d("[\\CAMPOS]")
        return tree
        
    def lista_campos(self):
        self.d("[LISTA_CAMPOS]")
        if(not self.peek(";")): return False
        tree = Tree("LISTA_CAMPOS")
        tree.addChild(self.treatFinal(";"))
        tree.addChild(self.campos())
        tree.addChild(self.lista_campos())
        self.d("[\\LISTA_CAMPOS]")
        return tree
     
    def numero(self):
        self.d("[NUMERO]")
        tree = Tree("NUMERO")
        if(not self.peek("numeric")): return False
        tree.addChild(self.treatFinal("numeric"))
        self.d("[\\NUMERO]")
        return tree
        
    def id(self):
        self.d("[ID]")
        tree = Tree("ID")
        if(not self.peek("alphanumeric")): return False
        tree.addChild(self.treatFinal("alphanumeric"))
        self.d("[\\ID]")
        return tree
        
    def const_valor(self):
        self.d("[CONST_VALOR]")
        tree = Tree("CONST_VALOR")
        if self.peek("const_valor"): tree.addChild(self.treatFinal("const_valor"))
        else: tree.addChild(self.exp_mat())
        self.d("[\\CONST_VALOR]")
        return tree
        
    def exp_mat(self):
        self.d("[EXP_MAT]")
        tree = Tree("EXP_MAT")
        tree.addChild(self.parametro())
        if tree.addChild(self.op_mat()):
            tree.addChild(self.exp_mat())
        self.d("[\\EXP_MAT]")
        return tree
        
    def parametro(self):
        self.d("[PARAMETRO]")
        tree = Tree("PARAMETRO")
        if tree.addChild(self.numero()):
            return tree
        elif tree.addChild(self.id()):
            tree.addChild(self.nome())
            return tree
        else: return False
        self.d("[\\PARAMETRO]") #????????
            
    def nome(self):
        self.d("[NOME]")
        tree = Tree("NOME")
        if self.peek("."): 
            tree.addChild(self.treatFinal("."))
            tree.addChild(self.id())
            tree.addChild(self.nome())
        elif self.peek("["):
            tree.addChild(self.treatFinal("["))
            tree.addChild(self.parametro())
            tree.addChild(self.treatFinal("]"))
        elif self.peek("("):
            tree.addChild(self.treatFinal("("))
            tree.addChild(self.lista_param())
            tree.addChild(self.treatFinal(")"))
        self.d("[\\NOME]")
        return tree
        
    def op_mat(self):
        self.d("[OP_MAT]")
        tree = Tree("OP_MAT")
        ops = [ '+', '-', '*', '/']
        for op in ops:
            if self.peek(op):
                tree.addChild(self.treatFinal(op))
                return tree
        self.d("[\\OP_MAT]")
        return False
        
    