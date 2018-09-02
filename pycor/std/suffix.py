import sys
import pycor.langmodel as lm
import pycor.speechmodel as sm
import pycor.korutils
import pycor.korlangmodel as klm
import pycor.std.stem as stm
import pycor.std.aux as aux


suffixDoe = lm.regSuffix('되').setpos('Y') 
suffixHa = lm.regSuffix('하').setpos('Y')
suffixSiKi = lm.regSuffix('키').setpos('Y').after(lm.Suffix('시'))

sufGe = lm.Suffix('게').after([suffixHa,suffixDoe])
suffixDoe.after(sufGe)

suffixGi = lm.regSuffix('기').setpos('C').after([
    suffixHa,suffixDoe
    ])

suffixDeul = lm.regSuffix('들').setpos('C')
suffixJeok = lm.regSuffix('적').setpos('C')