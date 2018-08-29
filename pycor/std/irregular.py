import sys
import pycor.korutils
import pycor.langmodel as lm
import pycor.korlangmodel as klm
import pycor.std.aux as aux


afterJongsung = klm.ConstraintAfterJongsung()
afterVowel = klm.ConstraintAfterVowel()
afterPositiveVowel = klm.ConstraintAfterPositiveVowel()
afterNegativeVowel = klm.ConstraintAfterNegativeVowel()
afterVowel = klm.ConstraintAfterVowel()
final =  klm.ConstraintFinal()
first = klm.ConstraintFirst()
 
##################################################
# <ㄷ불규칙 동사>
# 깨닫- + -아 → 깨달아
# 붇- + -어나다 → 불어나다
# 묻〔問〕- + -어 → 물어 
# 눋- + -어 → 눌어  밥이 밥솥에 눌어 버렸다.
# 겯- + -어 → 결어  종이가 잘 결어 버렸다.
# 듣- + -어 → 들어
# 싣- + -어 → 실어
# .. passive ...
# 닫- + -리다 → 달리다
# 붇- + -리다 → 불리다
##################################################
''' 불어나다, 물어, 실어'''
irrD_Bud = klm.TransformedStem('불','붇', atag="V+IRD+AMBI", score=1).setpos('Y').incase(first) 
irrD_Mud = klm.TransformedStem('물','묻', atag="V+IRD+AMBI", score=1).setpos('Y').incase(first) 
irrD_Sid = klm.TransformedStem('실','싣', atag="V+IRD+AMBI", score=1).setpos('Y').incase(first)
''' 들어(듣다) '''
irrD_Deud = klm.TransformedStem('들','듣', atag="V+IRD+AMBI", score=2).setpos('Y').incase(first)

''' 깨달아(깨닫다), 치달아(치닫다),  '''
irrD_Dad = klm.TransformedStem('달','닫', atag="V+IRD", score=1).setpos('Y').incase(
                klm.ConstraintAfter(['깨','치']))
'''달리다(닫다), 불리다(붇다)'''
irrD_DadRi = klm.TransformedStem('달','닫', atag="V+PASS+IRD+AMBI", score=2).setpos('Y').incase(first)
irrD_BudRi = klm.TransformedStem('불','붇', atag="V+PASS+IRD+AMBI", score=2).setpos('Y').incase(first) 


aux.auxEo.after([irrD_Bud, irrD_Mud, irrD_Sid, irrD_Deud ])
aux.eptEot.after([irrD_Bud, irrD_Mud, irrD_Sid, irrD_Deud ])
aux.auxA.after( irrD_Dad )
aux.eptAt.after( irrD_Dad )

aux.auxEu.after([irrD_Bud, irrD_Mud, irrD_Sid, irrD_Deud, irrD_Dad])
aux.etmEun.after([irrD_Bud, irrD_Mud, irrD_Sid, irrD_Deud, irrD_Dad])
aux.etmEul.after([irrD_Bud, irrD_Mud, irrD_Sid, irrD_Deud, irrD_Dad])
aux.auxRi.after( [irrD_DadRi, irrD_BudRi] )
aux.auxRyeo.after( [irrD_DadRi, irrD_BudRi] )
aux.auxRyeot.after( [irrD_DadRi, irrD_BudRi] )


##################################################
# <르 불규칙 활용>
# 어간의 끝소리 '르'가 어미 '-아', '-어' 앞에서 ㄹㄹ로 바뀌는 활용이다.
# 구르- + -어 → 굴러
# 무르- + -어 → 물러
# 누르- + -어 → 눌러
# 벼르- + -어 왔던 → 별러 왔던
# 이르- + -어 → 일러[5]
# 모르- + -아 → 몰라
# 마르- + -아 → 말라
# 다르- + -아 → 달라
# 사르- + -아 → 살라
# 바르- + -아 → 발라
# 가르- + -아 → 갈라
# 나르- + -아 → 날라
# 자르- + -아 → 잘라


