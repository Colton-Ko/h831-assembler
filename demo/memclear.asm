;       H831 CPU
;       memclear.asm
;       Clears all data in
.main:          movi %x0, $0    ;
                movi %x1, $0    ;
                movi %x2, $0    ;
                movi %x3, $0    ;
                movi %x4, $0    ;
                movi %x5, $0    ;
                movi %x6, $0    ;
                movi %x7, $0    ;
                stkz            ;
.ramzero:       push %x0        ;
                inc %x1, %x1    ;
                cmpi %x1, $31   ;
                bnz .ramzero    ;
.halt:          breakpt         ;
