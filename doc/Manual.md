# **NOT Recursive** Web Crawler User Manual

To get the most up to date instruction on how to run the program, run

```bash
python src/main.py -h
```

Currently, this is the template used to run the program

```
 % python src/main.py -h
usage: main.py [-h] [-d --depth] [-t --thread_count] [-k --timeout] link

A multithreaded web scraper, exit early using CTRL + C

positional arguments:
  link               an absolute link to the starter website

optional arguments:
  -h, --help         show this help message and exit
  -d --depth         The maximum depth the crawer should search, provide a negative number to search infinitely
  -t --thread_count  Number of threads to create, for smaller depths less threads can be beneficial
  -k --timeout       time before a thread dies, higher numbers will prevent threads from closing prematurely, but also cause the program to run longer.
```

A few notes:

- `timeout * thread_count` is the amount of extra needed to run the program (worst case)

## Example

If i wanted to crawl `https://cs.usu.edu` with a depth of 5 and 10 threads, i would use the following command

```
python src/main.py https://cs.usu.edu -d 5 -t 10
```

if i wanted to do the same, with the default depth i would use

```
python src/main.py https://cs.usu.edu -t 10
```

If i have a slow connection, I will want to increase the amout of time before my threads close

```
python src/main.py https://cs.usu.edu -t 10 -k .75
```
