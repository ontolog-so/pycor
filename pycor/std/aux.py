import sys
import pycor.langmodel as lm
import pycor.korlangmodel as klm
import pycor.std.stem as stm


afterJongsung = klm.ConstraintAfterJongsung()
afterVowel = klm.ConstraintAfterVowel()
afterPositiveVowel = klm.ConstraintAfterPositiveVowel()
afterNegativeVowel = klm.ConstraintAfterNegativeVowel()
afterVowel = klm.ConstraintAfterVowel()
final =  klm.ConstraintFinal()
first = klm.ConstraintFirst()
 
###################################
# 어미 반복 요소들 
###################################
auxA = lm.Aux('아').incase([afterJongsung, afterPositiveVowel])
auxEo = lm.Aux('어').incase([afterJongsung, afterNegativeVowel])

auxYeo = lm.Aux('여').incase([afterVowel])
auxEu = lm.Aux('으').incase(afterJongsung)
auxRi = lm.Aux('리').incase([afterJongsung, afterNegativeVowel])
auxRyeo = lm.Aux('려')
auxRyeot = klm.TransformedAux('렸','리','었').tag("EPT-pp" )

auxDoae = lm.regAux( klm.TransformedAux('돼','되','어') ).ambiguous()
auxHae = lm.regAux( klm.TransformedAux('해','하', 'ㅣ') ).ambiguous()
auxJieo = lm.regAux( klm.TransformedAux('져','지','어').after([auxHae]) ).ambiguous()



auxStemDoeEo = lm.Aux('어').incase(lm.onlyAfter).after(lm.StemAux('되'))

jkpI = lm.Aux('이').tag('JKP')
jkpIEot = lm.Aux('었').tag('EPT-pp').incase(lm.onlyAfter).after(jkpI)
jkpYeot = lm.Aux('였').tag("EPT-pp" ).incase([afterVowel])
jkpIn = lm.Aux('인').tag('JKP')

auxJi  = lm.Aux('지').after([auxHae,auxDoae,jkpI,jkpIEot,jkpYeot,jkpIn])
auxI  = lm.Aux('이').incase(afterJongsung)

auxKyeo = lm.regAux(klm.TransformedAux('켜','키','어', escapeFirst=False).tag("EPT-pp" ))

stemAuxHa = lm.regAux(lm.StemAux('하'))
#########################################################################################################
# 한국어 어미 
#########################################################################################################

###################################
# EP 선어말 어미
###################################
#----------------------------------
# EPT	시제 선어말 어미
# 현재	-(느)ㄴ-	읽는다, 밟는다, 참는다, 솟는다
# 과거	-았-/-었-/-였-	읽었다, 밟았다, 참았다, 솟았다
# 과거 (회상)	-더-	읽더라, 밟더라, 참더라, 솟더라
# 추측	-겠-	읽었겠다, 밟았겠다, 참았겠다, 솟았겠다
# 미래	-겠-	읽겠다, 밟겠다, 참겠다, 솟겠다
# 미래 (의지)	-(으)리-	읽으리라, 밟으리라, 참으리라
#----------------------------------
eptNeun = lm.Aux('는').tag("EPT-pr")
#eptN  = klm.buildJongsungAux('ㄴ').tag("EPT-pr")
eptAt = lm.Aux('았').tag("EPT-pp").incase([afterJongsung,afterPositiveVowel])
eptEot = lm.Aux('었').tag("EPT-pp")
eptYeot = lm.Aux('였').tag("EPT-pp").incase(lm.onlyAfter).after(stemAuxHa)
eptGet = lm.Aux('겠').tag("EPT-f")
eptGet2 = lm.Aux('겠').tag("EPT-guess")
eptDeo = lm.Aux('더').tag("EPT-pp")
eptDeon = lm.regAux('던').tag("EPT-pp")
eptRiRa = lm.regMultiSyllablesAux('리라').tag("EPT-f").after([
        auxEu
        ])


#eptTimeSet = [eptNeun, eptN, eptAt,eptEot,eptYeot,eptGet,eptGet2]
eptTimeSet = [eptNeun, eptAt,eptEot,eptYeot,eptGet,eptGet2]

constraintsPastException = klm.ConstraintNotAfter(['했','혔','됐','갔','봤','잤','왔','줬','졌','았','었','였','렸', '웠', '왔'])

