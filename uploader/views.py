from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from uploader.models import Document
from uploader.forms import DocumentForm, CustomizeForm
#from plots.models import Data1
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
import csv, io

def csvreader(csvfile):
    xdata = []
    ydata = []
    #csvfile = open(csvfile,'rU')

    csvfile = io.StringIO(unicode(csvfile.read()), newline=None)

    dialect = csv.Sniffer().sniff(csvfile.readline(), [',',';', '\t', ' '])
    csvfile.seek(0)
    data_reader = csv.reader(csvfile, dialect)
    for row in data_reader:
        xdata.append(row[0])
        ydata.append(row[1])
    return xdata, ydata

def upload_response(request, **kwargs):
    # Handle file upload
    print "hello there!"
    if request.method == 'POST':
        if 'docfile' in request.FILES:
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_file = request.FILES['docfile']
                newdoc = Document(docfile = uploaded_file)

                # request.session['xdata'] = []
                # request.session['ydata'] = []
                #with open(uploaded_file) as csvfile:
                #data_reader = csv.reader(csvfile, delimiter=',')

                request.session['xdata'], request.session['ydata'] = csvreader(uploaded_file)

                # csvfile = uploaded_file
                # dialect = csv.Sniffer().sniff(csvfile.readline(), [',',';', '\t', ' '])
                # csvfile.seek(0)
                # data_reader = csv.reader(csvfile, dialect)
                # for row in data_reader:
                #     request.session['xdata'].append(row[0])
                #     request.session['ydata'].append(row[1])

                #Data1.objects.all().delete()
                #for line in uploaded_file:
                    #line =  line.split(',')
                    #d1 = Data1()
                    #d1.xdata = line[0]
                    #d1.ydata = line[1]
                    #d1.save()

                #newdoc.save()

                request.session['datafile_name'] = newdoc.docfile.name

                # Redirect to the document list after POST
                #return HttpResponseRedirect(reverse('uploadexample.views.upload_response'), {'images': "plots.views.graph_display", 'form': form})
                return HttpResponseRedirect(reverse('uploader.views.upload_response'))
                # return render_to_response('index.html', 
                #     {'images': "plots.views.graph_display", 'form': form},
                #     context_instance=RequestContext(request))
        else:
            customize_form = CustomizeForm(request.POST)
            #xlabel = request.POST.get('xlabel', '')
            form = DocumentForm() # A empty, unbound form
            #customize_form = CustomizeForm(
            #    initial={'xlabel': 'x label', 'ylabel': 'y label'}
            #)
            request.session['xlabel'] = request.POST.get('xlabel', '')
            request.session['ylabel'] = request.POST.get('ylabel', '')
            request.session['title'] = request.POST.get('title', '')

            return HttpResponseRedirect(reverse('uploader.views.upload_response'))
    else:
        #del request.session['xlabel']
        #del request.session['ylabel']
        form = DocumentForm() # A empty, unbound form
        customize_form = CustomizeForm(
                initial={'xlabel': 'x label', 'ylabel': 'y label', 'title': 'title'}
            )

    if 'title' in request.session:
        title = request.session['title']
        customize_form.initial['title']= title
    else:
        title = ''

    if 'xlabel' in request.session:
        xlabel = request.session['xlabel']
        customize_form.initial['xlabel']= xlabel
    else:
        xlabel = 'Set x Label'

    if 'ylabel' in request.session:
        ylabel = request.session['ylabel']
        customize_form.initial['ylabel']= ylabel
    else:
        ylabel = 'Set y label'

    return render_to_response(
            'plot.html',
            {'images': "plots.views.graph_display", 'xlabel': xlabel, 'ylabel': ylabel, 'title': title,
            'form': form, 'customize_form': customize_form},
            context_instance=RequestContext(request))

def new_plot(request, **kwargs):
    #del request.session['xlabel']
    #del request.session['ylabel']
    form = DocumentForm() # A empty, unbound form
    customize_form = CustomizeForm(
            initial={'xlabel': 'x label', 'ylabel': 'y label', 'title': 'title'}
        )

    return render_to_response(
            'plot.html',
            {'form': form, 'customize_form': customize_form},
            context_instance=RequestContext(request))

@csrf_exempt
def dragdropreceive(request):
    # Handle file upload
    #raise Exception(request.method)
    if request.method == 'POST':
        uploaded_file = request.FILES['pic']
        newdoc = Document(docfile = uploaded_file)
        
        request.session['xdata'], request.session['ydata'] = csvreader(uploaded_file)

        #newdoc.save()

        request.session['datafile_name'] = newdoc.docfile.name

        return HttpResponse("OK")
        #return HttpResponseRedirect(reverse('uploadexample.views.upload_response'))

        to_json = {
            "status": "File was uploaded successfully",
        }
    else:
        to_json = {
            "status": "Error, use POST",
        }
    #return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')
    return HttpResponse(simplejson.dumps(to_json))
