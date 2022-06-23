from tokopedia import *

while True:
    try:
        choose = int(input("Type 1 for input a KEYWORD(automatically). Type 2 for input a LINK(manually). input: "))
    except ValueError:
        print("input error. please input 1 or 2")
        continue
    if choose == 1:
        key_ = str(input("Input a keyword: "))
        if key_ != "":
            run_browser()
            search(key_)
            load_boxInfo()
            scrol_down(10)
            print_info()
            loop_scrap()
            break
        else:
            continue
    elif choose == 2:
        key_ = str(input("Input a link: "))
        run_browser()
        by_link(key_)
    else:
        continue

