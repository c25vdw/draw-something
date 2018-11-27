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
        print("Usage: {} <file1> <file2> ...".format(sys.argv[0]))
    else:
        for filename in sys.argv[1:]:
            run_decompressor(filename, "hello")