# -*- coding: utf-8 -*-
import json
import os
import argparse
import platform

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
    args = parser.parse_args()
    segdict = makedict('phrasetext.txt')
    if platform.system() == 'Windows':
        result = wordseg(args.text.decode('GBK'), segdict)
    else:
        result = wordseg(args.text.decode('utf-8'), segdict)
    showresult = result[0]
    for i in result[1:]:
        showresult += '|||'+i
    print showresult