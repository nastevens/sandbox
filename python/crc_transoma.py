import binascii
from itertools import chain, combinations, product

def crc_round(crc, d):
    crc_next = [False]*32
    crc_next[0] = crc[30] ^ d[1] ^ crc[24] ^ d[7]
    crc_next[1] = d[6] ^ d[7] ^ d[0] ^ crc[30] ^ crc[31] ^ d[1] ^ crc[24] ^ crc[25]
    crc_next[2] = crc[26] ^ d[5] ^ d[6] ^ d[7] ^ crc[30] ^ d[0] ^ d[1] ^ crc[31] ^ crc[24] ^ crc[25]
    crc_next[3] = d[4] ^ crc[26] ^ d[5] ^ crc[27] ^ d[6] ^ d[0] ^ crc[31] ^ crc[25]
    crc_next[4] = d[4] ^ crc[26] ^ d[5] ^ crc[27] ^ crc[28] ^ d[7] ^ crc[30] ^ d[1] ^ crc[24] ^ d[3]
    crc_next[5] = d[4] ^ crc[27] ^ d[6] ^ crc[28] ^ d[7] ^ crc[29] ^ crc[30] ^ d[0] ^ d[1] ^ crc[31] ^ d[2] ^ crc[24] ^ d[3] ^ crc[25]
    crc_next[6] = crc[26] ^ d[5] ^ d[6] ^ crc[28] ^ crc[29] ^ d[0] ^ crc[30] ^ crc[31] ^ d[1] ^ d[2] ^ d[3] ^ crc[25]
    crc_next[7] = d[4] ^ crc[26] ^ d[5] ^ crc[27] ^ d[7] ^ crc[29] ^ d[0] ^ crc[31] ^ d[2] ^ crc[24]
    crc_next[8] = d[4] ^ crc[27] ^ d[6] ^ crc[28] ^ d[7] ^ crc[24] ^ crc[0] ^ d[3] ^ crc[25]
    crc_next[9] = crc[26] ^ d[5] ^ d[6] ^ crc[28] ^ crc[29] ^ d[2] ^ d[3] ^ crc[25] ^ crc[1]
    crc_next[10] = d[4] ^ crc[26] ^ crc[2] ^ d[5] ^ crc[27] ^ d[7] ^ crc[29] ^ d[2] ^ crc[24]
    crc_next[11] = d[4] ^ crc[27] ^ d[6] ^ crc[3] ^ crc[28] ^ d[7] ^ crc[24] ^ d[3] ^ crc[25]
    crc_next[12] = crc[26] ^ d[5] ^ d[6] ^ crc[28] ^ d[7] ^ crc[4] ^ crc[29] ^ crc[30] ^ d[1] ^ d[2] ^ crc[24] ^ d[3] ^ crc[25]
    crc_next[13] = d[4] ^ crc[26] ^ d[5] ^ crc[27] ^ d[6] ^ crc[29] ^ d[0] ^ crc[30] ^ crc[5] ^ crc[31] ^ d[1] ^ d[2] ^ crc[25]
    crc_next[14] = d[4] ^ crc[26] ^ d[5] ^ crc[27] ^ crc[28] ^ crc[30] ^ d[0] ^ d[1] ^ crc[31] ^ crc[6] ^ d[3]
    crc_next[15] = d[4] ^ crc[27] ^ crc[28] ^ crc[29] ^ d[0] ^ crc[31] ^ d[2] ^ crc[7] ^ d[3]
    crc_next[16] = crc[28] ^ d[7] ^ crc[29] ^ d[2] ^ crc[24] ^ d[3] ^ crc[8]
    crc_next[17] = crc[9] ^ d[6] ^ crc[29] ^ crc[30] ^ d[1] ^ d[2] ^ crc[25]
    crc_next[18] = crc[26] ^ d[5] ^ crc[10] ^ crc[30] ^ d[0] ^ d[1] ^ crc[31]
    crc_next[19] = d[4] ^ crc[27] ^ crc[11] ^ d[0] ^ crc[31]
    crc_next[20] = crc[28] ^ crc[12] ^ d[3]
    crc_next[21] = crc[29] ^ crc[13] ^ d[2]
    crc_next[22] = d[7] ^ crc[14] ^ crc[24]
    crc_next[23] = d[6] ^ d[7] ^ crc[30] ^ d[1] ^ crc[15] ^ crc[24] ^ crc[25]
    crc_next[24] = crc[26] ^ d[5] ^ d[6] ^ d[0] ^ crc[31] ^ crc[16] ^ crc[25]
    crc_next[25] = d[4] ^ crc[17] ^ crc[26] ^ d[5] ^ crc[27]
    crc_next[26] = d[4] ^ crc[18] ^ crc[27] ^ crc[28] ^ d[7] ^ crc[30] ^ d[1] ^ crc[24] ^ d[3]
    crc_next[27] = d[6] ^ crc[19] ^ crc[28] ^ crc[29] ^ d[0] ^ crc[31] ^ d[2] ^ d[3] ^ crc[25]
    crc_next[28] = crc[26] ^ d[5] ^ crc[20] ^ crc[29] ^ crc[30] ^ d[1] ^ d[2]
    crc_next[29] = d[4] ^ crc[27] ^ crc[21] ^ crc[30] ^ d[0] ^ d[1] ^ crc[31]
    crc_next[30] = crc[28] ^ d[0] ^ crc[22] ^ crc[31] ^ d[3]
    crc_next[31] = crc[29] ^ crc[23] ^ d[2]
    return crc_next

def do_crc(data):
    crc = [True]*32
    for byte in data:
        string = '{:08b}'.format(int(byte))
        asbool = [True if bit == '1' else False for bit in string]
        crc = crc_round(crc, asbool)
    result = bytearray()
    for x in range(0,32,8):
        binary = ''.join('1' if boolean else '0' for boolean in crc[x:x+8])
        asint = int(binary, base=2)
        result.append(asint)
    return result

def default_pre(data_byte):
    return data_byte

def default_post(crc_byte):
    return crc_byte

def run_test_case(data, pre=[], post=[]):
    preprocessed = data[:]
    for f in list(pre):
        preprocessed = bytearray(map(f, preprocessed))
    crc = do_crc(preprocessed)
    postprocessed = crc[:]
    for f in list(post):
        postprocessed = bytearray(map(f, postprocessed))
    return postprocessed

def bitwise_invert(byte):
    return (byte ^ 0xFF) & 0xFF

def reverse_bits(byte):
    return int('{:08b}'.format(byte)[::-1], base=2) & 0xFF

def powerset(iterable):
    xs = list(iterable)
    return chain.from_iterable(combinations(xs, n) for n in range(len(xs)+1))

if __name__ == '__main__':
    #originaldata = bytearray([0x40, 0x10])
    #WANT = [bytearray('\x86\xfa\x73\xb7'), bytearray('\x9e\xa0\x31\x12')]
    originaldata = bytearray('0123456789')
    WANT = [bytearray('\x9c\x1c\xde\x9a'), bytearray('\xc6\xc7\x84\xa6')]
    print('Test data: 0x{}'.format(binascii.b2a_hex(originaldata)))

    tests = list(powerset([bitwise_invert, reverse_bits]))

    for tests in product(tests, tests):
        before, after = tests
        testdata = originaldata[:]
        result = run_test_case(testdata, pre=before, post=after)
        reverse = result[::-1]
        print(binascii.b2a_hex(result))
        print(binascii.b2a_hex(reverse))

        if result in WANT or reverse in WANT:
            print('found')
            print('{} {}'.format(before, after))
