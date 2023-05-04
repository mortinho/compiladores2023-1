
from token import *
import sintatico

def lexico(filepath, debug = False):
    with open(filepath, mode="r", encoding = "utf-8") as txt:
        linecounter =  0
        linhas = []
        for i in txt:
            linhas.append(i.strip())
            linecounter+=1
        
    line = 0
    readConst = False
    tokens = []

    for i in linhas:
        char = 0
        lastchar = 1
        line+=1
        buffer=""
        
        for j in range(len(i)):
            char+=1
            bufferSize = len(buffer)
            
            if i[j] == '\"':
                readConst = not readConst
                
                if not readConst:
                    tokens.append(Token(line,lastchar,buffer,const = True))
                    buffer = ""
                continue
                    
            if (bufferSize==0):
                lastchar = char
            
            if readConst:
                buffer+=i[j]
                
            elif i[j] in (separators()):
                if(bufferSize>0):
                    if not buffer.isnumeric():
                        if buffer[0].isnumeric():
                            newBuffer = ""
                            while buffer[0].isnumeric():
                                newBuffer+=buffer[0]
                                buffer=buffer[1:]
                            tokens.append(Token(line,lastchar,newBuffer))
                            lastchar+=len(newBuffer)
                    tokens.append(Token(line,lastchar,buffer))
                    buffer = ""
                    
                if i[j] not in separator:
                    tokens.append(Token(line,char,i[j]))
                
            elif i[j] not in separator:
                buffer+=i[j]
                if j == len(i)-1:
                    tokens.append(Token(line,lastchar,buffer))
                    
                

    remove = []
    for i in range(len(tokens)):
        if tokens[i].value == "=":
            if i==0: #oob prevenction
                continue
            if tokens[i-1].value == ":" and tokens[i].column - tokens[i-1].column == 1:
                tokens[i-1].value = ":="
                tokens[i-1].id = symbols[":="]
                remove.append(i)
        
        elif tokens[i].value == ".":
            if i == len(tokens) - 1:
                continue
            if tokens[i-1].id =="numeric" and tokens[i+1].id =="numeric":
                if i-1 in remove:
                    continue
                a = tokens[i-1]
                b = tokens[i+1]
                if a.column+len(a.value) == tokens[i].column == b.column -1:
                    a.value = a.value+"."+b.value
                    remove.append(i)
                    remove.append(i+1)

    for i in reversed(remove):
        tokens.pop(i)

    if debug:
        for i in tokens:
            print(i)
            
    return tokens


sintatico.Sintatico(lexico('./test.txt'),debug=False)