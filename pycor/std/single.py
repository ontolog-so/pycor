import sys
import pycor.langmodel as lm
import pycor.korutils
import pycor.korlangmodel as klm

##################################################
# SingleWords 세팅 
##################################################

lm.regSng("고스란히","MAG")
lm.regSng("빨리","MAG")
lm.regSng("약간","MAG")
lm.regSng("빨리","MAG")
lm.regSng("가장","MAG")
lm.regSng("같이","MAG")
lm.regSng("한편","MAG")
lm.regSng("그렇게","MAG")
lm.regSng("또한","MAG")
lm.regSng("또는","MAG")
lm.regSng("서로","MAG")
lm.regSng("각각","MAG")
lm.regSng("이미","MAG")
lm.regSng("듯이","MAG")

lm.regSng("그러나","MAJ")
lm.regSng("그리고","MAJ")
lm.regSng("그런데","MAJ")
lm.regSng("그래서","MAJ")
lm.regSng("아니라","MAJ")
lm.regSng("하지만","MAJ")
lm.regSng("또한","MAJ")
lm.regSng("혹은","MAJ")
lm.regSng("또","MAG")

lm.regSng("이","MM")
lm.regSng("그","MM")
lm.regSng("저","MM")
lm.regSng("이러한","MM")
lm.regSng("같은","MM")
lm.regSng("다른","MM")
lm.regSng("같은","MM")
lm.regSng("어떤","MM")
lm.regSng("모든","MM")
lm.regSng("몇가지","MM")

lm.regSng("따라","DN")
lm.regSng("통한","DN")
lm.regSng("대한","DN")
lm.regSng("관한","DN")
lm.regSng("위한","DN")
lm.regSng("통해","DN")
lm.regSng("대해","DN")
lm.regSng("관해","DN")
lm.regSng("위해","DN")
lm.regSng("의해","DN")
lm.regSng("수","DN")
lm.regSng("것","DN")
lm.regSng("곳","DN")
lm.regSng("때문","DN")




