; Symbol table
; a type INT location 0x20000000
; function INT main([])

; Symbol table main
; b type INT location -4

.section .text

MV fp, sp
JR func_main
HALT

func_main:
SW fp, 0(sp)
MV fp, sp
ADDI sp, sp, -4

ADDI sp, sp, -4

GETI t0
LA t1, 0x20000000
SW t0, 0(t1)

GETI t2
SW t2, -4(fp)

LA t3, 0x20000000
LW t4, 0(t3)
PUTI t4

LW t5, -4(fp)
PUTI t5


ADDI sp, sp, 4

ADDI sp, sp, 4
MV sp, fp
RET