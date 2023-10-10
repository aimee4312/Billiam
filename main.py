import pymongo
import interactions
import random

from interactions import slash_command
from config import TOKEN, MONGODB

billiam = interactions.Client(token=TOKEN)
mongo_billiam = pymongo.MongoClient(MONGODB)
db = mongo_billiam['Watchlist']

@billiam.event
async def on_ready():
    print('We have logged in as {0.user}'.format(billiam))

# /add-movie
@slash_command(
    name="add-movie",
    description="Add a movie to the list",
    options=[
        {
            "name": "movie",
            "description": "The name of the movie",
            "type": 3,
            "required": True,
        }
    ]
)
async def add_movie(ctx, movie: str):
    collection = db['Movies']
    existing_movie = collection.find_one({"name": movie})
    
    if existing_movie:
        print(f"Movie '{movie}' already exists in the collection.")
    else:
        movie_document = {
            "name": movie,
            "watched": False
        }
        collection.insert_one(movie_document)
        await ctx.respond(f"Added '{movie}' to the movie list.")

# /add-show
@slash_command(
    name="add-show",
    description="Add a show to the list",
    options=[
        {
            "name": "show",
            "description": "The name of the show",
            "type": 3,
            "required": True,
        }
    ]
)
async def add_show(ctx, show: str):
    collection = db['Shows']
    existing_show = collection.find_one({"name": show})
    
    if existing_show:
        print(f"Show '{show}' already exists in the collection.")
    else:
        show_document = {
            "name": show,
            "watched": False
        }
        collection.insert_one(show_document)
        await ctx.respond(f"Added '{show}' to the show list.")

# /get-movie
@slash_command(
    name="get-movie",
    description="Get a random movie off the list",
)
async def get_movie(ctx):
    collection = db['Movies']

    unwatched_movies = list(collection.find({"watched": False}))
    if not unwatched_movies:
        await ctx.respond("There are no unwateched movies in the list.")
    else:
        random_movie = random.choice(unwatched_movies)
        collection.update_one({"_id": random_movie["_id"]}, {"$set": {"watched": True}})
        await ctx.respond(f"Random Movie: {random_movie['name']}")

# /get-show
@slash_command(
    name="get-show",
    description="Get a random show off the list",
)
async def get_show(ctx):
    collection = db['Shows']

    unwatched_shows = list(collection.find({"watched": False}))
    if not unwatched_shows:
        await ctx.respond("There are no unwateched shows in the list.")
    else:
        random_show = random.choice(unwatched_shows)
        collection.update_one({"_id": random_show["_id"]}, {"$set": {"watched": True}})
        await ctx.respond(f"Random Show: {random_show['name']}")

# /viewed-movies
@slash_command(
    name="viewed-movies",
    description="Display list of viewed movies",
)
async def viewed_movies(ctx):
    collection = db['Movies']

    watched_movies = list(collection.find({"watched": True}))
    num_movies = collection.count_documents({"watched": True})
    if num_movies == 0:
        await ctx.respond("There are no movies watched.")
    else:
        
        movie_list = "\n".join([f"{i + 1}. {movie['name']}" for i, movie in enumerate(watched_movies)])
        await ctx.respond("List of Watched Movies:\n" + movie_list)

# /viewed-shows
@slash_command(
    name="viewed-shows",
    description="Display list of viewed shows",
)
async def viewed_shows(ctx):
    collection = db['Shows']

    watched_shows = list(collection.find({"watched": True}))
    num_shows = collection.count_documents({"watched": True})
    if num_shows == 0:
        await ctx.respond("There are no shows watched.")
    else:
        
        shows_list = "\n".join([f"{i + 1}. {show['name']}" for i, show in enumerate(watched_shows)])
        await ctx.respond("List of Watched Shows:\n" + shows_list)

# /unviewed-movies
@slash_command(
    name="unviewed-movies",
    description="Display list of unviewed movies",
)
async def unviewed_movies(ctx):
    collection = db['Movies']

    unwatched_movies = list(collection.find({"watched": False}))
    num_movies = collection.count_documents({"watched": False})
    if num_movies == 0:
        await ctx.respond("There are no movies unwatched.")
    else:
        
        movie_list = "\n".join([f"{i + 1}. {movie['name']}" for i, movie in enumerate(unwatched_movies)])
        await ctx.respond("List of Unwatched Movies:\n" + movie_list)

# /unviewed-shows
@slash_command(
    name="unviewed-shows",
    description="Display list of unviewed shows",
)
async def unviewed_shows(ctx):
    collection = db['Shows']

    unwatched_shows = list(collection.find({"watched": False}))
    num_shows = collection.count_documents({"watched": False})
    if num_shows == 0:
        await ctx.respond("There are no shows unwatched.")
    else:
        
        shows_list = "\n".join([f"{i + 1}. {show['name']}" for i, show in enumerate(unwatched_shows)])
        await ctx.respond("List of Unwatched Shows:\n" + shows_list)

# /remove-movie
@slash_command(
    name="remove-movie",
    description="Remove a movie from the list",
    options=[
        {
            "name": "movie",
            "description": "The name of the movie",
            "type": 3,
            "required": True,
        }
    ]
)
async def remove_movie(ctx, movie: str):
    collection = db['Movies']

    collection.delete_one({"name": movie})
    await ctx.respond(f"Removed '{movie}' from the movie list.")

# /remove-show
@slash_command(
    name="remove-show",
    description="Remove a show from the list",
    options=[
        {
            "name": "show",
            "description": "The name of the show",
            "type": 3,
            "required": True,
        }
    ]
)
async def remove_show(ctx, show: str):
    collection = db['Shows']

    collection.delete_one(show)
    await ctx.respond(f"Removed '{show}' from the show list.")

@billiam.event
async def on_message(message):
    if message.author == billiam.user:
        return
    await billiam.process_commands(message)


billiam.start()
