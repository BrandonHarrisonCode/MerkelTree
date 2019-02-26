#!/usr/bin/python3

from os import walk
from os.path import isfile, join
from hashlib import md5
import sys

indent = 0


class Node:
    def add_child(self, child):
        assert isinstance(child, Node)
        is_leaf = False
        if child in self.children:
            return
        self.children.append(child)
        hashes = []
        for node in self.children:
            hashes.append(node.get_hash())
        prehash = ''.join(hashes)
        self.node_hash = md5(prehash.encode('utf-8')).hexdigest()
        # print('{}Generated new hash for {} with prehash {} from {} children and final hash: {}'.format(' ' * indent * 2, self.path, prehash, len(self.children), self.node_hash))


    def get_hash(self):
        return self.node_hash


    def generate_file_hash(self, path):
        # print('{}Generating hash for {}'.format(' ' * indent * 2, path))
        file_hash = md5()

        if isfile(path):
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    file_hash.update(chunk)
        else:
            file_hash.update(''.encode('utf-8'))
        return file_hash.hexdigest()


    def __str__(self):
        output = '' + self.get_hash() + ' (' + self.path + ')'
        count = 0
        for child in self.children:
            toadd = str(child)
            for line in toadd.split('\n'):
                if line[0] == '\\' or line[0] == '|':
                    output += '\n   ' + line
                else:
                    if count == len(self.children) - 1:
                        output += '\n\--' + line
                    else:
                        output += '\n|--' + line
            count += 1
        return output


    def __init__(self, path):
        global indent
        self.path = path
        self.children = []
        self.node_hash = self.generate_file_hash(path)
        self.is_leaf = True
        # print('{}Created {} with hash: {}'.format(' ' * indent * 2, path, self.node_hash))

        for rt, dirs, files in walk(path):
            # print("{}Directories: {}".format(' ' * indent * 2, dirs))
            # print("{}Files: {}".format(' ' * indent * 2, files))
            # print("{}Pre-all Children count: {}".format(' ' * indent * 2, len(self.children)))
            for dir in dirs:
                if dir == './':
                    continue
                # print("{}Adding child called {}".format(' ' * indent * 2, dir))
                indent += 1
                new_child = Node(join(path, dir))
                indent -= 1
                self.add_child(new_child)
            # print("{}Post-dir Children count: {}".format(' ' * indent * 2, len(self.children)))
            for file in files:
                # print("{}Adding file called {}".format(' ' * indent * 2, file))
                indent += 1
                new_child = Node(join(path, file))
                indent -= 1
                self.add_child(new_child)
            # print("{}Post-files Children count: {}".format(' ' * indent * 2, len(self.children)))

        # print("{}Exiting init".format(' ' * indent * 2))


if __name__ == '__main__':
    tree = None
    if len(sys.argv) < 2:
        tree = Node('./')
    else:
        tree = Node(sys.argv[1])
    print(tree)
