Best practices for Regular Expressions
======================================

As your Regexs grow and form into beautiful pattern-matching powerhouses, it is important
to take good care of them, and they have a tendency to grow unruly as they mature.

Here are some several safe practices for handling your Regexs so that
they can have a long productive life without getting out of control:

- Use whitespace and comments in your regular expressions.
  Whitespace is set to be ignored by default (use /s to match whitespace) so use
  spaces and newlines to break up sections freely. Regex comments look like (?# this ).
- Never let a regex become too big to be easily understood. Split up big regex
  into smaller expressions. (Sensible splits won't hurt them).
- Maintain a Matches and Non-Matches
    - Reparse can use this to test your Regex to make sure they are matching properly
    - It helps maintainers see which regular expressions match what quickly
    - It helps show your intention with each expression, so that others can confidently improve or modify them
- Maintain a description which talks about what you are trying to match with each regex,
  what you are not matching and why, and possibly a url where they might learn more
  about that specific format.
- Having each regex author list his name can be a great boon. It gives them
  credit for their work, it encourages them to put forth their best effort, and is an easy way
  to name them.
  I often name the regex after the the author so I don't have to come up with unique names
  for all my regexs, since that are often really similar.


For more information about maintaining a regex-safe environment visit:

http://www.codinghorror.com/blog/2008/06/regular-expressions-now-you-have-two-problems.html
