import os
from pycor import langmodel as lm
import pycor.speechmodel as sm


Y_TAGS0 = set(['EFN','ETN','EFQ'])
Y_TAGS1 = set(['EPT-pp','EPT-f','EPT-guess','EFN','EFI','EC-to','EC-for','EC-but'])
Y_TAGS2 = set(['EPT-pr','ETM'])

C_TAGS0 = set(['JKS','JKC','JKP'])
C_TAGS1 = set(['JKG','JKB-TO','JKB-FM','JX-from','JKB-AS','JKB-WZ','JKB-LK','JC','JX','JKB-TT|AS|BY',
                'EC-evenif','JKG-as','JKB-CM'])
C_TAGS2 = set(['JKO','JX-SO'])
C_POS = set(['NP','NNB'])


def def_classify(head, force=True):
    if force or len(head.pos) == 0:
        if len(head.tails) == 0:
            if len(head.pos) == 0:
                head.addpos('SNG')
        else:
            tags = set()
            for tail in head.tails:
                tags.update(tail.tags)
                
            yscore = len(tags & Y_TAGS0) * 4 + len(tags & Y_TAGS1) * 3 + len(tags & Y_TAGS2) * 1
            cscore = len(tags & C_TAGS0) * 4 + len(tags & C_TAGS1) * 3 + len(tags & C_TAGS2) * 2
            
            head.removepos('AMBI')

            if yscore > cscore:
                head.removepos('C') 
                head.addpos('Y')
            elif cscore > yscore:
                head.removepos('Y')
                head.addpos('C')
            elif len(head.pos) == 0:
                head.addpos('AMBI')
    