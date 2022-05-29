from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv



def run_browser():
    global driver
    global wait
    global action
    driver =  webdriver.Chrome('chromedriver.exe')
    action = ActionChains(driver)
    wait = WebDriverWait(driver, 5)
    driver.get('https://tokopedia.com')

def search(keyword):
# manipulasi link
    global key_string
    key_string = keyword
    key_list = key_string.split(" ")
    key_string = "%20".join(key_list)

# create file
    
    columns = ["name", "price", "shop","location"]
    with open(key_string+".csv", "w", newline="", encoding="utf-8") as write:
        write = csv.writer(write)
        write.writerow(columns)

# Wait then find search bar
    try: 
        search_bar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-ubsgp5")))
        search_bar.clear() # search bar ga mau diclear
        search_bar.send_keys(keyword)

#find submit button
        search_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".css-1czin5k")))
        search_button.click()
    except:
        print("time out. Koneksi Internetmu mungkin lambat.")
        driver.quit()

def load_boxInfo():
#Wait box info. Box info contains name product, price product etc.
    try:
        box_info = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "css-974ipl")))#class box info2 produk
    except:
        print("time out. Koneksi Internetmu mungkin lambat.")
        driver.quit()

def scrol_down(steps):
# scroll down to load all boxInfos
    for down in range(0, steps):
        action.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(1.3)

def print_info():
#Assign total data
    total_names, total_prices, total_locations = 0, 0, 0
# Collect name, price, location datas
    name_data = []
    price_data = []
    location_data = []
# Join datas into a single list
    datas = []

# mendata semua nama produk
    product_names = driver.find_elements_by_class_name("css-1b6t4dn")
    for product_name in product_names:
        name_data.append(product_name.text)
        total_names += 1
    
# mendata semua harga produk
    product_prices = driver.find_elements_by_class_name("css-1ksb19c")
    for product_price in product_prices:
        price_data.append(product_price.text)
        total_prices += 1

# unique box info: 2 atau lebih produk teratas tidak memiliki locations
# wait_recommend_data untuk mendata unique box info.
# Data ini tidak memiliki location, maka isi dg blank("-") sebanyak 2x.
    try:
        recommend_data = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-kkkpmy")))#css selector box produk rekomendasi
        for recommend in recommend_data:
            location_data.append("-")
            location_data.append("-")
    except:
        pass

# mendata semua lokasi produk
    product_locations = driver.find_elements_by_class_name("css-1kdc32b")
    for product_location in product_locations:
        location_data.append(product_location.text)
        total_locations += 1

# Memisahkan data toko dengan data daerah
    shop_name = []
    city_location = []
    city_locs_index = 0
    shop_locs_index = 0

    for location in location_data:
        city_locs_index += 1
        if city_locs_index % 2 == 1:
            city_location.append(location_data[city_locs_index - 1])
        else:
            continue

    for location in location_data:
        shop_locs_index += 1
        if shop_locs_index % 2 == 0:
            shop_name.append(location_data[shop_locs_index - 1])
        else:
            continue

# Buat listed list [[name],[price],[city],[shop]]
    for data in range(0, len(name_data)):
        datas.append([])
        datas[data-1] = name_data[data-1], price_data[data-1], shop_name[data-1], city_location[data-1]

# rekam data. try except utk cegah error encoding.
    try:
        with open(key_string+".csv", "a", newline="", encoding="utf-8") as write:
            write = csv.writer(write)
            write.writerows(datas)
    except:
        print("mungkin ada error di encoding.")
        pass

    print(f"jumlah nama produk={total_names}. jumlah harga produk={total_prices}. Jumlah lokasi={total_locations}")

def next_page(): # ------->UNSOLVED. pakai link aja!
    try: # tombol next & prev punya class yg sama, atribut beda
        navpages = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".css-ad7yub-unf-pagination-item")))
        for navpage in navpages:
            label = navpage.get_attribute("aria-label")
            print(label)
            if label == "Halaman berikutnya":
                action.move_to_element(navpage).click().perform()#failed. do nothing
                break
            else:
                pass
    except:
        print("next_page error. time out. Koneksi Internemu mungkin lambat.")
        driver.quit()

def filter_hp(): # masih error
    try:
        filter_kategori = driver.find_element_by_css_selector(".css-3jtlip")
        filter_kategori.click()
    except:
        print("something wrong.")
        pass

def max_pages():
    # ambil nomor semua halaman
    navpages = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "css-1p7g6w2-unf-pagination-item")))
    pages = []
    for navpage in navpages:
        pages.append(navpage.text)
    akses = int(pages[-1].replace(".",""))
    print("Total pages = ", akses)
    return akses

def loop_scrap():
    for page in range(1,max_pages()): # in max_pages()
        link = r"https://www.tokopedia.com/search?navsource=home&page=1&q=cover%20spion&srp_component_id=02.01.00.00&st=product"
        link_list = link.split("=")
        link_list.insert(2, f'{page+1}&q')
        link_list.insert(3, key_string+"&srp_component_id")
        link = "=".join(link_list)
        driver.switch_to.new_window()
        driver.get(link)
        load_boxInfo()
        scrol_down(10)
        print_info()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    else:
        driver.quit()