irrR_MoR = klm.TransformedStem('몰','모르', atag="V+IRR+AMBI", score=1).incase(first)
irrR_MaR = klm.TransformedStem('말','마르', atag="V+IRR+AMBI", score=1).incase(first)
irrR_DaR = klm.TransformedStem('달','다르', atag="V+IRR+AMBI", score=1).incase(first)
irrR_SaR = klm.TransformedStem('살','사르', atag="V+IRR+AMBI", score=1).incase(first)
irrR_BaR = klm.TransformedStem('발','바르', atag="V+IRR+AMBI", score=1).incase(first)
irrR_GaR = klm.TransformedStem('갈','가르', atag="V+IRR+AMBI", score=1).incase(first)
irrR_NaR = klm.TransformedStem('날','나르', atag="V+IRR+AMBI", score=1).incase(first)
irrR_JaR = klm.TransformedStem('잘','자르', atag="V+IRR+AMBI", score=1).incase(first)

auxIrrLa = lm.regAux('라').incase(lm.onlyAfter).setpos('Y').after([
        irrR_MoR,irrR_MaR,irrR_DaR,irrR_SaR, irrR_BaR,irrR_GaR,irrR_NaR, irrR_JaR
        ])
auxIrrLat = lm.regAux('랐').incase(lm.onlyAfter).setpos('Y').after([
        irrR_MoR,irrR_MaR,irrR_DaR,irrR_SaR, irrR_BaR,irrR_GaR,irrR_NaR, irrR_JaR
        ])
aux.ecSeo.after(auxIrrLa)
aux.ecGo.after(auxIrrLat)

irrR_GuR = klm.TransformedStem('굴','구르', atag="V+IRR+AMBI", score=1).incase(first)
irrR_NuR = klm.TransformedStem('눌','누르', atag="V+IRR+AMBI", score=1).incase(first)
irrR_BuR = klm.TransformedStem('불','부르', atag="V+IRR+AMBI", score=1).incase(first)
irrR_MuR = klm.TransformedStem('물','무르', atag="V+IRR+AMBI", score=1).incase(first)
irrR_ByeoR = klm.TransformedStem('별','벼르', atag="V+IRR+AMBI", score=1).incase(first)
irrR_YiR = klm.TransformedStem('일','이르', atag="V+IRR+AMBI", score=1).incase(first)
irrR_JiR = klm.TransformedStem('질','지르', atag="V+IRR+AMBI", score=1)

auxIrrLeo = lm.regAux('러').incase(lm.onlyAfter).setpos('Y').after([
        irrR_GuR,irrR_NuR,irrR_BuR,irrR_MuR,irrR_ByeoR,irrR_YiR, irrR_JiR
        ])
        
auxIrrLeot = lm.regAux('렀').incase(lm.onlyAfter).setpos('Y').after([
        irrR_GuR,irrR_NuR,irrR_BuR,irrR_MuR,irrR_ByeoR,irrR_YiR, irrR_JiR
        ])
        
aux.ecSeo.after(auxIrrLeo)
aux.ecGo.after(auxIrrLeot)
##################################################
# <ㅂ 불규칙 동사/형용사>
# <모음조화에 따라 /ㅜ/로 바뀌는 경우>
# 덥- + -어 → 더워
# 우습- + -어 → 우스워
# 더럽- + -어 → 더러워
# 무섭- + -어 → 무서워
# 귀엽- + -어 → 귀여워
# 안쓰럽- + -어 → 안쓰러워
# 줍- + -어 → 주워
# 굽- + -어 → 구워
# ##################################################
irrB_U = klm.IrregularAux('우', headJongsung='ㅂ', tail='으', atag="ADJ|V+IRB").setpos('Y').incase([
                klm.ConstraintAfter(['나','더','스','러','서','주','구','고','도','다','까','로','벼'])]) 

irrB_Un = lm.regAux( klm.IrregularAux('운', headJongsung='ㅂ', tail='은', atag="ADJ|V+IRB").setpos('Y').incase([
        klm.ConstraintAfter(['나','더','스','러','서','주','구','고','도','다','까','로','벼' ]),
        final ]) )


irrB_Ul = lm.regAux( klm.IrregularAux('울', headJongsung='ㅂ', tail='을', atag="ADJ|V+IRB").setpos('Y').incase([
        klm.ConstraintAfter(['더','주','구','고','도','벼' ]),
        final ]) )

irrB_Ul2 = lm.regAux( klm.IrregularAux('울', headJongsung='ㅂ', tail='을', atag="ADJ|V+IRB" ).setpos('Y').incase([
        klm.ConstraintAfter(['나','스','러','서','여','로','다','까','벼' ]), klm.ConstraintMoreThanAfter(1), final ]) )

