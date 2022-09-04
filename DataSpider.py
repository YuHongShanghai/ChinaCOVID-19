import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import pickle
from config import *

def print_error(msg, end="\n"):
    print("\033[1;31m%s\033[0m" % (msg), end=end)


def print_success(msg, end="\n"):
    print("\033[1;32m%s\033[0m" % (msg), end=end)


def parse_link(link):
    response = requests.get(link)
    text = response.content.decode("utf-8")
    bs = BeautifulSoup(text, "html.parser")
    return bs


def get_total_page():
    bs = parse_link(home_page_url)
    script = bs.find_all("script")[-1].text
    total_page = re.search("\d+", script)
    if total_page == None:
        print_error("error, can not get total page!")
        return 0
    return int(total_page.group())

def get_links(page_url):
    print("scrapy page:", page_url, end=" ")
    try:
        bs = parse_link(page_url)
        content = bs.find(class_="list")
        links = content.find(class_="zxxx_list").find_all("a")
        links = ["http://www.nhc.gov.cn" + a.get("href") for a in links]
        print_success("SUCCESS")
        return links
    except:
        print_error("FAIL")
        return []


def get_data(link):
    print("\t|-scrapy link: ", link, end=" ")
    data = {"link": link, "title": "", "date": "", "text": "", "complete": False}
    global HAS_FAIL
    try:
        bs = parse_link(link)
        content = bs.find(class_="list")
        data["title"] = content.find(class_="tit").text
        data["date"] = content.find(class_="source").find_all("span")[3].text.split()[1]
        data["text"] = content.find(class_="con").text
        data["complete"] = data["title"] != "" and data["date"] != "" and data["text"] != ""
        if data["complete"]:
            print_success("SUCCESS", end=" ")
            print(data["title"], data["date"])
        else:
            print_error("data not complete")
    except:
        print_error("FAIL")

    return data


def load_data():
    if os.path.exists(data_file):
        data = pd.read_csv(data_file, encoding="utf-8")
        if os.path.exists(bak_data_file):
            os.remove(bak_data_file)
        os.rename(data_file, data_file + ".bak")
        return data.to_dict("records")
    return []


def load_cache():
    if os.path.exists(cache_file):
        file = open(cache_file, "rb")
        cache = pickle.load(file)
        file.close()
        return cache
    return {}


def save_cache(cache):
    file = open(cache_file, "wb")
    pickle.dump(cache, file)
    file.close()


def main():
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    try_count = 1
    max_total_page = 0
    while True:
        HAS_FAIL = False
        total_count = 0
        success_count = 0

        print("\n\n==========start scrapy data, try count: %d ==========" % try_count)
        total_page = get_total_page()
        if max_total_page > total_page:
            total_page = max_total_page
        else:
            max_total_page = total_page

        if total_page == 0:
            HAS_FAIL = True
            try_count += 1
            continue

        print("total %d pages" % (total_page))

        last_data = load_data()
        last_data_record = {}
        for i, row in enumerate(last_data):
            if row["complete"]:
                last_data_record[row["link"]] = i

        cache = load_cache()

        for p in range(1, total_page + 1):
            print("[%2d/%2d]" % (p, total_page), end=" ")
            if p == 1:
                url = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"
            else:
                url = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd_%d.shtml" % p

            if p != 1 and url in cache:
                print_success(url + " use links in cache")
                links = cache[url]
            else:
                links = get_links(url)
                if links:
                    cache[url] = links
                else:
                    HAS_FAIL = True

            data = []

            for link in links:
                if link in last_data_record:
                    data.append(last_data[last_data_record[link]])
                    print_success("\t"+ link + " use last data")
                    success_count += 1
                else:
                    one_data = get_data(link)
                    data.append(one_data)
                    if not one_data["complete"]:
                        HAS_FAIL = True
                    else:
                        success_count += 1
                total_count += 1

            if data:
                df = pd.DataFrame(data)
                if os.path.exists(data_file):
                    df.to_csv(data_file, mode="a", header=None, encoding="utf-8", index=False)
                else:
                    df.to_csv(data_file, mode="w", encoding="utf-8", index=False)
            if cache:
                save_cache(cache)
        print_success("========== has scrapyed %%%.2f ==========" % (success_count / total_count*100))

        if success_count == total_count:
            break
        if not HAS_FAIL:
            break
        try_count += 1

    if os.path.exists(bak_data_file):
        os.remove(bak_data_file)
    print_success("COMPLETE")
