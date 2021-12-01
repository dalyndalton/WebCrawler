# Software Development Plan

## Phase 0: Requirements Specification *(10%)*

**Deliver:**

<!-- *   A detailed written description of the problem this program aims to solve.
*   Describe what a *good* solution looks like.
    *   List what you already know how to do.
    *   Point out any challenges that you can foresee. -->

We're making a web crawler with some standard features and some "not so standard" features 😎

### Features
- Error handling of bad url's (2XX and 4XX errors)
  - Errors should be handled by the program rather than the `requests` library
- Parse urls, creating absolute url's when provided with relative ones
- ***Multithread Support***
- Simple CLI 
- Easy display and formatting
  - Websites will be listed underneath their parent in alphabetical order

### My knowledge
The hardest part of the assignment will be the self imposed multithreading requirement, but I chose to do this as I'm already familiar with `bs4` and the `requests` library from previous projects.

### Challenges
- Maintaining data safety when accessing queue and parent classes (preventing race conditions)
- Displaying the data after all links are created, originally you would print as found but now that isn't possible as its searching multiple places at the same time
- Keeping track of parents and child links will also be difficult, as we can't garentee that the link currenly being processed relates to the one prior.
- 
## Phase 1: System Analysis *(10%)*

**Deliver:**

<!-- *   List all of the data that is used by the program, making note of where it comes from.
*   Explain what form the output will take.
*   Describe what algorithms and formulae will be used (but don't write them yet). -->

Data from this program will be coming from the *WorldWideWeb*, or any web server that houses html.  Websites will be specified in the command line, along with several optional features.

```
python src/main.py link [depth[thread count]]
```

Users can provide a custom depth to prevent their program from eating the internet, and a custom thread count to min / max performance and time.

### Algorithms
We aren't doing much in the way of mathematics, but we are creating a few things of note.

- A double linked list of parents to children
- Parsing URLS and determining validity
- Locks for data safety
- 
## Phase 2: Design *(30%)*

### ILLEGAL IMPORTS AND THEIR USES
`queue` - provides a thread safe data structure for use with `threading`
`threading` - allows the creation of multiple threads to perform requests concurrently, this way i can request multiple websites at once.
`typing` - python type hinting, helps with ide completion and self documentation
`functools` - provides the total ordering decorator, which means I only have to write 2 comparison operators and it extrapolates the rest, used to allow for sorting on custom classes.
`argparse` - allows for the creation of simple command line interface arguments, also enables tab completion 

Ok so i got a *little* carried away with the imports, the assignments about 3rd party imports right? Plus everything here is included in the standard library, so no imports should be needed.

<!-- **Deliver:**

*   Function signatures that include:
    *   Descriptive names.
    *   Parameter lists.
    *   Documentation strings that explain the purpose, inputs and outputs.
*   Pseudocode that captures how each function works.
    *   Explain what happens in the face of good and bad input.
    *   Write a few specific examples that occurred to you. -->

If you want the signature, go look at the code.  I try to keep them attached there rather than here, reserving this for a higher level overview.

### `class Link()`
The link class acts as both a data structure and a data parser for our links and all of their information.  It includes four key variables

- `self.url : str` -> the url that's been provided by the scraper
- `self.depth : int` -> the current depth of the link, used alongside the max_depth checks
- `self.parent : Link` ->the parent link, used for displaying the link and maintaining relation
- `self.children : List[Link]` -> a list of the link's children, used for display
  
`self.parent` and `self.children` are all modified using their respective setters and adders.

This function also includes some comparison functions( `__lt__` and `__eq__`) that, alongside the `@totalordering`, allow the links to be sorted like a list of strings.

`print_list()` keeps track of both how many elements have been found, as well as displays the links and children with proper formatting recursively.  Returns the number of links found.

`handle_url` modifies the internal `url` variable by first checking its validity, converting to an absolute if needed, and discarding if missing the proper schema.

The link class does no error handling of its own, instead relying on the other handling of each individual thread.


### `CrawlerManager()`

This class acts as a central interface to create the nessesary structures for each thread, and share them.  This simple class provides 2 functions, and mirrors the data requried for the crawlers to work

Data shared with the `Crawler` class
- `links : Queue` : a Queue to store links that are ready to process
- `link_lock : Lock` : A flag that signals to all other threads that a thread is accessing the data, prevents threads from grabbing the same thread (race cases)
- `parent_lock : Lock` : Same as above, but for modifying parent links, this is used seperate for speed reasons.
- `visited: set` : contains all links that have been previously visted to prevent double reads
- `base_url : Link` : The first link provided by the user

Data unique to the manager
- `threads: List[Thread]` : a list of all currently running threads, used in conjunction with a listener to make sure all threads complete before exit
- `threadcount: int` : number of threads to create
- `depth: int ` : max depth requested by user

`run()` starts the web crawler. When ran, creates the specified number of threads and starts them, then silenly waits for all threads to finish
- We set the threads.dameon to true so that exiting the main program also kill all running threads.

`print_links` a simple wrapper to call `print_link` on the parent link provided.

### `Crawler(Thread)`
Crawler is a basic thread capable of processing html and executing requests for html.

To see what each variable does, see [`Crawler()`](###CrawlerManager)

`run()` - This is the bulk of the program, if something goes wrong it is more than likely here.
Here's how run works.  
```
while True:
    get link to process from queue
        if link cannot be found, exit thread
    
    check link
        if thread is None, visited, or past depth
            continue
    
    Get html and parse tags
    add current link to visited
    for each a tag in the html
        if tag isn't visited
            add tag to queue
            bind tag to parent
            bind parent to tag
```
Currently, run will only wait for .3 seconds for another request to show up before killing of it's thread. 
## Phase 3: Implementation *(15%)*

<!-- **Deliver:**

*   (More or less) working Python code.
*   Note any relevant and interesting events that happened while you wrote the code.
    *   e.g. things you learned, things that didn't go according to plan -->

Program was implemented through a fever dream.  Some things that needed to be changed was creating a central manager, my first attempt at printing failed as well.  However, the thread implementation worked much better than initially expected.


## Phase 4: Testing & Debugging *(30%)*

<!-- **Deliver:**

*   A set of test cases that you have personally run on your computer.
    *   Include a description of what happened for each test case.
    *   For any bugs discovered, describe their cause and remedy.
*   Write your test cases in plain language such that a non-coder could run them and replicate your experience. -->

### Bugs
- A bug was discovered during implementation where it would never progress past the first depth, this was due to incorrectly marking found links as visited before parsed.
- Threads created plenty of bugs when they would die early or never quit, this was remedied by only killing a thread when the queue is empty for .3 seconds.

## Phase 5: Deployment *(5%)*

**Deliver:**

*   Your repository pushed to GitLab.
*   **Verify** that your final commit was received by browsing to its project page on GitLab.
    *   Review the project to ensure that all required files are present and in correct locations.
*   **Validate** that your submission is complete and correct by cloning it to a new location on your computer and re-running it.
    *   Run through your test cases to avoid nasty surprises.


## Phase 6: Maintenance


  > - What parts of your program are sloppily written and hard to understand?

  A: Most of the threading part looks very convoluted, and took me a while to wrap my head around.  I assume if i were to visit this in the future I would go through the same headache again.
> *   Are there parts of your program which you aren't quite sure how/why they work?

   A: Yes, anything involving threading honestly.  I think I've got it down but not enough to say that I'm confident in it.
> * If a bug is reported in a few months, how long would it take you to find the cause?

A: It may take upwards of an hour, but with the small scope of the project many bugs can be easily found and located, especially considering the modular nature of the program structure.

> * Will your documentation make sense to
>   anybody besides yourself?
>   yourself in six month's time?

A: Yes, I feel as though my documentation is more than adequate, and if anything a little boring.

> *   How easy will it be to add a new feature to this program in a year?

A: Depending on the feature, it could be as simple as adding a method to the preexisting classes, or as hard as just starting over.  More than likely, new features should be moderately easy to add.

>  Will your program continue to work after upgrading OS, hardware, or python

Yes, all of the imports besides `bs4` and `requests` are included in the standard library, and no features marked for deprecation have been used.