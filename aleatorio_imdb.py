from imdb import *
import random
import argparse

def parse_args():
	ap = argparse.ArgumentParser()
	ap.add_argument('-trm', '--top-rated-movies', action='store_const', const=Scraper.TOP_RATED_MOVIES_URL, dest='choice', help='Escolha esse argumento caso você prefira ser indicado dos filmes mais bem votados')
	ap.add_argument('-trs', '--top-rated-shows', action='store_const', const=Scraper.TOP_RATED_SHOWS_URL, dest='choice', help='Escolha esse argumento caso você prefira ser indicado das séries mais bem votados')
	ap.add_argument('-pm', '--popular-movies', action='store_const', const=Scraper.MOST_POPULAR_MOVIES_URL, dest='choice', help='Escolha esse argumento caso você prefira ser indicado dos filmes mais populares')
	ap.add_argument('-ps', '--popular-shows', action='store_const', const=Scraper.MOST_POPULAR_SHOWS_URL, dest='choice', help='Escolha esse argumento caso você prefira ser indicado das séries mais populares')
	return vars(ap.parse_args())

def main(arg):
	some = Scraper.get(IMDBBase, arg)
	rand = random.choice(some)
	print(rand.details())

if __name__ == '__main__':
	try:
		arg = parse_args()['choice']
		main(arg)
	except Exception as ex:
		print(ex)