irrB_Wa = lm.regAux( klm.IrregularAux('와', headJongsung='ㅂ', tail='아', atag="ADJ|V+IRB") ).setpos('Y').incase([
        klm.ConstraintAfter(['고','도']), klm.ConstraintLessThanAfter(2) ])

irrB_Wa2 = lm.regAux( klm.IrregularAux('와', headJongsung='ㅂ', tail='아', atag="ADJ|V+IRB") ).setpos('Y').incase([
        klm.ConstraintAfter(['나','다','까','로' ]), klm.ConstraintMoreThanAfter(1) ]).setscore(-1)

irrB_Wat = klm.IrregularAux('왔', headJongsung='ㅂ', tail='았', atag="ADJ|V+IRB").setpos('Y').incase([
        klm.ConstraintAfter(['고','도']), klm.ConstraintLessThanAfter(2)])
        
irrB_Wat2 = klm.IrregularAux('왔', headJongsung='ㅂ', tail='았', atag="ADJ|V+IRB").setpos('Y').incase([
        klm.ConstraintAfter(['나','다','까','로' ]), klm.ConstraintMoreThanAfter(1)])
        
irrB_Weo = lm.regAux( klm.IrregularAux('워', headJongsung='ㅂ', tail='어', atag="ADJ|V+IRB") ).setpos('Y').incase([
        klm.ConstraintAfter(['더','주','구','고','도' ]) ]) 

irrB_Weo2 = lm.regAux( klm.IrregularAux('워', headJongsung='ㅂ', tail='어', atag="ADJ|V+IRB") ).setpos('Y').incase([
        klm.ConstraintAfter(['나','스','러','서','여','로','다','까','벼' ]), klm.ConstraintMoreThanAfter(1) ]) 

irrB_Weot = klm.IrregularAux('웠', headJongsung='ㅂ', tail='었', atag="ADJ|V+IRB").setpos('Y').incase([
        klm.ConstraintAfter(['더','주','구','고','도','누' ]) ]) 

irrB_Weot2 = klm.IrregularAux('웠', headJongsung='ㅂ', tail='었', atag="ADJ|V+IRB").setpos('Y').incase([
        klm.ConstraintAfter(['나','스','러','서','여','로','다','까','벼' ]), klm.ConstraintMoreThanAfter(1) ]) 

aux.ecNa.after([irrB_Weot2,irrB_Weot,irrB_Wat,irrB_Wat2])
aux.auxEu.after([irrB_Weot2,irrB_Weot,irrB_Wat,irrB_Wat2])
aux.auxEo.after([irrB_Weot2,irrB_Weot,irrB_Wat,irrB_Wat2])
aux.eptNeun.after([irrB_Weot2,irrB_Weot,irrB_Wat,irrB_Wat2])

aux.auxJi.after([irrB_Weot2,irrB_Weot,irrB_Wat,irrB_Wat2])
aux.ecDo.after([irrB_Weo, irrB_Weo2, irrB_Wa, irrB_Wa2])



aux.ecMyeon.after( irrB_U )
aux.ecMyeo.after( irrB_U )
aux.ecSeo.after([irrB_Wa,irrB_Wa2, irrB_Weo, irrB_Weo2])
aux.efnDa.after([irrB_Wat, irrB_Wat2, irrB_Weot,irrB_Weot2])
aux.ecGo.after([irrB_Wat,irrB_Wat2,irrB_Weot,irrB_Weot2])
aux.eppSeupNi.after([irrB_Wat,irrB_Wat2,irrB_Weot,irrB_Weot2])

aux.eptNeun.after([irrB_Wat,irrB_Wat2, irrB_Weot,irrB_Weot2])
aux.eptDeon.after([irrB_Wat,irrB_Wat2, irrB_Weot,irrB_Weot2])
aux.auxJi.after([irrB_Wa,irrB_Wa2, irrB_Weo, irrB_Weo2, irrB_Wat,irrB_Wat2, irrB_Weot,irrB_Weot2])
aux.ecJiMan.after([irrB_Wa,irrB_Wa2, irrB_Weo, irrB_Weo2, irrB_Wat,irrB_Wat2, irrB_Weot,irrB_Weot2])