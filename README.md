# next-vote
Easily configurable voting system for Next House

Obtain a copy of `residents.csv` and drop it in this folder.

# Configuration
The only file you need to modify is `config.js`. Many parameters should be self-explanatory, but I'll describe those which might not be clear:
- `document`: Set to a URL of a page to be displayed as an iframe. For example, put a link to embed the budget here. Leave blank if not needed.
- `question.shuffle`: Set to `true` and the order in which the options will be displayed are shuffled.
- `question.write_in`: Set to `true` to enable a write-in option.
- `question.option`: Either give a simple string, or an object with the following parameters:
    - `question.option.title`: Title of this option
    - `question.option.description`: A body of text (like a platform) above the option
    - `question.option.wing`: Show option only if user's wing equals this. (Format as "2E", "4W", etc.)
