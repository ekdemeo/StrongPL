import csv

from parser import Entry


path = "..\data\slownik_stronga.csv"

with open(path, 'r', encoding='utf-8') as csvfile:
    next(csvfile)
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        e = Entry()
        e = row[0]
        print(e)
        




