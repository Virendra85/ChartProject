from fastapi import FastAPI
from starlette.responses import FileResponse
from pydantic import BaseModel
import matplotlib.pyplot as plt
from typing import List
import numpy as np
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class Chartdata(BaseModel):
    title:str
    label:list
    series: List[List[int]] = []
    color: List[str] = []
    width = 3
    height = 3
    figure: List[int] = [width,height]
    years:list

@app.get("/info")
def read_info():
    return FileResponse("info.html")

@app.post("/bar")
def barchart(cd:Chartdata):
    plt.figure(figsize=(cd.figure[0], cd.figure[1]))
    plt.title(cd.title)
    x,a,b = [],0,[]
    b = [i for i in np.arange(0,len(cd.label),0.2)]
    for i in range(len(cd.series)):
        x.append([a+n for i,n in zip(range(len(cd.label)),[0.2*(i+1) for i in range(len(cd.label))])])
        a = x[-1][-1]+0.4
    for ((i, s),axis) in zip(enumerate(cd.series),x): # x contains the x_axis values to draw multiple bars
        plt.bar(axis, s, 0.17, color=cd.color)
    def addlabels(z, Y, W):
        for (i,j) in zip(Y,W):
            for (y,x) in zip(i,j):
                plt.text(x-0.05, y + 0.3, y)
    for i in cd.series:
        addlabels(cd.label, cd.series, x)
    ticks_x=[]
    for i in x:
        ticks_axis = 0
        for j in i:
            ticks_axis+=j
        ticks_axis = ticks_axis/len(i)
        ticks_x.append(ticks_axis) # ticks_x contains the values for x_label
    plt.tick_params(axis='x', which='both', bottom=False, top=False)
    plt.xticks(ticks=ticks_x, labels=cd.years[0:len(cd.series)])
    plt.legend()
    plt.savefig("static/bar.png")
    plt.close()
    return FileResponse("static/bar.png")

@app.post("/pie")
def piechart(cd:Chartdata):
    plt.figure(figsize=(8, 8))
    for ((i, s), y) in zip(enumerate(cd.series), cd.years):
        plt.subplot(1, len(cd.years), i + 1)
        plt.pie(s, None, cd.label, autopct="%.0f%%", colors=cd.color)
        plt.title(y)
    plt.suptitle("SALE CHART")
    plt.savefig("static/pie.png")
    plt.close()
    return FileResponse("static/pie.png")

@app.post("/line")
def linechart(cd:Chartdata):
    plt.figure(figsize=(cd.figure[0], cd.figure[1]))
    plt.title(cd.title)
    line=[]
    for i in range(len(cd.series[0])): # Making separate series for each label
        nums = []
        for j in range(len(cd.series)):
            nums.append(cd.series[j][i])
        line.append(nums)
    for l, c in zip(line, cd.color):
        plt.plot(cd.years[:len(l)], l, marker='o', color=c)
        for s, y in zip(l, cd.years):
            plt.text(x=y, y=s + 1, s='{:.0f}'.format(s))
    plt.tick_params(axis='x', which='both', bottom=False, top=False) # Removing x ticks
    plt.xticks(ticks=[i for i in cd.years[:len(line[0])]], labels=cd.years[:len(line[0])]) # Adding X ticks
    plt.legend(cd.label) # Adding legends
    plt.savefig("static/line.png")
    plt.close()
    return FileResponse("static/line.png")

