# Helloy 

This script retrieves content from a specific URL repeatedly while measuring 
the page load time. Crude statistics are calculated.

Utilizes selenium webdriver to wait for complete page load including AJAX requests.
Pokes with a different query parameter for each request to evade caching.

Currently you will need:
- python 3.6 (or pyenv to use 3.6 for this project)
- poetry (https://github.com/sdispater/poetry)
- geckodriver binary in your $PATH (https://github.com/mozilla/geckodriver/releases)

## Usage

```bash
git clone https://github.com/max-f/webpage_poke.git && cd webpage_poke
# Eventually (see above)
pyenv install 3.6.7
pyenv local 3.6.7
poetry install
poetry run poke [URL]
```

## Warning / Info:

Currently the default poke amount is 20 (sequential). 
The page owner might not like a high amount of requests from a single IP while caching is not taking effect.