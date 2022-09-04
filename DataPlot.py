import pandas as pd
from pyecharts.charts import Line, Map, Timeline
from pyecharts import options as opts
from config import *


def load_data():
    if os.path.exists(result_data_file):
        data = pd.read_csv(result_data_file, encoding="utf-8")
        return data
    return None


def plot_line(data):
    line = Line()
    line.add_xaxis(xaxis_data=data["date"].tolist())
    line.add_yaxis(series_name="全部新增", y_axis=data["total_xz"].tolist())
    for name in province_names:
        line.add_yaxis(series_name=name, y_axis=data[name].tolist())
    line.render("plot/line.html")


def plot_map(data):
    t = Timeline()
    date = data["date"].tolist()
    data = data[province_names]

    for i, d in enumerate(date):
        map = Map()
        values = data.iloc[i].tolist()

        map.add("", [list(z) for z in zip(province_names, values)], "china")
        map.set_global_opts(
            title_opts=opts.TitleOpts(title=d + "新增确诊"),
            visualmap_opts=opts.VisualMapOpts()
        )
        t.add(map, d)
    t.add_schema(is_auto_play=True, play_interval=100)
    t.render("plot/map.html")


def main():
    data = load_data()
    data.dropna(axis=0, how='any', inplace=True)
    data.sort_values("date", inplace=True)
    if not os.path.exists(plot_dir):
        os.mkdir(plot_dir)
    plot_line(data)
    plot_map(data)
