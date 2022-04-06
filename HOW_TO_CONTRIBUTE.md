# How to Contribute

## Master List of Tasks

- [] Create class 'client' with parameters: URL, PORT=443 (default), FlAG_FORMAT
    - [] \_\_init\_\_ should
        - [] crawl page and save entire source code to a variable
        - [] get 'robots.txt' and save output to file if response is 200 and not null
    - [] other methods: 
        - [] extract all comments from source code -> list
        - [] brute force directories -> TODO: add type hint 
        - [] parse text for flag (reuse code from forfuf) -> int (0 if flag, 1 if not found)
        - [] check out cookies
            - [] 
        - [] attack login pages
            - [] sql inject
            - [] command inject
        - [] attack input pages
            - [] command inject
            - [] xss
        - [] 
        - [] 

## Ideas
- make branch for Client method to download entire website source code and parse for flag
    (use `wget --mirror --convert-links --html-extension --wait=2 -o source <url>` ?)
    source: https://alvinalexander.com/linux-unix/how-to-make-offline-mirror-copy-website-with-wget/
