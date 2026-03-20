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

; Allocate space for local variables
ADDI sp, sp, -4 
ADDI sp, sp, -4

; read(a)
GETI t0
SW t0, -4(fp)

; read(b)
GETI t1
SW t1, -8(fp)

BLE t0, t1, else
then:
LA t2, 0x10000000
PUTS t2
J finish
else:
LA t3, 0x10000004
PUTS t3

finish:

MV sp, fp
LW fp, 0(fp)
RET



.section .strings
0x10000000 "True\n"
0x10000004 "False\n"
