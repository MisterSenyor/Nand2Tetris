@256
D=A
@SP
M=D
@Sys$ret.0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(Sys$ret.0)
(Main.T3)
@Main.T3$ret.0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.t1
0;JMP
(Main.T3$ret.0)
@Main.T3$ret.1
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.t2
0;JMP
(Main.T3$ret.1)
@Main.T3$ret.2
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.t3
0;JMP
(Main.T3$ret.2)
@Main.T3$ret.3
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.t4
0;JMP
(Main.T3$ret.3)
(Main.T3$WHILE)
@Main.T3$WHILE
0;JMP
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
D=M
@1
A=D-A
D=M
@THAT
M=D
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Main.t1)
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
M=-M
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@MainYpos0
D;JGT
@MainYneg0
0;JMP
(MainYpos0)
@SP
M=M-1
A=M
D=M
@MainXYpos0
D;JGE
@MainYgtX0
0;JMP
(MainYneg0)
@SP
M=M-1
A=M
D=M
@MainYltX0
D;JGT
@MainXYpos0
0;JMP
(MainXYpos0)
@SP
A=M+1
D=M-D
@MainYgtX0
D;JGT
@MainYeqX0
D;JEQ
@MainYltX0
0;JMP
(MainYltX0)
D=0
@Mainend0
0;JMP
(MainYgtX0)
D=-1
@Mainend0
0;JMP
(MainYeqX0)
D=0
@Mainend0
0;JMP
(Mainend0)
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
D=M
@1
A=D-A
D=M
@THAT
M=D
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Main.t2)
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
M=-M
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@MainYpos1
D;JGT
@MainYneg1
0;JMP
(MainYpos1)
@SP
M=M-1
A=M
D=M
@MainXYpos1
D;JGE
@MainYgtX1
0;JMP
(MainYneg1)
@SP
M=M-1
A=M
D=M
@MainYltX1
D;JGT
@MainXYpos1
0;JMP
(MainXYpos1)
@SP
A=M+1
D=M-D
@MainYgtX1
D;JGT
@MainYeqX1
D;JEQ
@MainYltX1
0;JMP
(MainYltX1)
D=-1
@Mainend1
0;JMP
(MainYgtX1)
D=0
@Mainend1
0;JMP
(MainYeqX1)
D=0
@Mainend1
0;JMP
(Mainend1)
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
D=M
@1
A=D-A
D=M
@THAT
M=D
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Main.t3)
@20000
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
M=-M
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
@30000
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@MainYpos2
D;JGT
@MainYneg2
0;JMP
(MainYpos2)
@SP
M=M-1
A=M
D=M
@MainXYpos2
D;JGE
@MainYgtX2
0;JMP
(MainYneg2)
@SP
M=M-1
A=M
D=M
@MainYltX2
D;JGT
@MainXYpos2
0;JMP
(MainXYpos2)
@SP
A=M+1
D=M-D
@MainYgtX2
D;JGT
@MainYeqX2
D;JEQ
@MainYltX2
0;JMP
(MainYltX2)
D=-1
@Mainend2
0;JMP
(MainYgtX2)
D=0
@Mainend2
0;JMP
(MainYeqX2)
D=0
@Mainend2
0;JMP
(Mainend2)
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
D=M
@1
A=D-A
D=M
@THAT
M=D
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Main.t4)
@20000
D=A
@SP
A=M
M=D
@SP
M=M+1
@30000
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
A=M-1
M=-M
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=M-D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@MainYpos3
D;JGT
@MainYneg3
0;JMP
(MainYpos3)
@SP
M=M-1
A=M
D=M
@MainXYpos3
D;JGE
@MainYgtX3
0;JMP
(MainYneg3)
@SP
M=M-1
A=M
D=M
@MainYltX3
D;JGT
@MainXYpos3
0;JMP
(MainXYpos3)
@SP
A=M+1
D=M-D
@MainYgtX3
D;JGT
@MainYeqX3
D;JEQ
@MainYltX3
0;JMP
(MainYltX3)
D=-1
@Mainend3
0;JMP
(MainYgtX3)
D=0
@Mainend3
0;JMP
(MainYeqX3)
D=0
@Mainend3
0;JMP
(Mainend3)
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
A=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M+1
@SP
M=D
@R13
D=M
@1
A=D-A
D=M
@THAT
M=D
@R13
D=M
@2
A=D-A
D=M
@THIS
M=D
@R13
D=M
@3
A=D-A
D=M
@ARG
M=D
@R13
D=M
@4
A=D-A
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Sys.init)
@Sys.init$ret.0
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.T3
0;JMP
(Sys.init$ret.0)
(Sys.init$WHILE)
@Sys.init$WHILE
0;JMP