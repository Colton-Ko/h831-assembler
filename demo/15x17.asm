; Calculate 15x17
.main:          movi %x0, $17           ;       x0 = accmulator
                movi %x1, $14           ;       x1 = constant
                movi %x2, $0            ;       x2 = index
.loop:          add  %x0, %x0, %x1      ;       x0 += x1
                inc  %x1, %x1           ;       x1 += 1
                cmp  %x1, %x2           ;       
                bnz  .loop              ;
.halt:          dbgout %x0              ;
                breakpt                 ;
