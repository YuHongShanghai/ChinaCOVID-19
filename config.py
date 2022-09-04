import os

home_page_url = "http://www.nhc.gov.cn/xcs/yqtb/list_gzbd.shtml"

data_dir = "data"
plot_dir = "plot"

data_file = os.path.join(data_dir, "data.csv")
cache_file = os.path.join(data_dir, "cache")
bak_data_file = data_file + ".bak"
result_data_file = os.path.join(data_dir, "result_data.csv")

province_names = ["河北","山西","辽宁","吉林", "黑龙江",
                  "江苏","浙江","安徽","福建","江西",
                  "山东","河南","湖北","湖南","广东",
                  "海南","四川","贵州","云南","陕西",
                  "甘肃","青海","内蒙古","广西","西藏",
                  "宁夏","新疆","北京","天津","上海",
                  "重庆"]