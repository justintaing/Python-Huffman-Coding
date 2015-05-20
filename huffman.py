__author__ = 'justintaing'

import queue
import re


class Node(object):
    def __init__(self, data, frequency):
        self.data = data
        self.frequency = frequency
        self.path = None
        self.left = None
        self.right = None

    def __del__(self):
        self.data = None
        self.frequency = None
        self.left = None
        self.right = None

    def __gt__(self, other):
        return self.frequency > other.frequency

    def __lt__(self, other):
        return self.frequency < other.frequency

    def __repr__(self):
        return "(%s %.5f)" % (self.data, self.frequency)


class HuffmanCode(object):
    def __init__(self):
        self._root = None
        self._coding = {}

    def is_empty(self):
        return self._root is None

    def delete(self):
        self._root = None
        self._coding = {}

    def run_huffman_algorithm(self, file):
        node_queue = queue.PriorityQueue()

        try:
            if not self.is_empty():
                self.delete()

            f = open(file, 'r')

            for line in f:
                # Ignore comments in encoding file
                if line[0] in ['#', '\n']:
                    continue
                letter = line[0]
                frequency = float(re.search(r'\d+', line).group())
                node_queue.put(Node(letter, float(frequency)))

            f.close()

            while node_queue.qsize() > 1:
                left_node, right_node = node_queue.get(), node_queue.get()
                left_node.path = 0
                right_node.path = 1

                root_node = Node(None, left_node.frequency+right_node.frequency)
                root_node.left = left_node
                root_node.right = right_node

                node_queue.put(root_node)

            self._root = node_queue.get()
            self._build_coding()
        except FileNotFoundError as v:
            print(v)
        except IndexError or ValueError as v:
            print(v, ": Invalid input format in '", file, '\'', sep='')
            print("Make sure values are in the format:")
            print("KEY FLOAT")

    def _build_code(self, node, path):
        if node.data is not None:
            self._coding[node.data] = path

    def _dfs(self, node, path=""):
        if node is None:
            return
        path += str(node.path) if node.path is not None else ""
        self._dfs(node.left, path)
        self._dfs(node.right, path)
        self._build_code(node, path)

    def _build_coding(self):
        self._dfs(self._root)

    def get_coding(self):
        return self._coding

    def encode(self, string):
        if self.is_empty():
            print("No Huffman coding found. Generate Huffman code first.")
            return
        encoded_string = [self._coding[char] for char in string]

        return "".join(encoded_string)

    def decode(self, path):
        traversal_node = self._root
        decoded_string = ""
        complete = False

        if self.is_empty():
            print("No Huffman coding found. Generate Huffman code first.")
            return 
        for i in path:
            if i == '0':
                traversal_node = traversal_node.left
            else:
                traversal_node = traversal_node.right
            if traversal_node.data in self._coding:
                decoded_string += traversal_node.data
                traversal_node = self._root
                complete = True
            else:
                complete = False
        # We've decoded a complete phrase if we've looped back to the root
        # by the end of the given path; the phrase is incomplete if we haven't
        if not complete:
            print("Incomplete or malformed code phrase")

        return decoded_string