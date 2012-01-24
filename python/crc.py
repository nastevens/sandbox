from binascii import a2b_hex, b2a_hex, crc32
import textwrap

def calc_ilr_crc(string):

    # Calculate CRC and mask to 4 bytes
    crc = crc32(string) & 0xFFFFFFFF

    # Split CRC into 4-element list
    crclist = list(a2b_hex('{0:08x}'.format(crc)))

    # Reverse byte order
    crclist.reverse()

    # Combine list back into string
    crcstr = b2a_hex(''.join(crclist))

    return crcstr

def brute_force():
    DESIRED = ['9EA03112', '86FA73B7','9C1CDE9A','C6C784A6']
    for i in xrange(2**30):
        hex_string = a2b_hex('{0:08x}'.format(i))
        crc = calc_ilr_crc(hex_string)
        if crc.upper() in DESIRED:
            print('Matching CRC {0} for input {1:04x}'.format(crc, i))

#if __name__ == '__main__':
#    brute_force()

if __name__ == '__main__':
    import sys
    if sys.argv[1] == '-x':
        print(calc_ilr_crc(a2b_hex(sys.argv[2])))
    else:
        try:
            print(calc_ilr_crc(sys.argv[1]))
        except:
            usage = textwrap.dedent('''
                    Prints the CRC of the provided string using the same method as the ILR.

                    Usage:
                    {0} <string>
                    {0} -x <hex string>''')
            print(usage.format(sys.argv[0]))
