from fastapi import FastAPI
from starlette.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import json

app = FastAPI()

class Chartdata(BaseModel):
    data:dict

@app.get("/excel")
def jsonToExcel():
    return FileResponse("Excel.xlsx")

@app.post("/excel")
def jsonToExcel(cd:Chartdata):
    with open("sample.json","w") as outfile:
        json.dump(cd.data,outfile)
    df_json = pd.read_json("sample.json")
    df_json.to_excel("Excel.xlsx")
    return FileResponse("Excel.xlsx")