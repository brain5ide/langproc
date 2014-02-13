import generate as gen
import re
import pprint

wordfile = 'wordlists/EN.txt'

allwords = [w.strip() for w in open(wordfile, "rb").readlines()]

TEST_COUNT = 0


def test_dict(plaintext, wlist):
    global TEST_COUNT
    TEST_COUNT = TEST_COUNT + 1
    print '------ TEST', TEST_COUNT, '------'
    print 'Testing string: ', plaintext
    scrambled = gen.scramble(plaintext)
    print 'Scrambled: ', ''.join(scrambled)
    words = gen.smart_words(wlist, scrambled, 4)
    print 'All words: ', words
    phrases = gen.possible_phrases(gen.phrases(words), scrambled)
    print 'Phrases: ', phrases
    curlen = len(phrases)+len(words)
    while 1:
        newphr = gen.phrases(dict(words.items() + phrases.items()))
        newpos = gen.possible_phrases(newphr, scrambled)
        newlen = len(newpos)+len(words)
        print 'Strict: Last iteration: ', curlen, ' New iteration: ', newlen
        if newlen <= curlen:
            phrases = newpos
            break
        phrases = newpos
        curlen = newlen

    finaldict = gen.phrase_mid(dict(words.items() + phrases.items()))
    print 'Finaldict: ', finaldict

    # keep finaldict for future references if needed
    curdict = finaldict
    curlen = len(curdict)

    while 1:
        phrcombo = gen.loose_phrases(curdict, scrambled)
        phrcombo_maxlen = gen.max_phraselen(phrcombo)
        phrcombo_mid = gen.phrase_mid(dict(phrcombo.items()+finaldict.items()))
        newlen = len(phrcombo_mid)
        print 'Loose: Last iteration: ', curlen, ' New iteration: ', newlen
        if newlen <= curlen:
            finalcombo = phrcombo_mid
            break
        curdict = phrcombo_mid
        curlen = newlen

    print 'Len phrases: ', len(phrases)

    print 'Len finaldict: ', len(finaldict)
    print 'Mid phrases: ', len(gen.phrase_mid(finaldict))

    print 'Len phrcombo: ', len(phrcombo)

    gen.phrase_lenstat(curdict)

test_string = 'Single simple sentence. Another simple constructor.' # Another one to check again!'
test_dict(test_string, allwords)
