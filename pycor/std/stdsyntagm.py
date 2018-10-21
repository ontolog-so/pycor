import sys
import pycor.syntagm as st
import pycor.speechmodel as sm


def handleEFN(lastpair, syntagmCursor, documentContext):
    lastpair.addpos("Y")
    pairs = syntagmCursor.currentPair(-3)
    # print("EFN", len(pairs), pairs)

def handleJKP(lastpair, syntagmCursor, documentContext):
    lastpair.addpos("C")
    pairs = syntagmCursor.currentPair(-4)
    # print("JKP", len(pairs), pairs)

st.ptSyntagm.addHandler("EFN",handleEFN).addHandler("JKP",handleJKP)