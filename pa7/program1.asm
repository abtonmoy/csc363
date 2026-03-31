; Symbol table GLOBAL
; name a type INT location 0x20000000
; name b type INT location 0x20000004
; name less type STRING location 0x10000000 value "a is less than b\n"
; name equal type STRING location 0x10000004 value "a is equal to b\n"
; name greater type STRING location 0x10000008 value "a is greater than b\n"
; Function: INT main([])

.section .text
MV fp, sp
JR func_main
HALT

func_main:
SW fp, 0(sp)
MV fp, sp
ADDI sp, sp, -4

; Read value for a
GETI t0
LA t1, 0x20000000
SW t0, 0(t1)

; Read value for b
GETI t2
LA t3, 0x20000004
SW t2, 0(t3)

; Compare a and b
; If a > b, print greater
; If a == b, print equal
; If a < b, print less

LA t1, 0x20000000
LW t0, 0(t1)
LA t3, 0x20000004
LW t2, 0(t3)

; First check if a > b
BGT t0, t2, print_greater

; If not greater, check if a == b
BEQ t0, t2, print_equal

; If neither greater nor equal, then a < b
J print_less

print_greater:
LA t4, 0x10000008
PUTS t4
J done

print_equal:
LA t4, 0x10000004
PUTS t4
J done

print_less:
LA t4, 0x10000000
PUTS t4

done:
MV sp, fp
LW fp, 0(fp)
RET

.section .strings
0x10000000 "a is less than b\n"
0x10000004 "a is equal to b\n"
0x10000008 "a is greater than b\n"
