from tokopedia import *

while True:
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