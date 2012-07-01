import re
import ply.yacc as yacc
from copy import deepcopy
from c_lex import tokens

temp_count = 0; # To keep a track of temp variables ... using $$
label_count = 0; # To keep a track of Labels .... using ~~
dict_var = {} # A dict for mapping register to vairables
register_count = 0 # To keep a track on registers .... using @@
string_count = 0 #To keep a count on number of strings ... Will store the sting in a map
converted_list = []
proc_name = "" # The name of the procedure ... Not being converted to SUIF code at present

precedence = (
    ('right', 'ASSIGN', 'EQ_PLUS', 'EQ_MINUS', 'EQ_TIMES', 'EQ_DIV'),
    ('left', 'DOUBLE_PIPE'),
    ('left', 'DOUBLE_AMPERSAND'),
    ('left', 'NOT_EQ', 'EQ'),
    ('left', 'GREATER', 'LESS', 'GREATER_EQ', 'LESS_EQ'),
  	('left', 'PLUS', 'MINUS'),
    ('left', 'ASTERISK', 'DIV'),
    ('right', 'UEXCLAMATION', 'UASTERISK', 'UMINUS', 'AMPERSAND'),
	('right', 'DOUBLE_PLUS', 'DOUBLE_MINUS'),
    
)
class ParseError(Exception):
    "Exception raised whenever a parsing error occurs."

    pass

def p_start(p):
	'''start : translation_unit'''
	global dict_var;
	global register_count;
	p[0] = p[1]
	for induction in range(len(p[0])):
		i = p[0][induction]
		i_list = list(i)
		for k in range(len(i_list)):
			j = i_list[k]
			if(j[:2] == "@@"):
				var = j[2:]
				if(dict_var.has_key(var)):
					i_list[k] = dict_var[var];
				else:
					temp_str = "r" + str(register_count);
					register_count = register_count + 1;
					dict_var[var] = temp_str;
					i_list[k] = temp_str;
			if j[:2] == "$$" :
				i_list[k] = j[2:]
			if j[:2] == "~~" :
				i_list[k] = "__" + j[2:]
		i = tuple(i_list)
		p[0][induction] = i;
					
	global converted_list
	converted_list = p[0]
	print "Grammar Accepted"
	pass

def p_translation_unit_01(p):
    '''translation_unit : external_declaration'''
    p[0] = p[1]
    pass
    
def p_translation_unit_02(p):
	'''translation_unit : translation_unit external_declaration'''
	if type(p[1]) == list :
		p[0] = p[1]
	else :
		p[0] = []
	if type(p[2]) == list :
		p[0].extend(p[2])
	pass
    
def p_external_declaration(p):
    '''external_declaration : function_definition
                            | declaration'''
    p[0] = p[1]

def p_function_definition_01(p):
	'''function_definition : type_specifier declarator compound_statement'''
	if type(p[1]) == list :
		p[0] = p[1]
	else :
		p[0] = []
	if type(p[2]) == list :
		p[0].extend(p[2])
		
	if type(p[3]) == list :
		p[0].extend(p[3])
	
	pass
    
def p_function_definition_02(p):
	'''function_definition : STATIC type_specifier declarator compound_statement'''
	if type(p[2]) == list :
		p[0] = p[2]
	else :
		p[0] = []
	if type(p[3]) == list :
		p[0].extend(p[3])
		
	if type(p[4]) == list :
		p[0].extend(p[4])	
	pass
    
def p_declaration_01(p):
    '''declaration : type_specifier declarator SEMICOLON'''
    # Doing nothing here at present ... just returning a []
    p[0] = p[2]

def p_declaration_02(p):
    '''declaration : EXTERN type_specifier declarator SEMICOLON'''
    # Doing nothing here at present ... just returning a []
    p[0] = p[3]

def p_declaration_list_opt_01(p):
    '''declaration_list_opt : empty'''
    p[0] = []

def p_declaration_list_opt_02(p):
    '''declaration_list_opt : declaration_list'''
    p[0] = p[1]

def p_declaration_list_02(p):
    '''declaration_list : declaration'''
    p[0] = p[1]
    
    
def p_declaration_list_03(p):
	'''declaration_list : declaration declaration_list '''
	p[0] = []
	if type(p[1]) == list:
		p[0].extend(p[1])
	if type(p[2]) == list:
		p[0].extend(p[2])
    
