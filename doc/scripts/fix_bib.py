# -*- coding: utf-8 -*-
# https://www.python.org/dev/peps/pep-0263/
# Stephen Weinreich
# Murmann Mixed-Signal Group, Stanford University
# Jan 2020

import fileinput
import re

STR_TITLE_FIELD = 'title ='
STR_BOOKTITLE_FIELD = 'booktitle ='

x = []
for line in fileinput.input("cadwiki_example.bib", inplace=True):
    # Fix months
    if 'month = {' in line:
        line = line.replace('{','').replace('}','')
    # Use IEEE format journal names
    if 'journal = {IEEE Transactions on Circuits and Systems I: Regular Papers},' in line:
        line = 'journal = IEEE_J_CASI_RP,\r\n'
    if 'journal = {IEEE Transactions on Circuits and Systems II: Express Briefs},' in line:
        line = 'journal = IEEE_J_CASII_EB,\r\n'
    if 'journal = {IEEE Transactions on Biomedical Circuits and Systems},' in line:
        line = 'journal = IEEE_J_BCAS,\r\n'
    if 'journal = {IEEE Journal of Solid-State Circuits},' in line:
        line = 'journal = IEEE_J_JSSC,\r\n'
    if STR_BOOKTITLE_FIELD in line:
        line = line.replace('Conference', 'Conf.')
        line = line.replace('Proceedings of the', 'Proc.')
        line = line.replace('Proceedings of', 'Proc.')
        line = line.replace('Symposium', 'Symp.')
        line = line.replace('National', 'Nat.')
        line = line.replace('International', 'Int.')
    # Fix titles: default no capitalization, except some specific words
    # Important: make sure all non-roman characters are in math (eg: mu should be $\mu$)
    if line.startswith(STR_TITLE_FIELD) or line.startswith(STR_BOOKTITLE_FIELD):# in line and 'booktitle = {' not in line:
        # line = line.replace('{{', '{').replace('}}', '}')
        line = line.replace('\n', '')
        line = line[0:-1] if line.endswith(',') else line
        line = line.replace('{', '')
        line = line.replace('}', '')
        line = line.replace('dB','{dB}')
        line = line.replace('Hz','{Hz}')
        line = line.replace('mV','{mV}')
        line = line.replace('IoT','{IoT}')
        line = line.replace('SoC', '{SoC}')
        line = line.replace('\\mu', '\\upmu')
        line = line.replace('nW', '{nW}')
        line = line.replace('mW', '{mW}')
        # Find all letters/words that are all caps, and standing on their own
        # Then replace them with {WORD} so that they're properly capitalized
        # TO DO: ignore anything already within {}
        # TO DO: Can I write this in a single line using re.sub? Seems inefficient to search, make a decision, then search again to replace
        # words = re.split('[,-:+ {}\$(0-9)]', line.strip().strip('title = '))
        words = re.split('[,-:+ {}\$(0-9)]', line.strip().strip(STR_TITLE_FIELD))
        for i,word in enumerate(words):
            if word == word.upper() and len(word) > 0 and word.isalnum():
                line = re.sub('(?P<a>^|[,-:+ {}\$(0-9)])('+word+u')(?P<b>[,-:+ {}\$(0-9)]|$)', '\g<a>{' + word + '}\g<b>', line)
                x.append([word, line])
        str_field = STR_TITLE_FIELD if line.startswith(STR_TITLE_FIELD) else STR_BOOKTITLE_FIELD
        line = str_field + ' {' + line.strip().strip(str_field) + '},\n'
    print line,

for y in x:
    print(y)