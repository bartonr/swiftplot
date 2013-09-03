# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def graph_display(request, txt_path="/documents/2013/08/11/modified_data.txt"):
    import csv
    import numpy as np
    #import django
    #import datetime
    
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib

    ##from matplotlib.dates import DateFormatter

    x = []
    y = []

    if 'datafile_name' in request.session:
        txt_path = "/" + request.session['datafile_name']
        #raise Exception(txt_path)
    else:
        txt_path="/documents/2013/08/11/modified_data.txt"

    #raise Exception(txt_path)

    # with open(settings.MEDIA_ROOT + txt_path,"rU") as csvfile:
    #     #data_reader = csv.reader(csvfile, delimiter=',')
    #     dialect = csv.Sniffer().sniff(csvfile.readline(), [',',';', '\t', ' '])
    #     csvfile.seek(0)
    #     data_reader = csv.reader(csvfile, dialect)
    #     for row in data_reader:
    #         x.append(row[0])
    #         y.append(row[1])
    x = request.session['xdata']
    y = request.session['ydata']

    fig=Figure(facecolor='None', dpi=150)
    ax=fig.add_subplot(111)

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

    #ax.set_ylabel('Current (A)')
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