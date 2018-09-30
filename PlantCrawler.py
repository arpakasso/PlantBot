# CS 4301.001 PlantBot Project Part 1
# Reena Suh & Elizabeth Trinh
# September 24, 2018

from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import Request, urlopen
import urllib.error
import ssl
import os


def main():
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    # retrieve urls
    relevant_urls = set()
    get_urls(starter_url, relevant_urls, set())
    print("\n== retrieved urls ==\n")
    print("Relevant Urls:\n" + '\n'.join(relevant_urls))
    with open('urls.txt', 'w') as f_0:
        f_0.write('\n'.join(relevant_urls))

    # scrape urls
    scrape_text(relevant_urls)
    print('\n== scraped urls ==\n')

    print("\n== end of crawler ==\n")


def get_urls(source_url: str, url_set: set, visited: set):
    print("Source:", source_url)
    req = Request(source_url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urlopen(req, context=ssl.SSLContext(ssl.PROTOCOL_TLS))
    html = res.read()

    soup = BeautifulSoup(html, 'html.parser')

    # find urls in the webpage
    for link in soup.find_all('a'):
        # stop when 15 links have been gathered
        if len(url_set) >= 15:
            return url_set
        link_str = str(link.get('href'))
        lower_link = link_str.lower()
        # check relevancy of link
        if ('plant' in lower_link or 'garden' in lower_link) and \
                ('care' in lower_link or 'guide' in lower_link):
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
            if '#' in link_str:
                i = link_str.find('#')
                link_str = link_str[:i]
            if link_str.startswith('http') and 'google' not in link_str \
                    and link_str.count('http') == 1:
                if link_str not in url_set and res.getcode() == 200:
                    print(link_str)
                    url_set.add(link_str)
    # iterate and scrape thru links until enough are found
    for sub_link in url_set.copy():
        if len(url_set) < 15:
            # check that the link hasn't been visited before
            if sub_link not in visited:
                visited.add(sub_link)
                try:
                    url_set.union(get_urls(sub_link, url_set, visited))
                except (urllib.error.URLError, ssl.SSLError):
                    url_set.remove(sub_link)
        else:
            return url_set
    return url_set


def visible(element):
    # function to determine if an element is visible
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'meta']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def scrape_text(urls: set):
    # scrape each of the urls
    for count, curr_url in enumerate(urls):
        req = Request(curr_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req, context=ssl.SSLContext(ssl.PROTOCOL_TLS)).read()
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.findAll(text=True)
        result = filter(visible, data)
        visible_text = list(result)  # list from filter
        curr_file_name = os.path.join(dir_name, str(count) + '.txt')
        print(curr_file_name)
        with open(curr_file_name, 'w', encoding='utf-8') as f:
            f.write(' '.join(t.strip() for t in visible_text))


if __name__ == '__main__':
    # constant variables
    starter_url = 'https://www.google.com/search?q=plant+care'
    base_url = 'https://garden.org'
    dir_name = 'in'
    url_file_name = 'urls.txt'

    main()
