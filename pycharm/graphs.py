from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.responses import FileResponse
from typing import Optional
from pydantic import BaseModel
import matplotlib.pyplot as plt
from typing import List
import numpy as np
import seaborn as sns
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/info")
def read_root():
    return FileResponse("info.html")

class Chartdata(BaseModel):
    title:str
    label:list
    series: List[List[int]] = []
    bins:list
    color: List[str] = []
    width = 3
    height = 3
    figure: List[int] = [width,height]
    years:list

@app.post("/bar")
def barchart(cd:Chartdata):
    plt.figure(figsize=(cd.figure[0], cd.figure[1]))
    plt.title(cd.title)
    x,a,b = [],0,[]
    b = [i for i in np.arange(0,len(cd.label),0.2)]
    for i in range(len(cd.series)):
        x.append([a+n for i,n in zip(range(len(cd.label)),[0.2*(i+1) for i in range(len(cd.label))])])
        a = x[-1][-1]+0.4
    for ((i, s),axis) in zip(enumerate(cd.series),x):
        plt.bar(axis, s, 0.17, color=cd.color)
    def addlabels(z, Y, W):
        for (i,j) in zip(Y,W):
            for (y,x) in zip(i,j):
                plt.text(x-0.05, y + 0.3, y)
    for i in cd.series:
        addlabels(cd.label, cd.series, x)
    plt.tick_params(axis='x', which='both', bottom=False, top=False)
    ticks_x=[]
    for i in x:
        ticks_axis = 0
        for j in i:
            ticks_axis+=j
        ticks_axis = ticks_axis/len(i)
        ticks_x.append(ticks_axis)
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
    for i, c in zip(cd.series, cd.color):
        line = sns.lineplot(x=cd.label, y=i, color=c)
        for x, j in zip(cd.label, i):
            plt.text(x=x, y=j + 1, s='{:.0f}'.format(j))
    plt.tick_params(axis='x', which='both', bottom=False, top=False)
    plt.xticks(ticks=[i for i in range(len(cd.years))], labels=cd.years)
    fig = line.get_figure()
    plt.legend(cd.label)
    fig.savefig("static/line.png")
    plt.close()
    return FileResponse("static/line.png")

@app.post("/advchart")
def advchart(cd:Chartdata):
    print("Seaborn graphs")
    plt.figure(figsize=(cd.figure[0],cd.figure[1]))
    plt.title(cd.title)

    if cd.type=="bar":
        X_axis = np.arange(len(cd.label))
        for ((i,s),c) in zip(enumerate(cd.series),cd.color):
           plt.bar(X_axis+0.2*(i+1),s,0.17,label=cd.label[i],color=c)
        w=c= 0.14
        def addlabels(x,y,w):
            for i in range(len(x)):
                plt.text(w, y[i]+0.3, y[i])
                w+=1
        for i in cd.series:
            addlabels(cd.label,i,w)
            w = c+0.20
            c=w
        plt.tick_params(axis='x',which='both',bottom=False,top=False)
        plt.xticks(ticks=[i+0.38 for i in range(len(cd.label))],labels=cd.years[0:len(cd.label)])
        plt.legend()
        plt.savefig("image.png")
        plt.close()
    if cd.type=="line":
        for i,c in zip(cd.series,cd.color):
            line = sns.lineplot(x=cd.label,y=i,color=c)
            for x,j in zip(cd.label,i):
                plt.text(x=x,y=j+1,s='{:.0f}'.format(j))
        plt.tick_params(axis='x',which='both',bottom=False,top=False)
        plt.xticks(ticks=[i for i in range(len(cd.years))],labels=cd.years)
        fig = line.get_figure()
        plt.legend(cd.label)
        fig.savefig("image.png")
        plt.close()
    if cd.type=="pie":
        plt.figure(figsize=(8,8))
        for ((i,s),y) in zip(enumerate(cd.series),cd.years):
            plt.subplot(1, len(cd.years),i+1)
            plt.pie(s,None,cd.label,autopct="%.0f%%",colors=cd.color)
            plt.title(y)
        plt.suptitle("SALE CHART")
        plt.savefig("image.png")
        plt.close()
    if cd.type=="hist":
        for ((i,s),l) in zip(enumerate(cd.series),cd.label):
            plt.subplot(1, len(cd.years),i+1)
            plt.hist(x=s,bins=cd.bins,color=cd.color[i])
            plt.title(l)
        plt.savefig("image.png")
        plt.close()
    if cd.type=="dist":
        dist = sns.distplot(cd.series)
        fig = dist.get_figure()
        fig.savefig("image.png")
        plt.close()
    if cd.type=="scatter":
        sca = sns.scatterplot(cd.series[0],cd.series[1],hue=cd.label)
        fig = sca.get_figure()
        fig.savefig("image.png")
        plt.close()
    if cd.type=="box":
        for s in cd.series:
            box = sns.boxplot(x = cd.label,y = s)
        fig = box.get_figure()
        fig.savefig("image.png")
        plt.close()
    if cd.type=="violin":
        for s in cd.series:
            v = sns.violinplot(x = cd.label,y = s)
        fig = v.get_figure()
        fig.savefig("image.png")
        plt.close()
    return FileResponse("image.png")

