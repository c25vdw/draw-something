import sys
sys.path.append('./huffman')
import huffman
import sys
import util


def run_compressor (filename):
    with open(filename, 'rb') as uncompressed:
        freqs = huffman.make_freq_table(uncompressed)
        tree = huffman.make_tree(freqs)
        uncompressed.seek(0)
        with open(filename+'.huf', 'wb') as compressed:
                util.compress(tree, uncompressed, compressed)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <file1> <file2> ...".format(sys.argv[0]))
    else:
        for filename in sys.argv[1:]:
            print ("Compressing '{0}' to '{0}.huf'".format(filename))
            run_compressor(filename)
