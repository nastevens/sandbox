if __name__ == '__main__':
    with open('output.csv', 'w') as f:
        f.write('Decimal,Hex\n')
        for i in range(130072, 262144+1):
            f.write('{},{:X}\n'.format(i, i))