def p_type_specifier(p):
    '''type_specifier : INT
                      | CHAR
                      | empty
                      | VOID
                      | FLOAT
                      | DOUBLE
                      | LONG'''
    p[0] = []
	
def p_declarator_01(p):
	'''declarator : direct_declarator'''
	if type(p[1]) == str:
		p[0] = [("cpy", "@@" + p[1], "[RAND]", "")]
	elif type(p[1]) == list:
		p[0] = p[1]   

def p_declarator_01_01(p):
	'''declarator : expression ASSIGN expression'''
	p[0] = [];
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	# for x = y ... got the x
	
	if(type(p[3]) == list) :
		p[0].extend(p[3])
		temp2 = p[3][-1][1]
		tup = ("cpy", temp1, temp2, "")
		p[0].append(tup)
	else :
		temp2 = p[3][1]
		p[0].append(("cpy", temp1, temp2, ""))
    
## Change made ....
def p_declarator_01_1(p):
	'''declarator : direct_declarator COMMA declarator'''
	p[0] = []
	if(type(p[1]) == list) :
		p[0].extend(p[1])
	if(type(p[1]) == str):
		p[0].append(("cpy", "@@" + p[1], "[RAND]", ""))	
	if(type(p[3]) == list) :
		p[0].extend(p[3])
		

def p_declarator_01_2(p):
	'''declarator : expression ASSIGN expression COMMA declarator'''
	p[0] = [];
	
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	# for x = y ... got the x
	
	if(type(p[3]) == list) :
		p[0].extend(p[3])
		temp2 = p[3][-1][1]
		tup = ("cpy", temp1, temp2, "")
		p[0].append(tup)
	else :
		temp2 = p[3][1]
		p[0].append(("cpy", temp1, temp2, ""))        
	if(type(p[5]) == list):
		p[0].extend(p[5])

def p_declarator_02(p):
	'''declarator : ASTERISK declarator'''

def p_direct_declarator_01(p):
    '''direct_declarator : ID'''
    p[0] = p[1]
    
def p_direct_declarator_02(p):
    '''direct_declarator : direct_declarator LPAREN parameter_type_list RPAREN'''
    p[0] = p[3]
    global proc_name
    proc_name = p[1]

def p_direct_declarator_03(p):
    '''direct_declarator : direct_declarator LPAREN RPAREN'''
    p[0] = []
    global proc_name
    proc_name = p[1]
    
def p_parameter_type_list_01(p):
    '''parameter_type_list : parameter_list'''
    p[0] = p[1]

#def p_parameter_type_list_02(p):
#    '''parameter_type_list : parameter_list COMMA ELLIPSIS'''
#    p[0] = []

def p_parameter_list_01(p):
	'''parameter_list : type_specifier expression'''
	if type(p[2]) == tuple:
		p[0] = [("cpy", p[2][1], "[MEM]", "")]
	else:
		p[0] = p[2]

def p_parameter_list_02(p):
	'''parameter_list : type_specifier expression COMMA parameter_list'''
	p[0] = []
	if(type(p[2]) == list) :
		p[0].extend(p[2])
	else:
		p[0] = [("cpy", p[2][1], "[MEM]", "")]
			
	if(type(p[4]) == list) :
		p[0].extend(p[4])

def p_parameter_declaration(p):
    '''parameter_declaration : type_specifier declarator'''
    # NOTE: this is the same code as p_declaration_01!
    p_declaration_01(p)

def p_compound_statement_01(p):
	'''compound_statement : LBRACE declaration_list_opt statement_list RBRACE'''
	if type(p[2]) == list :
		p[0] = p[2]
	else :
		p[0] = []
	
	if type(p[3]) == list:
		p[0].extend(p[3])
	pass

def p_compound_statement_02(p):
    '''compound_statement : LBRACE declaration_list_opt RBRACE'''
    p[0] = p[2]

def p_statement_list_02(p):
    '''statement_list : statement'''
    p[0] = p[1]
    pass
    
def p_statement_list_03(p):
	'''statement_list : statement statement_list '''
	p[0] = p[1]
	if type(p[1]) == list and type(p[2]) == list :
		p[0].extend(p[2])
	pass
    
# End of statement list ..

# Statements of a statement list ...
def p_statement(p):
    '''statement : compound_statement
                 | jump_statement
                 | iteration_statement                 | selection_statement				 | expression_statement
				 | label				 '''
    p[0] = p[1]
    pass

