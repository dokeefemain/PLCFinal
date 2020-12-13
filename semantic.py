from rda import lex
import re

expression = "a * b - 1 + c"
declaration = "a=5 b=True c=4"
class lexType:
    lin_num = 1
    def tokenize(self, code):
        rules = [
            ('INT',r'[a-zA-Z]\w*=\d(\d)*'),
            ('BOOL',r'[a-zA-Z]\w*=(True)*(False)*'),
            ('STRING',r'[a-zA-Z]\w*=\"[a-zA-Z]\w*\"'),
            ('CHAR',r'[a-zA-Z]\w*=\'[a-zA-Z]\''),
        ]
        tokens_join = '|'.join('(?P<%s>%s)' % x for x in rules)
        token = []
        lexeme = []
        for i in re.finditer(tokens_join, code):
            token_type = i.lastgroup
            token_lexeme = i.group(token_type)
            lexeme.append(token_lexeme)
            token.append(token_type)

        return token, lexeme
def checkSem(Token_arry,lexeme):
    for i in range(len(Token_arry)-1):
        curr = Token_arry[i]
        if curr != 'INT' and curr != 'CHAR' and curr != 'BOOL' and curr != 'STRING':
            frontback(Token_arry,lexeme,i)
def frontback(Token_arry,lexeme,i):
    curr = Token_arry[i]
    front = Token_arry[i+1]
    back = Token_arry[i-1]
    if curr == 'AND_AND' or curr == 'OR_OR' or curr == 'XOR':
        if front != 'BOOL' or back != 'BOOL':
            print('ERROR INCORRECT TYPE FOR BOOL OPERATION',lexeme[i-1],lexeme[i],lexeme[i+1])
    elif curr != 'LEFT_PAREN' or curr != 'RIGHT_PAREN':
        if front != 'INT' or back != 'INT':
            print('ERROR INCORRECT TYPE FOR INT OPERATION',lexeme[i-1],lexeme[i],lexeme[i+1]) 
def main(expression,declaration):
    Token_arry,lexeme = lexType().tokenize(declaration)
    Token_arry2,lexemes2 = lex().tokenize(expression)
    count = 0
    for i in range(len(Token_arry2)):
        if Token_arry2[i] == 'ID':
            Token_arry2[i] = Token_arry[count]
            count+=1
    print(expression)
    print(declaration)
    checkSem(Token_arry2,lexemes2)
def driver():
    expression = "a * b - 1 + c"
    declaration = "a=5 b=True c=4"
    main(expression,declaration)
    expression = "a * b - 1 + c"
    declaration = "a=5 b=6 c=4"
    main(expression,declaration)
    expression = "a && b + c"
    declaration = "a=True b=True c=False"
    main(expression,declaration)
driver()

#out
""" 
a * b - 1 + c
a=5 b=True c=4
ERROR INCORRECT TYPE FOR INT OPERATION a * b
ERROR INCORRECT TYPE FOR INT OPERATION b - 1

a * b - 1 + c
a=5 b=6 c=4

a && b + c
a=True b=True c=False
ERROR INCORRECT TYPE FOR INT OPERATION b + c 
"""
