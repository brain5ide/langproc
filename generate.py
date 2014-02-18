import pdb
#
import math
# random paketas atsitiktiniam zodziu sudeliojimui
import random

# regular expressions paketas patogiam skaidymui i tris dalis
import re

# itertools helps to create permutations
import itertools

import pprint

import sys

deep = ''

symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ', '.', ',', '?', '!', '(', ')', ':', ';', '-']
punc = '.,?!\(\);:\-'

# global counters
# how many phrases were tried to match in current iteration
match_count = 0
# how many phrases are predicted to match in current iteration
match_predict = 0
lastpr = 0.0


def scramble(text):
    if len(text) % 3 == 1:
        text = text + '  '
    if len(text) % 3 == 2:
        text = text + ' '

    split = re.findall('...?', text)
    random.shuffle(split)
    return split


def smart_words(wlist, crypt, permlength=3):
    cryptset = set(crypt)
    cryptlist = list(cryptset)
    tr_length = int(math.ceil(len(crypt)))
    print 'Triplet length of scrambled text: ', tr_length
    print 'Generating triplet permutations of length: ', permlength
    print 'Number of permutations: ', reduce(lambda x, y: x * y, list(xrange(int(math.ceil(len(crypt) / 3.0)), int(math.ceil(len(crypt) / 3 - permlength - 1)), -1)))
    if len(crypt) <= permlength:
        permutations = [p for p in itertools.permutations(cryptlist)]
    else:
        permutations = [p for p in itertools.permutations(cryptlist, permlength)]
    print 'Finding words in permutations'
    perms = [''.join(p) for p in permutations]
    print 'Making a flat list of permutations'
    permarr = zip(perms, permutations)
    print 'Permarr: ', permarr[0:10]
    permwords = [[w, sublist[1]] for sublist in permarr for w in re.findall(r"\w+", sublist[0])]
    print 'Generating a dict'
    permdict = {}
    for key, value in permwords:
        concat = ''.join(value)
        key = key.lower()
        mobj = re.search(r"\b"+key+r"\b", concat.lower())
        if not mobj:
            continue
        #mobj = re.search(key, concat.lower())
        wordstart = int(math.floor(mobj.start() / 3))
        wordend = int(math.floor(mobj.end() / 3))
        if mobj.end() % 3 != 0:
            wordend += 1
        cleanword = value[wordstart:wordend]
        if key in permdict:
            if cleanword not in permdict[key]:
                permdict[key] = permdict[key] + [cleanword]
        else:
            permdict[key] = [cleanword]

    #permdict = dict((key, value) for [key, value] in permwords)
    print 'Permutations completed'
    print 'Number of unique permutations: ', len(permdict)
    print 'Starting search of known words'
    found = {word: permdict[word] for word in wlist if word in permdict}
    print 'Found', len(found), 'words'
    return found

def phrase_beg(word_dict):
    """ pick words from dict that are a beginning of a phrase """
    newdict = {}
    for key in word_dict:
        for item in word_dict[key]:
            if re.match('[A-Za-z][ ][A-Za-z]', item[0]):
                if key not in newdict:
                    newdict[key] = [item]
                else:
                    newdict[key] = newdict[key] + [item]
    return newdict

def phrase_end(word_dict):
    """ pick words from dict that are an ending of a phrase """
    newdict = {}
    for key in word_dict:
        for item in word_dict[key]:
            if re.match('[A-Za-z][ ][A-Za-z]', item[-1]):
                if key not in newdict:
                    newdict[key] = [item]
                else:
                    newdict[key] = newdict[key] + [item]
    return newdict

def phrase_mid(word_dict):
    """ pick phrases from dict that are middle of a longer phrase """
    newdict = {}
    for key in word_dict:
        for item in word_dict[key]:
            if re.match('[A-Za-z][ ][A-Za-z]', item[-1]) or re.match('[A-Za-z][ ][A-Za-z]', item[0]):
                continue;
            if key not in newdict:
                newdict[key] = [item]
            else:
                newdict[key] = newdict[key] + [item]
    return newdict

def phrases(word_dict):
    phrases = {}
    for key in word_dict:
        for item in word_dict[key]:
            if re.match('[A-Za-z][ ][A-Za-z]', item[-1]):
                for key2 in word_dict:
                    for item2 in word_dict[key2]:
                        if item[-1] == item2[0]:
                            joinkey = key+' '+key2
                            if joinkey not in phrases:
                                phrases[joinkey] = [item + item2[1:]]
                            else:
                                phrases[joinkey] = phrases[joinkey] + [item + item2[1:]]

    return phrases

