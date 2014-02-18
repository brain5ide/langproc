import generate as gen
import re
import pprint
import sys
import getopt

from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

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
    curlen = len(phrases) + len(words)
    while 1:
        newphr = gen.phrases(dict(words.items() + phrases.items()))
        newpos = gen.possible_phrases(newphr, scrambled)
        newlen = len(newpos) + len(words)
        print 'Strict: Last iteration: ', curlen, ' New iteration: ', newlen
        if newlen <= curlen:
            phrases = newpos
            break
        phrases = newpos
        curlen = newlen

    finaldict = gen.phrase_mid(dict(words.items() + phrases.items()))
    print 'Finaldict: ', sorted(finaldict.items())

    # keep finaldict for future references if needed
    curdict = finaldict
    finaldict = {key: finaldict[key] for key in finaldict if len(key) > 3}
    print 'Tru finaldict: ', sorted(finaldict.items())
    curlen = len(curdict)

    while 1:
        phrcombo = gen.loose_phrases(curdict, scrambled)
        newlen = len(phrcombo)
        print 'Loose: Last iteration: ', curlen, ' New iteration: ', newlen
        if newlen <= curlen:
            finalcombo = phrcombo
            break
        curdict = phrcombo
        curlen = newlen

    puncts = gen.punct_only(scrambled)
    if len(puncts) > 0:
        finalcombo = gen.loose_phrases(dict(finalcombo.items() + puncts.items()), scrambled)

    final = gen.split_phrases_by_length(finalcombo)
    maxlen = gen.max_phraselen(finalcombo)
    printlen = maxlen
    final_sentences = gen.sentences(final[printlen])
    while len(final_sentences) == 0 and printlen != 0:
        printlen -= 1
        print 'Length ', printlen, ' has no valid sentences, in all', len(final[printlen]), 'of them.'
        final_sentences = gen.sentences(final[printlen])

    gen.print_struct(final_sentences, 'Answer: ')
    print 'Finaldict: ', len(finaldict), 'Curdict: ', len(curdict), ' Phrcombo: ', len(phrcombo)
    print 'Sentences: ', len(final_sentences)

    #gen.phrase_lenstat(newphrcombo)
    #print 'Newphrcombo: ', len(newphrcombo)

    #gen.print_struct(gen.sentences(phrcombo))
    #while 1:
    #    phrcombo = gen.loose_phrases(curdict, scrambled)
    #    phrcombo_split = gen.split_phrases_by_length(phrcombo)
    #    newlen = len(phrcombo)
    #    print 'Loose: Last iteration: ', curlen, ' New iteration: ', newlen
    #    if newlen <= curlen:
    #        finalcombo = phrcombo
    #        break
    #    curdict = phrcombo
    #    curlen = newlen

    #print 'Len phrases: ', len(phrases)

    #gen.phrase_lenstat(finalcombo)
    print 'Input: ', len(scrambled), scrambled


def usage():
    print 'Usage: '
    print '-d for debug'
    print 'Nothing for default values'
    return


def main(argv):
    d_TestString = 'There is no sunshine. She is gone. OK!'
    debug = False
    run = False
    teststring = d_TestString

    try:
        opts, args = getopt.getopt(argv, "d", ["debug"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-d", "--debug"):
            debug = True

    if debug is True:
        print 'Debug mode on'
        with PyCallGraph(output=GraphvizOutput()):
            run = True
            test_dict(teststring, allwords)

    if run is False:
        test_dict(teststring, allwords)

    return 0

if __name__ == "__main__":
    main(sys.argv[1:])

