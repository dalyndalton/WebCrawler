from crawler import CrawlerManager, validate
import sys
from time import perf_counter
import argparse


def main():
    # Creates argument parser and arguments
    parser = argparse.ArgumentParser(description="A multithreaded web scraper")
    parser.add_argument('Link', metavar='link', type=str,
                        help="an absolute link to the starter website")
    parser.add_argument('-d', metavar='--depth', type=int,
                        help="The maximum depth the crawer should search", default=3)
    parser.add_argument('-t', metavar='--thread_count',
                        help="Number of threads to create, for smaller depths less threads can be beneficial", type=int, default=10)

    args = parser.parse_args()
    print(args)
    url = args.Link
    max_depth = args.d
    threads = args.t

    # Invalid Link
    if not validate(url):
        print("Invalid url, please provide url with included schema 'http://' or 'https://'", file=sys.stderr)
        sys.exit(1)

    # Build data for threads
    print(
        f"Creating thread manager: \n threads - {threads} \n depth - {max_depth}", file=sys.stderr)

    manager = CrawlerManager(url, threads, max_depth)
    start = perf_counter()

    # Run program
    try:
        manager.run()
    except KeyboardInterrupt:
        print("program exited manually, exiting now . . .", flush=True)

    finally:
        sys.stdout.flush()
        print("\n", file=sys.stderr)
        total = manager.print_links()
        print(
            f"Finished in {perf_counter() - start:.03} | Parsed : {len(manager.visited)} | Queue: {manager.links.qsize()}\nTotal: {total}")


if __name__ == '__main__':
    main()
