# CS 1440 Assignment 5 Instructions


## Description

Rely on 3rd-party libraries to quickly produce a functioning web crawler.  Use
Exception Handling to deliver a safe and robust solution to our client.
Deliver a well-tested and documented programming product by the end of this
sprint.


## Previous Semester Assignment Statistics

Statistic                        | Value
--------------------------------:|:---------------
Average Hours Spent              | 5.81
Average Score % (Grade)          | 86.96% (B)
% students thought this was Easy | 57%
... Medium                       | 35%
... Hard                         |  5%
... Too Hard/Did not complete    |  3%


## Objectives

*   Use recursion to solve a real-world problem
    *   Identify base cases
    *   Avoid infinite recursion
*   Leverage software libraries instead of re-inventing wheels
    -   urllib
    -   Requests
    -   BeautifulSoup
*   Understand how URLs are constructed and used
*   Create robust software by handling exceptions instead of crashing


## Preparation

0.  Clone the starter code repository.
1.  Carefully read these instructions and other documentation provided.
2.  Install the required libraries (installation instructions are given below).  
    *   Ensure that all required libraries are correctly installed by running
        each of the programs found under the `demo/` directory
    *   The `crawl.py` starter program  will successfully run when all required
        libraries are installed.  It won't do anything useful, but it won't
        crash.
3.  Study the `crawl.py` starter program.
    *   Identify the base case(s) of this problem's recursion.
    *   Draft your Software Development Plan *before* you begin writing any
        code.  For this assignment it is especially important for you to really
        understand where you are going before you start writing code.


## Submission Instructions

*   This assignment is *not* eligible for the grading gift.  This due date cannot be moved.
*   Review the Course Rules document to avoid general penalties which apply to all assignments.
    *   **10 point penalty** if your repository is mis-named on GitLab.
    *   **10 point penalty per file** if your *Software Development Plan* and *Sprint Signature* documents in the `doc/` directory are left unchanged.
    *   Verify your submission on GitLab.  Clone your repo to a new location and test it there to ensure that it is complete and correct.
*   Use only the libraries named in this document.  If your code imports a library which your grader doesn't happen to have installed, the resulting `ModuleNotFoundError` will be treated as a crash and penalized at 50% of the assignment's value.


## Requirements

*   Your program will accept one or two command line arguments:
    1.  The starting URL specified as an *absolute* URL (see below for an explanation of what an absolute URL is)
        *   Print an error message and quit when this argument is not given
        *   Print an error message and quit when the user-specified URL is not *absolute*
            *   This must be your own error message; it is wrong if the **requests** library raises an exception here
    2.  *[Optional]* the maximum distance in number of links from the starting
            website to navigate.  When this parameter is not supplied or is not a
            positive integer your program will default to `3` links.
*   Modify the function `crawl()` to take the following parameters:
    *   `url`: an absolute URL
    *   `depth`: the current depth of recursion
    *   `maxdepth`: the maximum depth of recursion
    *   `visited`: a `set` of URLs which have already been visited
*   The return value of `crawl()` does not matter and may be ignored
*   Supply a starting distance of `0` the first time `crawl()` is called in
    your program.  In other words, the initial URL supplied from the command
    line is depth **0**.
*   You may supply an empty `set()` for the initial value of `visited`, or you
    can define some URLs that your crawler should never visit.  One reason you
    might do this would be if you encounter URLs that make your program behave
    badly. By adding these to `visited` you can avoid them entirely.
*   Each time `crawl()` is called:
    *   If the current value of `depth` exceeds `maxdepth`, immediately return from `crawl()`
    *   Otherwise:
        *   Print out the URL passed in through the `url` parameter
        *   Refer to the `depth` parameter to see the current depth of recursion
        *   Use indentation to indicate the current depth of recursion.  Print
            four spaces for each level of recursion (see the [sample output](Output.md))
        *   Use the **requests** library to fetch the webpage by `url`
        *   Print any exceptions that are raised and return from this
            invocation of `crawl()`.  Your program *must not crash* when an
            unavailable resource is encountered.
        *   Scan the resulting HTML for anchor tags `<a>`.  If the anchor tag has an `href` attribute:
            *   Discard the URL indicated by the `href` attribute if it does
                not specify a resource reachable by either the HTTP or HTTPS
                protocols.  The **requests** library only understands these two
                protocols.
            *   Discard the *fragment* portion of the URL, if present.
            *   Determine whether the `href` attribute refers to an absolute
                URL.  If not, make it into an absolute URL by using the
                `urljoin()` function and the current value of `url`
        *   Check whether the newly-formed absolute URL has been visited before
            *   If it has, loop to the next anchor tag found in the document,
                or return from this invocation of `crawl()` if there are no
                more URLs to reach from this page
            *   Otherwise, record this URL into `visited` and call `crawl()`
                again recursively with appropriate parameters 
                *   Don't forget to +1 your depth!