def p_label(p):
	'''label : ID COLON'''
	global label_count
	qwe = re.compile('L[0-9]+')
	a = qwe.match(p[1])
	if a:
		ttt =  a.group();
		label = int(ttt[1:])
		if label > label_count:
			label_count = label + 1;
	p[0] = [(p[1] + ":", "", "", "")]
	pass
    
def p_expression_statement(p):
    '''expression_statement : expression SEMICOLON'''
    p[0] = p[1]
    
def p_expresssion_01(p):
	'''expression : binary_expression
				| unary_expression
				| primary_expression
				| postfix_expression '''
	p[0] = p[1]

def p_binary_expression_01(p):
	'''binary_expression : expression ASSIGN expression '''
	p[0] = [];
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	# for x = y ... got the x
	
	if(type(p[3]) == list) :
		p[0].extend(p[3])
		temp2 = p[3][-1][1]
		tup = ("cpy", temp1, temp2, "")
		p[0].append(tup)
	else :
		temp2 = p[3][1]
		p[0].append(("cpy", temp1, temp2, ""))
		
	pass

def p_binary_expression_02(p):
	'''binary_expression : expression DOUBLE_PIPE expression '''
	global temp_count;
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	if(type(p[3]) == list) :
		p[0].extend(p[3]);
		temp2 = p[3][-1][1];
	else :
		temp2 = p[3][1]
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	p[0].append(('and', temp3, temp1, temp2))
	pass

def p_binary_expression_03(p):
	'''binary_expression : expression DOUBLE_AMPERSAND expression '''
	global temp_count;
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	if(type(p[3]) == list) :
		p[0].extend(p[3]);
		temp2 = p[3][-1][1];
	else :
		temp2 = p[3][1]
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	p[0].append(('ior', temp3, temp1, temp2))
	pass

def p_binary_expression_04(p):
	'''binary_expression : expression EQ expression '''
	global temp_count;
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	if(type(p[3]) == list) :
		p[0].extend(p[3]);
		temp2 = p[3][-1][1];
	else :
		temp2 = p[3][1]
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	p[0].append(('seq', temp3, temp1, temp2))

	pass

def p_binary_expression_05(p):
	'''binary_expression : expression NOT_EQ expression '''
	global temp_count;
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	if(type(p[3]) == list) :
		p[0].extend(p[3]);
		temp2 = p[3][-1][1];
	else :
		temp2 = p[3][1]
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	p[0].append(('sne', temp3, temp1, temp2))

def p_binary_expression_06(p):
	'''binary_expression : expression LESS expression '''
	global temp_count;
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	if(type(p[3]) == list) :
		p[0].extend(p[3]);
		temp2 = p[3][-1][1];
	else :
		temp2 = p[3][1]
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	p[0].append(('sl', temp3, temp1, temp2))
	pass

def p_binary_expression_07(p):
	'''binary_expression : expression GREATER expression '''
	global temp_count;
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	if(type(p[3]) == list) :
		p[0].extend(p[3]);
		temp2 = p[3][-1][1];
	else :
		temp2 = p[3][1]
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	p[0].append(('sl', temp3, temp2, temp1))
	pass
	
def p_binary_expression_08(p):
	'''binary_expression : expression LESS_EQ expression '''
	global temp_count;
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	if(type(p[3]) == list) :
		p[0].extend(p[3]);
		temp2 = p[3][-1][1];
	else :
		temp2 = p[3][1]
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	p[0].append(('sle', temp3, temp1, temp2))
	pass

def p_binary_expression_09(p):
	'''binary_expression : expression GREATER_EQ expression '''
	global temp_count;
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	if(type(p[3]) == list) :
		p[0].extend(p[3]);
		temp2 = p[3][-1][1];
	else :
		temp2 = p[3][1]
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	p[0].append(('sle', temp3, temp2, temp1))
	pass

def p_binary_expression_10(p):
	'''binary_expression : expression PLUS expression '''
	global temp_count;
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	if(type(p[3]) == list) :
		p[0].extend(p[3]);
		temp2 = p[3][-1][1];
	else :
		temp2 = p[3][1]
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	p[0].append(('add', temp3, temp1, temp2))
	pass

def p_binary_expression_11(p):
	'''binary_expression : expression MINUS expression '''
	global temp_count;
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	if(type(p[3]) == list) :
		p[0].extend(p[3]);
		temp2 = p[3][-1][1];
	else :
		temp2 = p[3][1]
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	p[0].append(('sub', temp3, temp1, temp2))
	pass

