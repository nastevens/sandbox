import sys

def merge(level, count, minlevel=0):
    if level <= minlevel:
        return count
    return (
        merge(level - 1, (count // 2) * 5, minlevel) +
        merge(level - 1, 3 * (count % 2), minlevel)
    )


if __name__ == '__main__':
    print(merge(*(int(arg) for arg in sys.argv[1:])))
