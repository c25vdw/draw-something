import io
# huffman package files
import server.huffman.util as util# ./huffman/util
import server.huffman.huffman as huffman
class HuffmanHandler:
    def __init__(self, entries_filename='entries'):
        self.compressed_filename = entries_filename + '.huf'

        self.entries_data_bytes = ""
        self.entries_data = ""
        self.entries = {}

    def get_entries(self):
        # "1 human;1 boat;2 dog;2 cat;3 reading;3 workout;"
        entries_str = self.decompress()
        pairs = list(filter(lambda x: len(x) > 0, entries_str.split(";")))
        print(pairs)
        # load the string entries into a dictionary.
        for pair in pairs:
            level, string = pair.split(" ")
            if level in self.entries:
                self.entries[level].append(string)
            else:
                self.entries[level] = [string]

        # {'1': ['human', 'boat'], '2': ['dog', 'cat'], '3': ['reading', 'workout']}
        return self.entries
        
    def decompress(self):
        self.compressed_stream = open(self.compressed_filename, 'rb')
        self.decompressed_stream = io.BytesIO()

        self.entries_data_bytes = util.decompress(self.compressed_stream, self.decompressed_stream)
        self.entries_data = self.entries_data_bytes.decode('utf-8')
        return self.entries_data

    def save_and_compress_to_file(self, entries_data):
        self.compressed_stream = open(self.compressed_filename, 'wb')
        
        data_stream = io.BytesIO(bytes(entries_data.encode('utf-8')))
        freqs = huffman.make_freq_table(data_stream)
        tree = huffman.make_tree(freqs)
        data_stream.seek(0)
        util.compress(tree, data_stream, self.compressed_stream)

if __name__ == "__main__":
    hh = HuffmanHandler()
    hh.get_entries()
    # data_stream = io.BytesIO(bytes(data.encode('utf-8')))
    # freqs = huffman.make_freq_table(data_stream)
    # tree = huffman.make_tree(freqs)
    # print(freqs, tree)
    # data = "1 human;1 boat;2 dog;2 cat;3 reading;3 workout;"
    # hh.save_and_compress_to_file(data)