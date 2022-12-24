from load import load
from fastapi import FastAPI
from fastapi.responses import FileResponse

# Load the trie
trie = load("words.txt")

# Create the FastAPI app
app = FastAPI()


@app.get("/suggest/{word}")
# Maps the `/suggest/{word}` path to the `suggest` function
async def suggest(word: str):

    # Queries with less than 3 characters are inefficient, so we ignore them
    if len(word) < 3:
        return []

    # Return the suggestions
    return trie.startsWith(word)


@app.get("/")
# `/` will return index.html
async def index():
    return FileResponse("index.html")
