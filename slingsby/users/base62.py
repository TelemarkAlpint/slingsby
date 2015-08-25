import math
import string
import sys

ALPHABET = string.digits + string.ascii_letters
PY2 = sys.version_info[0] == 2

if PY2:
    def ord_byte(char):
        return ord(char)
else:
    def ord_byte(byte):
        return byte


def ceildiv(dividend, divisor):
    ''' integer ceiling division '''
    return (dividend + divisor - 1) // divisor


def calc_chunklen(alph_len):
    '''
    computes the ideal conversion ratio for the given alphabet.
    A ratio is considered ideal when the number of bits in one output
    encoding chunk that don't add up to one input encoding chunk is minimal.
    '''
    binlen, enclen = min([
                          (i, i*8 / math.log(alph_len, 2))
                          for i in range(1, 7)
                         ], key=lambda k: k[1] % 1)

    return binlen, int(enclen)


def encode(digest):
    chunklen = calc_chunklen(len(ALPHABET))
    nchunks = ceildiv(len(digest), chunklen[0])
    binstr = digest.ljust(nchunks * chunklen[0], b'\0')

    return ''.join(
            _encode_chunk(binstr, i) for i in range(0, nchunks)
        )

def _encode_chunk(data, index):
    '''
    gets a chunk from the input data, converts it to a number and
    encodes that number
    '''
    chunk = _get_chunk(data, index)
    return _encode_long(_chunk_to_long(chunk))


def _encode_long(val):
    '''
    encodes an integer of 8*chunklen[0] bits using the specified
    alphabet
    '''
    chunklen = calc_chunklen(len(ALPHABET))
    return ''.join([
            ALPHABET[(val//len(ALPHABET)**i) % len(ALPHABET)]
            for i in reversed(range(chunklen[1]))
        ])


def _chunk_to_long(chunk):
    '''
    parses a chunk of bytes to integer using big-endian representation
    '''
    chunklen = calc_chunklen(len(ALPHABET))
    return sum([
            256**(chunklen[0]-1-i) * ord_byte(chunk[i])
            for i in range(chunklen[0])
        ])


def _get_chunk(data, index):
    '''
    partition the data into chunks and retrieve the chunk at the given index
    '''
    chunklen = calc_chunklen(len(ALPHABET))
    return data[index*chunklen[0]:(index+1)*chunklen[0]]
