"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the SPecifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


call_counter = {}


class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.filename = None
        self.output = output_stream
        self.curr_func = []

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        
        self.filename = filename
        self.label_counter = 0
        
    def write_unary(self, command: str):
        output = []

        output.append("@SP")
        output.append("A=M-1")
        if command == "neg":
            output.append("M=-M")
        elif command == "not":
            output.append("M=!M")
        
        self.output.write("\n".join(output) + "\n")

    def write_binary(self, command: str):
        output = []

        output.append("@SP")
        output.append("M=M-1")
        output.append("A=M")
        output.append("D=M")
        output.append("@SP")
        output.append("M=M-1")
        output.append("A=M")
    
        # Binary commands
        if command == "add":
            output.append("M=M+D")
        elif command == "sub":
            output.append("M=M-D")
        elif command == "and":
            output.append("M=M&D")
        elif command == "or":
            output.append("M=M|D")
        elif command == "shiftleft":
            output.append("M=M<<")
        elif command == "shiftright":
            output.append("M=M>>")

        output.append("@SP")
        output.append("M=M+1")
        
        self.output.write("\n".join(output) + "\n")
    
    def write_compare_eq(self):
        output = []

        output.append("@SP")
        output.append("M=M-1")
        output.append("A=M")
        output.append("D=M")
        output.append("@SP")
        output.append("M=M-1")
        output.append("A=M")
    
        output.append("D=M-D")
        output.append(f"@{self.filename}CMPIF{self.label_counter}")
        output.append("D;JEQ")
        
        output.append("@SP")
        output.append("A=M")
        output.append("M=0")
        
        output.append(f"@{self.filename}CMPSKIP{self.label_counter}")
        output.append("0;JMP")
        output.append(f"({self.filename}CMPIF{self.label_counter})")
        
        output.append("@SP")
        output.append("A=M")
        output.append("M=-1")
        
        output.append(f"({self.filename}CMPSKIP{self.label_counter})")
        output.append("@SP")
        output.append("M=M+1")
        
        self.output.write("\n".join(output) + "\n")
        self.label_counter += 1

    def write_compare_neq(self, command: str):
        output = []

        output.append("@SP")
        output.append("M=M-1")
        output.append("A=M")
        output.append("D=M")

        output.append(f"@{self.filename}Ypos{self.label_counter}")
        output.append("D;JGT")
        output.append(f"@{self.filename}Yneg{self.label_counter}")
        output.append("0;JMP")

        # Y > 0
        output.append(f"({self.filename}Ypos{self.label_counter})")
        output.append("@SP")
        output.append("M=M-1")
        output.append("A=M")
        output.append("D=M")

        output.append(f"@{self.filename}XYpos{self.label_counter}")
        output.append("D;JGE")
        output.append(f"@{self.filename}YgtX{self.label_counter}")
        output.append("0;JMP")

        # Y <= 0
        output.append(f"({self.filename}Yneg{self.label_counter})")
        output.append("@SP")
        output.append("M=M-1")
        output.append("A=M")
        output.append("D=M")

        output.append(f"@{self.filename}YltX{self.label_counter}")
        output.append("D;JGT")
        output.append(f"@{self.filename}XYpos{self.label_counter}")
        output.append("0;JMP")

        # XY >= 0
        output.append(f"({self.filename}XYpos{self.label_counter})")
        output.append("@SP")
        output.append("A=M+1")
        output.append("D=M-D")
        output.append(f"@{self.filename}YgtX{self.label_counter}")
        output.append("D;JGT")
        output.append(f"@{self.filename}YeqX{self.label_counter}")
        output.append("D;JEQ")
        output.append(f"@{self.filename}YltX{self.label_counter}")
        output.append("0;JMP")

        # Y < X
        output.append(f"({self.filename}YltX{self.label_counter})")
        if command == "lt":
            output.append("D=0")
        else:
            output.append("D=-1")
        output.append(f"@{self.filename}end{self.label_counter}")
        output.append("0;JMP")

        # Y > X
        output.append(f"({self.filename}YgtX{self.label_counter})")
        if command == "gt":
            output.append("D=0")
        else:
            output.append("D=-1")
        output.append(f"@{self.filename}end{self.label_counter}")
        output.append("0;JMP")

        # Y = X
        output.append(f"({self.filename}YeqX{self.label_counter})")
        output.append("D=0")
        output.append(f"@{self.filename}end{self.label_counter}")
        output.append("0;JMP")

        output.append(f"({self.filename}end{self.label_counter})")
        output.append("@SP")
        output.append("A=M")
        output.append("M=D")
        output.append("@SP")
        output.append("M=M+1")
        
        self.output.write("\n".join(output) + "\n")
        self.label_counter += 1


    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        if command == "neg" or command == "not":
            self.write_unary(command)
        elif command == "eq":
            self.write_compare_eq()
        elif command == "gt" or command == "lt":
            self.write_compare_neq(command)
        else:
            self.write_binary(command)


    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        output = []
        
        if segment == "constant":
            output.append(f"@{index}")
            output.append("D=A")
            output.append("@SP")
            output.append("A=M")
            output.append("M=D") # RAM[SP] = D = i
            
            output.append("@SP")
            output.append("M=M+1")
            
            self.output.write("\n".join(output) + "\n")
            return
        
        if segment == "argument":
            output.append("@ARG")
        elif segment == "local":
            output.append("@LCL")
        elif segment == "this" or segment == "pointer":
            output.append("@THIS")
        elif segment == "that":
            output.append("@THAT")
        elif segment == "temp":
            output.append("@5")

        if segment == "static":
            output.append(f"@{self.filename}.{index}")
        else:
            if segment in ["temp", "pointer"]:
                output.append("D=A")
            else:
                output.append("D=M")
            output.append(f"@{index}")
            output.append("A=A+D") # A = base_addr + i
        
        
            
        if command == "C_PUSH":
            output.append("D=M") # D = RAM[SEG+i]
            output.append("@SP")
            output.append("A=M")
            output.append("M=D") # RAM[SP] = D = RAM[SEG+i]
            
            output.append("@SP")
            output.append("M=M+1")
        
        elif command == "C_POP":
            output.append("D=A")
            output.append("@R13")
            output.append("M=D")
            output.append("@SP")
            output.append("M=M-1")
            output.append("A=M")
            output.append("D=M")
            output.append("@R13")
            output.append("A=M")
            output.append("M=D")
            

            
        self.output.write("\n".join(output) + "\n")

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        output = []
        
        if len(self.curr_func) == 0:
            output.append(f"({self.filename}${label})")
        else:
            output.append(f"({self.curr_func[-1]}${label})")
        
        self.output.write(output[0] + "\n")
    
    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        output = []
        
        if len(self.curr_func) == 0:
            output.append(f"@{self.filename}${label}")
        else:
            output.append(f"@{self.curr_func[-1]}${label}")
        
        output.append("0;JMP")
        
        self.output.write("\n".join(output) + "\n")
    
    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        output = []
        
        output.append("@SP")
        output.append("M=M-1")
        output.append("A=M")
        output.append("D=M")
        
        if len(self.curr_func) == 0:
            output.append(f"@{self.filename}${label}")
        else:
            output.append(f"@{self.curr_func[-1]}${label}")
        
        output.append("D;JNE")
        
        self.output.write("\n".join(output) + "\n")
        
    
    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        output = []
        self.curr_func.append(function_name)
        
        output.append(f"({self.curr_func[-1]})")
        
        self.output.write("\n".join(output) + "\n")
        
        for _ in range(n_vars):
            self.write_push_pop("C_PUSH", "constant", 0)
        

    
    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        output = []

        # push return address
        if len(self.curr_func) == 0:
            output.append(f"@{self.filename}$ret.0")
        else:
            if self.curr_func[-1] not in call_counter:
                call_counter[self.curr_func[-1]] = 0
            else:
                call_counter[self.curr_func[-1]] += 1
            output.append(f"@{self.curr_func[-1]}$ret.{call_counter[self.curr_func[-1]]}")
        output.append("D=A")
        output.append("@SP")
        output.append("M=M+1")
        output.append("A=M-1")
        output.append("M=D")
        
        # push LCL, ARG, THIS, THAT
        for x in ["@LCL", "@ARG", "@THIS", "@THAT"]:
            output.append(x)
            output.append("D=M")
            output.append("@SP")
            output.append("M=M+1")
            output.append("A=M-1")
            output.append("M=D")

        # ARG = SP - (5 + num_args)
        output.append("@SP")
        output.append("D=M")
        output.append(f"@{5 + n_args}")
        output.append("D=D-A")
        output.append("@ARG")
        output.append("M=D")

        # LCL = SP
        output.append("@SP")
        output.append("D=M")
        output.append("@LCL")
        output.append("M=D")

        
        # goto function name
        output.append(f"@{function_name}")
        output.append("0;JMP")
        

        # return address        
        if len(self.curr_func) == 0:
            output.append(f"({self.filename}$ret.0)")
        else:
            output.append(f"({self.curr_func[-1]}$ret.{call_counter[self.curr_func[-1]]})")
            
            
        self.output.write("\n".join(output) + "\n")
    
    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        output = []
        
        # FRAME = R13 = LCL
        output.append("@LCL")
        output.append("D=M")
        output.append("@R13")
        output.append("M=D")
        
        # ret-addrr = R14 = RAM[FRAME - 5]
        output.append("@5")
        output.append("A=D-A")
        output.append("D=M")
        output.append("@R14")
        output.append("M=D")
        
        # *ARG = pop()
        # NOTE - no need to set SP - 1 since we'll be changing SP right after this
        output.append("@SP")
        output.append("A=M-1")
        output.append("D=M")
        output.append("@ARG")
        output.append("A=M")
        output.append("M=D")
        
        # SP = ARG + 1
        output.append("@ARG")
        output.append("D=M+1")
        output.append("@SP")
        output.append("M=D")
        
        # THAT = RAM[FRAME - 1], THIS = RAM[FRAME - 2], ...
        addrs = ["THAT", "THIS", "ARG", "LCL"]
        for i in range(len(addrs)):
            output.append("@R13")
            output.append("D=M")
            output.append(f"@{i+1}")
            output.append("A=D-A")
            output.append("D=M")
            output.append(f"@{addrs[i]}")
            output.append("M=D")
        
        # GOTO ret-addr
        output.append("@R14")
        output.append("A=M")
        output.append("0;JMP")
        
        self.output.write("\n".join(output) + "\n")

        
        
    def write_bootstrap(self):
        output = []
        
        # SP = 256
        output.append("@256")
        output.append("D=A")
        output.append("@SP")
        output.append("M=D")
        
        self.output.write("\n".join(output) + "\n")
        
        # call Sys.init
        self.write_call("Sys.init", 0)