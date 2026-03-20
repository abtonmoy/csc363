; Symbol table
; name a type INT location 0x20000000
; Function: INT main([])

; Symbol table main
; name b type INT location -4

.section .text

MV fp, sp
JR func_main
HALT

func_main:
SW fp, 0(sp)        
MV fp, sp
ADDI sp, sp, -4

ADDI sp, sp, -4

LA t1, 0x20000000
LI t2, 6
SW t2, 0(t1)

LI t3, 7
SW t3, -4(fp)

ADDI sp, sp, 4

ADDI sp, sp, 4
MV sp, fp
LW fp, 0(fp)
RET

.section .strings
