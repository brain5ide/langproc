import generate as gen
import sys
import getopt
import pickle

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

    scrambled = gen.Scramble(plaintext)
    print 'Scrambled: ', ''.join(scrambled)

    words = gen.Words(wlist, scrambled, 4)
    print 'All words: ', words

    finaldict = gen.LoopPossiblePhrases(words, scrambled)
    print 'Finaldict: ', sorted(finaldict.items())

    finalcombo = gen.LoopLoosePhrases(finaldict, scrambled)

    puncts = gen.punct_only(scrambled)
    print 'Triplets that contain only punctuation: ', len(puncts)
    if len(puncts) > 0:
        print 'Including punct-only triplets in the queue.'
        finalcombo = gen.LoosePhrases(dict(finalcombo.items() + finaldict.items() + puncts.items()), scrambled)

    final_sentences = gen.LoopSentences(finalcombo)
    printlen = gen.max_phraselen(final_sentences)
    gen.print_struct(final_sentences, 'Answer: ')
    print len(final_sentences), 'sentences of', printlen, 'triplets'
    print 'Input: ', len(scrambled), scrambled


def usage():
    print 'Usage: '
    print '-d for debug'
    print 'Nothing for default values'
    return


def main(argv):
    d_TestString = 'Sentence and testing of scrambled algorithm. OK!'
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

