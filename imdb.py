import argparse
import requests
from bs4 import BeautifulSoup

class IMDBActor:
	pass

class IMDBSeason:
	pass

class IMDBEpisode:
	pass

class IMDBBase(object):
	def __init__(self, name:str, year:int, stars:str='', rating:float=0.0, n_ratings:int=0, link:str=''):
		self.name = name
		self.year = year
		self.stars = stars
		self.rating = rating
		self.n_ratings = n_ratings
		self.link = link

	def set_stars(self, stars:str):
		setattr(self, 'stars', stars)

	def set_rating(self, rating:float):
		setattr(self, 'rating', rating)

	def set_n_ratings(self, n_ratings:int):
		setattr(self, 'n_ratings', n_ratings)

	def set_link(self, link:str):
		setattr(self, 'link', link)

	def details(self):
		return f'Título: {self.name}\nAno: {self.year}\nEstrelas: {self.stars}\nPontuação: {self.rating}\nVotos: {self.n_ratings}\nLink: {self.link}'

	def __repr__(self):
		return self.name.lower().replace(' ', '_')

	def __str__(self):
		return f'{self.name} ({self.year})'

class IMDBMovie(IMDBBase):
	def __init__(self, name:str, year:int, stars:str='', rating:float=0.0, n_ratings:int=0, link:str=''):
		super().__init__(name, year, stars, rating, n_ratings, link)

class IMDBShow(IMDBBase):
	def __init__(self, name:str, year:int, stars:str='', rating:float=0.0, n_ratings:int=0, link:str=''):
		super().__init__(name, year, stars, rating, n_ratings, link)

class Scraper(object):

	TOP_RATED_MOVIES_URL = 'https://www.imdb.com/chart/top/'
	MOST_POPULAR_MOVIES_URL = 'https://www.imdb.com/chart/moviemeter/'
	TOP_RATED_SHOWS_URL = 'https://www.imdb.com/chart/toptv/'
	MOST_POPULAR_SHOWS_URL = 'https://www.imdb.com/chart/tvmeter/'
	TITLE = 'titleColumn'
	RATE = 'ratingColumn imdbRating'

	@classmethod
	def get(cls, movie_or_show, url):
		page = ''
		with requests.Session() as session:
			r = session.get(url)
			page = r.text

		soup = BeautifulSoup(page, 'html.parser')

		tb_rows = soup.find('tbody', class_='lister-list').find_all('tr')

		movies = []

		for row in tb_rows:
			try:
				title = row.find(class_=cls.TITLE)
				rate = row.find(class_=cls.RATE)

				name = title.find('a').string
				year = int(title.find('span').string[1:-1])
				stars = title.find('a').get('title')
				if rate.find('strong') != None:
					rating = float(rate.find('strong').string.replace(',', '.'))
					n_ratings = int(rate.find('strong').get('title')[13:-13].replace(',', ''))
				link = f"https://www.imdb.com{title.find('a').get('href')}"

				movies.append(movie_or_show(name, year, stars, rating, n_ratings, link))
			except Exception as ex:
				raise ex

		return movies

if __name__ == '__main__':
	print(Scraper.get(IMDBShow, Scraper.MOST_POPULAR_SHOWS_URL)[0].details())