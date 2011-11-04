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
    
    total_assets = Asset.objects.count()
    selected_count = 0
    selected = []
    
    if request.method == 'POST':
        
        form =  SearchForm(request.POST)
        
        if form.is_valid():
        
            selection = Asset.objects.all()
            d = form.cleaned_data
            if d['attr_name']:
                for i in d['attr_name'].split(','):
                    selection = selection.filter(attribute__name=i.strip())
                    
            selected_count = selection.count()
            
            if selected_count < 101:
                selected = [[i[0], translate_path(i[1]), i[1]]
                    for i in selection.values_list('pk', 'path__path_txt')]
    else:
        
        form = SearchForm()
    
    return render_to_response(
        "gis_asset/search.html",
        {   'total_assets': total_assets,
            'selected_count': selected_count,
            'form': form,
            'selected': selected,
        },
        RequestContext(request),
    )

def translate_path(path):
    
    path = path.strip('/').split('/')
    
    if path[0] == 'nrgisl':
        path[0] = 'file:///N:'
    else:
        path.pop(0)
        path[0] = 'file:///%s:' % path[0][0].upper()
        
    return '/'.join(path[:-1])
def asset(request, pk):
    
    asset = Asset.objects.get(pk=pk)
    
    

    return render_to_response(
        "gis_asset/asset.html",
        {   'asset': asset,
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
