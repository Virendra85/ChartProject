from fastapi import FastAPI
from starlette.responses import FileResponse
from typing import Optional
from pydantic import BaseModel
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List

app = FastAPI()

@app.get("/")
def intro():
    return {"msg":"Hello Guys"}

@app.get("/chart")
def chart():
    xa = [1,2,3]
    # plt.bar(x,y)
    plt.savefig("hsc.png")
    return FileResponse("hsc.png")

class Chartdata(BaseModel):
    title:str
    type:str
    label:list
    series: List[List[int]] = []
    bins:list
    color: List[str] = []
    width = 3
    height = 3
    figure: List[int] = [width,height]
    years:list

@app.post("/advvis")
def drawchart(cd:Chartdata):
    print("Seaborn charts")
    plt.figure(figsize=(cd.figure[0],cd.figure[1]))
    plt.title(cd.title)
    if cd.type=="bar":
        for s in cd.series:
            sns.barplot(x=cd.label,y=s)
        # sns.factorplot(x=cd.years,y=cd.series[0],hue=cd.label)
        plt.savefig("hsc.png")
        plt.close()
    if cd.type=="pie":
        plt.pie(cd.series[0],None,cd.label)
        plt.savefig("hsc.png")
        plt.close()
    if cd.type=="line":
        sns.lineplot(cd.series[0])
        plt.savefig("hsc.png")
        plt.close()
    if cd.type=="scatter":
        sns.scatterplot(cd.series[0],cd.series[1])
        plt.savefig("hsc.png")
        plt.close()
    if cd.type=="hist":
        sns.histplot(cd.series[0],cd.series[1])
        plt.savefig("hsc.png")
        plt.close()
    return FileResponse("hsc.png")

@app.post("/chart")
def drawchart(cd:Chartdata):
    plt.figure(figsize=(cd.figure[0],cd.figure[1]))
    plt.title(cd.title)
    if cd.type=="pie":
        plt.pie(cd.series[0],None,cd.label)
        plt.savefig("hsc.png")
        plt.close()
    if cd.type=="bar":
        plt.bar(cd.label,cd.series[0],color=cd.color[0])
        plt.savefig("hsc.png")
        plt.close()
    if cd.type=="barh":
        plt.barh(cd.label,cd.series[0],color=cd.color[0])
        plt.savefig("hsc.png")
        plt.close()
    if cd.type=="line":
        plt.plot(cd.series[0],cd.series[1])
        plt.savefig("hsc.png")
        plt.close()
    if cd.type=="scatter":
        plt.scatter(cd.series[0],cd.series[1],color=cd.color[0])
        plt.savefig("hsc.png")
        plt.close()
    if cd.type=="hist":
        plt.hist(cd.series[0],cd.bins,color=cd.color[0][1])
        plt.savefig("hsc.png")
        plt.close()
    if cd.type=="3d":
        ax = plt.axes(projection="3d")
        ax.plot3D(cd.series[0],cd.series[1],cd.bins,color=cd.color[0][0])
        plt.savefig("hsc.png")
        plt.close()
    return FileResponse("hsc.png")
