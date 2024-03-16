"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from SymbolTable import SymbolTable
from VMWriter import VMWriter

ops = {"+" : "ADD", 
    "-" : "SUB", 
    "-" : "NEG",
    "=" : "EQ", 
    ">" : "GT", 
    "<" : "LT", 
    "&" : "AND", 
    "|" : "OR", 
    "~" : "NOT", 
    "^" : "SHIFTLEFT", 
    "#" : "SHIFTRIGHT"}



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
        self.label_count = 0
        self.class_name = ''
    
    def get_new_label(self):
        label = 'label' + str(self.label_count)
        self.label_count += 1
        return label

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
    
    def is_string(self):
        return self.input.token_type() == "STRING_CONST"

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
    
    def read_tokens(self, count: int):
        out = ""
        for _ in range(count):
            token_type = self.input.token_type()
            if token_type == "KEYWORD":
                text = self.input.keyword()
            elif token_type == "SYMBOL":
                text = self.input.symbol()
            elif token_type == 'IDENTIFIER':
                text = self.input.identifier()
            elif token_type == 'INT_CONST':
                int_val = self.input.int_val()
                text = str(self.input.int_val())
            elif token_type == 'STRING_CONST':
                text = self.input.string_val()
            else:
                text = self.input.symbol()
            out += text
            self.check_advance()

        return out
        
    
    def check_advance(self):
        if self.input.has_more_tokens():
            self.input.advance()

    def compile_class(self) -> None:
        self.check_advance()
        self.read_tokens(1)  # 'class'
        self.class_name = self.read_tokens(1)  # className
        self.read_tokens(1)  # '{'
        while self.is_class_var_dec():
            self.compile_class_var_dec()
        while self.is_subroutine_dec():
            self.compile_subroutine()
        self.read_tokens(1)  # '}'
    
    def get_current_type(self):
        if self.input.token_type() == "KEYWORD":
            return self.input.keyword()
        else:
            return self.input.identifier()

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!

        kind = self.read_tokens(1)  # ('static' | 'field')

        var_type = self.get_current_type()
        self.read_tokens(1)  # type

        var_name = self.read_tokens(1)  # varName

        self.symbol_table.define(var_name, var_type, kind)

        while self.is_comma():
            self.read_tokens(1)  # ',' 

            var_name = self.read_tokens(1)  # varName

            self.symbol_table.define(var_name, var_type, kind)
        self.read_tokens(1)  # ;


    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        self.symbol_table.start_subroutine()
        subroutine_type = self.read_tokens(1)  # ('constructor' | 'function' | 'method')
        self.read_tokens(1)  # ('void' | type)
        subroutine_name = self.read_tokens(1)  # subroutineName 


        if subroutine_type == "method":
            self.vm_writer.write_push("ARG", 0)
            self.vm_writer.write_pop("POINTER", 0)
            self.symbol_table.define("this", self.class_name, "ARG")
        elif subroutine_type == "constructor":
            self.symbol_table.define("this", self.class_name, "ARG")
            self.vm_writer.write_push("CONST", self.symbol_table.var_count("FIELD"))
            self.vm_writer.write_call("Memory.alloc", 1)
            self.vm_writer.write_pop("POINTER", 0)


        self.read_tokens(1)  # '('

        self.compile_parameter_list()
        self.read_tokens(1)  # ')'

        num_locals = 0
        self.read_tokens(1)  # '{'
        while self.is_var_dec():
            num_locals += self.compile_var_dec()

        self.vm_writer.write_function(self.class_name + '.' + subroutine_name, num_locals)

        self.compile_statements()
        self.read_tokens(1)  # '}'

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        if not self.is_closing_bracket():
            var_type = self.get_current_type()
            self.read_tokens(1)  # type

            var_name = self.read_tokens(1)  # varName

            self.symbol_table.define(var_name, var_type, 'ARG')
            while self.is_comma():
                self.read_tokens(1)  # ','
                var_type = self.read_tokens(1)  # type

                var_name = self.read_tokens(1)  # varName

                self.symbol_table.define(var_name, var_type, 'ARG')

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        n_vars = 1
        self.read_tokens(1)  # 'var'
        var_type = self.get_current_type()
        self.read_tokens(1)  # type
        var_name = self.read_tokens(1)  # varName
        self.symbol_table.define(var_name, var_type, 'VAR')

        while self.is_comma():
            n_vars += 1
            self.read_tokens(1)  # ','
            var_name = self.read_tokens(1)  # varName
            self.symbol_table.define(var_name, var_type, 'VAR')
        self.read_tokens(1)  # ';'
        
        return n_vars

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
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

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.read_tokens(1)  # 'do'
        self.compile_expression()
        self.vm_writer.write_pop('TEMP', 0)
        self.read_tokens(1)  # ';'

    def get_segment_index_pair(self, var_name: str):
        
        segment = self.symbol_table.kind_of(var_name)
        if segment == "VAR":
            segment = "local"
        return segment, self.symbol_table.index_of(var_name)

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        self.check_advance()  # 'let'
        
        var_name = self.read_tokens(1)  # varName
        print(f"{var_name=}")
        segment, index = self.get_segment_index_pair(var_name)
        if segment is None or index is None:
            raise ValueError(f"{segment=}, {index=}, {var_name=}")

        if self.is_square_opening_bracket():
            self.vm_writer.write_push(segment, index)

            self.read_tokens(1)  # '['
            self.compile_expression()
            self.read_tokens(1)  # ']'

            self.vm_writer.write_arithmetic('ADD')

            self.read_tokens(1)  # '='
            self.compile_expression()
            self.read_tokens(1)  # ';'

            self.vm_writer.write_pop('TEMP', 0)
            self.vm_writer.write_pop('POINTER', 1)
            self.vm_writer.write_push('TEMP', 0)
            self.vm_writer.write_pop('THAT', 0)
        else:
            self.read_tokens(1)  # '='
            self.compile_expression()
            self.read_tokens(1)  # ';'

            self.vm_writer.write_pop(segment, index)
        
        

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        loop_label = self.get_new_label()
        end_label = self.get_new_label()

        self.vm_writer.write_label(loop_label)

        self.read_tokens(2)  # 'while' '('
        self.compile_expression()
        self.vm_writer.write_arithmetic('NOT')

        self.vm_writer.write_if(end_label)

        self.read_tokens(2)  # ')' '{'
        self.compile_statements()
        self.read_tokens(1)  # '}

        self.vm_writer.write_goto(loop_label)
        self.vm_writer.write_label(end_label)

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.read_tokens(1)  # 'return'
        if not self.is_semicolon():
            self.compile_expression()
        else:
            self.vm_writer.write_push('CONST', 0)
        self.vm_writer.write_return()
        self.read_tokens(1)  # ';'

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.read_tokens(2)  # 'if' '('
        self.compile_expression()

        self.vm_writer.write_arithmetic('NOT')
        else_label = self.get_new_label()
        self.vm_writer.write_if(else_label)

        self.read_tokens(2)  # ')' '{'
        self.compile_statements()
        self.read_tokens(1)  # '}'

        end_label = self.get_new_label()
        self.vm_writer.write_goto(end_label)
        self.vm_writer.write_label(else_label)

        if self.is_else_clause():
            self.read_tokens(2)  # 'else' '{'
            self.compile_statements()
            self.read_tokens(1)  # '}'
        
        self.vm_writer.write_label(end_label)

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        
        self.compile_term()
        while self.is_op():
            op = self.input.symbol()
            self.check_advance()
            self.compile_term()
            if op in ops:
                self.vm_writer.write_arithmetic(ops[op])
            elif op == "*":
                self.vm_writer.write_call("Math.multiply", 2)
            else:
                self.vm_writer.write_call("Math.divide", 2)

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
        if self.is_unary_op():
            op = self.input.symbol()
            self.check_advance()
            self.compile_term()
            self.vm_writer.write_arithmetic(ops[op])
        elif self.is_opening_bracket():
            self.check_advance()  # '('
            self.compile_expression()
            self.check_advance()  # ')'
        elif self.is_identifier():
            id = self.input.symbol()
            self.check_advance()
            if self.is_square_opening_bracket():
                self.check_advance()  # '['
                self.compile_expression()
                self.check_advance()  # ']'
                self.vm_writer.write_push(*self.get_segment_index_pair(id))
                self.vm_writer.write_arithmetic("ADD")
                self.vm_writer.write_pop("POINTER", 1)
                self.vm_writer.write_push("THAT", 0)
            elif self.is_subroutine_call_second_token():
                n_args = 0
                if id in self.symbol_table.sub_table or id in self.symbol_table.class_table:
                    tmp = id
                    id = self.symbol_table.type_of(id)
                    n_args += 1
                    self.vm_writer.write_push(self.symbol_table.kind_of(tmp), self.symbol_table.index_of(tmp))
                if self.is_dot():
                    self.check_advance()  # '.'
                    id +=  '.' + self.input.symbol() # identifier
                    self.check_advance() # get to (
                else:
                    id = self.class_name + '.' + id
                    n_args += 1
                    self.vm_writer.write_push("POINTER", 0)
                n_args += self.compile_subroutine_call_second_token()
                self.vm_writer.write_call(id, n_args)
            else:
                self.vm_writer.write_push(*self.get_segment_index_pair(id))
        elif self.is_string():
            string = self.input.symbol()[1:-1]
            self.vm_writer.write_push(len(string))
            self.vm_writer.write_call("String.new", 1)
            for char in string:
                self.vm_writer.write_push("CONST", int(char))
                self.vm_writer.write_call("String.appendChar", 2)
            self.check_advance()
        elif self.input.token_type() == "BOOL_CONST":
            if self.input.symbol() == "true":
                self.vm_writer.write_push("CONST", "0")
                self.vm_writer.write_arithmetic("NOT")
            else:
                self.vm_writer.write_push("CONST", "0")
            self.check_advance()
        else:
            self.vm_writer.write_push("CONST", self.input.symbol())  # constant (int or string or keyword)
            self.check_advance()

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        if not self.is_closing_bracket():
            self.compile_expression()
            count = 1
            while self.is_comma():
                self.check_advance()  # ','
                count += 1
                self.compile_expression()
                
            return count
        return 0


    def is_subroutine_call_second_token(self):
        return self.is_opening_bracket() or self.is_dot()


    def compile_subroutine_call_second_token(self):
        self.check_advance()  # '('
        n_args = self.compile_expression_list()
        self.check_advance()  # ')'
        
        return n_args
        

