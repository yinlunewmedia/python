from flask import Flask, render_template, request
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.charts import Bar
import pandas as pd


app = Flask(__name__)

imports = pd.read_csv("imports.csv", encoding='utf-8', delimiter="\t")
exports = pd.read_csv('exports2.csv', encoding='utf-8', delimiter="\t")
df = pd.read_csv('exports.csv', encoding='utf-8', delimiter="\t")
world = pd.read_csv('exports_all.csv', encoding='utf-8', delimiter="\t")
type = df['type'].tolist()
name = imports['Country Name'].tolist()
imports_2018=list(tuple(zip(name,imports['2018'].tolist())))
exports_2018=list(tuple(zip(name,exports['2018'].tolist())))
US_imports = imports.iloc[207, 1:]
US_exports = exports.iloc[207, 1:]
US = US_exports - US_imports
CN_imports = imports.iloc[37, 1:]
CN_exports = exports.iloc[37, 1:]
CN = CN_exports - CN_imports
year = [int(x) for x in imports.columns.values[1:]]

def imports_2018_map() -> Map:
    c = (
        Map()
            .add('进口', imports_2018, 'world')
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(min_=imports['2018'].min(), max_=imports['2018'].max()),
            title_opts=opts.TitleOpts(title="世界2018年各国进口额"),
        )
    )
    return c.render_embed()

def exports_2018_map() -> Map:
    b = (
        Map()
            .add('出口', exports_2018, 'world')
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(min_=imports['2018'].min(), max_=imports['2018'].max()),
            title_opts=opts.TitleOpts(title="世界2018年各国出口额"),
        )
    )
    return b.render_embed()

def bar_base() -> Bar:
    o = (
        Bar(init_opts=opts.InitOpts(width='1280px', height='720px'))
            .add_xaxis(year)
            .add_yaxis("US", US.tolist(), )
            .add_yaxis("CN", CN.tolist(), )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="贸易差额"),
            datazoom_opts=opts.DataZoomOpts(),
        )
    )
    return o.render_embed()

exports_imports_available_loaded = list(df.type.dropna().unique())

@app.route('/',methods=['GET'])
def entry()->'html':
    title="中美贸易战与全球经济形势的联系"
    return render_template('entry.html',
                           the_title = title)

@app.route('/exports_imports_data',methods=['POST'])
def exports_imports()->'html':
    data_str = df.to_html()
    exports_imports_available = exports_imports_available_loaded
    return render_template('exports_data.html',
                           the_res = data_str,
                           the_select_type = exports_imports_available)

@app.route('/exports_imports_compare',methods=['POST'])
def exports_imports_compare()->'html':
    return render_template('fsl.html',
                           the_plot_all_1 = imports_2018_map(),
                           the_plot_all_2 = exports_2018_map())

@app.route('/worldhhh',methods=['POST'])
def world_exports()->'html':
    data_world = world.to_html()
    return render_template('exports_data2.html',
                           the_res = data_world,)

@app.route('/uncn',methods=['POST'])
def uncn()->'html':
    word="中美贸易差"
    return render_template('uncn.html',
                           the_plot_all=bar_base(),
                           h1=word)

@app.route('/worldppp',methods=['POST'])
def worldphoto()->'html':
    return render_template('worldppp.html')

@app.route('/exports_data',methods=['POST'])
def exports()->'html':
    the_type = request.form["the_type_selected"]
    dfs = df.query("type=='{}'".format(the_type))
    if the_type=='exports':
        the_photo=exports_2018_map()
    if the_type=='imports':
        the_photo=imports_2018_map()
    data_str = dfs.to_html()
    exports_imports_available = exports_imports_available_loaded
    return render_template('exports_data3.html',
                           the_res=data_str,
                           the_select_type=exports_imports_available,
                           the_plot_all=the_photo)

if __name__ == '__main__':
    app.run(debug=True)
