; Symbol table 
; name true type InnerType.STRING location 0x10000000 value "True\n"
; name false type InnerType.STRING location 0x10000004 value "False\n"
; Function: InnerType.INT main([])

; Symbol table main
; name a type InnerType.INT location -4
; name b type InnerType.INT location -8

.section .text
;Current temp: 
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
LW t0, -4(fp)
LW t1, -8(fp)
BLE t0, t1, out_1
LA t2, 0x10000000
PUTS t2
J out_1
out_1:
LI t3, 0
SW t3, 8(fp)

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
