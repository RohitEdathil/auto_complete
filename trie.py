class Trie:
    # Static property
    end = "#"

    def __init__(self):
        # Initialize the root node as an empty dictionary
        self.root = {}

    def insert(self, word):
        node = self.root
        for char in word:
            node = node.setdefault(char, {})
        node[Trie.end] = Trie.end

    def _dfs(self, node, prefix):
        result = []
        for char in node:
            if char == Trie.end:
                result.append(prefix)
            else:
                result += self._dfs(node[char], prefix + char)
        return result

    def startsWith(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node:
                return []
            node = node[char]

        return self._dfs(node, prefix)
