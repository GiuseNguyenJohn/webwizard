# How to Contribute

## Master List of Tasks
- Functions:
    - [x] parse_for_flag -> list (UNIT TEST)
    - [x] get_files_in_dir -> list (UNIT TEST)
    - [x] extract_comments -> list (UNIT TEST)
    - [x] extract_comments_from_file -> list
    - [x] parse_file_for_flag -> list

- [] Create class 'client' with parameters: URL
    - [x] \_\_init\_\_ should
        - [x] save url
        - [x] save directory
        - [x] save webwizard_output directory
    - [] other methods: 
        - [x] check_robots -> bool
        - [x] crawl_robots -> dict
        - [x] extract_comments -> list
        - [x] get_cookies -> dict
        - [x] get_remote_files -> list
        - [x] mirror -> None
        - [x] parse_website_for_flag -> list

## Questions
- directory parameter for Client class?

## Ideas
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