def p_binary_expression_12(p):
	'''binary_expression : expression ASTERISK expression '''
	global temp_count;
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	if(type(p[3]) == list) :
		p[0].extend(p[3]);
		temp2 = p[3][-1][1];
	else :
		temp2 = p[3][1]
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	p[0].append(('mul', temp3, temp1, temp2))
	pass

def p_binary_expression_13(p):
	'''binary_expression : expression DIV expression '''
	global temp_count;
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	if(type(p[3]) == list) :
		p[0].extend(p[3]);
		temp2 = p[3][-1][1];
	else :
		temp2 = p[3][1]
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	p[0].append(('div', temp3, temp1, temp2))
	pass

def p_binary_expression_14(p):
	'''binary_expression : expression EQ_PLUS expression '''
	global temp_count;
	p[0] = []
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	temp4 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	if(type(p[3]) == list) :
		p[0].extend(p[3]);
		temp2 = p[3][-1][1];
	else :
		temp2 = p[3][1]	
	p[0].append(("add", temp3, temp1, temp2))
	p[0].append(("cpy", temp1, temp3, ""))
	pass

def p_binary_expression_15(p):
	'''binary_expression : expression EQ_MINUS expression '''
	global temp_count;
	p[0] = []
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	temp4 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	if(type(p[3]) == list) :
		p[0].extend(p[3]);
		temp2 = p[3][-1][1];
	else :
		temp2 = p[3][1]	
	p[0].append(("sub", temp3, temp1, temp2))
	p[0].append(("cpy", temp1, temp3, ""))
	pass

def p_binary_expression_16(p):
	'''binary_expression : expression EQ_TIMES expression '''
	global temp_count;
	p[0] = []
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	temp4 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	if(type(p[3]) == list) :
		p[0].extend(p[3]);
		temp2 = p[3][-1][1];
	else :
		temp2 = p[3][1]	
	p[0].append(("mul", temp3, temp1, temp2))
	p[0].append(("cpy", temp1, temp3, ""))
	pass

def p_binary_expression_17(p):
	'''binary_expression : expression EQ_DIV expression '''
	global temp_count;
	p[0] = []
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	temp4 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	if(type(p[1]) == list) :
		p[0] = p[1];
		temp1 = p[1][-1][1];
	else :
		p[0] = []
		temp1 = p[1][1]
	if(type(p[3]) == list) :
		p[0].extend(p[3]);
		temp2 = p[3][-1][1];
	else :
		temp2 = p[3][1]	
	p[0].append(("div", temp3, temp1, temp2))
	p[0].append(("cpy", temp1, temp3, ""))
	pass		
def p_unary_expression_01(p):
	'''unary_expression : PLUS expression ''' 
	p[0] = p[2]
	pass

#Added for i++ and ++i	
def p_unary_expression_02(p):
	'''unary_expression : DOUBLE_PLUS primary_expression ''' 
	global temp_count;
	p[0] = []
	temp1 = p[2][1]
	temp2 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	
	p[0].append(("ldc", temp2, "1", ""))
	
	p[0].append(("add", temp3, temp1, temp2))
	p[0].append(("cpy", temp1, temp3, ""))
	pass	

def p_unary_expression_03(p):
	'''unary_expression : primary_expression DOUBLE_PLUS''' 
	global temp_count;
	p[0] = []
	temp2 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	
	p[0].append(("ldc", temp2, "1", ""))
	
	p[0].append(("add", temp3, p[1][1], temp2))
	p[0].append(("cpy", p[1][1], temp3, ""))
	pass
##
def p_unary_expression_021(p):
	'''unary_expression : DOUBLE_MINUS primary_expression ''' 
	global temp_count;
	p[0] = []
	temp1 = p[2][1]
	temp2 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	
	p[0].append(("ldc", temp2, "1", ""))
	
	p[0].append(("sub", temp3, temp1, temp2))
	p[0].append(("cpy", temp1, temp3, ""))
	pass	

def p_unary_expression_031(p):
	'''unary_expression : primary_expression DOUBLE_MINUS''' 
	global temp_count;
	p[0] = []
	temp2 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	
	p[0].append(("ldc", temp2, "1", ""))
	
	p[0].append(("sub", temp3, p[1][1], temp2))
	p[0].append(("cpy", p[1][1], temp3, ""))
	pass
