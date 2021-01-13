from imdb import IMDb
ia = IMDb()

def get_id(title):
	movies = ia.search_movie(title)
	return movies[0].movieID

def get_description(title):
	try:
		id = get_id(title)
		description = ia.get_movie(id)['plot'][0]
	except:
		return "Unable to generate description"
	return description.split('::')[0]
