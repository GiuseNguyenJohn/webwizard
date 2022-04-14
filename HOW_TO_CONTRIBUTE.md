# How to Contribute

## Master List of Tasks
- Functions:
    - [x] parse_for_flag -> list (UNIT TEST)
    - [x] get_files_in_dir -> list (UNIT TEST)
    - [x] extract_comments -> list 
    - [x] parse_file_for_flag -> list
    - [x] 

- [] Create class 'client' with parameters: URL
    - [x] \_\_init\_\_ should
        - [x] save url
    - [] other methods: 
        - [x] mirror (download) entire website and parse for flag -> int
        - [] extract all comments from source code -> list
        - [] brute force directories -> TODO: add type hint 
        - [] check out cookies
        - [x] parse robots.txt

## Ideas
- make branch for Client method to download entire website source code and
    parse for flag (no linux binaries allowed, python only), try using
    this: https://pypi.org/project/pywebcopy/
    
- attack login pages
    - sql inject
    - command inject
    
- attack input pages
    - command inject
    - xss

## ASCII Art
Put suggestions for cool fonts here

**Fire Font-k**
```
                  )                             (     
 (  (      (   ( /(  (  (   (          )  (     )\ )  
 )\))(    ))\  )\()) )\))(  )\  (   ( /(  )(   (()/(  
((_)()\  /((_)((_)\ ((_)()\((_) )\  )(_))(()\   ((_)) 
_(()((_)(_))  | |(_)_(()((_)(_)((_)((_)_  ((_)  _| |  
\ V  V // -_) | '_ \\ V  V /| ||_ // _` || '_|/ _` |  
 \_/\_/ \___| |_.__/ \_/\_/ |_|/__|\__,_||_|  \__,_|  
```
**Merlin1**
```
 __   __  ___   _______  _______   __   __  ___   __   ________        __        _______   ________   
|"  |/  \|  "| /"     "||   _  "\ |"  |/  \|  "| |" \ ("      "\      /""\      /"      \ |"      "\  
|'  /    \:  |(: ______)(. |_)  :)|'  /    \:  | ||  | \___/   :)    /    \    |:        |(.  ___  :) 
|: /'        | \/    |  |:     \/ |: /'        | |:  |   /  ___/    /' /\  \   |_____/   )|: \   ) || 
 \//  /\'    | // ___)_ (|  _  \\  \//  /\'    | |.  |  //  \__    //  __'  \   //      / (| (___\ || 
 /   /  \\   |(:      "||: |_)  :) /   /  \\   | /\  |\(:   / "\  /   /  \\  \ |:  __   \ |:       :) 
|___/    \___| \_______)(_______/ |___/    \___|(__\_|_)\_______)(___/    \___)|__|  \___)(________/  
```
