import datetime
import os

import openpyxl
import pandas as pd

from apps.models import Person
from qux.utils.phone import phone_number
from apps.transport.models import BusRider, BusRoute


def import_excel():
    filepath = "/Users/vishal/Downloads/transportroutelist/"
    files = os.listdir(filepath)
    failed = []
    dflist = []
    for filename in files:
        f = os.path.join(filepath, filename)
        df = pd.read_excel(
            f,
            header=None,
            names=[
                "x",
                "name",
                "grade",
                "phone",
                "address",
                "area",
                "time",
                "filename",
            ],
        )
        df["filename"] = filename
        df.name = df.name.str.strip()
        row = df.index[(df.name.str.endswith("Name") == True)]
        if row.empty:
            failed.append(df)
        else:
            df = df.loc[row[0] :]
            df = df[df.columns[1:8]]
            dflist.append(df)


def import_better():
    filepath = "/Users/vishal/Downloads/transportrouteslist/"
    files = os.listdir(filepath)
    routes = {}
    records = []
    for filenum, filename in enumerate(files):
        f = os.path.join(filepath, filename)
        wb = openpyxl.load_workbook(f)
        ws = wb.active

        route_name = ws.cell(1, 1).value
        route_details = ws.cell(2, 1).value
        bus_parent = ws.cell(3, 1).value
        attendant = ws.cell(4, 1).value
        route = {
            "name": route_name,
            "route": route_details,
            "bus_parent": bus_parent,
            "attendant": attendant,
        }
        routes[filenum] = route

        for r in range(6, ws.max_row + 1):
            phone = str(ws.cell(r, 4).value)
            phone = phone.split(",")[0].split("/")[0]
            phone = phone_number(phone)
            record = {
                "route": filenum,
                "name": ws.cell(r, 2).value,
                "grade": ws.cell(r, 3).value,
                "phone": phone,
                "address": ws.cell(r, 5).value,
                "area": ws.cell(r, 6).value,
                "time": ws.cell(r, 7).value,
            }
            records.append(record)

    for route in routes:
        routes[route]["object"] = BusRoute.create_record(routes[route])

    for r in records:
        for x in ["rider", "address", "area"]:
            if hasattr(r.get(x, None), "strip"):
                pieces = [x.strip().upper() for x in str(r[x]).strip().split(",")]
                r[x] = ", ".join(pieces)

        person = Person.create_record(r)
        if person is None:
            continue

        rider = BusRider()
        rider.rider = person
        rider.route = routes[r["route"]]["object"]
        rider.area = r["area"]
        rider.time = datetime.time(7)
        rider.save()

    return routes, records
