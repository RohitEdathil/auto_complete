from trie import Trie
from os.path import join
from tqdm import tqdm


def load(file):
    file = open(join("data", file), "r").readlines()

    trie = Trie()

    for line in tqdm(file, desc="Inserting words", total=len(file)):
        if len(line) < 4:
            continue

        trie.insert(line.strip())

    return trie