def loose_phrases(word_dict, triplets):
    global match_count
    global match_predict
    global lastpr

    match_count = 0
    match_predict = len(word_dict) ** 2
    lastpr = 0.0

    res = {key1+key2: [item1+item2] for key1 in word_dict for key2 in word_dict for item1 in word_dict[key1] for item2 in word_dict[key2] if items_match(item1, item2, triplets) is True}
    return dict(res.items() + word_dict.items())

def items_match(item1, item2, triplets):
    global match_count
    global match_predict
    global lastpr

    match_count += 1
    percent = float(match_count)/match_predict * 100
    if match_count % 1000000 == 0 or ((percent - lastpr) > 5.0) :
        lastpr = percent
        print '[' + str(match_count) + ']/[' + str(match_predict) + ']', '%.2f'%percent, '%'
        sys.stdout.flush()

    if len(item1)+len(item2) > len(triplets):
        return False
    list1 = list(item1)
    list2 = list(item2)
    if len([it for it in triplets if it in list1+list2]) < len(list1+list2):
        return False

    patterns = False
    if re.match('[A-Za-z][A-Za-z][A-Za-z' + punc + ']', item1[-1]) and re.match('[ ][A-Za-z][A-Za-z]', item2[0]):
        patterns = True
    if re.match('[A-Za-z][A-Za-z' + punc + '][ ]', item1[-1]) and re.match('[A-Za-z][A-Za-z '+punc+'][A-Za-z '+punc+']', item2[0]):
        patterns = True
    if re.match('[A-Za-z][A-Za-z][A-Za-z]', item1[-1]) and re.match('[ '+punc+'][ '+punc+'][ '+punc+']', item2[0]):
        patterns = True
    if patterns == False:
        return False

    if len(phrase_possible([item1+item2], triplets)) == 0:
        return False

    return True


def phrase_possible(phrase, triplets):
    """ validates if a phrase is possible with given triplets """
    temp_trip = triplets[:]
    res = []
    for variant in phrase:
        good = True
        for item in variant:
            if item not in temp_trip:
                good = False
            else:
                temp_trip.remove(item)
        if good==True:
            res.append(variant)
    return res


def possible_phrases(phrases, triplets):
    res = {phr: phrase_possible(phrases[phr], triplets) for phr in phrases if len(phrase_possible(phrases[phr], triplets))>0}
    return res

def max_phraselen(phrases):
    maxlen = 0
    maxphrase = []
    for phr in phrases:
        for item in phrases[phr]:
            ln = len(item)
            if ln > maxlen:
                maxlen = ln
                maxphrase = []
            if ln == maxlen:
                maxphrase.append(phrases[phr])

    return maxlen


def split_phrases_by_length(phrases):
    rez = dict()
    maxl = max_phraselen(phrases)
    for i in range(1, maxl+1):
        rez[i] = dict()

    for single in phrases:
        for item in phrases[single]:
            rez[len(item)][single] = phrases[single]

    #print_struct(rez[maxl-1], 'Max-1: ')
    #print_struct(rez[maxl], 'Max: ')

    return rez

def phrase_lenstat(phrases):
    print 'Lenstat: '
    spl = split_phrases_by_length(phrases)
    for i in spl:
        print 'Length: ', i, ', # of phrases: ', len(spl[i])


def print_struct(phrases, prefix=''):
    for key in phrases:
        #print prefix, 'Key: ', key
        for item in phrases[key]:
            print prefix, ''.join(item)


def sentences(phrases):
    rez = {key: [item] for key in phrases for item in phrases[key] if valid_sentence(''.join(item)) is True}
    return rez


def punct_only(triplets):
    global punc
    rez = dict()
    for item in triplets:
        if re.search('['+punc+' ]['+punc+' ]['+punc+' ]', item):
            rez[item] = [(item, )]
    return rez


def valid_sentence(string):
    expr = "[A-Z]"
    expr += "(?:[^.?!]+|"
    expr += "[^a-zA-Z0-9-_]"
    expr += "(?:[a-zA-Z0-9-_].\d+\.|a\.[\s\-]?A\.)"
    expr += ")"
    expr += "{3,}[\.\?\!]+(?!\s[a-z])"

    sentences = re.findall(expr, string + ' .')
    if ' '.join(sentences) != string.strip():
        return False
    else:
        return True


