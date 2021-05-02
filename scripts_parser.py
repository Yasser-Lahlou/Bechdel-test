import requests, re, csv
from bs4 import BeautifulSoup

URL = 'https://imsdb.com/all-scripts.html'
URL_BASE = 'https://www.imsdb.com/scripts/'

headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36'
            }
# save all home page scripts
def scrap_list(url):
    response = requests.get(url, headers=headers)
    with open('data/IMSDB_script_list', "w") as f:
        f.write(response.text)
scrap_list(URL)

# create list of movie titles and script urls and saves in csv
def movie_list():
    with open('data/IMSDB_script_list', "r") as f:
        data = f.read()
    soup = BeautifulSoup(data, features="lxml")
    movies_list = soup.select('p a')
    list_urls = []
    for movie in movies_list:
        #get clean movie title
        clean_title = movie.text
        #get filepath movie title
        movie_title = movie['title']
        movie_title = movie_title.replace(' ', '-')
        movie_title = re.sub(r'\:', '', movie_title)
        movie_title = re.sub(r'-Script', '', movie_title)
        movie_url = URL_BASE + movie_title + '.html'
        list_urls.append([movie_title, movie_url, clean_title])
    with open('data/movie_titles.csv', 'w', newline='') as f:
        wr = csv.writer(f)
        wr.writerows(list_urls)
    return list_urls

# create list of movie titles to perform a search
def movie_csv():
    list_urls = movie_list()
    list_titles = [movie[2] for movie in list_urls]
    with open('data/movie_titles.txt', "w") as f:
        for title in list_titles:
            f.write("%s\n" % title)
# for each movie url, save script content in a .txt file (and identifies errors)
def scrap_script(title, url, clean_title):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, features="lxml")
    tags = soup.select('pre')
    non_scraped = []
    if len(tags) != 0:
        script = tags[-1]
        with open(f'IMSDB_scripts/{title}.txt', "w", encoding='utf-8', errors='ignore') as f:
            f.write(clean_title)
            f.write('\n')
            f.write(script.text)
    else:
        non_scraped.append(title)
    return non_scraped

# create all .txt files
for movie in movie_list():
    scrap_script(movie[0], movie[1], movie[2])
