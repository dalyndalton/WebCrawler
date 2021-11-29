# CS 1440 Assignment 5 Rubric

| Points | Criteria
|:------:|-----------------------------------------------------------------------------------------------------------
| 10 pts | Software Development Plan is comprehensive and well-written<br/>DuckieCorp project conventions are followed, including a filled-out Sprint Signature
| 10 pts | A User's Manual explains in simple terms how the crawler is run<br/>Avoid explaining internal details about how the program works<br/>Write to an audience of end-users, not programmers (like a board game manual)
| 20 pts | User interface meets requirements<br/>Format of output meets requirements (esp. indentation)<br/>Runtime duration and count of visited sites is displayed when the crawler exits
| 15 pts | Exception Handling protects the crawler from crashing when encountering invalid/uncooperative sites or other problems<br/>Program gracefully exits upon receipt of `KeyboardInterrupt` exception<br/>Catch other exceptions, display an error message, and continue on to the next URL<br/>Getting hung up (or freezing) on some websites is *not* penalized
| 20 pts | `crawl()` is a recursive function, and is implemented such that it meets requirements

**Total points: 75**


## Penalties

*   This assignment is *not* eligible for the grading gift.  This due date cannot be moved.
*   Review the Course Rules document to avoid general penalties which apply to all assignments.
    *   **10 point penalty** if your repository is mis-named on GitLab.
    *   **10 point penalty per file** if your *Software Development Plan* and *Sprint Signature* documents in the `doc/` directory are left unchanged.
    *   Verify your submission on GitLab.  Clone your repo to a new location and test it there to ensure that it is complete and correct.
*   Use only the libraries named in the instructions.  If your code imports a library which your grader doesn't happen to have installed, the resulting `ModuleNotFoundError` will be treated as a crash and penalized at 50% of the assignment's value.
