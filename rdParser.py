"""
CS530 Spring 2021: Programming Assignment 2 Part B.
Richard Sutherland 

I the undersigned promise that the attached assignment is my own work.
While I was free to discuss ideas with others, the work contained is my own. 
I recognize that should this not be the case, I will be subject to penalties as 
outlined in the course syllabus. 
RICHARD SUTHERLAND (812217192)

"""


"""

A LL recursive descent parser for validating simple expressions.

You would need to first write the grammar rules (non-terminal) in EBNF according to the token
patterns and grammar rules specified in Assignment 2 Task A. 
You can then follow the examples of the parsing procedure pseudocode implementation in Figure 5.17
in the textbook to write the recursive descent parsing procedures for the validation parsing.

The following recursive descent parsing algorithm is a LL parser. It implements one parsing 
procedure for each one of the above non-terminals (grammar rules), starting from the top of the 
parse tree, then drilling into lower hierachical levels.

The procedures work together to handle all combinations of the grammar rules, and they 
automatically handle the nested compositions of terms with multi-level priority brackets. 

---------------------------------------------------------------------
Usage

r = recDecsent('7 - 17')
self.log.append(r.validate()) # will print True as '7 - 17' is a valid expression

r = recDecsent('7 - ')
self.log.append(r.validate()) # will print False as '7 - ' is an invalid expression

"""

import re
from functools import *

class recDescent:
    
    # relational (unary) operators (prefix)
    relop = ['<', '>', '<=', '>=', '=', '!=', 'not']
    
    # binary operators (infix)
    dashop = ['-', '–']
    logicop = ['and', 'or']

    # tokens for manipulating priority
    priopen = '('
    priclose = ')'

    # constructor to initialize and set class level variables
    def __init__(self, expr = ""):

        # string to be parsed
        self.expr = expr

        # tokens from lexer tokenization of the expression
        self.tokens = []
        
        self.index = 0
        self.log = []
    # lexer - tokenize the expression into a list of tokens
    # the tokens are stored in an list which can be accessed by self.tokens
    # do not edit any piece of code in this function
    def lex(self):
        self.tokens = re.findall("[-\(\)=]|[!<>]=|[<>]|\w+|[^ +]\W+", self.expr)
        # filter out the possible spaces in the elements
        self.tokens = list(filter((lambda x: len(x)), 
                           list(map((lambda x: x.strip().lower()), self.tokens))))    
    
    # parser - determine if the input expression is valid or not
    
    # validate() function will return True if the expression is valid, False otherwise 
    # do not change the method signature as this function will be called by the autograder
    def validate(self):
    # use your parsing procedures below to validate
        self.lex()
        return self.isExp()

    # parsing procedures corresponding to the grammar rules - follow Figure 5.17
    
    # advance the index if we can
    def advance(self):
        if(self.index + 1 > len(self.tokens) - 1):
            self.log.append(f'tried to advance out of range to index: {self.index+1}')
            return False
        else:
            self.index += 1
            self.log.append(f'advancing to next token ({self.index})')
            return True
    
    #check for <op> ::= and | or
    def isOp(self):
        self.log.append(f'calling isOp @ index: {self.index}')
        return self.tokens[self.index] in self.logicop

    # check for (
    def isOpenParen(self):
        self.log.append(f'calling isOpenParen @ index: {self.index}')
        return self.tokens[self.index] == self.priopen
    
    # check for )
    def isCloseParen(self):
        self.log.append(f'calling isCloseParen @ index: {self.index}')
        return self.tokens[self.index] == self.priclose
    
    # check for int
    def isInt(self):
        token = self.tokens[self.index]
        self.log.append(f'calling isInt @ index: {self.index}')
        return re.match("^\d+$", token) is not None

    # check for <relop> ::= < | > | <= | >= | = | != | not
    def isRelop(self):
        token = self.tokens[self.index]
        self.log.append(f'calling isRelop @ index: {self.index}')
        return token in self.relop
    
    # check for int-int
    def isRange(self):
        self.log.append(f'calling isRange @ index: {self.index}')
        found = False
        if self.isInt():
            if self.advance():
                if self.tokens[self.index] in self.dashop:
                    if self.advance():
                        if self.isInt():
                            found = True          
        return found
            
    # check for <term> non terminal
    def isTerm(self):
        self.log.append(f'calling isTerm @ index: {self.index}')
        found = False
        if self.isRange():
            found = True
            self.advance()
        elif self.isRelop():
            if self.advance():
                if self.isInt():
                    found = True
                    self.advance()
        elif self.isOpenParen():
            if self.advance():
                if self.isExp():
                    if self.isCloseParen():
                        found = True
                        self.advance()
        return found

    
    def isExp(self):
        startIndex = self.index
        found = False
        if self.isTerm():
            found = True
            while self.isOp() and found == True:
                self.advance()
                if not self.isTerm():
                    found = False
        if found:
            self.log.append(f'found exp: {self.tokens[startIndex:self.index+1]}')
        return found
    
    def printLog(self):
        for l in self.log:
            print(l)
        
