# I mean you said you wanted some 3rd party libraries :D
import sys
from threading import Event, Thread, Lock
from queue import Queue, Empty
from typing import List, Set
from urllib.parse import urldefrag, urlparse, urljoin
from bs4 import BeautifulSoup
import requests
from requests import ConnectionError
from urllib.parse import urljoin

# Use for link comparison and sorting
from functools import total_ordering

from requests.models import InvalidURL


@total_ordering
class Link():
    """ Extension of a simple link, that also keeps track of peers, parent, and depth
    """

    def __init__(self, url: str, depth: int) -> None:
        """Creates a link with some extra attributes

        Args:
            url (str): a valid url
            depth (int): the depth of the current link in relation to the base
        """
        self.url: str = url
        self.depth: int = depth

        self.parent: Link = None
        self.children: List[Link] = []

    def set_parent(self, parent: 'Link') -> None:
        self.parent = parent

    def add_child(self, child: 'Link') -> None:
        self.children.append(child)

    def __str__(self) -> str:
        return self.url

    # Comparison for sorted output
    def __lt__(self, other: 'Link'):
        return self.url < other.url

    def __eq__(self, other: 'Link') -> bool:
        return self.url == other.url

    def __hash__(self) -> int:
        return hash(self.url)

    def handle_url(self, base_url: str) -> None:
        """
        Modifies the current Link's url by performing checks and stripping info:
        - removes fragments
        - converts to absolute link
        - removes all links but links containing http and https schemas

        Args:
            base_url (str): the base url, provided by the user

        """
        # Remove Fragments
        self.url, _ = urldefrag(self.url)

        # Parse url into parts
        dump = urlparse(self.url)

        # Check for absolute
        if not dump.scheme:
            self.url = urljoin(base_url, self.url)

        # Remove all other protocols
        elif dump.scheme != 'http' and dump.scheme != 'https':
            self.url = None

    def print_link(self) -> int:
        """Prints all of the links recursively, and returns the number of links found

        Returns:
            int: number of links found
        """
        print(('\t' * self.depth) + self.url)
        total = 1
        self.children.sort()
        for link in self.children:
            total += link.print_link()
        return total


class Crawler(Thread):

    def __init__(self, parent: Link, links: Queue, visited: set, url_lock: Lock, set_lock: Lock, max_depth: int, timeout: float):
        """Creates a web crawler thread for processing html

        Args:
            parent (Link): the base link provided by the user
            links (Queue): A queue to store all links to process
            visited (set): a set of all previously processed links
            url_lock (Lock): flag to prevent racing
            parent_lock (Lock): flag to prevent racing
            max_depth (int, optional): Maximum depth possible.
            timeout (int) : time before thread dies waiting
        """
        Thread.__init__(self)
        self.max_depth = max_depth
        self.base_url: Link = parent
        self.links: Queue[Link] = links
        self.visited: Set[str] = visited
        self.timeout = timeout

        self.url_lock: Lock = url_lock
        self.set_lock: Lock = set_lock
        self._stop_event: Event = Event()

    def run(self) -> None:
        """
        The code here looks messy, but its for a reason.  Whenever modifying data that is shared between threads we first need to prevent it's use in other threads, and then access it.
        """
        while not self._stop_event.is_set():
            # Print update
            print(
                f"Links found: {len(self.visited) } | Queue Estimate: {self.links.qsize()}", file=sys.stderr, end='\r')

            # get link lock, used to maintain thread safety
            self.url_lock.acquire()

            try:
                # Thread times out after .3 seconds
                link = self.links.get(True, .3)

            except Empty:
                # only exit if
                if self.links.all_tasks_done:
                    self.stop()
                    break
                continue

            finally:
                self.url_lock.release()

            # Check if link returned
            if link is None:
                continue

            # Check if depth is reached
            if self.max_depth is not None:
                if link.depth == self.max_depth:
                    continue

            try:

                # Get HTML Tags
                req = requests.get(link.url)
                soup = BeautifulSoup(req.content, "html.parser")

                # signifies to queue to continue
                self.links.task_done()

                # search for href
                for tag in soup.find_all('a'):
                    tempLink = Link(tag.get("href"), link.depth + 1)
                    tempLink.handle_url(self.base_url.url)

                    self.set_lock.acquire()
                    visit = tempLink.url not in self.visited
                    self.set_lock.release()

                    if visit and tempLink.url is not None:
                        # Bind Link
                        link.add_child(tempLink)
                        tempLink.set_parent(link)

                        self.links.put(tempLink)

                        self.set_lock.acquire()
                        self.visited.add(tempLink.url)
                        self.set_lock.release()

            except ConnectionError as e:
                print(f"Error: {link} | connection refused",
                      file=sys.stderr, flush=True)

            except InvalidURL:
                print(f"Error: {link} | invalid URL",
                      file=sys.stderr, flush=True)

            except Exception as e:
                print(f"Error: {link} | {type(e)}",
                      file=sys.stderr, flush=True)

    def stop(self):
        self._stop_event.set()


class CrawlerManager():
    """manages and controls threads from a single interface"""

    def __init__(self, url: str, threads: int, max_depth: int, timeout: float) -> None:
        """Creates a manager to manage each of the cralwer threads from a single interface.

        Args:
            url (str): the first absolute url to search
            threads (int): the number of threads (workers) to create
            max_depth (int): the maximum recursion before search stops
        """
        self.links = Queue(0)

        self.link_lock = Lock()
        self.set_lock = Lock()

        self.visited: Set[str] = set()
        self.base_url: Link = Link(url, 0)
        self.links.put(self.base_url)
        self.visited.add(self.base_url.url)

        self.threads: List[Thread] = []
        self.threadcount = threads
        self.depth = max_depth
        self.timeout = timeout

    def run(self):
        """Creates and runs each of the threads
        """
        for _ in range(self.threadcount):
            crawler = Crawler(self.base_url, self.links,
                              self.visited, self.link_lock, self.set_lock, self.depth, self.timeout)
            crawler.start()
            self.threads.append(crawler)

        # Waits for each thread to finish
        for idx, crawler in enumerate(self.threads):
            crawler.join()
            print(f"Closing crawler {idx + 1}",
                  file=sys.stderr, flush=True, end='\r')

    def stop(self) -> None:
        """
        Stops all currently running threads when requested
        """
        for thread in self.threads:
            thread.stop()

    def print_links(self) -> int:
        return self.base_url.print_link()


def validate(url: str) -> bool:
    if urlparse(url).scheme:
        return True
    return False
