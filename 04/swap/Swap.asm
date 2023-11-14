// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.
// First, find min and max
@R14
D=M // start of array

// i pointer
@i_addr
M=D
@i
M=0

// min=max=&start
@i_addr
D=M

@max_addr
M=D
A=D
D=M
@max
M=D

@i_addr
D=M

@min_addr
M=D
A=D
D=M
@min
M=D


// len
@R15
D=M
@len
M=D


// for(i=base_addr, i<len; i++) {if(*max < *i){max=i;} if(*min > *i){min=i;}}
(LOOP)

@max
D=M
@i
D=D-M
@IFMAX
D;JGT


@i_addr
D=M

@max_addr
M=D
A=D
D=M
@max
M=D


(IFMAX)


@min
D=M
@i
D=D-M
@IFMIN
D;JLT


@i_addr
D=M

@min_addr
M=D
A=D
D=M
@min
M=D


(IFMIN)


@i_addr
M=M+1
A=M
D=M
@i
M=D

@len
M=M-1
D=M
@LOOP
D;JGT






@max
D=M
@tmp
M=D // tmp = max
@min
D=M // D = min

@max_addr
A=M
M=D // *max_addr = D = min

@tmp
D=M // D = tmp = max
@min_addr
A=M
M=D // *min_addr = D = max

// finishing loop
(END)
@END
0;JMP