import re
from imdb import IMDb

ia = IMDb()

def prepare_title(title):
	pattern1 = '(- Season .*)'
	pattern2 = r'( \[.*\] )'
	if re.search(pattern1, title):
		parts = re.split(pattern1, title)
		title =''.join(parts[0])
	elif re.search(pattern2, title):
		parts = re.split(pattern2, title)
		title = ' '.join((parts[0], parts[2]))
	return title

def get_id(title):
	movies = ia.search_movie(title)
	return movies[0].movieID

def get_description(title):
	try:
		id = get_id(prepare_title(title))
		description = ia.get_movie(id)['plot'][0]
	except:
		return "Unable to generate description"
	return description.split('::')[0]
