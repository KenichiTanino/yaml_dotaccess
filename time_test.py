import timeit

from box_sample import main as box_main
from simplenamespace_sample import main as simplenamespace_sample_main


def main():
    
    print(f"box={timeit.timeit(box_main, number=100)}")
    print(f"simplenamespace={timeit.timeit(simplenamespace_sample_main, number=100)}")

if __name__ == "__main__":
    main()