def p_unary_expression_04(p):
	'''unary_expression : MINUS expression %prec UMINUS'''
	global temp_count;
	if(type(p[2]) == list) :
		p[0] = p[2];
		temp1 = p[2][-1][1];
	else :
		p[0] = []
		temp1 = p[2][1]
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	p[0].append(('neg', temp3, temp1, ""))
	pass
	
def p_unary_expression_05(p):
	'''unary_expression : ASTERISK expression %prec UASTERISK'''
	global temp_count;
	if(type(p[2]) == list) :
		p[0] = p[2];
		temp1 = p[2][-1][1];
	else :
		p[0] = []
		temp1 = p[2][1]
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	p[0].append(('load', temp3, temp1, ""))	
	pass
	
def p_unary_expression_06(p):
	'''unary_expression : EXCLAMATION expression %prec UEXCLAMATION'''		
	global temp_count;
	if(type(p[2]) == list) :
		p[0] = p[2];
		temp1 = p[2][-1][1];
	else :
		p[0] = []
		temp1 = p[2][1]
	temp3 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	p[0].append(('not', temp3, temp1, ""))	

def p_unary_expression_061(p): #Temp
	'''unary_expression : AMPERSAND expression %prec AMPERSAND'''
	p[0] = p[2]
	pass	
#def p_postfix_expression_01(p):
#    '''postfix_expression : primary_expression'''
#    t[0] = t[1]

def p_postfix_expression_02(p):
	'''postfix_expression : primary_expression LPAREN argument_expression_list RPAREN'''
	global temp_count;
	temp1 = "$$t" + str(temp_count) # A dirty hack :)
	temp2 = "$$*t" + str(temp_count) # A dirty hack :)
	
	temp_count = temp_count + 1;
	# Need to work on this TODO
	p[0] = [('ldc', temp1, "&" + p[1][1][2:], "0")] # The 2: is to remove $$   
		
	temp_list = ["call", "",  temp2]
	if(type(p[3]) == list):
		for x in p[3]:
			if (x[0][:2] == "__"):
				continue;
			p[0].append(x)
		for i in p[3]:
			j = i[1]
			temp_list.append(j)
		
		temp_tuple = tuple(temp_list)
#		p[0].append(("call", temp2, '(' + t_str +')', ""))
		p[0].append(temp_tuple)
    	
		
	pass

def p_postfix_expression_03(p):
	'''postfix_expression : primary_expression LPAREN RPAREN'''
	global temp_count;
	temp1 = "$$t" + str(temp_count)
	temp_count = temp_count + 1;
	# Need to work on this TODO
	p[0] = [('ldc', temp1, "&" + p[1][1][2:], "0")]    
		
	p[0].append(("call", "", '*' + temp1, "()"))
	pass
    
#def p_postfix_expression_04(p):
#    '''postfix_expression : postfix_expression LBRACKET expression RBRACKET'''
#    pass
    
def p_argument_expression_list_01(p):
    '''argument_expression_list : expression'''
    p[0] = p[1]
    pass
    
def p_argument_expression_list_02(p):
    '''argument_expression_list :  expression COMMA argument_expression_list'''
    p[0] = [];
    if (type(p[1]) == list):
    	p[0].extend(p[1]);
    else:
    	p[0].append(p[1])
    if (type(p[3]) == list):
    	p[0].extend(p[3]);
    else:
    	p[0].append(p[3])	
    pass
    
def p_primary_expression_01(p):
    '''primary_expression : ID'''
    p[0] = ("__ID", "@@" + p[1], "","")
    pass

def p_primary_expression_02(p):
    '''primary_expression : INUMBER'''
    global temp_count;
    temp1 = "$$t" + str(temp_count);
    temp_count = temp_count + 1;
    p[0] = [("ldc", temp1, p[1], "")]
    pass
    
def p_primary_expression_03(p):
    '''primary_expression : FNUMBER'''
    global temp_count;
    temp1 = "$$t" + str(temp_count);
    temp_count = temp_count + 1;
    p[0] = [("ldc", temp1, p[1], "")]
    pass
    
def p_primary_expression_04(p):
	'''primary_expression : CHARACTER'''
	p[0] = ("__CONST", p[1], "","")
	pass

def p_primary_expression_05(p):
    '''primary_expression : string_literal'''
    p[0] = p[1]
    pass
    
