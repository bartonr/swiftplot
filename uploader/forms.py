from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 2 megabytes'
    )

class CustomizeForm(forms.Form):
    xlabel = forms.CharField(
    	widget=forms.TextInput(attrs={'style':'width: 90%;', 'placeholder':'x label'}))
    ylabel = forms.CharField(
    	widget=forms.TextInput(attrs={'style':'width: 90%;', 'placeholder':'y label'}))
    title = forms.CharField(
    	widget=forms.TextInput(attrs={'style':'width: 90%;', 'placeholder':'Title'}))