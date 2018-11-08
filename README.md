# Helloy 

This script retrieves content from a specific URL repeatedly while measuring 
the page load time. Crude statistics are calculated.

Utilizes selenium webdriver to wait for complete page load including AJAX requests.
Pokes with a different query parameter for each request to evade caching.

Currently you will need:
- poetry (https://github.com/sdispater/poetry)
- geckodriver binary in your $PATH

Usage:

```bash
git clone && cd webpage_poke
poetry install
poetry run poke [URL]
```
