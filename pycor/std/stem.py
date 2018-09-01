import sys
import pycor.langmodel as lm
import pycor.speechmodel as sm
import pycor.korutils
import pycor.korlangmodel as klm


constraintFirst = klm.ConstraintFirst()

##################################################
# 어간 : 있 / 없
##################################################
stemIt = lm.regStem('있', atag='V').setpos('Y')
stemUp = lm.regStem('없', atag='V').setpos('Y')

npI = lm.regStem("이", atag='NP').incase(constraintFirst).setpos('NP')
npGeu = lm.regStem("그", atag='NP').incase(constraintFirst).setpos('NP')
npGeuNyeo = lm.regStem("녀").incase(lm.onlyAfter).after(lm.Stem("그").setpos('NP').incase(constraintFirst))
npJeo = lm.regStem("저", atag='NP').incase(constraintFirst).setpos('NP')
lm.regStem("나", atag='NP').incase(constraintFirst).setpos('NP')
lm.regStem("너", atag='NP').incase(constraintFirst).setpos('NP')
npWoori = lm.regStem("리").setpos('NP').after(lm.Stem("우").setpos('NP').incase(constraintFirst))
npNeoHi = lm.regStem("희").setpos('NP').incase(lm.onlyAfter).after([
    lm.Stem("너").setpos('NP').incase(constraintFirst),
    lm.Stem("저").setpos('NP').incase(constraintFirst)
])
npDangSin = lm.regStem("신").incase(lm.onlyAfter).after(lm.Stem("당").setpos('NP').incase(constraintFirst))
lm.regStem("분").incase(lm.onlyAfter).after(lm.Stem("러").incase(lm.onlyAfter).after(
        lm.Stem("여").setpos('NP').incase(constraintFirst)))
npGeot = lm.regStem("것").setpos('NP').after([
    lm.Stem("그").setpos('NP').incase(constraintFirst),
    lm.Stem("저").setpos('NP').incase(constraintFirst),
    lm.Stem("이").setpos('NP').incase(constraintFirst)
])
lm.regStem("들").setpos('NP').incase(lm.onlyAfter).after([npGeot,npI,npGeu,npGeuNyeo,npJeo,npWoori,npNeoHi,npDangSin])

lm.regStem("때", atag='NNB').setpos('NNB').incase(constraintFirst)
lm.regStem("등", atag="NNB").setpos('NNB').incase(constraintFirst)
lm.regStem("뿐", atag="NNB").setpos('NNB').incase(constraintFirst)
lm.regStem("곳", atag="NNB").setpos('NNB').incase(constraintFirst)
lm.regStem("바", atag="NNB").setpos('NNB').incase(constraintFirst)




##################################################
#  관형사 
##################################################
npI = lm.regStem("적", atag='MM').setpos('VA')


##################################################
#  -주의 
##################################################
lm.regAux(lm.StemAux("주의", escapeFirst=True)).tag("ISM").escape(['지','건물','기업','점']).setscore(2)