*   Handle exceptions such that your program prints a human-friendly message and keeps running
    *   The exception to this requirement is that this program makes a clean exit when the user presses `Ctrl-C`
        *   Do not let the program display a stack-trace in this case
            *   Catch `KeyboardInterrupt`
            *   Report how long the program ran, and how many unique URLs were visited
            *   Politely tell the user goodbye
*   Write a Users' Manual which explains how to use the program
    *   Explain the difference between *absolute* and *relative* URLs


## Utilizing software libraries

As Fred Brooks Jr. explains in his essay *No Silver Bullet*, one of the biggest
advancements of modern software engineering is the availability of libraries of
pre-written code.  Reusing well-crafted code enables us to create bigger, more
reliable and more featureful systems faster and more cheaply than writing every
line of code from scratch.  Software engineers spend a considerable portion of
their time learning how to incorporate new libraries into their projects.  Part
of the lesson of this assignment is to install and use code libraries written
by others to free you to pursue your immediate goal.

But this is only a small part of this assignment; you get to start from a
functional and nearly complete program.  Your goal is to add the element of
recursion; you do not need to use features of the libraries beyond what is
shown in the starter code to do this.  My advice is to stick to the starter
code and keep things simple.

Nevertheless, it is helpful to understand what the 3rd party code is doing in
your program.  I have included demo programs under the `demo/` directory for
this purpose.  I don't anticipate that you will need to spend much effort
studying these.


### Python Standard Library

#### [urllib.parse](https://docs.python.org/3.9/library/urllib.parse.html)  URL Parsing Library

The `urlparse()` function easily evaluates whether a URL is absolute and
suitable for use with the Requests library.

```
>>> from urllib.parse import urlparse
>>> parsed = urlparse('https://cs.stanford.edu/~knuth/news.html?query=The Art of Computer Programming#this-is-a-fragment')
>>> print(parsed)
ParseResult(scheme='https', netloc='cs.stanford.edu', path='/~knuth/news.html', params='', query='query=The Art of Computer Programming', fragment='this-is-a-fragment')
```

See the [urlparse.py demo program](../demo/demo_urlparse.py) for a more complete demonstration.


The `urljoin()` function combines an absolute URL with a relative URL,
resulting in a new absolute URL.  When two absolute URLs are joined, the paths
are matched as far as they are the same.

```
>>> from urllib.parse import urljoin
>>> absPlusRel = urljoin('https://cs.stanford.edu/', '~knuth/musings.html')
>>> print(absPlusRel)
https://cs.stanford.edu/~knuth/musings.html

>>> absPlusAbs = urljoin('https://cs.stanford.edu/~knuth/vita.html', 'https://cs.stanford.edu/~knuth/graphics.html')
>>> print(absPlusAbs)
https://cs.stanford.edu/~knuth/graphics.html
```

See the [urljoin.py demo program](../demo/demo_urljoin.py) for a more complete demonstration.


*This library is part of the Python standard distribution and does not need to
be installed manually.*



### 3rd Party Libraries

You need only use the libraries described below to complete this assignment.
In fact, your program should **not** use any other 3rd-party libraries because
of the extra work it creates for the graders.

The official documentation is linked for each library; at this point in the
semester I expect you to be capable of doing your own research.


#### [Requests](http://docs.python-requests.org/en/master/) HTTP Library

A simple interface to making HTTP requests from a Python program.

```
>>> import requests
>>> r = requests.get('http://checkip.dyndns.com')
>>> print(r.text)
<html><head><title>Current IP Check</title></head><body>Current IP Address: 13.103.37.144</body></html>
```


