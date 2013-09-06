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

    #Allow reading files in universal inline mode.
    csvfile = io.StringIO(unicode(csvfile.read()), newline=None)

    #Search for possible formatting with different separators
    dialect = csv.Sniffer().sniff(csvfile.readline(), [',',';', '\t', ' '])

    csvfile.seek(0)
    data_reader = csv.reader(csvfile, dialect)
    for row in data_reader:
        xdata.append(row[0])
        ydata.append(row[1])
    return xdata, ydata

def upload_response(request, **kwargs):
    # Handle file upload
    if request.method == 'POST':
        if 'docfile' in request.FILES:
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_file = request.FILES['docfile']
                newdoc = Document(docfile = uploaded_file)

                request.session['xdata'], request.session['ydata'] = csvreader(uploaded_file)
                request.session['datafile_name'] = newdoc.docfile.name
                #newdoc.save()

                # Redirect to the document list after POST
                return HttpResponseRedirect(reverse('uploader.views.upload_response'))
        else:
            #The page was called from the customize button, not to upload a file
            customize_form = CustomizeForm(request.POST)
            form = DocumentForm() # A empty, unbound form
            request.session['xlabel'] = request.POST.get('xlabel', '')
            request.session['ylabel'] = request.POST.get('ylabel', '')
            request.session['title'] = request.POST.get('title', '')

            return HttpResponseRedirect(reverse('uploader.views.upload_response'))
    else:
        #This page was called without any input.
        #del request.session['xlabel']
        #del request.session['ylabel']
        form = DocumentForm() # A empty, unbound form
        customize_form = CustomizeForm(
                initial={'xlabel': 'x label', 'ylabel': 'y label', 'title': 'title'}
            )

    #If the customized title, xlabel, and ylabel have been created already, add them.
    #Otherwise revert to default.
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
    # Handle drag and drop file upload.
    if request.method == 'POST':
        uploaded_file = request.FILES['pic']
        newdoc = Document(docfile = uploaded_file)
        
        request.session['xdata'], request.session['ydata'] = csvreader(uploaded_file)

        request.session['datafile_name'] = newdoc.docfile.name

        return HttpResponse("OK")

        to_json = {
            "status": "File was uploaded successfully",
        }
    else:
        to_json = {
            "status": "Error, use POST",
        }
    #return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')
    return HttpResponse(simplejson.dumps(to_json))
