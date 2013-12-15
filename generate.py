# random paketas atsitiktiniam zodziu sudeliojimui
import random

# regular expressions paketas patogiam skaidymui i tris dalis
import re

# file that contains words
wordfile = 'wordlists/EN.txt'

# number of words to produce
wordnum = 10

allwords = [w.strip() for w in open(wordfile, "rb").readlines()]

used_words = random.sample(allwords, wordnum)
plaintext = " ".join(used_words)

split_text = re.findall('..?', plaintext) 
random.shuffle(split_text)
crypt_text = ''.join(split_text) 
