import re
class lex:
    lin_num = 1
    def tokenize(self, code):
        rules = [
            ('AND_AND',r'&&'),
            ('AND',r'&'),
            ('OR_OR',r'\|\|'),
            ('XOR',r'~\|'),
            ('FALSE',r'False'),
            ('INT',r'\d(\d)*'),
            ('GREATER',r'>'),
            ('GREATER_EQUAL',r'>='),
            ('LESS_EQUAL',r'<='),
            ('LESS',r'<'),
            ('NOT',r'!'),
            ('MOD',r'%'),
            ('EQUAL',r'='),
            ('PLUS_PLUS',r'\+\+'),
            ('MINUS_MINUS',r'--'),
            ('TIMES_EQUAL',r'\*='),
            ('PLUS',r'\+'),
            ('MINUS',r'\-'),
            ('TIMES',r'\*'),
            ('DIV',r'\/'),
            ('ID',r'[a-zA-Z]\w*'),
            ('LEFT_PAREN', r'\('),
            ('RIGHT_PAREN', r'\)'),
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
class expr(object):
    def __init__(self,expression,index):
        self.expression = expression
        self.index = index
    def lex(self):
        tmp = self.expression[self.index]
        self.index += 1
        return tmp
    def checkLast(self):
        if self.index +1 == len(self.expression):
            return True
        else:
            return False
    def get2(self):
        tmp = self.expression[:2]
        return tmp
    def getExp(self):
        return self.expression
    def getIndex(self):
        return self.index-1

    
def exprr(exp):
    exp_array = exp.getExp()
    highest = 10
    highestI = 0
    for i in exp_array:
        curr = exp.lex()
        if curr != 'INT' and curr != 'ID':
            tmp = level1(i)
            if tmp < highest:
                highest = tmp
                highestI = exp.getIndex()
                highestVal = i
    exp_array.pop(highestI)
    print(highestVal,"is exicuted")
    return exp_array

    
def level1(curr):
    if curr == 'PLUS_PLUS' or curr == 'MINUS_MINUS':
        return 1
    else:
        return level2(curr)
def level2(curr):
    if curr == 'PLUS_PLUS' or curr == 'MINUS_MINUS':
        return 2
    else:
        return level3(curr)
def level3(curr):
    if curr == 'TIMES' or curr =='GREATER_EQUAL' or curr == 'AND':
        return 3
    else:
        return level4(curr)
def level4(curr):
    if curr == 'PLUS' or curr == 'MINUS' or curr == 'LESS_EQUAL':
        return 4
    else:
        return level5(curr)
def level5(curr):
    if curr == 'MINUS' or curr =='PLUS' or curr == 'MOD':
        return 5
    else:
        return level6(curr)
def level6(curr):
    if curr == 'GREATER' or curr =='LESS' or curr =='NOT':
        return 6
    else:
        return level7(curr)
def level7(curr):
    if curr == 'AND_AND' or curr =='DIV':
        return 7
    else:
        return level8(curr)
def level8(curr):
    if curr == 'OR_OR' or curr =='XOR':
        return 8
    else:
        return level9(curr)
def level9(curr):
    if curr == 'EQUAL' or curr =='/=':
        return 9
    else:
        return 10
def solve_paren(Token_arry):
    tmp_Token_arry = Token_arry
    for i in range(len(tmp_Token_arry)):
        if tmp_Token_arry[i] == "LEFT_PAREN":
            indexs = i
        elif tmp_Token_arry[i] == "RIGHT_PAREN":
            indexf = i+1
            RDA(Token_arry[indexs+1:indexf-1])
            Token_arry=tmp_Token_arry[:indexs]+tmp_Token_arry[indexf:]
            return solve_paren(Token_arry)
    return Token_arry
    
def RDA(Token_arry):
    test = True
    while test:
        tmp = expr(Token_arry,0)
        Token_arry = exprr(tmp)
        test = False
        for i in Token_arry:
            if i!= 'ID' and i!='INT':
                test = True
    
def RDA1(Token_arry):
    Token_arry = solve_paren(Token_arry)
    RDA(Token_arry)
def main(expression):
    Token_arry,Token_lexeme = lex().tokenize(expression)
    print("Order of operations for",expression,"is:")
    RDA1(Token_arry)
def driver():
    main("a ~| b - 1 + c")
    
    main("a * (b - 1) / c % d")
    main("(a - b) / c & (d * e / a - 3)")
    main("( a + b <= c ) * ( d > b - e )")
    main("-a || c = d && e")
    main("a > b ˜| c || d <= 17")
    main("-a + b")
    main("a + b * c + d")
    main("E = ++(a++)")

#Output for 1-9
""" Order of operations for a * b - 1 + c is:
TIMES is exicuted
MINUS is exicuted
PLUS is exicuted
Order of operations for a * (b - 1) / c % d is:
MINUS is exicuted
TIMES is exicuted
MOD is exicuted
DIV is exicuted
Order of operations for (a - b) / c & (d * e / a - 3) is:
MINUS is exicuted
TIMES is exicuted
MINUS is exicuted
DIV is exicuted
AND is exicuted
DIV is exicuted
Order of operations for ( a + b <= c ) * ( d > b - e ) is:
PLUS is exicuted
LESS_EQUAL is exicuted
MINUS is exicuted
GREATER is exicuted
TIMES is exicuted
Order of operations for -a || c = d && e is:
MINUS is exicuted
AND_AND is exicuted
OR_OR is exicuted
EQUAL is exicuted
Order of operations for a > b ˜| c || d <= 17 is:
LESS_EQUAL is exicuted
GREATER is exicuted
OR_OR is exicuted
Order of operations for -a + b is:
MINUS is exicuted
PLUS is exicuted
Order of operations for a + b * c + d is:
TIMES is exicuted
PLUS is exicuted
PLUS is exicuted
Order of operations for E = ++(a++) is:
PLUS_PLUS is exicuted
PLUS_PLUS is exicuted
EQUAL is exicuted """
#driver()