eptPasts = [
    klm.TransformedAux('갔','가','았', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('겼','기','었', escapeFirst=True).tag("EPT-pp" ),
    klm.TransformedAux('꼈','끼','었', escapeFirst=True).tag("EPT-pp" ),
    klm.TransformedAux('됐','되','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('뒀','두','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('랐','르','았', escapeFirst=False).tag("EPT-pp" ),
    auxRyeot,
    klm.TransformedAux('쌌','싸','았', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('썼','쓰','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('왔','오','았', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('였','이','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('웠','우','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('봤','보','았', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('잤','자','았', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('줬','주','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('챘','채','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('켰','키','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('졌','지','었', escapeFirst=False).tag("EPT-pp").after(auxHae),
    klm.TransformedAux('쳤','치','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('탔','타','았', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('했','하','였', escapeFirst=False).tag("EPT-pp" ).setscore(2),
    klm.TransformedAux('혔','히','었').tag("EPT-pp" ),
    eptAt, eptEot, eptYeot
]

eptDeon.after([eptAt, eptEot, eptYeot])
eptDeon.after(eptPasts)
auxEu.after([eptAt, eptEot, eptYeot, jkpIEot, jkpYeot])
auxEu.after(eptPasts)
auxJi.after([eptPasts, eptTimeSet])
eptNeun.after(eptPasts)

eptGet2.incase(lm.onlyAfter).after(eptPasts)

#----------------------------------
# EPH	존칭 선어말 어미
# 주체 높임	-(으)시-	잡으시고, 뽑으시고, 참으시고, 드시고
#----------------------------------
ephSi = lm.Aux('시').tag("EPH").after([
        auxEu
        ])
ephSin = lm.Aux('신').tag("EPH+EPT-pr").after([
        auxEu
        ])
ephSil = lm.Aux('살').tag("EPH+EPT-f").after([
        auxEu
        ])


ephSyeot = lm.Aux('셨').tag("EPH+EPT-pp").after([
        auxEu
        ])
#----------------------------------
# EPP	공손 선어말 어미
# -삽-, -(으)옵-	웃삽고, 가옵고, 그러하옵고, 기쁘옵고
#----------------------------------
eppOp = lm.Aux('옵').tag("EPP").after([
        auxEu
        ])
eppSeupNi = lm.MultiSyllablesAux('습니').tag("EPP")

# 현재 시제 는
eptNeun.after([ephSi, eptGet])

eptGet2.after([ephSi])

###################################
# 선어말 어미 조합들 
###################################

# 과거 시제 었  
eptEot.after([eptEot, eptYeot, eptGet2, ephSi, auxJi])
eptEot.after(eptPasts)

# 회상/추측  더 
eptDeo.after([eptEot, eptGet2])


###################################
# ET 전성 어미
###################################
###################################
# ETN	명사형 전성 어미
# -(으)ㅁ, -기
###################################
etnEum = lm.Aux('음').tag("ETN").incase(afterJongsung)
etnM = klm.JongsungAux(['함','됨','짐'],'ㅁ').tag("ETN") 
etnGi = lm.regAux('기').tag("ETN").setscore(-1).ambiguous()

etnIm = lm.Aux(['임']).tag("ETN").tag("JKP")

# ~음으-, ~ㅁ으-
auxEu.after([etnEum,etnM])

###################################
# ETM	관형사형 전성 어미 
# -(으)ㄴ, -는, -(으)ㄹ
###################################
etmEun = lm.regAux('은').tag("ETM").incase(afterJongsung).after([etnEum, etnM]).setscore(-2)
etmNeun = lm.regAux('는').tag("ETM").incase(afterVowel).after([etnGi]).setscore(-2)
etmN = lm.regAux(klm.JongsungAux(['린','된','한','친'], 'ㄴ')).tag("ETM").setscore(-3).ambiguous()
etmEul = lm.regAux('을').tag("ETM").incase(afterJongsung).setscore(-2)
etmL = lm.regAux(klm.JongsungAux(['릴','될','할','칠'], 'ㄹ')).tag("ETM").setscore(-3)

etmSiKin = lm.regAux(klm.JongsungAux('킨', 'ㄴ')).tag("ETM").incase(lm.ConstraintAfter('시'))
etmHaeJin = lm.regAux(klm.JongsungAux('진', 'ㄴ')).tag("ETM").incase(lm.ConstraintAfter('해'))

etmSiKil = lm.regAux(klm.JongsungAux('킬', 'ㄹ')).tag("ETM").incase(lm.ConstraintAfter('시'))
etmHaeJil = lm.regAux(klm.JongsungAux('질', 'ㄹ')).tag("ETM").incase(lm.ConstraintAfter('해'))

etmNeun.after([auxRi,auxRyeo, ephSi, auxRyeo])
etmEul.after(eptPasts)

###################################
# ETA	부사형 전성 어미 
# -이, -게, -도록
###################################
etaY = lm.regAux('이').tag("ETA").incase(afterJongsung).setscore(-2)
etaGe = lm.regAux('게').tag("ETA").setscore(-2)
etaDoRok = lm.regMultiSyllablesAux('도록').tag("ETA").setscore(-2)


###################################
# EFN	평서형 종결 어미 
# -다/-는다-/-ㄴ다
# -구나/-는구나
# -군/는군
# -네
# -으마/-마
# -을걸/-ㄹ걸
# -을게/ㄹ게
# -을래/-ㄹ래
# -을라/-ㄹ라
# -는단다/-ㄴ단다/-단다
# -란다
###################################
efnDa = lm.regAux('다').tag("EFN").after([
        klm.buildJongsungAux('ㄴ'),
        eptNeun
        ])

efnNiDa = lm.regMultiSyllablesAux('니다').tag("EFN").after([
        lm.Aux('십'), 
        lm.Aux('습').after(eptPasts),
        klm.TransformedAux('합','하','니')
])

efnDa.after(eptTimeSet).after(eptPasts)
efnDa.after([ephSyeot,ephSin,auxRi,eppSeupNi, eptAt,eptEot,eptYeot])

efnDanDa = lm.regMultiSyllablesAux('단다').tag("EFN").after([
        klm.buildJongsungAux('ㄴ').tag("EFN"),
        eptNeun
        ])
efnDanDa.after(eptTimeSet).after(eptPasts)
efnDanDa.after([ephSyeot,ephSin,eptAt,eptEot])
        
efnRanDa = lm.regMultiSyllablesAux('란다').tag("EFN").incase(afterVowel).after([
        auxI, eptDeo
        ])

efnGuNa = lm.regMultiSyllablesAux('구나').tag("EFN").after([
        eptNeun, eptDeo
        ])
efnGuNa.after(eptTimeSet).after(eptPasts)
efnGuNa.after([ephSyeot,eptAt,eptEot])

efnGun = lm.regAux('군').tag("EFN").after([
        eptNeun, eptDeo
        ])
efnGun.after([eptTimeSet,eptAt,eptEot])

efnNe = lm.regAux('네').tag("EFN")
efnNe.after(eptTimeSet).after(eptPasts)
efnNe.after([ephSi, ephSyeot, eptAt,eptEot])

efnMa = lm.regAux('마').tag("EFN").incase(afterVowel).after([
        auxEu
        ])

efnGeol = lm.regAux(['걸','게']).tag("EFN").incase(lm.onlyAfter).after([
        klm.buildJongsungAux('ㄹ').tag("EFN"),
        lm.Aux('을').tag("EFN").incase(afterJongsung)
        ])

efnRa = lm.regAux(['래','라']).tag("EFN").incase(lm.onlyAfter).after([
        klm.buildJongsungAux('ㄹ').tag("EFN"),
        lm.Aux('을').tag("EFN").incase(afterJongsung),
        eptDeo
        ])

###################################
# EFQ	의문형 종결 어미
# -으냐/-냐/-느냐
# -으니/-니
# -련
# -으랴/-랴
# -을쏘냐/-ㄹ쏘냐
# -대, -담
###################################
efqNya = lm.regAux('냐').tag("EFQ").after([
        lm.Aux('느').tag("EFQ"),
        auxEu
        ])
efqNi = lm.regAux('니').tag("EFQ").after([
        auxEu
        ])
efqGa = lm.regAux('가').tag("EFQ").after([
        eptNeun
        ])     
efqJi = lm.regAux('지').tag("EFQ").after([
        eptNeun
        ])     
efqRyeon = lm.regAux('련').tag("EFQ")

efnSoNya = lm.regMultiSyllablesAux('쏘냐').tag("EFQ").incase(lm.onlyAfter).after([
        klm.buildJongsungAux('ㄹ').tag("EFQ"),
        lm.Aux('을').tag("EFQ").incase(afterJongsung)
        ])
#efqDae = lm.regAux('대').tag("EFQ").setscore(-2)
#efqDam = lm.regAux('담').tag("EFQ").setscore(-2)

efqNya.after([eptAt,eptEot])
efqNi.after([eptAt,eptEot])

###################################
# EFO	명령형 종결 어미
# -아라/-어라/-여라
# -으려무나/려무나
# -으렴/-렴
# -소서
# -아/-어
# -지
###################################
efoRa = lm.regAux('라').tag("EFO").incase(afterVowel).after([
        auxA, auxEo,
        lm.Aux('여').tag("EFO").incase([afterJongsung, afterNegativeVowel]),
        lm.Aux('여').tag("EFO").incase([afterVowel])
        ])
efoRyeoMuNa = lm.regMultiSyllablesAux('려무나').tag("EFO").incase(afterVowel).after([
        auxEu
        ])
efoRyeom = lm.regAux('렴').tag("EFO").incase(afterVowel).after([
        auxEu
        ])
efoSoSeo = lm.regMultiSyllablesAux('소서').tag("EFO").incase(afterVowel).after([
        auxEu
        ])
efoA = lm.regAux('아').tag("EFO").incase([afterJongsung, afterPositiveVowel])
efoEo = lm.regAux('어').tag("EFO").incase([afterJongsung, afterNegativeVowel])
efoJi = lm.regAux('지').tag("EFO")

###################################
# EFA	청유형 종결 어미
# -자, -(으)ㅂ시다, -세
###################################
efoJa = lm.regAux('자').tag("EFA")
efoSiDa = lm.regMultiSyllablesAux('시다').tag("EFA").incase(lm.onlyAfter).after([
        klm.buildJongsungAux('ㅂ').tag("EFA"),
        lm.Aux('읍').tag("EFA").incase(afterJongsung)
        ])
efoSe = lm.regAux('세').tag("EFA")

###################################
# EFI	감탄형 종결 어미
# -는구나, -도다
###################################
efiNeunGuNa = lm.regMultiSyllablesAux('구나').incase(lm.onlyAfter).tag("EFI").after(eptNeun)
efiDoDa = lm.regMultiSyllablesAux('도다').tag("EFI").after(eptNeun)

###################################
# EC 연결 어미 
###################################
#----------------------------------
# EC 연결 어미 > 나열 : ~고, ~(으)며
#----------------------------------
ecGo = lm.regAux('고').tag("EC-and")
ecMyeo = lm.regAux('며').tag("EC-and").incase(afterVowel).after([
        auxEu
        ])


ecGo.after([efnDa, ephSi, eptYeot, eptEot, eptAt])
ecGo.after(eptPasts)
ecMyeo.after([efnDa, ephSi])

#----------------------------------
# EC 연결 어미 > 동시에 나열 : ~(으)면서,~자, ~자마자
#----------------------------------
ecMyeonSeo = lm.regMultiSyllablesAux('면서').tag("EC-and").incase(afterVowel).after([
        auxEu, efnDa  
        ])
ecJa = lm.regAux('자').tag("EC-and").after([
        lm.MultiSyllablesAux('자마'), jkpI
        ])


#----------------------------------
# EC 연결 어미 > 시간 전환 : ~다가
#----------------------------------
ecDaGa = lm.regMultiSyllablesAux('다가').tag("EC-and")
ecDaGa.after(eptPasts)

#----------------------------------
# EC 연결 어미 > 대립/대조 : ~(으)나, ~만, ~는데/~(으)ㄴ데, ~아도/어도
#----------------------------------
ecNa = lm.regAux('나').tag("EC-but").incase(afterVowel).after([
        auxEu
        ])
ecJiMan = lm.regAux('만').tag("EC-but").after([
        auxJi
        ])

ecDe = lm.regAux('데').tag("EC-but").incase(lm.onlyAfter).after([
        eptNeun
        ])
ecDo = lm.regAux('도').tag("EC-but").incase(lm.onlyAfter).after([
        auxA, auxEo, auxHae, auxDoae, auxYeo, ecMyeonSeo, etaGe
        ])

ecDeDa = lm.regAux('다').tag("EC-and").incase(lm.onlyAfter).after([
        ecDe
        ])
#----------------------------------
# EC 연결 어미 > 이유/원인 : ~아서/어서, ~(으)니, ~(으)니까, ~(으)므로, ~느라고
#----------------------------------
ecSeo = lm.regAux('서').tag("EC-because").incase(afterVowel).after([
        auxA, auxEo, auxHae, auxYeo, auxStemDoeEo
        ])
ecNi = lm.regAux('니').tag("EC-because").incase(afterVowel).after([
        auxEu
        ])
ecNiGga = lm.regMultiSyllablesAux('니까').tag("EC-because").incase(afterVowel).after([
        auxEu
        ])
ecMeuRo = lm.regMultiSyllablesAux('므로').tag("EC-because").incase(afterVowel).after([
        auxEu, jkpI, jkpIEot, jkpYeot
        ])

#----------------------------------
# EC 연결 어미 > 조건 : ~(으)면,~(으)려면, ~아야/어야
#----------------------------------
ecMyeon = lm.regAux('면').tag("EC-incase").incase(afterVowel).after([
        auxEu
        ])
ecRyeoMyeon = lm.regMultiSyllablesAux('려면').tag("EC-to").incase(afterVowel).after([
        auxEu
        ])
ecYa = lm.regAux('야').tag("EC-incase").incase(afterVowel).after([
        auxA, auxEo, auxYeo, ecMyeon, auxKyeo
        ])

# ~아야, ~어야 
ecYa.after([auxA, auxEo, auxHae, auxStemDoeEo])
#----------------------------------
# EC 연결 어미 > 목적 : ~(으)러, ~(으)려고, ~도록, ~게
#----------------------------------
ecReo = lm.regAux('러').tag("EC-for").incase(afterVowel).after([
        auxEu
        ])
ecRyeoGo = lm.regMultiSyllablesAux('려고').tag("EC-for").incase(afterVowel).after([
        auxEu
        ])
ecDoRok = lm.regMultiSyllablesAux('도록').tag("EC-for")
ecGe = lm.regAux('게').tag("EC-for") 

#----------------------------------
# EC 연결 어미 > 인정 : ~아도/어도, ~(으)ㄹ지라도, ~더라도
#----------------------------------
ecDo2 = lm.regAux('도').tag("EC-may").incase(lm.onlyAfter).after([
        auxA, auxEo
        ])
ecJiRaDo = lm.regMultiSyllablesAux('지라도').tag("EC-evenif").incase(afterJongsung).after([
        lm.Aux('을').tag("EC-evenif").incase(afterJongsung),
        lm.Aux('일').tag("EC-evenif"),
        klm.buildJongsungAux('ㄹ').tag("EC-evenif")
        ])
#----------------------------------
# EC 연결 어미 > 선택 : ~거나, ~든지
#----------------------------------
ecGeoNa = lm.regMultiSyllablesAux('거나').tag("EC-or").after([jkpI])
ecDeunJi = lm.regMultiSyllablesAux('든지').tag("EC-or").after([jkpI])

ecGeoNa.after([eptEot, eptAt, eptYeot, efnDa])
ecDeunJi.after([eptEot, eptAt, eptYeot, efnDa])
#----------------------------------
# EC 연결 어미 > 방법/수단 : ~아서/어서, ~고
#----------------------------------
#ecSeo2 = lm.regAux('서').tag("EC-by").incase(afterVowel).after([
#        lm.Aux('아').tag("EC-by").incase([afterJongsung, afterPositiveVowel]),
#        lm.Aux('어').tag("EC-by").incase([afterJongsung, afterNegativeVowel])
#        ])
#ecGo2 = lm.regAux('고').tag("EC-by")

#----------------------------------
# EC 연결 어미 > 배경 : ~는데/~(으)ㄴ데, ~(으)니
#----------------------------------
ecDe2 = lm.regAux('데').tag("EC-while").incase(afterVowel).after([
        etmEun, etmNeun, jkpIn, 
        klm.buildJongsungAux('ㄴ').tag("EC-while")
        ])

ecNi2 = lm.regAux('니').tag("EC-while").incase(afterVowel).after([
        auxEu, 
        lm.Aux('더')
        ])




#########################################################################################################
# 어미 조합  
#########################################################################################################
# ~이라, ~다라 
auxRa = lm.Aux('라').after([efnDa,jkpI])

ecMyeonSeo.after(auxRa)


#########################################################################################################
# 한국어 조사 
#########################################################################################################
###################################
# JKS	주격 조사 
# 이/가, 께서, 에서, (서)
###################################
jksI = lm.regAux('이').tag("JKS").incase([afterJongsung,final])
jksGa = lm.regAux('가').tag("JKS").incase([afterVowel,final])
jksSeo = lm.regAux(['서']).tag("JKS").setscore(-2).incase([lm.onlyAfter]).after([
        lm.Aux('께').tag("JKS").setscore(-1),
        lm.Aux('에').tag("JKS").setscore(-2),
        ])

jksI.after([etnEum, etnM, etnIm])
jksGa.after([etnGi ])

###################################
# JKP	서술격 조사*
# 이다 , 다  
###################################
jkpIda = lm.regAux('다').tag("JKP" ).after([
        jkpI, etnGi,jkpIEot,jkpYeot,
        lm.Aux('니').incase(lm.onlyAfter).after(lm.Aux('입').tag("JKP" )),
        ]) 

###################################
# JKC	보격 조사 
# 이/가
###################################
jkcI = lm.regAux('이').tag("JKC").incase([afterJongsung,final])
jkcGa = lm.regAux('가').tag("JKC").incase([afterVowel,final])

# jkcI = lm.regAux('이').tag("JKC").incase([afterJongsung,final,
#         lm.ConstraintCollocation(nextWordFirst='되')
#                 .Or(lm.ConstraintCollocation(nextWordFirst='된'))
#                 .Or(lm.ConstraintCollocation(nextWordFirst='안'))
#                 .Or(lm.ConstraintCollocation(nextWordFirst='아니'))
#                 .Or(lm.ConstraintCollocation(nextWordFirst='아닌'))
#         ])
# jkcGa = lm.regAux('가').tag("JKC").incase([afterVowel,final,
#         lm.ConstraintCollocation(nextWordFirst='되')
#                 .Or(lm.ConstraintCollocation(nextWordFirst='된'))
#                 .Or(lm.ConstraintCollocation(nextWordFirst='안'))
#                 .Or(lm.ConstraintCollocation(nextWordFirst='아니'))
#                 .Or(lm.ConstraintCollocation(nextWordFirst='아닌'))
#         ])

jkcI.after([etnEum, etnM, etnIm])
jkcGa.after([etnGi ])

###################################
# JKG	관형격 조사 
# 의
###################################
jkgEui = lm.regAux(['의']).tag("JKG").incase([final])

jkgEui.after([etnEum, etnM,etnGi])

# 원래는 동사의 관형사 형이나 일상적으로 관형격 조사로 잘못쓰임  
errGatEun = lm.regMultiSyllablesAux('같은').tag("JKG-as") 


###################################
# JKO	목적격 조사 
# 을/를/ㄹ
###################################
jkoEul = lm.regAux('을').tag("JKO").incase([afterJongsung])
jkoReul = lm.regAux('를').tag("JKO").incase([afterVowel])
#auxL = lm.regAux( klm.buildJongsungAux('ㄹ') ).tag("JKO").ambiguous()
# ㄹ은 제한적으로 
jkoEul.after([etnM, etnIm])
jkoReul.after([efqGa, efqNya, efqJi])

###################################
# JKB	부사격 조사 
###################################
# JKB-TO 수혜격 조사: 에/에게/께/한테
###################################
jkbE_to = lm.regAux('에').tag("JKB-TO")
jkbEGe = lm.regMultiSyllablesAux('에게').tag("JKB-TO") 
jkbGge = lm.regAux('께').tag("JKB-TO")
jkbHante = lm.regMultiSyllablesAux('한테').tag("JKB-TO") 

jkbE_to.after([etnEum, etnM,etnGi])

###################################
# JKB-FM 원천격 조사: 에서/에게서/에서부터
###################################
jkbESeo = lm.regMultiSyllablesAux('에서').tag("JKB-FM")  
jkbEGeSeo = lm.regMultiSyllablesAux('에게서').tag("JKB-FM") 
jkbBuTeo = lm.regMultiSyllablesAux('부터').tag("JKB-FM")

jkbBuTeo.after([jkbESeo,jkbEGeSeo,etnEum, etnM,etnGi])
jkbESeo.after([etnEum, etnM,etnGi])

#----------------------------------
# JX 부터/로부터/으로부터
#----------------------------------
jxBuTeo = lm.regMultiSyllablesAux('부터').tag("JX-from").after([
        lm.Aux('로').tag("JX-from").after([auxEu, etnGi])
        ])


###################################
# JKB-CM 비교격 조사: 보다
###################################
jkbBoDa = lm.regMultiSyllablesAux('보다').tag("JKB-CM").after([etnEum, etnM,etnGi])

###################################
# JKB-TT 방향격 조사: (으)로
# JKB-AS 위격 조사: (으)로(서)
# JKB-BY  도구격 조사: (으)로(써)
###################################
jkbEuRo = lm.regAux('로').tag("JKB-TT|AS|BY").after([auxEu,etnGi])
jkbRoSeo = lm.regMultiSyllablesAux('로서').tag("JKB-AS")
jkbEuRoSeo = lm.regMultiSyllablesAux('으로서').tag("JKB-AS")
jkbEuRoSseo = lm.regMultiSyllablesAux('으로써').tag("JKB-BY").after([etnEum, etnM,etnGi])



###################################
# JKB-WZ  동반격 조사: 와/과, (이)랑
###################################
jkbWa = lm.regAux('와').tag("JKB-WZ").incase(afterVowel).after([etnGi])
jkbGwa = lm.regAux('과').tag("JKB-WZ").incase(afterJongsung).after([etnEum, etnM])
jkbIRang = lm.regAux('랑').tag("JKB-WZ").after(lm.Aux('이').tag("JKB-WZ"))

###################################
# JKB-AT  시간을 나타내는 조사: 에
###################################
jkbE_at = lm.regAux('에').tag("JKB-AT")
###################################
# JKB-LK   같이, 처럼
###################################
jkbGatYi = lm.regMultiSyllablesAux('같이').tag("JKB-LK").after([etnEum, etnM,etnGi])
jkbCheoReom = lm.regMultiSyllablesAux('처럼').tag("JKB-LK").after([etnEum, etnM,etnGi])

###################################
# JKV	호격 조사 
# 야/아, 여/이여/이시여
###################################
jkvA = lm.regAux('아').tag("JKV").incase(afterJongsung)
jkvYa = lm.regAux('야').tag("JKV").incase(afterVowel)
jkvYeo = lm.regAux('여').tag("JKV").incase(afterVowel).after([
        lm.Aux('이').tag("JKV").incase(afterJongsung),
        lm.Aux('시').tag("JKV").incase(afterVowel).after(
                lm.Aux('이').tag("JKV").incase(afterJongsung))
        ])

###################################
# JKQ	인용격 조사 
# 고, 라고, ~이라고
###################################
jkqGo = lm.regAux('고').tag("JKQ").after([
        efnDa, auxRa
        ])


###################################
# JC	접속 조사(이음토씨)
# 와/과, 하고, 이며, 에다, (이)랑
###################################
jcWa = lm.regAux('와').tag("JC").incase(afterVowel).after([etnGi])
jcGwa = lm.regAux('과').tag("JC").incase(afterJongsung).after([etnEum, etnM])
jcHaGo = lm.regMultiSyllablesAux('하고').tag("JC").setscore(-1).ambiguous()
jcIMyeo = lm.regMultiSyllablesAux('이며').tag("JC").after([etnEum, etnM,etnGi])
jcEDa = lm.regMultiSyllablesAux('에다').tag("JC").after([etnEum, etnM,etnGi]) 
jcIRang = lm.regAux('랑').tag("JC").incase(afterVowel).after(lm.Aux('이').tag("JC").incase(afterJongsung))

###################################
# JX	보조사 
###################################
#----------------------------------
# JX 보조사 은/는/-ㄴ, 도
#----------------------------------
jxEun = lm.regAux('은').tag("JX-SO").incase([afterJongsung,final]).after([etnEum, etnM ])
jxNeun = lm.regAux('는').tag("JX-SO").incase([afterVowel,final]).after([etnGi])
jxN = lm.regAux(klm.JongsungAux(['난,넌,린'], jongsungs="ㄴ")).tag("JX-SO").incase([afterVowel,final])
jxDo = lm.regAux('도').tag("JX-SO").incase([final])

jxDo.after([jkbESeo,jkbE_at,jkbE_to,jkbEGe,jkbEuRo,jkqGo,efqGa, efqNya, efqJi, etnGi])
jxNeun.after([efqGa, efqNya, efqJi])

#----------------------------------
# JX 보조사 까지, 마저, 조차
#----------------------------------
jxGgaJi = lm.regMultiSyllablesAux('까지').tag("JX").after([etnEum, etnM,etnGi])
jxMaJeo = lm.regMultiSyllablesAux('마저').tag("JX").after([etnEum, etnM,etnGi]) 
jxMaDa = lm.regMultiSyllablesAux('마다').tag("JX").after([etnEum, etnM,etnGi]) 
jxJoCha = lm.regMultiSyllablesAux('조차').tag("JX").after([etnEum, etnM,etnGi])

# ~에서도, ~에도, ~에게도, ~으로도, ~까지도, ~마저도 , ~조차도 , ~(으)로도
jxDo.after([jkbESeo,jkbE_at,jkbE_to,jkbEGe,jkbEuRo,jxGgaJi,jxMaJeo,jxJoCha,jkbEuRo])
# ~에서조차, ~에조차, ~에게조차, ~으로조차,
jxJoCha.after([jkbESeo,jkbE_at,jkbE_to,jkbEGe,jkbEuRo])
# ~으로까지 
jxGgaJi.after([jkbEuRo])
#----------------------------------
# JX 보조사 뿐/만
#----------------------------------
jxBbun = lm.regAux('뿐').tag("JX").after([etnEum, etnM,etnGi]) 
jxMan = lm.regAux('만').tag("JX").after([
        etnEum, etnM, etnGi, lm.Aux('야').incase(afterVowel), jkqGo, jkbEuRoSeo, jkbRoSeo
        ]) 
jxEun.after(jxMan)

#----------------------------------
# JX 보조사 밖에
#----------------------------------
jxBakE = lm.regMultiSyllablesAux('밖에').tag("JX").after([etnEum, etnM,etnGi, jkqGo]) 
#----------------------------------
# JX 보조사 마는
#----------------------------------
jxMaNeun = lm.regMultiSyllablesAux('마는').tag("JX") 

#----------------------------------
# JX 보조사 일랑
#----------------------------------
jxIlLang = lm.regMultiSyllablesAux('일랑').tag("JX").after([etnEum, etnM,etnGi]) 

#----------------------------------
# JX 보조사 커녕/ㄴ커녕/는커녕/은커녕 
#----------------------------------
jxKeoNyoung = lm.regMultiSyllablesAux('커녕').tag("JX").after([
        klm.JongsungAux(['긴'], jongsungs="ㄴ").tag("JX"),
        etmEun,
        etmNeun,
        ])
#----------------------------------
# JX 보조사 손
#----------------------------------
jxSon = lm.regAux('손').tag("JX") 
#----------------------------------
# JX 보조사 들/ㄴ들/인들/엔들
#----------------------------------
jxDeul = lm.regAux('들').tag("JX").after([
        klm.buildJongsungAux('ㄴ').tag("JX"),
        lm.Aux('인').incase([afterJongsung]).tag("JX"),
        lm.Aux('엔').incase([afterVowel]).tag("JX"),
        ])
#----------------------------------
#----------------------------------
#----------------------------------
# JX 보조사 그래/그려
#----------------------------------
jxGre = lm.regMultiSyllablesAux('그래').tag("JX") 
jxGryeo = lm.regMultiSyllablesAux('그려').tag("JX") 

#----------------------------------
# JX 보조사 따라
#----------------------------------
jxDdaRa = lm.regMultiSyllablesAux('따라').tag("JX") 
#----------------------------------
# JX 보조사 토록
#----------------------------------
jxToRok = lm.regMultiSyllablesAux('토록').tag("JX") 
#----------------------------------
# JX 보조사 치고
#----------------------------------
jxChiGo = lm.regMultiSyllablesAux('치고').tag("JX") 
#----------------------------------
# JX 보조사 ㄴ즉/인즉
jxJeuk = lm.regAux('즉').tag("JX").after([klm.buildJongsungAux('ㄴ').tag("JX")])
jxInJeuk = lm.regMultiSyllablesAux('인즉').tag("JX") 
#----------------------------------
# JX 보조사 대로
#----------------------------------
jxDaeRo = lm.regMultiSyllablesAux('대로').tag("JX") 

#----------------------------------
# JX 보조사 받침에 따라 '이'가 앞에 붙는 조사
#  (이)나
#  (이)란
#  (이)든지
#  (이)나마
#  (이)야(말로)
jxNa = lm.regAux('나').tag("JX").incase(afterVowel).after(jkpI)
jxRan = lm.regAux('란').tag("JX").incase(afterVowel).after(jkpI)
jxDeunJi = lm.regMultiSyllablesAux('든지').incase(afterVowel).tag("JX").after(jkpI)
jxNaMa = lm.regMultiSyllablesAux('나마').incase(afterVowel).tag("JX").after(jkpI)
jxYa = lm.regAux('야').tag("JX").incase(afterVowel).after(jkpI)




###################################
#  어미 - 조사 조합 
###################################

auxKe = lm.Aux('케').tag('PAS')

auxHa = lm.Aux('하').incase(lm.onlyAfter).after([jkqGo,auxKe])
auxHan = lm.regAux('한').incase(lm.onlyAfter).after([jkqGo,auxKe])

# ~하지 
auxHaJi = lm.regAux('지').after([auxHa])

# ~지도 , ~이라도, ~라도, ~보다도 
jxDo.after([auxJi,auxRa, jkbBoDa])
# ~하지 
auxJi.after([auxHa])

# ~이던, ~이었던, ~였던 
eptDeon.after([jkpI, jkpIEot,jkpYeot])

# ~하다, ~한다, ~지다  
efnDa.after([auxHa, auxHan, auxJi])
# ~하자, ~지자, ~이자 
ecJa.after([auxHa,auxJi,auxI])
# ~하는, ~다는, ~지는, ~이라는, ~라는, ~다라는
etmNeun.after([auxHa,auxJi,efnDa,auxRa]) 
# ~하면, ~다면, ~지면 ~이면, ~이라면, ~다라면, ~라면
ecMyeon.after([auxHa,auxJi,efnDa,auxI,auxRa])
# ~하기, ~했기
etnGi.after([eptPasts])

# ~이기 
etnGi.after(jkpI)

# ~이고 ,~이었고, ~였고
ecGo.after([jkpI, jkpIEot,jkpYeot])

# ~음을 ~ㅁ을
jkoEul.after([etnEum, etnM])
# ~음은 ~ㅁ은
jxEun.after([etnEum,etnM])
# ~음이 ~ㅁ이
jkcI.after([etnEum,etnM])
# ~음이, ~ㅁ이 
auxI.after([etnEum, etnM])
# ~기를 
jkoReul.after([etnGi ])
# ~기가  
jkcGa.after([etnGi ])

# ~했음
etnEum.after(eptPasts)

# ~에서의, ~부터의 , ~까지의, ~와의, ~고의, ~하고의 , ~에의 , ~으로의, ~로서의 , ~으로서의, ~으로써의 
jkgEui.after([jkbESeo, jkbBuTeo,jxBuTeo, jxGgaJi, jcWa, jcGwa, 
        jcHaGo, jkbE_to, jkbEuRo, jkbRoSeo, jkbEuRoSeo, jkbEuRoSseo])

# ~에서도, ~부터도 , ~까지도, ~와도, ~고도, ~하고도 , ~에도 , ~으로도, ~로서도 , ~으로서도, ~으로써도 
ecDo.after([jkbESeo, jkbBuTeo,jxBuTeo, jxGgaJi, jcWa, jcGwa, 
        jcHaGo, jkbE_to,jkbEuRo, jkbRoSeo, jkbEuRoSeo, jkbEuRoSseo])

# ~에서만 ~부터만 
jxMan.after([jkbESeo,jkbEGe,jkbE_to, jkbBuTeo,jxBuTeo])

# ~는 
jxNeun.after([jkbWa,jkbGwa,jksI,jkbE_to,jkbEGe,jkbGge,jkbHante,jkbESeo,jkbEGeSeo,jkbBuTeo,jxBuTeo,
        jkbBoDa,jkbEuRo,jkbEuRoSeo,jkbRoSeo,jkbEuRoSseo,jkbE_at,jkbGatYi,jkqGo,jcHaGo,ecSeo])
# ~은 
jxNeun.after([jkbIRang,jkbCheoReom])

# ~되어있다, 되어있는, 되어있을
auxStemIt = lm.Aux('있').incase(lm.onlyAfter).after(auxStemDoeEo)
efnDa.after(auxStemIt)
etmNeun.after(auxStemIt)
etmEul.after(auxStemIt)

##################################################
# 띄어쓰기 헷갈리는 의존 명사들
##################################################

# 전성 어미 혹은 의존 명사 
# ~는지, ~은지, ~을지, ~를지, ~ㄴ지, ~ㄹ지 
etnJi = lm.regAux('지').incase(lm.onlyAfter).after([
        etmNeun, etmEun, etmN, etmEul, etmL
        ])

jkoReul.after([etnJi])
jxNeun.after([etnJi])
jksGa.after([etnJi])
jxDo.after([etnJi])
jkbE_to.after([etnJi])

# ~때문
dnDdaeMun = lm.regMultiSyllablesAux('때문')
auxDdaeMunE = lm.regAux('에').incase(lm.onlyAfter).after(dnDdaeMun)
jxEun.after(dnDdaeMun)
jksI.after(dnDdaeMun)
jkpIda.after(dnDdaeMun)

##################################################
# 띄어쓰기 헷갈리는 부사들
##################################################
auxDeuSi = lm.regMultiSyllablesAux('듯이').tag("MAG") 