See the [requests.py demo program](../demo/demo_requests.py) for a more complete demonstration.

Install this library by running

```
pip3 install --user requests
```


#### [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) HTML Parsing Library

BeautifulSoup uses a pluggable HTML parser to parse a (possibly invalid)
document into a tree representation.  BeautifulSoup provides methods and
Pythonic idioms that make it easy to navigate, search, and modify the parse
tree.

```
>>> from bs4 import BeautifulSoup
>>> soup = BeautifulSoup("<html><head><title>Current IP Check</title></head><body>Current IP Address: 13.103.37.144</body></html>")
>>> text = soup.find('body').text
>>> print(text)
Current IP Address: 13.103.37.144
```

See the [beautifulsoup.py demo program](../demo/demo_beautifulsoup.py) for a more complete demonstration.

Install this library by running

```
pip3 install --user beautifulsoup4
```


## Absolute and Relative URLs

An absolute URL contains enough information by itself to locate a resource on a
network.  It includes, at minimum, a scheme followed by the token `://`
followed by a hostname.

The **scheme** (a.k.a. protocol) is the `http`, `https`, `ftp`, `telnet`, `ssh`,
etc. which may occur before the `://` token (when present).  This indicates how
the client program (i.e. your web browser or the `crawl.py` program) will
communicate with the server.

The **hostname** comes after the optional `scheme://` at the beginning of a URL and
before the next `/` character.  A hostname identifies a machine on the
internet.  The hostname may be a plain IP address or a human-friendly string
that can be resolved to an IP address.

Following the hostname may come the optional components **path**, **query
parameters** and/or **fragment**.

### Examples of Absolute URLs

*   `https://duckduckgo.com`
*   `https://gitlab.cs.usu.edu/erik.falor/cs1440-falor-erik-assn5/-/blob/master/instructions/README.md`
*   `https://usu.instructure.com/courses/547414/assignments/2698431?module_item_id=3503120`
*   `http://dwm.suckless.org/tutorial/#content`


### Examples of Relative URLs

*   `duckduckgo.com`
    -   A hostname only, no scheme
*   `erik.falor/cs1440-falor-erik-assn5/-/blob/master/instructions/README.md`
    -   No scheme nor hostname
*   `assignments/2698431?module_item_id=3503120`
    -   No scheme nor hostname, only a partial path
    -   The presence of query parameters don't affect whether this URL is absolute or not
*   `#content`
    -   A fragment-only relative URL which refers to back the same page it is found on
    -   A URL like this should be ignored by your program

Many resources presented on websites are referred to by a relative URL, which
leave off one or more of these components.  When a relative URL is encountered,
the client combines the corresponding information from the current document to
convert the relative URL into an absolute one.  Your `crawl()` function must
therefore know the URL of its current document so that it can substitute
missing information into relative URLs.

For example, if you point your program at `http://cs.usu.edu` and encounter a
link to `/articles.aspx`, your program will convert this to the absolute URL
`http://cs.usu.edu/articles.aspx` by means of the `urljoin()` function from the
`urllib.parse` library.


### Fragment Identifiers in URLs

A part of a URL occurring after a `#` symbol is known as a fragment, and refers
to a sub-section within a document.  Our program is concerned only with entire
documents; either a document has been visited or it has not.

Fragments should be removed from an absolute URL before checking whether it has
been visited before or not.

All relative URLs beginning with `#` refer to another location within the
current document.  Because your program should not visit the same document
twice, such URLs should be discarded.


## What URLs are "the same"?

You may find examples with your browser that don't match these rules.  These rules apply to this web crawler.

-   URLs with and without a trailing `/` are *different*
    -   e.g. your program treats `http://unnovative.net` and `http://unnovative.net/` as **different** sites
-   URLs beginning with `http://` and `https://` are *different*
    -   e.g. your program treats `http://cs.usu.edu` and `https://cs.usu.edu/` as **different** sites
-   URLs which differ only in their fragment are *the same*
    -   e.g. your program treats `http://unnovative.net`, `http://unnovative.net#hello` and `http://unnovative.net#goodbye` as **the same** site
