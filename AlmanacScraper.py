from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import ssl
from PlantPage import PlantPage
import _pickle as pickle
import sys

def main():
    urls = get_links()
    page_list = dict()
    for url in urls:
        plant = scrape_link(url)
        page_list[plant.name] = plant
    # page_list += [scrape_link("https://www.almanac.com/plant/growing-hyacinth-muscari")]
    file = open("plantpages.pkl", "wb")
    pickle.dump(page_list, file)
    file.close()
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
    """
    Retrieve only h3 tags and div tags with a specific class from Soup
    :param tag: html element
    :return: filtered soup
    """
    try:
        if tag.name == 'h3' and 'pane-title' in tag.attrs['class']:
            return True
        if tag.name == 'div' and 'field-item' in tag.attrs['class'] and 'even' in tag.attrs['class']:
            return True
    except:
        return False
    return False

def parse_page(plant, soup):
    """
    Scrape data from a plant page. Store data in a dictionary (mock db)
    and a PlantPage object.
    :param plant: page title - the plant name
    :param soup: bs4 object
    :return: PlantPage object
    """
    text = ""   # stores text on the page
    urls = set()
    plant_page = PlantPage(plant)
    [x.extract() for x in soup.findAll(['script', 'form'])]    # remove script tags from soup
    [x.extract() for x in soup.findAll('div', {'id':'comments'})]    # remove comments from soup
    curr_head = ""  # keep track of what the following text pertains to
    plant_page.add_heading(curr_head)
    for element in soup.find_all(match_h3_and_div):
        # update the heading (topic)
        if element.name == 'h3':
            if element.get_text():
                curr_head = element.get_text().strip()
                plant_page.add_heading(curr_head)
                text += curr_head + '\n'
        # get text from the div
        else:
            # save links from the div
            for link in element.find_all('a'):
                if link.get('href'):
                    if link.get('href')[0] == '/':
                        urls.add(base_url + link.get('href'))
                    else:
                        urls.add(link.get('href'))
            # save text from the div
            if element.get_text():
                div_text = element.get_text().strip()
                for line in div_text.split('\n'):
                    if line.strip():
                        plant_page.add_div(curr_head, line)
                text += div_text + '\n'
    plant_page.set_text(text)
    plant_page.set_references(urls)
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
    sys.setrecursionlimit(3500)
    starter_url = 'https://www.almanac.com/gardening/growing-guides'
    base_url = 'https://www.almanac.com'
    db = dict()
    main()
    dbfile = open("plantdb.pkl", "wb")
    pickle.dump(db, dbfile)
    dbfile.close()
    print(db)
