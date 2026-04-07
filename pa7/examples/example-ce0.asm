MV fp, sp
JR func_main
HALT

func_main:
    SW fp, 0(sp)
    MV fp, sp
    RET
