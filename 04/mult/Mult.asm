// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// Multiplies R0 and R1 and stores the result in R2.
//
// Assumptions:
// - R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.
// - You can assume that you will only receive arguments that satisfy:
//   R0 >= 0, R1 >= 0, and R0*R1 < 32768.
// - Your program does not need to test these conditions.
//
// Requirements:
// - Your program should not change the values stored in R0 and R1.
// - You can implement any multiplication algorithm you want.

// Put your code here.

// checking for 0
@tmp
M=0 // set tmp=0

@R0
D=M // D=RAM[0]
@ELSE
D;JEQ // goto final steps if 0

@R1
D=M // D=RAM[1]
@ELSE
D;JEQ // goto final steps if 0
@count
M=D


@R0
D=M // D=RAM[0]
@tmp
M=D // tmp=RAM[0]


(LOOP)
@count
M=M-1
D=M // D=RAM[1]
@ELSE
D;JEQ // if count==0 goto ELSE

@tmp
D=M // D=tmp
@R0
D=D+M
@tmp
M=D // tmp=tmp+RAM[0]

// return to beginning of loop
@LOOP
0;JMP

(ELSE)

@tmp
D=M // D=tmp=RAM[0]*RAM[1]
@R2
M=D // RAM[2]=RAM[0]*RAM[1]

// finishing loop
(END)
@END
0;JMP
