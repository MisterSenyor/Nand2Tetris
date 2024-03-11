"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream, symbol_table: SymbolTable, vm_writer: VMWriter) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.input = input_stream
        self.output = output_stream
        self.indent_count = 0
        self.symbol_table = symbol_table
        self.vm_writer = vm_writer

    def is_class_var_dec(self):
        return self.input.token_type() == "KEYWORD" and self.input.keyword() in ["STATIC", "FIELD"]

    def is_subroutine_dec(self):
        return self.input.token_type() == "KEYWORD" and self.input.keyword() in ["CONSTRUCTOR", "FUNCTION", "METHOD"]

    def is_comma(self):
        return self.input.token_type() == "SYMBOL" and self.input.symbol() == ","

    def is_opening_bracket(self):
        return self.input.token_type() == "SYMBOL" and self.input.symbol() == "("

    def is_closing_bracket(self):
        return self.input.token_type() == "SYMBOL" and self.input.symbol() == ")"

    def is_curly_closing_bracket(self):
        return self.input.token_type() == "SYMBOL" and self.input.symbol() == "}"

    def is_semicolon(self):
        return self.input.token_type() == "SYMBOL" and self.input.symbol() == ";"

    def is_dot(self):
        return self.input.token_type() == "SYMBOL" and self.input.symbol() == "."

    def is_square_opening_bracket(self):
        return self.input.token_type() == "SYMBOL" and self.input.symbol() == "["
    
    def is_square_closing_bracket(self):
        return self.input.token_type() == "SYMBOL" and self.input.symbol() == "]"

    def is_var_dec(self):
        return self.input.token_type() == "KEYWORD" and self.input.keyword() == "VAR"
    
    def is_let_statement(self):
        return self.input.token_type() == "KEYWORD" and self.input.keyword() == "LET"

    def is_if_statement(self):
        return self.input.token_type() == "KEYWORD" and self.input.keyword() == "IF"

    def is_while_statement(self):
        return self.input.token_type() == "KEYWORD" and self.input.keyword() == "WHILE"

    def is_do_statement(self):
        return self.input.token_type() == "KEYWORD" and self.input.keyword() == "DO"

    def is_return_statement(self):
        return self.input.token_type() == "KEYWORD" and self.input.keyword() == "RETURN"

    def is_else_clause(self):
        return self.input.token_type() == "KEYWORD" and self.input.keyword() == "ELSE"

    def is_op(self):
        return self.input.token_type() == "SYMBOL" and self.input.symbol() in '+-*/&|<>='

    def is_unary_op(self):
        return self.input.token_type() == "SYMBOL" and self.input.symbol() in '-~^#'

    def is_identifier(self):
        return self.input.token_type() == "IDENTIFIER"

    def write_line(self, xml_header, xml_content):
        self.output.write(self.indent_count * '  ' + f"<{xml_header}> {xml_content} </{xml_header}>\n")

    def write_current_token(self):
        token_type = self.input.token_type()
        if token_type == "KEYWORD":
            keyword = self.input.keyword()
            self.write_line('keyword', keyword.lower())
        elif token_type == "SYMBOL":
            symbol = self.input.symbol()
            if symbol == '<':
                symbol = '&lt;'
            elif symbol == '>':
                symbol = '&gt;'
            elif symbol == '&':
                symbol = '&amp;'
            self.write_line('symbol', symbol)
        elif token_type == 'IDENTIFIER':
            identifier = self.input.identifier()
            self.write_line('identifier', identifier)
        elif token_type == 'INT_CONST':
            int_val = self.input.int_val()
            int_val = str(self.input.int_val())
            self.write_line('integerConstant', int_val)
        elif token_type == 'STRING_CONST':
            string_val = self.input.string_val()
            string_val = string_val[1:-1]
            self.write_line('stringConstant', string_val)

    def write_open(self, xml_header: str):
        self.output.write(self.indent_count * '  ' + f"<{xml_header}>\n")
        self.indent_count += 1
    
    def write_close(self, xml_header: str):
        self.indent_count -= 1
        self.output.write(self.indent_count * '  ' + f"</{xml_header}>\n")

    def read_write_tokens(self, count: int):
        for _ in range(count):
            self.write_current_token()
            self.check_advance()
    
    def check_advance(self):
        if self.input.has_more_tokens():
            self.input.advance()

    def compile_class(self) -> None:
        self.check_advance()
        self.write_open("class")
        self.read_write_tokens(3)  # 'class' className '{'
        while self.is_class_var_dec():
            self.compile_class_var_dec()
        while self.is_subroutine_dec():
            self.compile_subroutine()
        self.read_write_tokens(1)  # '}'
        self.write_close("class")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        self.write_open("classVarDec")
        self.read_write_tokens(3)  # ('static' | 'field') type varName
        while self.is_comma():
            self.read_write_tokens(2)  # ',' varName
        self.read_write_tokens(1)  # ;
        self.write_close("classVarDec")


    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        self.write_open("subroutineDec")
        self.read_write_tokens(4)  # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '('
        self.compile_parameter_list()
        self.read_write_tokens(1)  # ')'
        self.compile_subroutine_body()
        self.write_close("subroutineDec")
    
    def compile_subroutine_body(self) -> None:
        self.write_open("subroutineBody")
        self.read_write_tokens(1)  # '{'
        while self.is_var_dec():
            self.compile_var_dec()
        self.compile_statements()
        self.read_write_tokens(1)  # '}'
        self.write_close("subroutineBody")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        self.write_open("parameterList")
        if not self.is_closing_bracket():
            self.read_write_tokens(2)  # type varName
            while self.is_comma():
                self.read_write_tokens(3)  # ',' type varName
        self.write_close("parameterList")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self.write_open("varDec")
        self.read_write_tokens(3)  # 'var' type varName
        while self.is_comma():
            self.read_write_tokens(2)  # ',' varName
        self.read_write_tokens(1)  # ';'
        self.write_close("varDec")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        self.write_open("statements")
        while not self.is_curly_closing_bracket():
            if self.is_let_statement():
                self.compile_let()
            if self.is_if_statement():
                self.compile_if()
            if self.is_while_statement():
                self.compile_while()
            if self.is_do_statement():
                self.compile_do()
            if self.is_return_statement():
                self.compile_return()
        self.write_close("statements")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.write_open("doStatement")
        self.read_write_tokens(1)  # 'do'
        self.compile_subroutine_call()
        self.read_write_tokens(1)  # ';'
        self.write_close("doStatement")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        self.write_open("letStatement")
        self.read_write_tokens(2)  # 'let' varName
        if self.is_square_opening_bracket():
            self.read_write_tokens(1)  # '['
            self.compile_expression()
            self.read_write_tokens(1)  # ']'
        self.read_write_tokens(1)  # '='
        self.compile_expression()
        self.read_write_tokens(1)  # ';'
        self.write_close("letStatement")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.write_open("whileStatement")
        self.read_write_tokens(2)  # 'while' '('
        self.compile_expression()
        self.read_write_tokens(2)  # ')' '{'
        self.compile_statements()
        self.read_write_tokens(1)  # '}
        self.write_close("whileStatement")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.write_open("returnStatement")
        self.read_write_tokens(1)  # 'return'
        if not self.is_semicolon():
            self.compile_expression()
        self.read_write_tokens(1)  # ';'
        self.write_close("returnStatement")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.write_open("ifStatement")
        self.read_write_tokens(2)  # 'if' '('
        self.compile_expression()
        self.read_write_tokens(2)  # ')' '{'
        self.compile_statements()
        self.read_write_tokens(1)  # '}'
        if self.is_else_clause():
            self.read_write_tokens(2)  # 'else' '{'
            self.compile_statements()
            self.read_write_tokens(1)  # '}'
        self.write_close("ifStatement")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        self.write_open("expression")
        self.compile_term()
        while self.is_op():
            self.read_write_tokens(1)  # op
            self.compile_term()
            self.write_current_token()
            self.check_advance()
        self.write_close("expression")

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        self.write_open("term")
        if self.is_unary_op():
            self.read_write_tokens(1)  # op
            self.compile_term()
        elif self.is_opening_bracket():
            self.read_write_tokens(1)  # '('
            self.compile_expression()
            self.read_write_tokens(1)  # ')'
        elif self.is_identifier():
            self.read_write_tokens(1)  # identifier
            if self.is_square_opening_bracket():
                self.read_write_tokens(1)  # '['
                self.compile_expression()
                self.read_write_tokens(1)  # ']'
            elif self.is_subroutine_call_second_token():
                self.compile_subroutine_call_second_token()
        else:
            self.read_write_tokens(1)  # constant (int or string or keyword)
        self.write_close("term")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        self.write_open("expressionList")
        if not self.is_closing_bracket():
            self.compile_expression()
            while self.is_comma():
                self.read_write_tokens(1)  # ','
                self.compile_expression()
        self.write_close("expressionList")


    def is_subroutine_call_second_token(self):
        return self.is_opening_bracket() or self.is_dot()


    def compile_subroutine_call_second_token(self):
        if self.is_dot():
            self.read_write_tokens(2)  # '.' identifier    
        self.read_write_tokens(1)  # '('
        self.compile_expression_list()
        self.read_write_tokens(1)  # ')'


    def compile_subroutine_call(self):
        # no open & closing brackets!
        self.read_write_tokens(1)  # identifier
        self.compile_subroutine_call_second_token()
