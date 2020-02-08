import argparse


def merge(level, count, minlevel=0):
    if level <= minlevel:
        return count
    return (
        merge(level - 1, (count // 2) * 5, minlevel) +
        merge(level - 1, 3 * (count % 2), minlevel)
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('level', type=int, help='Desired level')
    parser.add_argument('count', type=int, help='Desired number')
    parser.add_argument(
        'minlevel', type=int, default=0, nargs='?', help='Minimum level to use'
    )
    args = parser.parse_args()
    assert args.level >= 0
    assert args.level >= args.minlevel
    assert args.level < 20
    assert args.count >= 0
    assert args.minlevel >= 0
    assert args.minlevel < 20
    print(merge(args.level, args.count, args.minlevel))
