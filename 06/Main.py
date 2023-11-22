"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")
    
    parser = Parser(input_file)
    table = SymbolTable()
    
    # First pass
   
    addr = 0
    
    while parser.has_more_commands():
        parser.advance()
        
        command_type = parser.command_type()
        if command_type == "L_COMMAND":
            if table.contains(parser.symbol()):
                raise Exception("Can't define label twice")
            table.add_entry(parser.symbol(), addr)
            
        else:
            addr += 1
        
    # Second pass
    bin_lines = []
    RAM_addr = 16
    
    # resetting parser
    parser.line_index = -1
    
    
    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()
        if command_type == "L_COMMAND":
            continue
            
        elif command_type == "A_COMMAND":
            if parser.symbol().isdigit():
                addr = int(parser.symbol())
            else:
                if not table.contains(parser.symbol()):
                    table.add_entry(parser.symbol(), RAM_addr)
                    RAM_addr += 1
                
                addr = table.get_address(parser.symbol())
            
            bin_lines.append("{0:b}".format(addr).zfill(16))
            
        
        elif command_type == "C_COMMAND":
            dest = Code.dest(parser.dest())
            jump = Code.jump(parser.jump())
            if '<<' in parser.line or '>>' in parser.line:
                shift = Code.shift(parser.comp())
                bin_lines.append(shift + dest + jump)
            else:
                comp = Code.comp(parser.comp())
                bin_lines.append("111" + comp + dest + jump)
        
        
    # Write output
    for line in bin_lines:
        output_file.write(line + "\n")
    
            


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
