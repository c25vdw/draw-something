import sys
sys.path.append('./huffman')

import util



def run_decompressor (compressed, decompress_to):
    # first is a string, second param is opened file stream object.
    compressed_f = open(compressed, 'rb')
    decompress_to_f = open(decompress_to, 'wb')
    util.decompress(compressed_f, decompress_to_f)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <huffman filename> <plain filename> ...".format(sys.argv[0]))
    else:
        run_decompressor(sys.argv[1], sys.argv[2])