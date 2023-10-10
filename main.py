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

    movie_document = {
        "name": movie,
        "watched": False
    }
    collection.insert_one(movie_document)
    await ctx.respond(f"Added '{movie}' to the movie list.")

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

    show_document = {
        "name": show,
        "watched": False
    }
    collection.insert_one(show_document)
    await ctx.respond(f"Added '{show}' to the show list.")

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
@billiam.event
async def on_message(message):
    if message.author == billiam.user:
        return
    await billiam.process_commands(message)


billiam.start()
