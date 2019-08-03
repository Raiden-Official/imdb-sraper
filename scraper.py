from bs4 import BeautifulSoup
import requests
import re
import json 
import sys


# The Godfather
# url = 'https://www.imdb.com/title/tt0068646/'

# Avengers : Endgame
# url = 'https://www.imdb.com/title/tt4154796/'

# Comment the below line if you want to use the above urls to fetch data.
url = sys.argv[1]

# Get content on the wesite by posting request.
response = requests.get(url, timeout = 5)
content = BeautifulSoup(response.content, 'html.parser')

movie_summary_text = content.find('div', class_='summary_text').text.strip()
movie_credit_details = content.find_all('div', class_='credit_summary_item')

movie_director_name = movie_credit_details[0].find_all('a')[0].string
writers_data = movie_credit_details[1].find_all('a')
stars_data = movie_credit_details[2].find_all('a')

movie_writer_names = []
for writer in writers_data:
    if writer.string != '1 more credit':
        movie_writer_names.append(writer.string)

movie_star_names = []
for star in stars_data:
    if star.string != 'See full cast & crew':
        movie_star_names.append(star.string)

movie_imdb_rating = content.find_all('span', attrs={'itemprop':'ratingValue'})[0].string

movie_details = content.find('div', class_='subtext')

movie_content_rating = movie_details.contents[0].strip()
movie_duration = movie_details.find('time').string.strip()

movie_genres = []
movie_genre_and_release_date = movie_details.find_all('span', class_='ghost')[1].find_next_siblings('a')
for tags in movie_genre_and_release_date:
    if re.match('(^[0-9])', tags.string):
        movie_release_date = tags.string.strip()
    else:
        movie_genres.append(tags.string)

movie_poster_url = content.find('div', class_='poster').contents[1].contents[1]['src']
movie_label = content.find('h1', class_='').contents
movie_name = movie_label[0].strip()
movie_year = movie_label[1].find('a').string

# Print the movie name in cmd and create an object from the scraped data:
print("Getting data for movie: "+movie_name)
movieJson = {}
movieJson['name'] = movie_name
movieJson['year'] = movie_year
movieJson['content_rating'] = movie_content_rating
movieJson['duration'] = movie_duration
movieJson['genres'] = movie_genres
movieJson['release_date'] = movie_release_date
movieJson['imdb_rating'] = movie_imdb_rating
movieJson['summary'] = movie_summary_text
movieJson['director'] = movie_director_name
movieJson['writers'] = movie_writer_names
movieJson['stars'] = movie_star_names

# Note: r+ mode appends data in front of the old data 
with open('movies.json', 'r+') as f:
    try:
        movies = json.load(f)
    except:
        json.dump([], f)
        movies = []
with open('movies.json', 'w') as f:
    # check if data doesen't exist already and then update
    exists =  False
    for movie in movies:
        if movie['name'] == movie_name:
            exists = True
        else:
            exists = False

    if exists:
        json.dump(movies, f)
    else:
        movies.append(movieJson)
        json.dump(movies, f)

