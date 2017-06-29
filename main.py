import sys


def main():
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("USAGE : python applehealthdata.py /path/to/datum.xml",file=sys.stderr)
        sys.exit(1)

    # data = HealthDataExtractor(sys.argv[1])

