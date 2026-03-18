; Symbol table 
; name a type InnerType.INT location 0x20000000
; Function: InnerType.INT main([])

; Symbol table main
; name b type InnerType.INT location -4

.section .text

MV fp, sp
JR func_main
HALT

func_main:
SW fp, 0(sp)
MV fp, sp
ADDI sp, sp, -4
ADDI sp, sp, -4
SW t1, 0(sp)
ADDI sp, sp, -4
SW t2, 0(sp)
ADDI sp, sp, -4
SW t3, 0(sp)
ADDI sp, sp, -4
SW t4, 0(sp)
ADDI sp, sp, -4
LA t1, 0x20000000
LI t0, 6
SW t0, 0(t1)
LI t2, 7
SW t2, -4(fp)
LI t3, 0
SW t3, 8(fp)
J func_ret_main
func_ret_main:
ADDI sp, sp, 4
LW t4, 0(sp)
ADDI sp, sp, 4
LW t3, 0(sp)
ADDI sp, sp, 4
LW t2, 0(sp)
ADDI sp, sp, 4
LW t1, 0(sp)
MV sp, fp
LW fp, 0(fp)
RET


.section .strings
