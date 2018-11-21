from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import ssl
from PlantPage import PlantPage

def main():
    urls = get_links()
    page_list = list()
    # for url in urls:
    #     page_list += [scrape_link(url)]
    page_list += [scrape_link("https://www.almanac.com/plant/growing-hyacinth-muscari")]
    return page_list


def scrape_link(link):
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    res = urlopen(req, context=ssl.SSLContext(ssl.PROTOCOL_TLS))
    html = res.read()
    soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
    print(link)
    title = soup.title.string
    title = title[:title.find(':')]
    if '|' in title:
        title = title[:title.find('|')]
    print(title)
    parse_table(title, soup.find('table'))

    page = parse_page(title, soup)
    page.set_link(link)
    return page


def parse_table(plant, table):
    for tr in table.find_all('tr'):
        th = tr.find('th')
        td = tr.find('td')
        if th and th.string and th.string.strip():
            row_name = th.string.strip()
            if td and td.a:
                print(row_name, td.a.string)
                if row_name not in db.keys():
                    if row_name != 'Botanical Name':
                        for val in td.find_all('a'):
                            db[row_name] = {val.string : [plant]}
                else:
                    if row_name != 'Botanical Name':
                        details_dict = db[row_name]
                        for val in td.find_all('a'):
                            if val.string not in details_dict.keys():
                                details_dict[val.string] = [plant]
                            else:
                                details_dict[val.string] += [plant]


def match_h3_and_div(tag):
    try:
        if tag.name == 'h3' and 'pane-title' in tag.attrs['class']:
            return True
        if tag.name == 'div' and 'field-item' in tag.attrs['class'] and 'even' in tag.attrs['class']:
            return True
    except:
        return False
    return False

def parse_page(plant, soup):
    text = ""
    urls = set()
    plant_page = PlantPage(plant)
    # remove script tags from soup
    [x.extract() for x in soup.findAll(['script', 'form'])]
    # remove comments from soup
    [x.extract() for x in soup.findAll('div', {'id':'comments'})]
    curr_head = ""
    plant_page.add_heading(curr_head)
    for element in soup.find_all(match_h3_and_div):
        if element.name == 'h3':
            if element.get_text():
                curr_head = element.get_text().strip()
                plant_page.add_heading(curr_head)
                text += curr_head + '\n'
        else:
            for link in element.find_all('a'):
                if link.get('href'):
                    urls.add(base_url + link.get('href'))
            if element.get_text():
                div_text = element.get_text().strip()
                plant_page.add_div(curr_head, div_text)
                text += div_text + '\n'
    print(text)
    return plant_page
    # '\n'.join(urls)


def get_links():
    req = Request(starter_url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urlopen(req, context=ssl.SSLContext(ssl.PROTOCOL_TLS))
    html = res.read()
    soup = BeautifulSoup(html, 'html.parser')
    urls = set()
    for link in soup.find_all('a'):
        if link.get('href') and link.get('href').startswith('/plant/'):
            urls.add(base_url + link.get('href'))
    return urls


if __name__ == '__main__':
    # constant variables
    starter_url = 'https://www.almanac.com/gardening/growing-guides'
    base_url = 'https://www.almanac.com'
    db = dict()
    content_db = dict()
    main()
    print(db)
