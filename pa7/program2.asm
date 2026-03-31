; Symbol table GLOBAL
; name prompt type STRING location 0x10000000 value "Please enter a positive integer\n"
; Function: INT main([])

; Symbol table main
; name n type INT location -4
; name count type INT location -8

.section .text
MV fp, sp
JR func_main
HALT

func_main:
SW fp, 0(sp)
MV fp, sp
ADDI sp, sp, -4

; Allocate space for local variables n and count
ADDI sp, sp, -4
ADDI sp, sp, -4

; Initialize n = 0
LI t0, 0
SW t0, -4(fp)

; Initialize count = 0
LI t1, 0
SW t1, -8(fp)

; Prompt loop - keep asking until n > 0
prompt_loop:
; Print prompt
LA t2, 0x10000000
PUTS t2

; Read n
GETI t3
SW t3, -4(fp)

; Check if n > 0
LI t4, 0
BLE t3, t4, prompt_loop

; Now we have valid n > 0, do Collatz
; while (n > 1)
collatz_loop:
; Load n
LW t5, -4(fp)

; Check if n > 1
LI t6, 1
BLE t5, t6, collatz_done

; Print n
PUTI t5

; Check if n is even or odd
; n % 2 = n - (n/2)*2
; Divide n by 2
LI t7, 2
DIV t8, t5, t7
; Multiply result by 2
MUL t9, t8, t7
; Subtract from n to get remainder
SUB t10, t5, t9

; If remainder == 0, n is even
LI t11, 0
BNE t10, t11, n_is_odd

; n is even: n = n / 2
SW t8, -4(fp)
J increment_count

n_is_odd:
; n is odd: n = 3*n + 1
LI t12, 3
MUL t13, t5, t12
ADDI t14, t13, 1
SW t14, -4(fp)

increment_count:
; count = count + 1
LW t15, -8(fp)
ADDI t16, t15, 1
SW t16, -8(fp)

J collatz_loop

collatz_done:
; Print n (which is now 1)
LW t17, -4(fp)
PUTI t17

; Print count
LW t18, -8(fp)
PUTI t18

; Clean up and return
ADDI sp, sp, 4
ADDI sp, sp, 4
MV sp, fp
LW fp, 0(fp)
RET

.section .strings
0x10000000 "Please enter a positive integer\n"
