from crawler import CrawlerManager, validate
import sys
from time import perf_counter


def main():
    # TODO: Add a proper flag parser
    # Missing Link
    if len(sys.argv) < 2:
        print("Missing absolute URL to scrape", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]

    # Invalid Link
    if not validate(url):
        print("Invalid url, please provide url with included schema 'http://' or 'https://'", file=sys.stderr)
        sys.exit(1)

    # Optional Max Depth
    max_depth = int(sys.argv[2]) if len(sys.argv) >= 3 else 3

    # Optional Thread Count
    threads = int(sys.argv[3]) if len(sys.argv) >= 4 else 20

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
