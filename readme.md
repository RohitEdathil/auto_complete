# Autocomplete using Trie

We have seen word-suggestions given to us by a lot of software, ever wondered how its done? There is a data structure called Trie which is used to store words and then used to suggest words very efficiently. We are going to see how such a system can be made.

Python will be used to implement the Trie data structure and then we will use it to make a word-suggestion API using FastAPI.

## What is a Trie?

A Trie is a tree-like data structure, with each node having a character and a list of children. If we were to trace from the root-node to a leaf-node, we would get a complete word.

Here is a Trie for the words

```
art apple article boat boar botswana approve ask add
```

![Trie](https://github.com/RohitEdathil/auto_complete/blob/master/img/1.jpg)

## World list

We need a list of words to build our Trie. I used [https://github.com/RohitEdathil/auto_complete/blob/master/data/words.txt](https://github.com/RohitEdathil/auto_complete/blob/master/data/words.txt). Also we will filter out words with length less than 4 later.

## Dependencies

We have to install the following dependencies to run the code: `tqdm`(Progress bar), `fastapi`(For the API), `uvicorn` (To run the server)
Install them using pip:

```bash
pip install tqdm fastapi uvicorn
```

## Code Structure

```
auto_complete
    ├── data
    │   └── words.txt (The word list)
    ├─ main.py (The API server)
    ├─ load.py (Loads the word list into a Trie)
    ├─ index.html (A simple frontend)
    └─ trie.py (The Trie data structure)
```

## Implementint Trie

### Initialization

This section will be done in `trie.py`.
First of all, we need a special character to denote the end of a word. I used `#` for this. We also need a root node, which will be an empty dictionary to start with.

```python
class Trie:
    #
    end = "#"

    def __init__(self):
        self.root = {}

```

### Inserting a word

Lets take a set of words to begin with

```
add art apple adict approve
```

The tree should look like this
![Trie](https://github.com/RohitEdathil/auto_complete/blob/master/img/2.jpg)

When we think of this as a nested python dictionary it should be:

```json
{
  "a": {
    "d": {
      "d": {
        "#": "#"
      },
      "i": {
        "c": {
          "t": {
            "#": "#"
          }
        }
      }
    },
    "r": {
      "t": {
        "#": "#"
      }
    },
    "p": {
      "p": {
        "l": {
          "e": {
            "#": "#"
          }
        },
        "r": {
          "o": {
            "v": {
              "e": {
                "#": "#"
              }
            }
          }
        }
      }
    }
  }
}
```

The algorithm for inserting a word is:

- Set node as root
- For each character in the word
  - If the character is not in the node, add it, set value as blank dictionary
  - Set node as the child of the character
- Set the value of the node as `#`

```python
def insert(self, word):
    node = self.root
    for char in word:
        # setdefault sets the value of the key to a blank dictionary if it does not exist and returns the value
        node = node.setdefault(char, {})

    # Marks the end of the word
    node[Trie.end] = Trie.end
```

### Search by prefix

When we supply a prefix, we want to get all the words that start with that prefix. For example, if we supply `ap` as the prefix, we should get `apple` and `approve`.

The algorithm for this is:

- Set node as root
- For each character in the prefix
  - If the character is not in the node, return an empty list
  - Set node as the child of the character
- Return all the words in the subtree of the node

```python
def startsWith(self, prefix):
    node = self.root
    for char in prefix:
        if char not in node:
            return []
        node = node[char]
    return self._dfs(node, prefix)
```

Here `_dfs` is a recursive function that traverses the subtree of the node and returns all the words in it.

Algorithm for `_dfs`:

- Set result as empty list
- For each key in the node
  - If the key is `#`, append the word to the result
  - Else, recursively call `_dfs` on the child of the key and append the result to the result
- Return the result

```python
def _dfs(self, node, prefix):
    result = []
    for char in node:
        if char == Trie.end:
            result.append(prefix)
        else:
            result += self._dfs(node[char], prefix + char)
    return result
```

## Loading the word list

This section will be done in `load.py`.

This file will have a simple function that loads the word list into a Trie and returns it.

```python

# Imports
from trie import Trie
from os.path import join
from tqdm import tqdm


def load(file):
    # Opens the file and reads all the lines
    file = open(join("data", file), "r").readlines()

    # Creates a new Trie
    trie = Trie()

    # Loops through all the lines (tqdm is just a progress bar)
    for line in tqdm(file, desc="Inserting words", total=len(file)):

        # Filters out words with length less than 4
        if len(line) < 4:
            continue

        # Inserts the word into the Trie
        trie.insert(line.strip())

    # Returns the Trie
    return trie

```

## API

The HTTP API will just have one endpoint, `/suggest`, which will take a path parameter `prefix` and return a JSON response with the list of words that start with the prefix.

Example request (Say we are running the server on `localhost:8000`):

```
http://localhost:8000/suggest/ap
```

Response:

```json
["apple", "approve"]
```

The code with explanations as comments:

```python
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


```

## Running the server

To run the server, run the following command:

```bash
uvicorn main:app --reload
```

## Testing

Open `http://localhost:8000/suggest/ap` in your browser. You should see the suggestions for `ap`.

A simple frontend could help us see the suggestions as we type.

Here is the code for the frontend (in `index.html`)

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Autocomplete</title>
  </head>
  <body>
    <input type="text" id="prefix" oninput="suggest()" />
    <p id="words"></p>
  </body>

  <style>
    html {
      background-color: rgb(50, 50, 50);
      margin: 0px;
      font-family: monospace;
    }

    body {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0px;
    }

    input {
      width: 300px;
      height: 30px;
      font-size: 20px;
      padding: 5px;
      border: 1px solid #ccc;
      border-radius: 5px;
    }

    #words {
      margin-top: 20px;
      font-size: 20px;
      height: 500px;
      background-color: rgb(39, 39, 39);
      color: white;
      width: 300px;
      padding: 12px;
      border-radius: 20px;
      overflow: auto;
    }
  </style>

  <script>
    function suggest() {
      const req = new XMLHttpRequest();
      const q = document.getElementById("prefix").value;
      req.open("GET", `http://localhost:8000/suggest/${q}`, true);

      req.onload = function () {
        const data = JSON.parse(this.response);
        const words = document.getElementById("words");
        words.innerHTML = "";
        data.forEach((word) => {
          const p = document.createElement("p");
          p.innerHTML = word;
          words.appendChild(p);
        });
      };

      req.send();
    }
  </script>
</html>
```

At this point you can run the server and open `http://localhost:8000` in your browser. You should see the frontend.

## Links

- GitHub repo: [https://github.com/RohitEdathil/auto_complete](https://github.com/RohitEdathil/auto_complete)

- Live demo: [https://auto-complete.rohitedathil.repl.co/](https://auto-complete.rohitedathil.repl.co/)
