
import csv
from string import Template
from unicode import decode
import sqlite3
import itertools

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
\plain \f2\fs22 $strong_id \plain \f3\lang1032\fs22\cf2 $word_uni \plain \f2\b\fs22\cf2  
\plain \f2\fs22 [\plain \f2\b\fs22 $word_ascii]; \plain \f2\i\fs22 $part_of_speech
$meaning
\par \plain \f2\fs22 P: $origin
\line \plain \f2\fs22 W: ($occ_count) \plain \f2\fs22 $occ \par}
""")

    def format_meaning(self):
        if not self.meaning2:
            self.meaning = r"""\par \plain \f2\b\fs22 """ + self.meaning1 + """\n"""
            return
        else:
            self.meaning = r"""\par \plain \f2\b\fs22 1. """ + self.meaning1 + """\n"""
            self.meaning = self.meaning + r"""\line \ltrch 2. """ + self.meaning2 + """\n"""

        if self.meaning3:
            self.meaning = self.meaning + r"""\line 3. """ + self.meaning3 + """\n"""
            

    def format(self):
        self.format_meaning()
        return self.rtf.substitute(self.__dict__)


## Functions 
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

def readcsv_entires(path):
    with open(path, 'r', encoding='utf-8') as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            e = Entry()
            e.strong_id = row[0]
            e.id = e.strong_id[1:]
            merged_split = row[1].split(';')
            words = merged_split[0].split(' ')
            e.word_uni = decode(words[1].strip())
            e.word_ascii = decode(words[2].strip('[]'))
            e.part_of_speech = merged_split[1].strip();
            e.meaning1 = decode(row[2]) 
            e.meaning2 = decode(row[3]) 
            e.meaning3 = decode(row[4])
            e.origin = replace_strongid_by_link(decode(row[5]))
            e.occ_count = row[6]
            e.occ = decode(row[7])
            yield e;



dict_path = "..\data\slownik_stronga.csv"
db_path = '..\data\StrongPL_test.twm'

conn = sqlite3.connect(db_path)
entries = readcsv_entires(dict_path)

entries = itertools.islice(entries, 100)

for entry in entries:
    id = str(int(entry.id)+1)
    conn.execute("UPDATE content set data = ? where topic_id = ?", (entry.format(), id))
    print("updated " + id)

conn.commit()
conn.close()


# e = 'coś komuś'
# d = decode(e)
# print(d)
# e = Entry();
# e.id = 'G13'
# e.word_uni = decode(r'ἄβυσσος')
# e.word_ascii = 'abyssos'
# e.part_of_speech = 'rzeczownik'
# e.meaning1 = decode(r'otchłań (dosł.: nie posiadający głębi, nie posiadający dna)')
# e.meaning2 = decode(r'głębia, przepaść')
# e.meaning3 = decode(r'świat podziemny')
# e.occ_count = '9'
# e.origin = replace_strongid_by_link(decode(r'od G1 (jako partykuła przecząca) i odmiany G1037'))
# e.occ = decode('Łk 8:31; Rz 10:7; Ap 9:1; Ap 9:2; Ap 9:11; Ap 11:7; Ap 17:8; Ap 20:1; Ap 20:3')

# print(e.format())