import re
from imdb import Cinemagoer

ia = Cinemagoer()

def prepare_title(title):
	pattern1 = '(- Season .*)'
	pattern2 = r'( \[.*\])$'
	if re.search(pattern1, title):
		parts = re.split(pattern1, title)
		title = ''.join(parts[0])
	elif re.search(pattern2, title):
		parts = re.split(pattern2, title)
		title = ''.join(parts[0])
	return title

def get_id(title):
	movies = ia.search_movie(title)
	return movies[0].movieID

def get_description(title):
	try:
		id = get_id(prepare_title(title))
		description = ia.get_movie(id)['plot'][0]
	except IndexError:
		return "Title not found on IMDB"
	except KeyError:
		return "Description is not available for this title"
	return description.split('::')[0]
