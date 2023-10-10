import pymongo
import interactions

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
            "name": "movie_name",
            "description": "The name of the movie",
            "type": 3,
            "required": True,
        }
    ]
)
async def add_movie(ctx, movie_name: str):
    collection = db['Movies']

    movie_document = {
        "name": movie_name,
        "watched": False
    }
    collection.insert_one(movie_document)
    await ctx.respond(f"Added '{movie_name}' to the movie list.")

@billiam.event
async def on_message(message):
    if message.author == billiam.user:
        return
    await billiam.process_commands(message)


billiam.start()
