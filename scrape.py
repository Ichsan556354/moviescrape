import requests
from bs4 import BeautifulSoup
import mysql.connector

connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="movie_imdb"
)

cursor = connection.cursor()
headers = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
}
data=[]

def scrape_data():
    r = requests.get('https://www.imdb.com/chart/top/', headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    results = soup.find("ul", class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-71ed9118-0 kxsUNk compact-list-view ipc-metadata-list--base")

    movies_elements = results.find_all("div", class_="ipc-metadata-list-summary-item__tc")

    selected_data = movies_elements[:100]
    for idx, movies_element in enumerate(selected_data, 1):
        title_movies = movies_element.find("h3", class_="ipc-title__text")
        year_movies = movies_element.find("span", class_="sc-be6f1408-8 fcCUPU cli-title-metadata-item")
        rating = movies_element.find("span", attrs={"data-testid": "ratingGroup--imdb-rating"})

        title2 = title_movies.text.strip().replace(f'{str(idx)}. ', '')
        year = year_movies.text.strip()
        rating2 = rating.text.strip().split()
        rating = rating2[0]
        viewer = rating2[1].replace('(', '').replace(')', '')

        print(f"{idx}. Title: {title2}")
        print(f"Year = {year}")
        print(f"Rating = {rating}")
        print(f"Penonton = {viewer}")
        print()

        data.append({"id": idx-1, "title": title2, "year": int(year), "rating": float(rating), "viewer": viewer})
        cursor.execute("INSERT INTO movie1 (title, year, rating, viewer) VALUES (%s, %s, %s, %s)", (title2, int(year), float(rating), viewer))
    connection.commit()
    cursor.close()
    connection.close()

scrape_data()
print(data)