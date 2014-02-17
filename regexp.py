import re

tests = []
tests.append('ne ')
tests.append('gone. ')
tests.append('sune. ')

for item in tests:
    print 'Test: ', item, 'Result: ', re.findall(r'\bne\b', item)
