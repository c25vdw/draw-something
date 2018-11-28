"""
Assignment 1: Huffman Coding

name: Lucas Zeng
id #:   1539168
CMPUT 274 FALL, 2018

"""
import server.bitio
import server.huffman
import pickle
import sys


def read_tree(tree_stream):
    '''Read a description of a Huffman tree from the given compressed
    tree stream, and use the pickle module to construct the tree object.
    Then, return the root node of the tree itself.

    Args:
      tree_stream: The compressed stream o read the tree from.

    Returns:
      A Huffman tree root constructed according to the given description.
    '''
    tree = pickle.load(tree_stream)
    return tree
    
def decode_byte(tree, bitreader):
    """
    Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leaf is returned.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.
    """
    curr = tree.root
    try:
        while True:
            try:
                bit = bitreader.readbit()
            except EOFError: # end of file, manually break
                break

            if bit == 0:
                curr = curr.left
            elif bit == 1:
                curr = curr.right
            if hasattr(curr, 'value'): # is a leaf
                return curr.value
    except:
        print("you have wrong file modes, please use 'wb' and 'rb'")
        sys.exit(1)

def decompress(compressed, uncompressed):
    '''First, read a Huffman tree from the 'tree_stream' using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.
    '''
    tree = read_tree(compressed)

    # initialize bit handlers
    bitReader = bitio.BitReader(compressed)
    bitWriter = bitio.BitWriter(uncompressed)
    try:
        while True:
            try:
                bit = decode_byte(tree, bitReader)
            except EOFError: # until file ends
                break
            if bit == None: # check for invalid bit
                break
            bitWriter.writebits(bit, 8)
        bitWriter.flush()
    except: # check for file io errors, most possibly mode errors
        print("you have wrong file modes, please use 'wb' and 'rb'")
        compressed.close()
        sys.exit(1)

    # closing uncompressed will trigger an error in http server.
    uncompressed_bytes = uncompressed.getvalue()
    compressed.close()
    uncompressed.close()
    return uncompressed_bytes

def write_tree(tree, tree_stream):
    '''Write the specified Huffman tree to the given tree_stream
    using pickle.

    Args:
      tree: A Huffman tree.
      tree_stream: The binary file to write the tree to.
    '''
    pickle.dump(tree, tree_stream)

def compress(tree, uncompressed, compressed):
    '''First write the given tree to the stream 'tree_stream' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    '''
    try:
        write_tree(tree, compressed)
        encoding_table = huffman.make_encoding_table(tree.root)
        bitWriter = bitio.BitWriter(compressed)
        bitReader = bitio.BitReader(uncompressed)
        try:
            while True:
                char = bitReader.readbits(8)
                bits_to_write = encoding_table[char]
                for b in bits_to_write:
                    bitWriter.writebit(b)
        except EOFError:
            bitWriter.flush()
        
    except:
        print("you have wrong file modes, please use 'wb' and 'rb'")
        compressed.close()
        uncompressed.close()
        sys.exit(1)
    # always closes two files
    compressed.close()
    uncompressed.close()

