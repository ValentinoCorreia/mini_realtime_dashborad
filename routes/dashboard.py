import json
from time import sleep

from flask import Blueprint
from flask import render_template, Response

from flask_login import login_required


import psutil

bp = Blueprint("dashboard", __name__)

@bp.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html")


@bp.route("/data_stream")
@login_required
def stream():
    ram = psutil.virtual_memory()
    def getData():
        while True:
            cpu_usage = psutil.cpu_percent(interval=0.5)
            
            data = {}
            data["cpu_usage"] = cpu_usage
            # data["ram"] = {
            #     "total": ram.total,
            #     "used": ram.available
            # }
            data["ram_usage"] = ram.percent
            yield f"data: {json.dumps(data)}\n\n"
            sleep(0.5)
            
    return Response(getData(), content_type='text/event-stream')
