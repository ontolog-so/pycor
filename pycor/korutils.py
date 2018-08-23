
#####################
# ch가 한글인지 여부 
#####################
def isKorChar(ch):
    code = ord(ch)
    return code >= 44032 and code <= 55203 

def isKor(str):
    if str is None:
        return False
    
    code = None
    if len(str) > 1:
        code = ord( str[len(str)-1] )
    else:
        code = ord(str[0])
    
    return code >= 44032 and code <= 55203 


def isAlpha(ch):
    return ch.isalpha()


def isNumeric(ch):
    return ch.isnumeric()


POSITIVE_VOWEL = ["ㅏ", "ㅐ", "ㅑ", "ㅒ","ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ"]
NEGATIVE_VOWEL = ["ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅜ", "ㅝ", "ㅞ", "ㅟ", "ㅠ" ]
NEUTRAL_VOWEL = ["ㅡ", "ㅢ", "ㅣ" ]

phoneme_first = [ "ㄱ", "ㄲ", "ㄴ", "ㄷ", "ㄸ", "ㄹ", "ㅁ", "ㅂ", "ㅃ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅉ", 
                 "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ" ]
phoneme_vow = [ "ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ", "ㅖ", "ㅗ", "ㅘ", "ㅙ", "ㅚ", "ㅛ", "ㅜ", 
               "ㅝ", "ㅞ", "ㅟ", "ㅠ", "ㅡ", "ㅢ", "ㅣ" ]
phoneme_final = [ "", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ",
                "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ",  "ㅍ", "ㅎ" ]

def decompose(ch) :
    code = ord(ch)
    if code <44032 or code > 55203:
        raise Exception('korchar_devide [' + ch + "] is not korean charactor")
    orch = code - 0xAC00;
    first  = int(orch / 588)
    vowel = int((orch - (first*588)) / 28) 
    final = int ( ( (orch - (first*588)) - (vowel*28) ) )
    return phoneme_first[first], phoneme_vow[vowel], phoneme_final[final]

'''
종성 제거
'''
def removeJongsung(ch) :
    code = ord(ch)
    if code <44032 or code > 55203:
        raise Exception('korchar_devide [' + ch + "] is not korean charactor")
    orch = code - 0xAC00;
    first  = int(orch / 588)
    vowel = int((orch - (first*588)) / 28) 
    
    return chr(0xAC00 + first * 21 * 28 + vowel * 28 )

def addJongsung(ch, jongsung) :
    code = ord(ch)
    if code <44032 or code > 55203:
        raise Exception('korchar_devide [' + ch + "] is not korean charactor")
    orch = code - 0xAC00;
    first  = int(orch / 588)
    vowel = int((orch - (first*588)) / 28) 
    final = phoneme_final.index(jongsung)
    return chr(0xAC00 + first * 21 * 28 + vowel * 28 + final )


'''
초,중,종성 조합
'''
def compose(cho , jung, jong=u'') :
    a = phoneme_first.index(cho)
    b = phoneme_vow.index(jung)
    c = phoneme_final.index(jong)    
    return chr(0xAC00 + a * 21 * 28 + b * 28 + c)

    
