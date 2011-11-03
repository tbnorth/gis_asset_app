# Create your views here.
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django import forms
import json

from models import *

format_list = [('', '----')]
format_list.extend([(i[0],i[0]) 
    for i in Format.objects.values_list('name')])

geom_type_list = [('', '----')]
geom_type_list.extend([(i[0],i[0]) 
    for i in Geom_type.objects.values_list('name')])

class SearchForm(forms.Form):
    """Options for query viewing"""
    
    formats = forms.MultipleChoiceField(required=False, 
        choices=format_list)
        
    geom_types = forms.MultipleChoiceField(required=False, 
        choices=geom_type_list)
        
    asset_name = forms.CharField(required=False,
        widget = forms.TextInput(attrs={'class':'asset_name', 'size': 80}))
        
    attr_name = forms.CharField(required=False,
        widget = forms.TextInput(attrs={'class':'attr_name', 'size': 80}))
        
    path_txt = forms.CharField(required=False,
        widget = forms.TextInput(attrs={'class':'path_txt', 'size': 80}))

def search(request):
    
    return render_to_response(
        "gis_asset/search.html",
        {
            'form': SearchForm(),
        },
        RequestContext(request),
    )

def autocomplete(request):
    
    context = request.REQUEST['context']
    query = request.REQUEST['query']
    all = request.REQUEST.get('all', False)
    
    model, field = {
        'attr_name': (Attribute, 'name'),
        'asset_name': (Asset, 'name'),
        'path_txt': (Path, 'path_txt'),
    }[context]
    
    if all:
        suggestions = model.objects.filter(**{field+'__icontains': query})
    else:
        suggestions = model.objects.filter(**{field+'__istartswith': query})
    suggestions = [i[0] 
        for i in suggestions.values_list(field).order_by(field).distinct()]

    return HttpResponse(
        json.dumps({
            'query': query,
            'suggestions': suggestions,
        }),
        mimetype='text/plain'
    )
