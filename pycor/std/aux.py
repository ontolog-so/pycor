import sys
import pycor.morpheme as lm
import pycor.kormorpheme as klm
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
auxEo = lm.Aux('어').incase([afterNegativeVowel])
auxDoeEo = lm.regMultiSyllablesAux('되어')

auxYeo = lm.Aux('여').incase([afterVowel])
auxYeoTr = lm.regAux(klm.TransformedAux('여','이','어')).incase([afterJongsung]).ambiguous()

auxEu = lm.Aux('으').incase(afterJongsung)
auxRi = lm.Aux('리').incase([afterJongsung, afterNegativeVowel])
auxRyeo = lm.regAux('려')
auxRyeoTr = lm.regAux(klm.TransformedAux('려','리','어')).ambiguous()
auxRyeot = klm.TransformedAux('렸','리','었').tag("EPT-pp" )
auxDoae = lm.regAux( klm.TransformedAux('돼','되','어') ).ambiguous()
auxHae = lm.regAux( klm.TransformedAux('해','하', 'ㅣ') ).ambiguous()
auxJieo = lm.regAux( klm.TransformedAux('져','지','어').after([auxHae]) ).ambiguous()
auxGieEo = lm.regAux( klm.TransformedAux('겨','기','어')).ambiguous()
auxChiEo = lm.regAux( klm.TransformedAux('쳐','치','어')).ambiguous()
auxChuEo = lm.regAux( klm.TransformedAux('춰','추','어'))
auxKyeo = lm.regAux(klm.TransformedAux('켜','키','어', escapeFirst=False))
auxGgyeo = lm.regAux(klm.TransformedAux('껴','끼','어', escapeFirst=False))



# 되-어 
auxStemDoeEo = lm.Aux('어').incase(lm.ConstraintAfter('되'))
# 하-고 
auxStemHaGo = lm.Aux('고').incase(lm.ConstraintAfter('하'))

# 되-기~, 하-기~, 지-기~ --> 에, 에는, 도 
auxStem_Gi = lm.Aux('기').incase(lm.ConstraintAfter(['되','하','지']))



jkpI = lm.Aux('이').tag('JKP')
auxEo.after(jkpI)
jkpIEot = lm.Aux('었').tag('JKP-pp').incase(lm.onlyAfter).after(jkpI)
jkpYeot = lm.Aux('였').tag("JKP-pp" ).incase([afterVowel]).incase(lm.ConstraintNotAfter('하'))
jkpIn = lm.Aux('인').tag('JKP')
jkpIl = lm.Aux('일').tag('JKP')

# ~해지, ~돼지, ~이지, ~이었지, ~였지, ~인지, ~일지
auxJi  = lm.regAux('지').after([auxHae,auxDoae, auxChiEo,auxChuEo,
        auxKyeo,auxGgyeo,jkpI,jkpIEot,jkpYeot,jkpIn,jkpIl])
auxJi2  = lm.regAux('지').incase(klm.ConstraintAfter(['하','되']))
auxI  = lm.Aux('이').incase(afterJongsung)

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
eptN  = klm.buildJongsungAux('ㄴ', escape=['는']).tag("EPT-pr") 
eptN.escapeFirst = False
eptAt = lm.Aux('았').tag("EPT-pp").incase([afterPositiveVowel])
eptEot = lm.Aux('었').tag("EPT-pp")
eptYeot = lm.Aux('였').tag("EPT-pp").incase(klm.ConstraintAfter("하"))
eptGet = lm.Aux('겠').tag("EPT-f")
eptGet2 = lm.Aux('겠').tag("EPT-guess")
eptDeo = lm.Aux('더').tag("EPT-pp")
eptDeon = lm.regAux('던').tag("EPT-pp")
eptRiRa = lm.regMultiSyllablesAux('리라').tag("EPT-f").after([
        auxEu
        ])


eptTimeSet = [eptNeun, eptAt,eptEot,eptYeot,eptGet,eptGet2]

constraintsPastException = klm.ConstraintNotAfter(['했','혔','됐','갔','봤','잤','왔','줬','졌','았','었','였','렸', '웠', '왔'])

