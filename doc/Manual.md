# Recursive Web Crawler User Manual

To get the most up to date instruction on how to run the program, run
```bash
python src/main.py -h
```

Currently, this is the template used to run the program
```
usage: main.py [-h] [-d --depth] [-t --thread_count] link

A multithreaded web scraper, exit early using CTRL + C

positional arguments:
  link               an absolute link to the starter website

options:
  -h, --help         show this help message and exit
  -d --depth         The maximum depth the crawer should search, provide a negative number to search infinitely
  -t --thread_count  Number of threads to create, for smaller depths less threads can be beneficial
  ```
  - link [REQUIRED] - the absolute link to start crawling on, must include http:// or https://

  - -d depth - provided by doing `-d #` where `#` is the depth you want the program to search.  Default is 3

  - -t threads - number of threads to create when crawling the program, larger searches benefit from more threads, while smaller search suffer from more threads.  Defaults to 5, not recommended to create more than 20.

## Example
If i wanted to crawl `https://cs.usu.edu` with a depth of 5 and 10 threads, i would use the following command

```
python src/main.py https://cs.usu.edu -d 5 -t 10
```

if i wanted to do the same, with the default depth i would use

```
python src/main.py https://cs.usu.edu -t 10
```