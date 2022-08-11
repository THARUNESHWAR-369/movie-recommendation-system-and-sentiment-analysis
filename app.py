from flask import Flask
from flask import render_template
from flask import request

# import from constant
from constants.utils import UTILS

# Initialize app
app = Flask(__name__)

__UTILS = UTILS()


@app.route('/', methods=['POST', 'GET'])
def home():
    
    # Get all Movie names
    __MOVIE_NAME_LIST = __UTILS.getMovieNames()
    
    # Initialize variables
    __STATUS = False
    __ERROR = None
    
    # Get Top Search results
    __TOP_SEARCH = __UTILS.getTopSearch()
    
    if request.method == "POST":
        print(request.form.to_dict())
        searchMovieName = request.form.get('movie-name')
        
        try:
            __MOVIE_DETAILS, __CAST_DETAILS, _ = __UTILS.getMovieDetails(movie_name=searchMovieName)
            __REVIEW_DICT = __UTILS.scrap_review(imdb_id = __MOVIE_DETAILS['imdb_id'])
            __RECOMMEND_MOVIE_DETAILS_LIST = None if type(__UTILS.recommendMovie(movie_name=searchMovieName)) == str else __UTILS.recommendMovie(movie_name=searchMovieName)
            __TOP_SEARCH = None
            __STATUS = True
            
            return {
                'status':__STATUS,
                "movie-details":__MOVIE_DETAILS ,
                'cast-details':__CAST_DETAILS,
                "reviews-details":__REVIEW_DICT,
                "recommend-movies":__RECOMMEND_MOVIE_DETAILS_LIST
                }
        except:
            __STATUS = False
            return {
                "status":__STATUS
            }
    
    return render_template('home.html',error=__ERROR, movieNamesList=__MOVIE_NAME_LIST, status=__STATUS, topSearch=__TOP_SEARCH)




"""
from flask import Blueprint
from flask import render_template
from flask import request

# import from constant
from .constants.utils import UTILS

# Initialize app
__MRS = Blueprint("/", __name__) #url_prefix=""

__UTILS = UTILS()


@__MRS.route('/', methods=['POST', 'GET'])
def home():
    
    # Get all Movie names
    __MOVIE_NAME_LIST = __UTILS.getMovieNames()
    
    # Initialize variables
    __STATUS = False
    __ERROR = None
    
    # Get Top Search results
    __TOP_SEARCH = __UTILS.getTopSearch()
    
    if request.method == "POST":
        print(request.form.to_dict())
        searchMovieName = request.form.get('movie-name')
        
        try:
            __MOVIE_DETAILS, __CAST_DETAILS, _ = __UTILS.getMovieDetails(movie_name=searchMovieName)
            __REVIEW_DICT = __UTILS.scrap_review(imdb_id = __MOVIE_DETAILS['imdb_id'])
            __RECOMMEND_MOVIE_DETAILS_LIST = None if type(__UTILS.recommendMovie(movie_name=searchMovieName)) == str else __UTILS.recommendMovie(movie_name=searchMovieName)
            __TOP_SEARCH = None
            __STATUS = True
            
            return render_template('home.html', error=__ERROR, movieNamesList=__MOVIE_NAME_LIST, status=__STATUS,context={
                'status':__STATUS,
                "movie-details":__MOVIE_DETAILS ,
                'cast-details':None if len(__CAST_DETAILS) == 0 else __CAST_DETAILS,
                "reviews-details":__REVIEW_DICT,
                "recommend-movies":__RECOMMEND_MOVIE_DETAILS_LIST
                }
            )
        except Exception as e:
            print("APP ERROR: ",e)
            __STATUS = False
            return render_template('home.html',error=__ERROR, movieNamesList=__MOVIE_NAME_LIST, status=__STATUS, topSearch=__TOP_SEARCH )
    
    return render_template('home.html',error=__ERROR, movieNamesList=__MOVIE_NAME_LIST, status=__STATUS, topSearch=__TOP_SEARCH)
"""