eptPasts = [
    klm.TransformedAux('갔','가','았', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('겼','기','었', escapeFirst=True).tag("EPT-pp" ),
    klm.TransformedAux('꼈','끼','었', escapeFirst=True).tag("EPT-pp" ),
    klm.TransformedAux('났','나','았', escapeFirst=True).tag("EPT-pp" ),
    klm.TransformedAux('냈','내','었', escapeFirst=True).tag("EPT-pp" ),
    klm.TransformedAux('됐','되','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('뒀','두','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('랐','르','았').tag("EPT-pp" ),
    auxRyeot, 
    klm.TransformedAux('셨','시','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('쌌','싸','았', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('썼','쓰','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('왔','오','았', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('였','이','었', escapeFirst=False).incase([afterJongsung]).tag("EPT-pp" ),
    eptTimeSet,
    klm.TransformedAux('웠','우','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('봤','보','았', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('잤','자','았', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('줬','주','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('챘','채','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('췄','추','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('켰','키','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('졌','지','었', escapeFirst=False).tag("EPT-pp").after(auxHae),
    klm.TransformedAux('쳤','치','었', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('탔','타','았', escapeFirst=False).tag("EPT-pp" ),
    klm.TransformedAux('했','하','였', escapeFirst=False).tag("EPT-pp" ) ,
    klm.TransformedAux('혔','히','었').tag("EPT-pp" ),
    klm.JongsungAux(['샀','섰','갔'], jongsungs="ㅆ").tag("EPT-pp" )
]

# eptDeon.after([eptAt, eptEot, eptYeot])
eptDeon.after(eptPasts)
auxEu.after([eptPasts, eptTimeSet, jkpIEot, jkpYeot])
auxJi.after([eptPasts, eptTimeSet])
eptNeun.after([eptPasts, eptTimeSet, jkpIEot, jkpYeot])

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

eppSeupNi.after([eptTimeSet,eptPasts,jkpYeot,jkpIEot])

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
etnEum = lm.regAux(lm.PosAux('음')).setpos("CY").incase(afterJongsung)
etnM = lm.regAux(lm.PosAux(['함','됨','짐','쁨','픔'])).setpos("CY").ambiguous()
etnGi = lm.regAux(lm.PosAux('기')).setpos("CY").ambiguous()

etnIm = lm.Aux(['임']).tag("ETN").tag("JKP")

# ~음으-, ~ㅁ으-
#auxEu.after([etnEum,etnM])

###################################
# ETM	관형사형 전성 어미 
# -(으)ㄴ, -는, -(으)ㄹ
###################################
etmEun = lm.regAux('은').tag("ETM").incase(afterJongsung).after([etnEum, etnM]) 
etmNeun = lm.regAux('는').tag("ETM").after([etnGi, eptPasts]) 
etmIn = lm.regAux('인').tag("ETM+JKP").ambiguous()
etmIl = lm.regAux('일').tag("ETM+JKP").ambiguous()
etmN = lm.regAux(klm.JongsungAux(['린','된','한','친','낸','룬','선','른','춘','진','쁜','픈','간' ], 'ㄴ')).tag("ETM").ambiguous()
etmEul = lm.regAux('을').tag("ETM").incase(afterJongsung) 
etmL = lm.regAux(klm.JongsungAux(['릴','될','할','칠','낼','룰','설','를', '출','질','쁠','플','갈' ], 'ㄹ')).tag("ETM").ambiguous()
# etmLeL = lm.regAux(klm.JongsungAux('를', 'ㄹ')).tag("ETM").incase(lm.ConstraintAfter(['기','나','다','마','치']))
etmReul = lm.regAux('를').tag("ETM").incase(afterVowel) 

etmSiKin = lm.regAux(klm.JongsungAux('킨', 'ㄴ')).tag("ETM").incase(lm.ConstraintAfter('시'))
etmHaeJin = lm.regAux(klm.JongsungAux('진', 'ㄴ')).tag("ETM").incase(lm.ConstraintAfter('해'))

etmSiKil = lm.regAux(klm.JongsungAux('킬', 'ㄹ')).tag("ETM").incase(lm.ConstraintAfter('시'))
etmHaeJil = lm.regAux(klm.JongsungAux('질', 'ㄹ')).tag("ETM").incase(lm.ConstraintAfter('해'))

etmNeun.after([auxRi,auxRyeo, ephSi])
etmEul.after(eptPasts)

###################################
# ETA	부사형 전성 어미 
# -이, -게, -도록
###################################
constraintsHaJiDoi = lm.ConstraintAfter(["하","지","되"])
etaY = lm.regAux('이').tag("ETA").incase(afterJongsung)
etaGe = lm.regAux('게').tag("ETA").incase(constraintsHaJiDoi).setscore(1)
etaDoRok = lm.regMultiSyllablesAux('도록').tag("ETA").incase(constraintsHaJiDoi).setscore(1)



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
        eptN, eptNeun
        ])

efnNiDa = lm.regMultiSyllablesAux('니다').tag("EFN").after([
        lm.Aux('십'), 
        lm.Aux('습').after(eptPasts),
        klm.TransformedAux('합','하','니')
])

efnDa.after(eptTimeSet).after(eptPasts)
efnDa.after([ephSyeot,ephSin,auxRi,eppSeupNi,jkpIEot,jkpYeot])

efnDanDa = lm.regMultiSyllablesAux('단다').tag("EFN2").after([
        klm.buildJongsungAux('ㄴ').tag("EFN"),
        eptNeun
        ])
efnDanDa.after(eptTimeSet).after(eptPasts)
efnDanDa.after([ephSyeot,ephSin,eptEot])
        
efnRanDa = lm.regMultiSyllablesAux('란다').tag("EFN2").incase(afterVowel).after([
        auxI, eptDeo
        ])

efnGuNa = lm.regMultiSyllablesAux('구나').tag("EFN2").after([
        eptNeun, eptDeo
        ])
efnGuNa.after(eptTimeSet).after(eptPasts)
efnGuNa.after([ephSyeot])

# ~는군, ~더군, ~겠군, ~었군, ~했군
efnGun = lm.regAux('군').tag("EFN2").incase(lm.onlyAfter).after([eptTimeSet,eptEot,eptNeun, eptDeo])

efnNe = lm.regAux('네').tag("EFN2").ambiguous()
# ~이네 
efnNe.after(jkpI)

efnNe.after(eptTimeSet).after(eptPasts)
efnNe.after([ephSi, ephSyeot])

efnMa = lm.regAux('마').tag("EFN2").incase(afterVowel).after([
        auxEu
        ]).ambiguous()

efnGeol = lm.regAux(['걸','게']).tag("EFN2").incase(lm.onlyAfter).after([
        klm.buildJongsungAux('ㄹ').tag("EFN"),
        lm.Aux('을').tag("EFN").incase(afterJongsung)
        ]).ambiguous()

efnRa = lm.regAux(['래','라']).tag("EFN2").incase(lm.onlyAfter).after([
        klm.buildJongsungAux('ㄹ').tag("EFN"),
        lm.Aux('을').tag("EFN").incase(afterJongsung),
        eptDeo
        ]).ambiguous()

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
        lm.Aux('느').tag("EFQ").after([jkpIEot,jkpYeot]),
        auxEu, jkpI, jkpIEot
        ])
efqNi = lm.regAux('니').tag("EFQ").after([
        auxEu
        ])
efqGa = lm.regAux('가').tag("EFQ-ga").incase(lm.onlyAfter).after([
        eptNeun
        ])     
efqGga = lm.regAux('까').tag("EFQ").incase(lm.onlyAfter).after([
        klm.buildJongsungAux('ㄹ'), lm.Aux('을').incase(lm.onlyAfter).after(eptPasts)
        ])     
efqJi = lm.regAux('지').tag("EFQ").incase(lm.onlyAfter).after([
        eptNeun, klm.buildJongsungAux('ㄹ'), lm.Aux('을').incase(lm.onlyAfter).after(eptPasts)
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
        auxA, auxEo,auxDoeEo,
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
efoJi = lm.regAux('지').tag("EFO").ambiguous().setscore(-2)

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


ecGo.after([efnDa, ephSi, eptYeot, eptTimeSet])
ecGo.after(eptPasts)
ecMyeo.after([efnDa, ephSi])

#----------------------------------
# EC 연결 어미 > 동시에 나열 : ~(으)면서,~자, ~자마자
#----------------------------------
ecMyeonSeo = lm.regMultiSyllablesAux('면서').tag("EC-and").incase(afterVowel).after([
        auxEu, efnDa, jkpI
        ])
ecJa = lm.regAux('자').tag("EC-and").after([
        lm.MultiSyllablesAux('자마'), jkpI
        ])


#----------------------------------
# EC 연결 어미 > 시간 전환 : ~다가
#----------------------------------
ecDaGa = lm.regMultiSyllablesAux('다가').tag("EC-and")
ecDaGa.after([eptTimeSet,eptPasts,jkpIEot, jkpYeot])

#----------------------------------
# EC 연결 어미 > 대립/대조 : ~(으)나, ~만, ~는데/~(으)ㄴ데, ~아도/어도
#----------------------------------
ecNa = lm.regAux('나').tag("EC-but").incase(afterVowel).after([
        auxEu
        ])
ecJiMan = lm.regAux('만').tag("EC-but").incase(lm.onlyAfter).after([
        lm.Aux('지').tag("EC-but").after(eptPasts).after([jkpI,jkpIEot,jkpYeot])
        ])

ecDe = lm.regAux('데').tag("EC-but").incase(lm.onlyAfter).after([
        eptNeun, lm.Aux('는').incase(lm.onlyAfter).after([eptTimeSet,eptPasts,jkpIEot, jkpYeot])
        ])
ecDo = lm.regAux('도').tag("EC-but").incase(lm.onlyAfter).after([
        auxA, auxEo,auxDoeEo, auxHae, auxDoae, auxYeo,auxYeoTr,auxRyeoTr, ecMyeonSeo, etaGe, auxGieEo
        ])

# ~하되
ecHaDoe = lm.regAux('되').tag("EC-but").incase(lm.ConstraintAfter('하'))

#----------------------------------
# EC 연결 어미 > 이유/원인 : ~아서/어서, ~(으)니, ~(으)니까, ~(으)므로, ~느라고
#----------------------------------
ecSeo = lm.regAux('서').tag("EC-because").incase(afterVowel).after([
        auxA, auxEo,auxDoeEo, auxDoae, auxHae, auxYeo,auxYeoTr,auxRyeoTr, auxStemDoeEo, auxStemHaGo , 
        auxRyeoTr, auxGieEo, auxChiEo, auxChuEo
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
# EC 연결 어미 > 조건 : ~(으)면,~(으)려면, ~자면, ~아야/어야
#----------------------------------
ecMyeon = lm.regAux('면').tag("EC-incase").incase(afterVowel).after([
        auxEu
        ])
ecRyeoMyeon = lm.regMultiSyllablesAux('려면').tag("EC-to").incase(afterVowel).after([
        auxEu
        ])
ecJaMyeon = lm.regMultiSyllablesAux('자면').tag("EC-to") 

# ~아야, ~어야 
ecYa = lm.regAux('야').tag("EC-incase").incase(afterVowel).after([
        auxA, auxEo, auxDoeEo, auxYeo,auxYeoTr,auxRyeoTr, ecMyeon, auxKyeo,auxGgyeo, auxHae, auxStemDoeEo, auxStemHaGo, auxGieEo, auxChiEo,
        auxDoae, auxJieo, auxChuEo
        ])

# ecE = lm.regAux('에').tag("EC-incase").incase(lm.onlyAfter).after(auxStem_Gi)
# ecENeun = lm.regAux('는').incase(lm.onlyAfter).after(ecE)
# ecEDo = lm.regAux('도').incase(lm.onlyAfter).after(ecE)

#----------------------------------
# EC 연결 어미 > 목적 : ~(으)러, ~(으)려고, ~도록, ~게
#----------------------------------
ecReo = lm.regAux('러').tag("EC-for").incase(afterVowel).after([
        auxEu
        ])
# ~려, ~으려 
ecRyeo = lm.regAux('려').tag("EC-for").incase(afterVowel).after([
        auxEu
        ])
ecRyeoGo = lm.regAux('고').incase(lm.onlyAfter).after([ecRyeo])

ecGoJa = lm.regMultiSyllablesAux('고자').tag("EC-for")

ecDoRok = lm.regMultiSyllablesAux('도록').tag("EC-for")
ecGe = lm.regAux('게').tag("EC-for").setscore(-1)

#----------------------------------
# EC 연결 어미 > 인정 : ~아도/어도, ~(으)ㄹ지라도, ~더라도
#----------------------------------
ecDo2 = lm.regAux('도').tag("EC-may").incase(lm.onlyAfter).after([
        auxA, auxDoeEo,auxEo
        ])
ecJiRaDo = lm.regMultiSyllablesAux('지라도').tag("EC-evenif").incase(afterJongsung).after([
        lm.Aux('을').tag("EC-evenif").incase(afterJongsung),
        lm.Aux('일').tag("EC-evenif"),
        klm.buildJongsungAux('ㄹ').tag("EC-evenif")
        ])
ecDeoRaDo = lm.regMultiSyllablesAux('더라도').tag("EC-evenif")

ecDeun = lm.regAux('든').tag("EC-evenif").after([jkpI,jkpIEot])

#----------------------------------
# EC 연결 어미 > 선택 : ~거나, ~든지
#----------------------------------
ecGeoNa = lm.regMultiSyllablesAux('거나').tag("EC-or") 
ecDeunJi = lm.regMultiSyllablesAux('든지').tag("EC-or") 

ecGeoNa.after([jkpI, eptEot, eptTimeSet, efnDa, eptPasts])
ecDeunJi.after([jkpI, eptEot, eptTimeSet, efnDa])

#----------------------------------
# EC 연결 어미 > 방법/수단 : ~아, ~어, ~아서/어서, ~고
#----------------------------------
ecA = lm.regAux('아').tag("EC-by").incase([afterPositiveVowel])
ecEo = lm.regAux('어').tag("EC-by").incase([afterNegativeVowel])

ecGo2 = lm.regAux('고').tag("EC-by").ambiguous()
ecSeo2 = lm.regAux('서').tag("EC-by").incase(afterVowel).after([
       auxA, auxEo,auxDoeEo, ecGo2
       ])

#----------------------------------
# EC 연결 어미 > 배경 : ~는데/~(으)ㄴ데, ~(으)니
#----------------------------------
ecDe2 = lm.regAux('데').tag("EC-while").incase(lm.onlyAfter).after([
        etmEun, jkpIn, eptNeun, eptN
        ])

ecDeDa = lm.regAux('다').tag("EC-and").incase(lm.onlyAfter).after([ecDe2])

ecNi2 = lm.regAux('니').tag("EC-while").incase(afterVowel).after([
        auxEu, 
        lm.Aux('더').after(eptPasts)
        ])




#########################################################################################################
# 어미 조합  
#########################################################################################################
# ~이라, ~다라 
auxRa = lm.regAux('라').after([efnDa,jkpI])

ecMyeonSeo.after(auxRa)
ecMyeo.after([auxRa])

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

jksYaMalLo = lm.regMultiSyllablesAux('야말로').tag("JKS").incase([afterVowel]).after([ jkpI ])

jksI.after([etnEum, etnM, etnIm])
jksGa.after([etnGi ])

###################################
# JKP	서술격 조사*
# 이다 , 다  
###################################
jkpIda = lm.regAux('다').tag("JKP" ).incase(lm.onlyAfter).after([
        jkpI, etnGi,jkpIEot,jkpYeot,
        lm.Aux('니').incase(lm.onlyAfter).after(lm.Aux('입').tag("JKP" )),
        ]) 

jkpDa = lm.regAux('다').tag("JKP-da").incase(afterVowel)

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
jkbEn_to = lm.regAux('엔').tag("JKB-TO")
jkbEGe = lm.regMultiSyllablesAux('에게').tag("JKB-TO") 
jkbEGen = lm.regMultiSyllablesAux('에겐').tag("JKB-TO") 
jkbGge = lm.regAux('께').tag("JKB-TO")
jkbGgen = lm.regAux('껜').tag("JKB-TO")
jkbHante = lm.regMultiSyllablesAux('한테').tag("JKB-TO") 
jkbHanten = lm.regMultiSyllablesAux('한텐').tag("JKB-TO") 

jkbE_to.after([etnEum, etnM,etnGi])
jkbEn_to.after([etnEum, etnM, etnGi])

###################################
# JKB-FM 원천격 조사: 에서/에게서/에서부터
###################################
jkbESeo = lm.regMultiSyllablesAux('에서').tag("JKB-FM")  
jkbESeon = lm.regMultiSyllablesAux('에선').tag("JKB-FM")  
jkbEGeSeo = lm.regMultiSyllablesAux('에게서').tag("JKB-FM") 
jkbEGeSeon = lm.regMultiSyllablesAux('에게선').tag("JKB-FM") 
jkbBuTeo = lm.regMultiSyllablesAux('부터').tag("JKB-FM")
jkbBuTeon = lm.regMultiSyllablesAux('부턴').tag("JKB-FM")

jkbBuTeo.after([jkbESeo,jkbEGeSeo,etnEum, etnM,etnGi])
jkbBuTeon.after([jkbESeo,jkbEGeSeo,etnEum, etnM,etnGi])
jkbESeo.after([etnEum, etnM,etnGi])
jkbESeon.after([etnEum, etnM,etnGi])

#----------------------------------
# JX 부터/로부터/으로부터
#----------------------------------
jxBuTeo = lm.regMultiSyllablesAux('부터').tag("JX-from").after([
        lm.Aux('로').tag("JX-from").after([auxEu, etnGi])
        ])
jxBuTeon = lm.regMultiSyllablesAux('부턴').tag("JX-from").after([
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
jkbRoOnly = lm.regAux('로').tag("JKB-TT|AS|BY").ambiguous()
jkbEuRo = lm.regAux('로').tag("JKB-TT|AS|BY").incase(lm.onlyAfter).after([auxEu,etnGi])
jkbRoSeo = lm.regMultiSyllablesAux('로서').tag("JKB-AS")
jkbEuRoSeo = lm.regMultiSyllablesAux('으로서').tag("JKB-AS") 
jkbEuRoSseo = lm.regMultiSyllablesAux('로써').tag("JKB-BY").after(lm.Aux('으').after([etnEum, etnM,etnGi]))






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
# 고, 라고, ~이라고, ~다고, ~자고 
###################################
jkqGo = lm.regAux('고').tag("JKQ").after([
        efnDa, auxRa, efoJa
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
jxDo = lm.regAux('도').tag("JX-SO").incase([final]).ambiguous()

jxDo.after([jkbESeo,jkbE_at,jkbE_to,jkbEGe,jkbEuRo,jkbRoOnly,jkqGo,efqGa, efqNya, efqJi, etnGi, ecDe2])
jxNeun.after([efqGa, efqNya, efqJi])

#----------------------------------
# JX 보조사 까지, 마저, 조차
#----------------------------------
jxGgaJi = lm.regMultiSyllablesAux('까지').tag("JX").after([etnEum, etnM,etnGi])
jxMaJeo = lm.regMultiSyllablesAux('마저').tag("JX").after([etnEum, etnM,etnGi]) 
jxMaDa = lm.regMultiSyllablesAux('마다').tag("JX").after([etnEum, etnM,etnGi]) 
jxJoCha = lm.regMultiSyllablesAux('조차').tag("JX").after([etnEum, etnM,etnGi])

# ~에서도, ~에도, ~에게도, ~으로도, ~까지도, ~마저도 , ~조차도 , ~(으)로도
jxDo.after([jkbESeo,jkbE_at,jkbE_to,jkbEGe,jkbEuRo,jkbRoOnly, jxGgaJi,jxMaJeo,jxJoCha])
# ~에서조차, ~에조차, ~에게조차, ~으로조차,
jxJoCha.after([jkbESeo,jkbE_at,jkbE_to,jkbEGe,jkbEuRo,jkbRoOnly])
#----------------------------------
# JX 보조사 뿐/만
#----------------------------------
jxBbun = lm.regAux('뿐').tag("JX").after([etnEum, etmL,etnGi,jkbESeo,jkbEuRo,jkbEuRoSeo, jkbRoSeo]) 
jxMan = lm.regAux('만').tag("JX").after([
        etnEum, etmL, etnGi, lm.Aux('야').incase(afterVowel), jkqGo, jkbEuRoSeo, jkbRoSeo, jxBbun
        ]) 

jxEun.after(jxMan)
jkoEul.after(jxMan)
jksI.after(jxMan)

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
jxDdaRa.after([jkbE_to, jkbE_at])

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
#  (이)나마
#  (이)야(말로)
jxNa = lm.regAux('나').tag("JX").incase(afterVowel).after(jkpI)
jxRan = lm.regAux('란').tag("JX").incase(afterVowel).after(jkpI)
# jxDeunJi = lm.regMultiSyllablesAux('든지').incase(afterVowel).tag("JX").after(jkpI)
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
jxDo.after([auxJi,auxJi2, auxRa, jkbBoDa])

# ~이던, ~이었던, ~였던 
eptDeon.after([jkpI, jkpIEot,jkpYeot])

# ~하다, ~한다, ~지다  
efnDa.after([auxHa, auxHan, auxJi])
# ~하자, ~지자, ~이자 
ecJa.after([auxHa,auxJi,auxI])
# ~하는, ~다는, ~지는, ~이라는, ~라는, ~다라는
etmNeun.after([auxHa,auxJi,auxJi2,efnDa,auxRa]) 
# ~하면, ~다면, ~지면 ~이면, ~이라면, ~다라면, ~라면
ecMyeon.after([auxHa,auxJi,efnDa,auxI,auxRa])
# ~하기, ~했기
etnGi.after([eptPasts, eptTimeSet])

# ~이기 
etnGi.after(jkpI)
# ~라기, ~이라기 
etnGi.after(auxRa)

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

# ~에서다, ~부터다 , ~까지다
efnDa.after([jkbESeo, jkbBuTeo,jxBuTeo, jxGgaJi])

# ~에서의, ~부터의 , ~까지의, ~와의, ~고의, ~하고의 , ~에의 , ~으로의, ~로서의 , ~으로서의, ~으로써의 
jkgEui.after([jkbESeo, jkbBuTeo,jxBuTeo, jxGgaJi, jcWa, jcGwa, 
        jcHaGo, jkbE_to, jkbEuRo,jkbRoOnly, jkbRoSeo, jkbEuRoSeo, jkbEuRoSseo])

# ~에서도, ~부터도 , ~까지도, ~와도, ~고도, ~하고도 , ~에도 , ~으로도, ~로서도 , ~으로서도, ~으로써도 
ecDo.after([jkbESeo, jkbBuTeo,jxBuTeo, jxGgaJi, jcWa, jcGwa, 
        jcHaGo, jkbE_to,jkbEuRo, jkbRoOnly, jkbRoSeo, jkbEuRoSeo, jkbEuRoSseo])

# ~에서만 ~부터만 , ~야만 
jxMan.after([jkbESeo,jkbEGe,jkbE_to, jkbBuTeo,jxBuTeo,jkbEuRo, jkbRoOnly, jkbRoSeo, jkbEuRoSeo, jkbEuRoSseo, ecYa])

# ~에서나 ~부터나 
jxNa.after([jkbESeo,jkbEGe,jkbE_to, jkbEuRo,jkbRoOnly, jkbRoSeo, jkbEuRoSeo, jkbEuRoSseo])

# ~에서가, ~부터가 , ~까지가, ~와가 , ~에가 , ~으로가, ~로서가 , ~으로서가, ~으로써가
jksGa.after([jkbESeo, jkbBuTeo,jxBuTeo, jxGgaJi, jcWa, jkbE_to, jkbEuRo,jkbRoOnly, jkbRoSeo, jkbEuRoSeo, jkbEuRoSseo])

# ~에서보다, ~한테보다, ~부터보다 , ~까지보다, ~와보다 , ~에보다 , ~으로보다, ~로서보다 , ~으로서보다, ~으로써보다
jkbBoDa.after([jkbESeo,jkbHante, jkbBuTeo,jxBuTeo, jxGgaJi, jcWa, jkbE_to, jkbEuRo,jkbRoOnly, jkbRoSeo, jkbEuRoSeo, jkbEuRoSseo])


# ~으로까지 , ~에서까지, ~에까지, 에게까지, 으로까지, ~기까지 
jxGgaJi.after([jkbEuRo, jkbRoOnly, jkbESeo,jkbE_at,jkbE_to,jkbEGe, etnGi])

# ~와는 ... ~려는  ~으려는 
jxNeun.after([jkbWa,jkbGwa,jxGgaJi, jksI,jkbE_to,jkbEGe,jkbGge,jkbHante,jkbESeo,jkbEGeSeo,jkbBuTeo,jxBuTeo,
        jkbBoDa,jkbEuRo,jkbRoOnly,jkbEuRoSeo,jkbRoSeo,jkbEuRoSseo,jkbE_at,jkbGatYi,jkqGo,jcHaGo,ecSeo, ecRyeo ])
# ~이랑은 ~처럼은
jxEun.after([jkbIRang,jkbCheoReom])

jkbWa.after([jkbESeo])



# ~되어있다, 되어있는, 되어있을, ~하고있다, 하고있는, 하고있을
auxStemIt = lm.Aux('있').incase(lm.onlyAfter).after([auxStemDoeEo,auxStemHaGo])
efnDa.after(auxStemIt)
etmNeun.after(auxStemIt)
etmEul.after(auxStemIt)

##################################################
# 조사, 어미와 헷갈리는 명사  
##################################################
lm.regAux(lm.StemAux('쟁이'))
lm.regAux(lm.StemAux('장이'))

##################################################
# 띄어쓰기 헷갈리는 의존 명사들
##################################################

# 전성 어미 혹은 의존 명사 
# ~는지, ~은지, ~을지, ~를지, ~ㄴ지, ~ㄹ지 
efqJi.after([ etmNeun, etmEun, etmN, etmEul, etmL ])

jkoReul.after([efqJi])
jxNeun.after([efqJi])
jksGa.after([efqJi])
jxDo.after([efqJi])
jkbE_to.after([efqJi])

# ~때문
dnDdaeMun = lm.regMultiSyllablesAux('때문')
auxDdaeMunE = lm.regAux('에').incase(lm.onlyAfter).after(dnDdaeMun)
jxEun.after(dnDdaeMun)
jksI.after(dnDdaeMun)
jkpIda.after(dnDdaeMun)

# ~만큼
dnManKeum = lm.regMultiSyllablesAux('만큼')
jxEun.after(dnManKeum)
jxDo.after(dnManKeum)

# ~만치
dnManChi = lm.regMultiSyllablesAux('만치')
jxNeun.after(dnManChi)
jxDo.after(dnManChi)

# ~게
dnGe = lm.regAux('게').incase(lm.onlyAfter).after([etmNeun, etmEun, etmN, etmEul, etmL])
jxMan.after(dnGe)
jxNeun.after(dnGe)
jxDo.after(dnGe)

# ~케
dnKe = lm.regAux(klm.TransformedAux('케','하','게')).ambiguous().setscore(-3)

# ~수
dnSu = lm.regAux('수').incase(lm.onlyAfter).after([etmEul, etmL,etmSiKil,etmHaeJil])
stm.stemIt.after(dnSu)
stm.stemUp.after(dnSu)

# ~뿐이었, ~뿐이
jkpIEot.after([jxBbun])
jkpI.after([jxBbun])

# ~ㄹ때 ~ㄴ때
dnDde = lm.regAux('때').after([etmL,etmN,etmEul,etmReul, etmEun, etmNeun, etmIl,etmIn])

##################################################
# 띄어쓰기 헷갈리는 부사들
##################################################
auxDeuSi = lm.regMultiSyllablesAux('듯이').tag("MAG") 
auxDeuSi.after(eptTimeSet).after(eptPasts)
