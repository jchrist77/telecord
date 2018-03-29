source_text = '''
text1
text2
http://url.com/bla1/blah1/
text3
text4
[label](http://url.com/bla2/blah2/)
[label](https://url.com/bla2/blah2/)
[label]https://url.com/bla2/blah2/
:sparkle: #LUN :arrow_right:
:sparkle: Critical Oversold levels (3.75/5)
:part_alternation_mark: Vol: 15.12 BTC
:dollar: Price: 0.00114004 BTC
:clock3: 1H: -1.06%
:clock1: 24H: -7.84%
:clock6: 7D: -24.27%
text5
text6    '''

import re
#url_reg = r'\((http[^)]+)\)'
url_reg = r'(https?[:.]+[^\s\)]+)'
result = re.sub(url_reg, r'<\1>', source_text)
print(result)
