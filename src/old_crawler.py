#!/usr/bin/python3


# pip install --user requests beautifulsoup4
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import sys
import time


print("\tTODO: delete each TODO message as you fulfill it")

print("\tTODO: You will need to change crawl's signature to fulfill this assignment.")
def crawl(url):
    """
    Given an absolute URL, print each hyperlink found within the document.

    Your task is to make this into a recursive function that follows hyperlinks
    until one of two base cases are reached:

    0) No new, unvisited links are found
    1) The maximum depth of recursion is reached
    """

    print("\tTODO: Check the current depth of recursion; return now if you have gone too deep")
    print("\tTODO: Print this URL with indentation indicating the current depth of recursion")
    print("\tTODO: Handle exceptions (including KeyboardInterrupt) gracefully and prevent this program from crashing")
    response = requests.get(url)
    if not response.ok:
        print(f"crawl({url}): {response.status_code} {response.reason}")
        return

    html = BeautifulSoup(response.text, 'html.parser')
    links = html.find_all('a')
    for a in links:
        link = a.get('href')
        if link:
            # Create an absolute address from a (possibly) relative URL
            absoluteURL = urljoin(url, link)

            # Only deal with resources accessible over HTTP or HTTPS
            if absoluteURL.startswith('http'):
                print(absoluteURL)

    print("\n\tTODO: Don't just print URLs found in this document, visit them!")
    print("\tTODO: Trim fragments ('#' to the end) from URLs")
    print("\tTODO: Use a `set` data structure to keep track of URLs you've already visited")
    print("\tTODO: Call crawl() on unvisited URLs")

    return


## An absolute URL is required to begin
if len(sys.argv) < 2:
    print("Error: no Absolute URL supplied")
    sys.exit(1)
else:
    url = sys.argv[1]

print("\tTODO: determine whether variable `url` is an absolute URL")

print("\tTODO: allow the user to optionally override the default recursion depth of 3")
maxDepth = 3

plural = 's' if maxDepth != 1 else ''
print(f"Crawling from {url} to a maximum depth of {maxDepth} link{plural}")


print("\tTODO: note what time the program began")

print("\tTODO: crawl() keeps track of its max depth with a parameter, not a global!")
print("TODO: wrap this call to crawl() in a try/except block to catch KeyboardInterrupt")
crawl(url)

print("\tTODO: after the program finishes for any reason, report how long it ran and the number of unique URLs visited")

print("\tTODO: are all of the TODOs deleted?")
