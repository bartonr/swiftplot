# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import csv
import numpy as np

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib

def graph_display(request, txt_path="/documents/2013/08/11/modified_data.txt"):

    x = []
    y = []

    if 'datafile_name' in request.session:
        txt_path = "/" + request.session['datafile_name']
    else:
        txt_path="/documents/2013/08/11/modified_data.txt"

    #Get x and y from data already stored in request.session.
    x = request.session['xdata']
    y = request.session['ydata']


    #Create a figure...
    fig=Figure(facecolor='None', dpi=150)
    ax=fig.add_subplot(111)

    #...label the axes...
    if 'title' in request.GET:
        ax.set_title(request.GET['title'])
        #ax.set_title(request.session['datafile_name'])
    else:
        ax.set_title('Set title')

    if 'xlabel' in request.GET:
        ax.set_xlabel(request.GET['xlabel'])
    else:
        ax.set_xlabel('Set x label')

    if 'ylabel' in request.GET:
        ax.set_ylabel(request.GET['ylabel'])
    else:
        ax.set_xlabel('Set y label')

    #... adjust graph styles
    ax.grid(True)
    #fig.set_facecolor('None')

    font = {'family' : 'normal',
         'weight' : 'normal',
         'size'   : 14}

    matplotlib.rc('font', **font)
    ax.plot(x, y, 'b-')

    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response