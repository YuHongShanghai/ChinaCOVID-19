import re
import pandas as pd
from config import *
from datetime import datetime, timedelta


def load_data():
    if os.path.exists(data_file):
        data = pd.read_csv(data_file, encoding="utf-8")
        return data.to_dict("records")
    return []


def parse_text(text):
    text = text.strip()
    text = text.replace(" ", "")

    data = {"total_xz": None}
    for p in province_names:
        data[p] = None

    total_xz = re.search(r"报告，?新增确诊病例(\d+)例.*?\n", text)
    if not total_xz:
        total_xz = re.search(r"报告新增新型冠状病毒感染的肺炎确诊病例(\d+)例.*?\n", text)
    if total_xz:
        data["total_xz"] = int(total_xz.group(1))
        detail_text = total_xz.group()
        xz_detail_data = parse_detail(detail_text)
        if xz_detail_data:
            for k in xz_detail_data:
                data[k] = xz_detail_data[k]

        return data
    if "报告无新增确诊病例" in text:
        data["total_xz"] = 0
        return data

    return data


def parse_detail(text):
    detail = re.split(r"新增", text)[1]
    data = {}
    for p in province_names:
        data[p] = 0

    lst = re.findall(r"(含?\d+)\D*?（(.*?)）", detail)
    for item in lst:
        if "含" in item[0]:
            continue
        d = item[1]
        if "在" in d and not re.search(r"\d+", d):
            for p in province_names:
                if p in d:
                    data[p] = int(item[0])
                    break

        for v in d.split("，"):
            result = re.search(r"(.*?)(\d+)例", v)
            if not result:
                continue
            pn = result.group(1)
            num = result.group(2)
            pn = pn.replace("省", "")
            if pn in data:
                data[pn] += int(num)
    return data


def main():
    data = load_data()
    parse_data = []
    for row in data:
        text = row["text"]
        result = parse_text(text)
        result["date"] = (datetime.strptime(row["date"], "%Y-%m-%d") + timedelta(-1)).strftime("%Y-%m-%d")
        parse_data.append(result)
    df = pd.DataFrame(parse_data)
    df.to_csv(result_data_file, mode="w", encoding="utf-8", index=False)
