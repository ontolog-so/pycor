import sys
import pycor.morpheme as lm
import pycor.speechmodel as sm
import pycor.korutils
import pycor.kormorpheme as klm
import pycor.std.stem as stm
import pycor.std.aux as aux


yongEonConsts = lm.ConstraintSuffixWithoutTags(['JKG','JKS','JKP','JKO','JX-SO','JKB-TO','JKB-AT' ,'JKB-FM','JX-from','JKB-AS','JKB-WZ','JKB-LK','JC','JX','JKB-TT|AS|BY'])
cheEonConsts = lm.ConstraintSuffixWithTags(['JKG','JKS','JKP','JKO','JX-SO','JKB-TO','JKB-AT' ,'JKB-FM','JX-from','JKB-AS','JKB-WZ','JKB-LK','JC','JX','JKB-TT|AS|BY'])

# suffixDoe = lm.regSuffix('되').setpos('Y').setProtoPos('C')
# suffixHa = lm.regSuffix('하').setpos('Y').setProtoPos('C').after(lm.Suffix('당').setProtoPos('C'))
# suffixBad = lm.regSuffix('받').setpos('Y').setProtoPos('C')
# suffixSiKi = lm.regSuffix('키').setpos('Y').after(lm.Suffix('시').setpos('Y').setProtoPos('C'))
# # TODO ~해지 --> 해 / 지 수정 필요 
# suffixJi = lm.regSuffix('지').incase(yongEonConsts).incase(lm.onlyAfter).setpos('Y').setProtoPos('Y').after([
#     aux.auxHae,aux.auxA, aux.auxEo
#     ])

# sufGe = lm.Suffix('게').after([suffixHa,suffixDoe,suffixJi])
# suffixDoe.after(sufGe)

# suffixGi = lm.regSuffix('기').setpos('C').after([
#     suffixHa,suffixDoe,suffixJi
#     ])

# suffixDeul = lm.regSuffix('들').setpos('C').setProtoPos('C').incase(cheEonConsts)
# suffixJeok = lm.regSuffix('적').setpos('VA').setProtoPos('C')