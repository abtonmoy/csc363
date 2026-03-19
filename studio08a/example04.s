; Symbol table GLOBAL
; name true type STRING location 0x10000000 value "True\n"
; name false type STRING location 0x10000004 value "False\n"
; Function: INT main([])

; Symbol table main
; name a type INT location -4
; name b type INT location -8

; generating code to print ; name true type STRING location 0x10000000 value "True\n"
.section .text
;Current temp: null
;IR Code: 
MV fp, sp
JR func_main
HALT

func_main:
SW fp, 0(sp)
MV fp, sp
ADDI sp, sp, -4
ADDI sp, sp, -8
SW t1, 0(sp)
ADDI sp, sp, -4
SW t2, 0(sp)
ADDI sp, sp, -4
SW t3, 0(sp)
ADDI sp, sp, -4
SW t4, 0(sp)
ADDI sp, sp, -4
SW t5, 0(sp)
ADDI sp, sp, -4
SW t6, 0(sp)
ADDI sp, sp, -4
GETI t1
SW t1, -4(fp)
GETI t2
SW t2, -8(fp)
LW t3, -4(fp)
LW t4, -8(fp)
BLE t3, t4, out_1
LA t5, 0x10000000
PUTS t5
out_1:
LI t6, 0
SW t6, 8(fp)
J func_ret_main
func_ret_main:
ADDI sp, sp, 4
LW t6, 0(sp)
ADDI sp, sp, 4
LW t5, 0(sp)
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
0x10000000 "True\n"
0x10000004 "False\n"
