#!/usr/bin/python3

from crawler import CrawlerManager, validate
import sys
from time import perf_counter
import argparse


def main():
    # Creates argument parser and arguments
    parser = argparse.ArgumentParser(
        description="A multithreaded web scraper, exit early using CTRL + C")
    parser.add_argument('Link', metavar='link', type=str,
                        help="an absolute link to the starter website")
    parser.add_argument('-d', metavar='--depth', type=int,
                        help="The maximum depth the crawer should search, provide a negative number to search infinitely", default=3)
    parser.add_argument('-t', metavar='--thread_count',
                        help="Number of threads to create, for smaller depths less threads can be beneficial", type=int, default=5)
    parser.add_argument('-k', metavar='--timeout',
                        help="time before a thread dies, higher numbers will prevent threads from closing prematurely, but also cause the program to run longer.", default=0.3, type=float)

    args = parser.parse_args()
    url = args.Link
    max_depth = args.d
    threads = args.t
    timeout = args.k

    if max_depth == 1:
        threads = 1

    # Invalid Link
    if not validate(url):
        print("Invalid url, please provide url with included schema 'http://' or 'https://'", file=sys.stderr)
        sys.exit(1)

    # Build data for threads
    print(
        f"Running Crawler: \n threads - {threads} \n depth - {max_depth}\n timeout - {timeout}", file=sys.stderr)

    manager = CrawlerManager(url, threads, max_depth, timeout)
    start = perf_counter()

    # Run program
    try:
        manager.run()
    except KeyboardInterrupt:
        print("\nprogram exited manually, exiting now . . .",
              flush=True, file=sys.stderr)
        manager.stop()

    finally:
        time = perf_counter() - start
        sys.stdout.flush()
        print("", file=sys.stderr)
        total = manager.print_links()
        print(
            f"Finished in {time:.3} | Parsed : {len(manager.visited)} | Remaining: {manager.links.qsize()}\nTotal: {total}", file=sys.stderr)


if __name__ == '__main__':
    main()
