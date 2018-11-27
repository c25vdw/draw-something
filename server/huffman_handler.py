import io
import sys

sys.path.append('./huffman')
import util
import huffman

class HuffmanHandler:
    def __init__(self, entries_filename='entries'):
        self.compressed_filename = entries_filename + '.huf'

        self.entries_data_bytes = ""
        self.entries_data = ""

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
    data = hh.decompress()
    print(data)
    # data_stream = io.BytesIO(bytes(data.encode('utf-8')))
    # freqs = huffman.make_freq_table(data_stream)
    # tree = huffman.make_tree(freqs)
    # print(freqs, tree)
    data += "123123123"
    hh.save_and_compress_to_file(data)