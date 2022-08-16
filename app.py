from flask import Flask
from flask import render_template
from flask import request

# import from constant
from constants.utils import UTILS


from tpblite import TPB

# Create a TPB object with a domain name
t = TPB('https://tpb.party')

# Or create a TPB object with default domain
t = TPB()

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
    
    """if request.method == "POST":
        print(request.form.to_dict())
        searchMovieName = request.form.get('movie-name')
        
        try:
            #__MOVIE_DETAILS, __CAST_DETAILS, _ = __UTILS.getMovieDetails(movie_name=searchMovieName)
            __REVIEW_DICT =None# __UTILS.scrap_review(imdb_id = __MOVIE_DETAILS['imdb_id'])
            #print("__REIRE_DICT: ",__REVIEW_DICT)
            __RECOMMEND_MOVIE_DETAILS_LIST = None if type(__UTILS.recommendMovie(movie_name=searchMovieName)) == str else __UTILS.recommendMovie(movie_name=searchMovieName)
            print("__RECOMMEND_MOVIE_DETAILS_LIST: ",__RECOMMEND_MOVIE_DETAILS_LIST)
            __TOP_SEARCH = None
            __STATUS = True
            
            return {
                'status':__STATUS,
                #"movie-details":__MOVIE_DETAILS ,
                #'cast-details':__CAST_DETAILS,
                "reviews-details":__REVIEW_DICT,
                "recommend-movies":__RECOMMEND_MOVIE_DETAILS_LIST
                }
        except Exception as e:
            print("app error: ",e)
            __STATUS = False
            return {
                "status":__STATUS
            }"""
    
    return render_template('home.html',error=__ERROR, movieNamesList=__MOVIE_NAME_LIST, status=__STATUS, topSearch=__TOP_SEARCH)


@app.route('/getMovieDetails', methods=['POST', 'GET'])
def getMovieDetails():
    if request.method == "POST":
        searchMovieName = request.form.get('movie-name')
        print("searchMovieName: ",searchMovieName)
        __MOVIE_DETAILS, __CAST_DETAILS, _ = __UTILS.getMovieDetails(movie_name=searchMovieName)
        
        if (__MOVIE_DETAILS and __CAST_DETAILS) != None:
            return {
            'status':True,
            "movie-details":__MOVIE_DETAILS ,
            'cast-details':__CAST_DETAILS,
            }
        return {
            "status":False
        }
    return {
        "status":False
    }


@app.route('/getMovieReviews', methods=['POST', 'GET'])
def getMovieReviews():
    if request.method == "POST":
        movie_imdb_id = request.form.get('movie_imdb_id')
        __REVIEW_DICT =  __UTILS.scrap_review(imdb_id = movie_imdb_id)
        __get = True
        return {
            'status':True,
            "reviews-details":__REVIEW_DICT,
        }
    return {
        "status":False
    }


@app.route('/getRecommendedMovies', methods=['POST', 'GET'])
def getRecommendedMovies():
    if request.method == "POST":
        searchMovieName = request.form.get('movie-name')
        print("MOVIE_NAME: ",searchMovieName)
        __RECOMMEND_MOVIE_DETAILS_LIST = __UTILS.recommendMovie(movie_name=searchMovieName)
        print("__RECOMMEND_MOVIE_DETAILS_LIST: ",__RECOMMEND_MOVIE_DETAILS_LIST)
        __get = True
        return {
            'status':True,
            "recommend-movies":__RECOMMEND_MOVIE_DETAILS_LIST,
        }
    return {
        "status":False
    }
    
@app.route("/getTorrents", methods=["POST", "GET"])
def getTorrent():
    if request.method == "POST":
        movie_name = request.form.to_dict()['movie-name']
        torrents = t.search(movie_name)
        torrent = torrents.getBestTorrent(min_seeds=30, min_filesize='500 MiB', max_filesize='4 GiB')
        try:
            print(torrent.title, torrent.filesize, torrent.url)
            return {
                "status":True,
                "torrent-title":torrent.title,
                "torrent-filesize":torrent.filesize,
                "torrent-magnetlink":torrent.magnetlink
            }
        except:
            return {
                "status":False,
                "error-msg":"No torrent found..."
            }
    return {
        "status":False,
        "error-msg":"No torrent found..."
    }


if __name__ == '__main__':
    app.debug = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.run()