def p_primary_expression_06(p):
    '''primary_expression : LPAREN expression RPAREN'''
    p[0] = p[2]
    pass
    
def p_string_literal_01(p):
    '''string_literal : STRING'''
    global string_count;
    global temp_count;
    temp1 = "$$t" + str(temp_count);
    temp_count = temp_count + 1;
    temp_str = "&__tmp_string_" + str(string_count)
    
    string_count = string_count + 1
    p[0] = [("ldc", temp1, temp_str, "0")]
    pass
    
#def p_string_literal_02(p):
#    '''string_literal : string_literal STRING'''
#    pass
    
def p_jump_statement_01(p):
    '''jump_statement : RETURN SEMICOLON'''
    p[0] = [("ret", "", "", "")]
    pass
    
def p_jump_statement_02(p):
    '''jump_statement : RETURN expression SEMICOLON'''
    p[0] = []
    if type(p[2]) == list :
    	p[0].extend(p[2])
    	ret = p[2][-1][1]
    else :
    	ret = p[2][1]
    p[0].append(("ret", ret, "", ""))	
    pass
    
def p_jump_statement_03(p):
	'''jump_statement : BREAK SEMICOLON'''
 	p[0] = [("~~break", "", "", "")]  
	pass
    
def p_jump_statement_04(p):
	'''jump_statement : CONTINUE SEMICOLON'''
	p[0] = [("~~continue", "", "", "")]  
	pass

def p_jump_statement_05(p) :
	'''jump_statement : GOTO ID SEMICOLON'''
	p[0] =  [("jmp", p[2], "", "")]
	pass
	    
def p_iteration_statement_01(p):
	'''iteration_statement : WHILE LPAREN expression RPAREN statement'''
	global label_count;
	p[0] = []
	temp_lab1 = "~~L" + str(label_count) # For begining of loop
	label_count = label_count + 1
	
	p[0].append((temp_lab1 + ":", "", "", ""))	
	
	temp_lab2 = "~~L" + str(label_count) # For end of loop
	label_count = label_count + 1
	if type(p[3]) == list:
		p[0].extend(p[3])
		cond = p[3][-1][1];
	else :
		cond = "Issues"
	p[0].append(("bfls", cond, "", temp_lab2))
	
	# Searching for break and continue
	if(type(p[5]) == list) :
		for i in range(len(p[5])) :
			if(p[5][i][0] == "~~break") :
				p[5][i] = ("jmp", temp_lab2, "", "")
			if(p[5][i][0] == "~~continue") :
				p[5][i] = ("jmp", temp_lab1, "", "")
		p[0].extend(p[5])

	p[0].append(("jmp", temp_lab1, "", ""));
	p[0].append((temp_lab2 + ":", "", "", ""));		
	
	pass

def p_iteration_statement_02(p):
	'''iteration_statement : DO statement WHILE LPAREN expression RPAREN SEMICOLON'''
	global label_count;
	is_continue = 0;
	is_break = 0;
	p[0] = []
	temp_lab1 = "~~L" + str(label_count) # For begining of loop
	label_count = label_count + 1
	p[0].append((temp_lab1 + ":", "", "", ""))	
	temp_lab2 = "~~L" + str(label_count) # For end of loop
	label_count = label_count + 1
	temp_lab3 = ""
	
	# Searching for break and continue
	
	if(type(p[2]) == list) :
		for i in range(len(p[2])) :
			if(p[2][i][0] == "~~break") :
				p[2][i] = ("jmp", temp_lab2, "", "")
				is_break = 1;
			if(p[2][i][0] == "~~continue") :
				temp_lab3 = "~~L" + str(label_count) # check for continue 
				label_count = label_count + 1
				p[2][i] = ("jmp", temp_lab3, "", "")
				is_continue = 1;
		p[0].extend(p[2])
	
	if is_continue :
		p[0].append((temp_lab3 + ":", "", "", ""));		
	if type(p[5]) == list:
		p[0].extend(p[5])
		cond = p[5][-1][1];
	else :
		cond = "Issues"
	p[0].append(("btru", cond, "", temp_lab1))
	if is_break:
		p[0].append((temp_lab2 + ":", "", "", ""));		
	
	pass
    
