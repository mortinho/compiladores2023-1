finals = [
            "begin",
            "end",
            "const",
            "type",
            "var",
            "integer",
            "real",
            "array",
            "record",
            "of",
            "function",
            "while",
            "if",
            "then",
            "write",
            "read",
            "else"
         ]

symbols = { 
            ":=":"receives",
            "=":"equals",
            ";":"semicolon",
            ":":"colon",
            ",":"comma",
            ".":"dot",
            "<":"lessthan",
            ">":"morethan",
            "!":"exclamation",
            "+":"plus",
            "-":"minus",
            "*":"asterisk",
            "/":"divide",
            "(":"openparenthesis",
            ")":"closeparenthesis",
            "[":"openbrackets",
            "]":"closebrackets" 
           }

separator = [
            " "
            ]
    
def separators():
    return list(symbols) + separator
    
class Token:
    def __init__(self,line,column,value, const = False):
        self.line = line
        self.column = column
        self.value = value
        if const:
            self.id = "const_valor"
        elif(value in symbols.keys()):
            self.id = symbols[value]
        elif(value in finals):
            self.id = value
        elif(value.isnumeric()):
            self.id = "numeric"
        elif(value.isalnum()):
            if value[0].isalpha():
                self.id = "alphanumeric"
            else:
                self.id = "error"
        else:
            self.id = "error"
            print("unidentified token at line ",line," at the ",column," character")
    
    def __str__(self):
        return str(self.line) + "," + str(self.column) + ": " + self.id + " " + self.value
        
