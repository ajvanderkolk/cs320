# PART 1
# Data Source: https://data-cityofmadison.opendata.arcgis.com/datasets/cityofmadison::upper-state-street-pedestrian-counts/about
# cleaned dataset with below.


## TODO:
# debug with tester.py




import pandas as pd
from flask import Flask, request, jsonify, Response
from time import time
from io import BytesIO
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
pd.options.mode.chained_assignment = None  # default='warn'

app = Flask(__name__)
df = pd.read_csv("main.csv")
df['Time'] = pd.to_datetime(df['Time']).dt.normalize()

visit_times = {} # dict of visit times, for each IP
total_views = 0
a_views = 0
b_views = 0
best_ver = ""
matplotlib.use("Agg")



                        ##### landing page #####
@app.route('/')
def home():
    global total_views
    global best_ver
    
    with open("src/index.html") as f:
        html = f.read()
    
    if total_views % 2 == 1:
        case = "A"
    elif total_views % 2 == 0:
        case = "B"
        
    if total_views >= 10:
        case = best_ver
    
    if case == "A":
        html = html.replace("#donate_link#", "?from=A")
        html = html.replace("#donate_link_color#", "green")
    elif case == "B":
        html = html.replace("#donate_link#", "?from=B")
        html = html.replace("#donate_link_color#", "blue")
    
    total_views += 1
    if total_views == 10:
        if a_views >= b_views:
            best_ver = "A"
        else:
            best_ver = "B"
            
    return html

                        ##### browse html #####
@app.route('/browse.html')
def browse():
    with open("src/browse.html") as f:
        html = f.read()
    title = "<h1>Browse</h1>"
    return html + title + df.to_html(buf=None, justify='center', table_id='pedestrian-data')

                        ##### donate html #####
# TODO: donate.html
@app.route('/donate.html')
def donate():
    global a_views
    global b_views
    view = request.args.get('from')
    
    with open("src/donate.html") as f:
        html = f.read()
    
    if True: #ab_counter < 10:
        if view == 'A':
            a_views += 1
        elif view == 'B':
            b_views += 1
    return html

                        ##### browse json #####
@app.route('/browse.json')
def browse_json():
    global visit_times
    ip = request.remote_addr
    
    if ip not in visit_times:
        visit_times[ip] = time()
        return jsonify(df.to_dict())
    elif time() - visit_times[ip] > 60:
        visit_times[ip] = time()
        return jsonify(df.to_dict())
    else:
        return Response("<b>go away</b>",
                              status=429,
                              headers={"Retry-After": "3"})      

                        ##### visitors json #####
# TODO: visitors.json endpoint
@app.route('/visitors.json')
def visitors():
    return jsonify(list(visit_times.keys()))

                        ##### timeseries_area_chart svg #####
@app.route('/timeseries_area_chart.svg')
def timeseries_area_chart():
    y = list(df.columns)[1:-1]
    fig, ax = plt.subplots()
    df.plot.area(x='Time', y=y, ax=ax, rot=15)
    ax.set_xlabel("Day")
    ax.set_ylabel("Number of Pedestrians")
    ax.set_title("June 2020 State Street Pedestrian Data by Day")
    
    plt.tight_layout()
    fake_file = BytesIO()
    ax.get_figure().savefig(fake_file, format="svg", bbox_inches="tight")
    plt.close()
    
    return Response(fake_file.getvalue(), headers={"Content-type": "image/svg+xml"})

                        ##### 344statestreet_bar_chart svg #####
@app.route('/statestreet344_bar_chart.svg')
def statestreet344_bar_chart():
    try:
        bins = request.args["bins"]
    except:
        bins = None
    f = df[['Time','F344_State_St_']]
    f['F344_State_St_'] = f['F344_State_St_'].div(1000000)
    
    if bins == "by_week":
        denom = 'W-Mon'
        bin_title = 'Week'
        f = f.resample(denom, on='Time').sum().reset_index()
    elif bins == "by_dayofweek" or bins is None:
        days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday']
        bin_title = 'Day of Week'
        f['Time'] = f['Time'].dt.day_name()
        f = f.groupby(f['Time']).sum().reindex(days).reset_index()
    
    fig, ax = plt.subplots()
    f.plot.bar(x='Time', ax=ax, rot=15)
    ax.set_xlabel(f"{bin_title}")
    ax.set_ylabel("Number of Pedestrians (Millions)")
    ax.set_title(f"June 2020 State St 344 Pedestrian Data by {bin_title}")
    
    plt.tight_layout()
    fake_file = BytesIO()
    ax.get_figure().savefig(fake_file, format="svg", bbox_inches="tight")
    plt.close()
    
    return Response(fake_file.getvalue(), headers={"Content-type": "image/svg+xml"})

                        ##### email post endpoint #####
@app.route('/email', methods=["POST"])
def email():
    email = str(request.data, "utf-8")
    if len(email.split(".")[-1]) == 3 and len(email.split("@")) == 2: # 1
        with open("emails.txt", "a") as f:
            f.write(email + "\n") # 2
        with open("emails.txt", "r") as f:
            num_subscribed = sum(1 for _ in f) # count number of lines
            
        return jsonify(f"thanks {email}, your subscriber number is {num_subscribed}!")
    return jsonify("Your email address is invalid. Example: 'someone@gmail.com'") # 3

                        ##### robots txt #####
@app.route("/robots.txt")
def bot_rules():
    return flask.Response("""\
    User-Agent: *
    Disallow: /never
    """, headers={"Content-Type": "text/plain"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!

# NOTE: app.run never returns (it runs forever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.