def p_iteration_statement_03(p):
	'''iteration_statement : FOR LPAREN expression_statement expression_statement expression RPAREN statement'''
	global label_count;
	
	p[0] = []
	if type(p[3]) == list:
		p[0].extend(p[3])
	temp_lab1 = "~~L" + str(label_count) # For begining of loop
	label_count = label_count + 1
	temp_lab2 = "~~L" + str(label_count) # For end of loop
	label_count = label_count + 1
	temp_lab3 = ""
	
	p[0].append((temp_lab1 + ":", "", "", ""))
	if type(p[4]) == list :
		p[0].extend(p[4])
		cond = p[4][-1][1];
	else :
		cond = "Issues"
	p[0].append(("bfls", cond, "", temp_lab2))
	
	continue_present = 0
	
	# Searching for break and continue
	if(type(p[7]) == list) :
		for i in range(len(p[7])) :
			if(p[7][i][0] == "~~break") :
				p[7][i] = ("jmp", temp_lab2, "", "")
			if(p[7][i][0] == "~~continue") :
				continue_present = 1
				temp_lab3 = "~~L" + str(label_count) # For induction in loop
				label_count = label_count + 1
				p[7][i] = ("jmp", temp_lab3, "", "")
		p[0].extend(p[7])
	
	if(continue_present):
		p[0].append((temp_lab3 + ":", "", "", ""))
	
	if(type(p[5]) == list) :
		p[0].extend(p[5])
	
	p[0].append(("jmp", temp_lab1, "", ""));
	p[0].append((temp_lab2 + ":", "", "", ""));		
	
	pass
    
def p_selection_statement_01(p):
	'''selection_statement : IF LPAREN expression RPAREN statement'''
	global label_count;
	
	if type(p[3]) == list :
		p[0] = p[3]
		cond = p[3][-1][1];
	else :
		p[0] = []
		cond = "Issues"
	
	temp_lab = "~~L" + str(label_count)
	label_count = label_count + 1
	p[0].append(("bfls", cond, "", temp_lab))
	if type(p[5]) == list :
		p[0].extend(p[5])
	
	p[0].append((temp_lab + ":", "", "", ""))	
	pass
    
def p_selection_statement_02(p):
	'''selection_statement : IF LPAREN expression RPAREN statement ELSE statement'''
	global label_count;
	
	if type(p[3]) == list :
		p[0] = p[3]
		cond = p[3][-1][1];
	else :
		p[0] = []
		cond = "Issues"
	
	temp_lab = "~~L" + str(label_count)
	label_count = label_count + 1
	p[0].append(("bfls", cond, "", temp_lab))
	if type(p[5]) == list :
		p[0].extend(p[5])
	
	temp_lab2 = "~~L" + str(label_count)
	label_count = label_count + 1
	p[0].append(("jmp", temp_lab2, "", ""))
	p[0].append((temp_lab + ":", "", "", ""))	
	if type(p[7]) == list :
		p[0].extend(p[7])
	p[0].append((temp_lab2 + ":", "", "", ""))
	pass
    
def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print "Syntax Error present in the code ... Please check it", p
    #raise ParseError()


#  ---------------------------------------------------------------
#  End of cparse.py
#  -----------------
def get_proc_name():
	return proc_name

def run_parser():
	yacc.yacc()
	import sys
	file = open(sys.argv[1])
	lines = file.readlines()
	file.close()
	strings = ""
	for i in lines:
		strings += i
	#lex.input(strings)
	yacc.parse(strings)
	
def write_file():
	line_number = 1;
	f = open('inter_suif.txt', 'w')
	for i in converted_list:
		
		string = ""
		string = string + "[" + str(line_number) + "]:\t"
		line_number = line_number + 1;
		string = string + i[0] + "\t\t" + i[1]	
		if i[0] == "call":
			string = string + " ( ";
			for j in range(2, len(i)):
				if j !=2:
					string = string + " , "
				string = string + i[j];
			string = string + " )\n"
			f.write(string)
			continue;	
		if len(i) == 4 :
			
			if i[2] != "":
				string = string + " = " + i[2] 
				if i[3] != "":
					if i[0] == "ldc":
						string = string + " + " + i[3]
					else:	
						string = string + " , " + i[3]
			elif i[3] != "":
				string = string + " , " + i[3]
			string = string + "\n"
			f.write(string)
		else :
			#print "-------------" , i;
			pass
			 
				
    
if(__name__ == "__main__"):
	run_parser()
	write_file(converted_list)
	
