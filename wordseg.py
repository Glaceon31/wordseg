# -*- coding: utf-8 -*-
import json
import os
import argparse
import platform
import codecs

def addpharse(phrase, segdict):
    #print phrase
    nowpos = segdict
    for i in range(0, len(phrase)):
        if nowpos.has_key(phrase[i]):
            nowpos = nowpos[phrase[i]]
            continue
        else:
            nowpos[phrase[i]] = {}
            nowpos = nowpos[phrase[i]]
            continue

def makedict(filename):
    segdict = {}
    phrases = json.loads(open(filename, 'rb').read())
    for i in phrases:
        addpharse(i,segdict)
    return segdict

def wordseg(text, segdict):
    result = []
    pos = 0
    nextpos = 1
    #text = text[:3]+'1'+text[3:]

    while pos < len(text):
        #print pos,nextpos,len(text),result,text[pos]
        if not segdict.has_key(text[pos]):
            result.append(text[pos:nextpos])
            pos = nextpos
            nextpos = pos+1
            continue
        dictpos = segdict[text[pos]]
        while nextpos <= len(text):
            if nextpos >= len(text):
                result.append(text[pos:nextpos])
                pos = nextpos
                nextpos = pos+1
                break
            if not dictpos.has_key(text[nextpos]):
                result.append(text[pos:nextpos])
                pos = nextpos
                nextpos = pos+1
                break
            else:
                dictpos = dictpos[text[nextpos]]
            nextpos += 1
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('text')
    parser.add_argument('-f', '--file', action="store_true")
    parser.add_argument('-o', '--outputfile', action="store", default = '')
    args = parser.parse_args()
    segdict = makedict('phrasetext.txt')
    if args.file:
        textinput = open(args.text, 'rb').read().split('\n')
        if platform.system() == 'Windows':
            result = '\n'.join([' '.join(wordseg(text.decode('GBK'), segdict)) for text in textinput])
        else:
            result = wordseg(textinput.decode('utf-8'), segdict)
    else:
        textinput = args.text
        if platform.system() == 'Windows':
            result = ' '.join(wordseg(textinput.decode('GBK'), segdict))
        else:
            result = ' '.join(wordseg(textinput.decode('utf-8'), segdict))
    print result
    if args.outputfile:
        output = codecs.open(args.outputfile, 'wb', 'utf-8')
        output.write(result)
        output.close()