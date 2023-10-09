import discord
import requests
import json
import random
import pymongo

from config import TOKEN
from discord.ext import commands

mongo_client = pymongo.MongoClient("mongodb+srv://billiam:1fVVhMFspTHjx64E@cluster0.d15oseu.mongodb.net/")

intents = discord.Intents.all() 
client = discord.Client(command_prefix='!', intents=intents)
db = mongo_client['Watchlist']

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person / bot!"
]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content

    # Random inspo
    if msg.startswith('!inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    
    # Random encouragement
    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))
    
    # Add movie
    if msg.startswith('!add-movie'):
        movie_name = msg.split('!add-movie', 1)[1].strip()
        collection = db['Movie']

        movie_document = {
            "name": movie_name,
            "watched": False
        }

        collection.insert_one(movie_document)

        await message.channel.send(f"Added '{movie_name}' to the movie list.")

    # Add show
    if msg.startswith('!add-show'):
        show_name = msg.split('!add-show', 1)[1].strip()
        collection = db['Show']

        show_document = {
            "name": show_name,
            "watched": False
        }

        collection.insert_one(show_document)

        await message.channel.send(f"Added '{show_name}' to the show list.")
    
     # See movie list
    if msg.startswith('!list-movies'):
        collection = db['Movie']
        movies = collection.find({"watched": False})

        num_movies = collection.count_documents({"watched": False})
        if num_movies == 0:
            await message.channel.send("There are no unwatched movies in the list.")
        else:
            # Create a numbered list of shows
            movie_list = "\n".join([f"{i + 1}. {movie['name']}" for i, movie in enumerate(movies)])

            await message.channel.send("List of unwatched movies:\n" + movie_list)

    # See show list
    if msg.startswith('!list-shows'):
        collection = db['Show']
        shows = collection.find({"watched": False})

        num_shows = collection.count_documents({"watched": False})
        if num_shows == 0:
            await message.channel.send("There are no unwatched shows in the list.")
        else:
            # Create a numbered list of shows
            show_list = "\n".join([f"{i + 1}. {show['name']}" for i, show in enumerate(shows)])

            await message.channel.send("List of Unwatched Shows:\n" + show_list)
    
    # Get a random movie
    if msg.startswith('!get-movie'):
        collection = db['Movie']

        unwatched_movies = list(collection.find({"watched": False}))
        if not unwatched_movies:
            await message.channel.send("There are no unwatched movies in the list.")
        else:
            random_movie = random.choice(unwatched_movies)
            collection.update_one({"_id": random_movie["_id"]}, {"$set": {"watched": True}})
            await message.channel.send(f"Random Movie: {random_movie['name']}")


client.run(TOKEN)
