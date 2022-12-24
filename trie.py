class Trie:
    def __init__(self):
        self.root = {}
        self.end = -1

    def insert(self, word):
        node = self.root
        for char in word:
            node = node.setdefault(char, {})
        node[self.end] = self.end

    def _dfs(self, node, prefix):
        result = []
        for char in node:
            if char == self.end:
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
