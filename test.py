source_text = '''
text1
text2
http://url.com/bla1/blah1/
text3
text4
[label](http://url.com/bla2/blah2/)
text5
text6    '''

import re
#url_reg = r'\((http[^)]+)\)'
url_reg = r'([a-z]*[:.]+[^\s\)]+)'
result = re.sub(url_reg, r'<\1>', source_text)
print(result)
