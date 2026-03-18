; Symbol table GLOBAL
; Function: INT main([])

.section .text

MV fp, sp
JR func_main
HALT

func_main:
RET

.section .strings 