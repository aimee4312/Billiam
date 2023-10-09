import discord
import requests
import json
import random
import pymongo

from config import TOKEN
mongo_client = pymongo.MongoClient("mongodb+srv://billiam:1fVVhMFspTHjx64E@cluster0.d15oseu.mongodb.net/")

intents = discord.Intents.all() 
client = discord.Client(command_prefix='!', intents=intents)

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

    if msg.startswith('!inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    
    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))
    
    if msg.startswith('!add-movie'):
        movie_name = msg.split('!add-movie', 1)[1].strip()

        db = mongo_client['Unwatched']
        collection = db['Movie']

        movie_document = {
            "name": movie_name,
            "watched": False
        }

        collection.insert_one(movie_document)

        await message.channel.send(f"Added '{movie_name}' to the movie list.")

    if msg.startswith('!add-show'):
        show_name = msg.split('!add-show', 1)[1].strip()

        db = mongo_client['Unwatched']
        collection = db['Show']

        show_document = {
            "name": show_name,
            "watched": False
        }

        collection.insert_one(show_document)

        await message.channel.send(f"Added '{show_name}' to the show list.")
    
client.run(TOKEN)
