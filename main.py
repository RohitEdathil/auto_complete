
from trie import Trie
from os.path import join
from tqdm import tqdm
from time import time_ns

file = open(join("data", "words.txt"), "r").readlines()

trie = Trie()

for line in tqdm(file, desc="Inserting words", total=len(file)):

    if len(line) < 4:
        continue

    trie.insert(line.strip())

while True:
    prefix = input("Enter a prefix: ")
    t = time_ns()
    result = trie.startsWith(prefix)
    t2 = (time_ns() - t) / 10**6
    print(f"Found {len(result)} words in {t2} ms")
