import requests
from bs4 import BeautifulSoup


URLS = [
    'http://www.sejm.gov.pl/prawo/konst/polski/wstep.htm',
    'http://www.sejm.gov.pl/prawo/konst/polski/1.htm',
    'http://www.sejm.gov.pl/prawo/konst/polski/2.htm',
    'http://www.sejm.gov.pl/prawo/konst/polski/3.htm',
    'http://www.sejm.gov.pl/prawo/konst/polski/4.htm',
    'http://www.sejm.gov.pl/prawo/konst/polski/5.htm',
    'http://www.sejm.gov.pl/prawo/konst/polski/6.htm',
    'http://www.sejm.gov.pl/prawo/konst/polski/7.htm',
    'http://www.sejm.gov.pl/prawo/konst/polski/8.htm',
    'http://www.sejm.gov.pl/prawo/konst/polski/9.htm',
    'http://www.sejm.gov.pl/prawo/konst/polski/10.htm',
    'http://www.sejm.gov.pl/prawo/konst/polski/11.htm',
    'http://www.sejm.gov.pl/prawo/konst/polski/12.htm',
    'http://www.sejm.gov.pl/prawo/konst/polski/13.htm',
]

def get_raw_text():
    text = ''
    for url in URLS:
        text += BeautifulSoup(requests.get(url).content, 'html.parser').text
    return text


def main():
    text = get_raw_text()
    with open('constitution.txt', 'wt') as f:
        f.write(get_raw_text())


if __name__ == '__main__':
    main()