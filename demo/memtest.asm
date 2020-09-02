;       H831 CPU
;       memtest.asm
.main:  movi %x0, $1    ;       Set x0 to 0                     0
        movi %x1, $32   ;       Set x1 to 32                    1
        movi %x7, $0    ;       Set base ptr to 0               2
.loop:  push %x0        ;       Write x0 to stack               3
        inc %x0, %x0    ;       Increment x0 by 1               4
        cmp %x0, %x1    ;       Compare x0 , x1                 5
        bnz .loop       ;
.check: pop %x2         ;       Read from stack                 6
        cmp %x0, %x2    ;       If memory write incorrect       7
        bnz .halt       ;       halt                            8
        dec %x0, %x0    ;       Decrement x0                    9
        cmp %x0, $1     ;       Do 32 times                     10
        bnz .check      ;                                       11
        not %x4,%x4     ;                                       12
.halt:  breakpt         ;                                       13