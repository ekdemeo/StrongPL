import unicodedata
from string import Template
from unicode import decode

def isstrongid(value):
        return (value[0] == 'G' or value[0] == 'H') and value[1:].isdigit()

def replace_strongid_by_link(text):
    text_split = text.split()
    return ' '.join(map(replace_if_id, text_split))

def replace_if_id(token):
    if isstrongid(token):
        return Link(token).format()
    else:
        return token
        

class Link:
    def __init__(self, id):
        self.strongid = id
        self.tid = int(id[1:])+1

    linkid = Template(r"""{\field{\*\fldinst HYPERLINK "tw://[self]?tid=$tid"}{\fldrslt \plain \f2\fs22\cf1 $strongid }}""")

    def format(self):
            return self.linkid.substitute(self.__dict__)



class Entry:
    rtf = Template(r"""{\rtf1\fbidis\ansi\ansicpg0\uc0\deff0\deflang0\deflangfe0
{\fonttbl
{\f0\fnil Arial;}
{\f1\fnil verdana;}
{\f2\fnil\fcharset238 Calibri;}
{\f3\fnil\fcharset161 Cambria;}}
{\colortbl;\red0\green0\blue255;\red192\green80\blue77;}
\pard\sl276\slmult1\fi0\li0\ql\ri0\sb0\sa195\itap0 
\plain \f2\fs22 $id \plain \f3\lang1032\fs22\cf2 $word_uni \plain \f2\b\fs22\cf2  
\plain \f2\fs22 [\plain \f2\b\fs22 $word_ascii]; \plain \f2\i\fs22 $part_of_speech
\par \plain \f2\b\fs22 1. $meaning1
\line \ltrch 2. $meaning2 
\line 3. $meaning3
\par \plain \f2\fs22 P: $origin
\line \plain \f2\fs22 W: ($occ_count) \plain \f2\fs22 $occ \par}
""")

    def format(self):
        return self.rtf.substitute(self.__dict__)



e = Entry();
e.id = 'G13'
e.word_uni = decode(r'ἄβυσσος')
e.word_ascii = 'abyssos'
e.part_of_speech = 'rzeczownik'
e.meaning1 = decode(r'otchłań (dosł.: nie posiadający głębi, nie posiadający dna)')
e.meaning2 = decode(r'głębia, przepaść')
e.meaning3 = decode(r'świat podziemny')
e.occ_count = '9'
e.origin = replace_strongid_by_link(decode(r'od G1 (jako partykuła przecząca) i odmiany G1037'))
e.occ = decode('Łk 8:31; Rz 10:7; Ap 9:1; Ap 9:2; Ap 9:11; Ap 11:7; Ap 17:8; Ap 20:1; Ap 20:3')
print(e.format())