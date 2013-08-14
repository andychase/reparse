Best practices for Regular Expressions
======================================

Take good care of your Regex, and they'll take good care of you, so to speak.
There are several best practices for dealing with Regex so that they are useful,
without getting out of control.

- use whitespace and comments in your regular expression
- maintain a Matches and Non-Matches
    - RE|PARSE can use this to test your Regex to make sure they are working properly
    - Helps maintainers see which regular expressions do what
    - Help show your intention with each expression, so that others can improve or change it
- maintain a description which talks about what you are matching with each regex, and
  possibly a url where they can find more information about that format
- Having each regex author list his name can be a great boon, both because it gives them
  credit for their work, as well as it encourages them to put forth their best effort.
  I often put the author and a short name as the name of the regex, which is an easy way
  to come up with unique names for regexes that are often really similar.


Here are some resources for more info

http://www.codinghorror.com/blog/2008/06/regular-expressions-now-you-have-two-problems.html