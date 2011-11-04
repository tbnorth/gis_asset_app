# Create your views here.
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django import forms
from django.db.models import Q
import json

from models import *

format_list = [('', '(all)')]
format_list.extend([(i[0],i[0]) 
    for i in Format.objects.values_list('name')])

geom_type_list = [('', '(all)')]
geom_type_list.extend([(i[0],i[0]) 
    for i in Geom_type.objects.values_list('name')])

class SearchForm(forms.Form):
    """Options for query viewing"""
    
    formats = forms.MultipleChoiceField(required=False, 
        choices=format_list,
        help_text = '(ignored for now)')
        
    geom_types = forms.MultipleChoiceField(required=False, 
        choices=geom_type_list,
        help_text = '(ignored for now)')
        
    asset_name = forms.CharField(required=False,
        help_text = 'Comma sep. dataset filenames without extension, select records matching <strong>any</strong> of these',
        widget = forms.TextInput(attrs={'class':'asset_name', 'size': 80}))
        
    attr_name = forms.CharField(required=False,
        help_text = 'Comma sep. attrib. names, select records containing <strong>any</strong> of these',
        widget=forms.TextInput(attrs={'class':'attr_name', 'size': 80}))
        
    path_txt = forms.CharField(required=False,
        help_text = 'Comma sep. path fragments, select records containing <strong>any</strong> of these - e.g. "2011", or "2011/res"',
        widget = forms.TextInput(attrs={'class':'path_txt', 'size': 80}))

    min_records = forms.IntegerField(required=False,
        help_text='Show only datasets with at least this many records')
        
    max_records = forms.IntegerField(required=False,
        help_text="Don't show datasets with more than this many records")

    min_date = forms.DateField(required=False,
        help_text='Show only datasets modified on or after this date')
        
    max_date = forms.DateField(required=False,
        help_text='Show only datasets modified on or before this date')

    search_within_selected = forms.BooleanField(required=False,
        help_text = 'Check to search withing selected - search previous conditions <strong>AND</strong> these conditions')      
    
    sort_by = forms.ChoiceField(required=True, initial='modified',
        help_text = 'Show results (when &lt;= 100) by date/path',
        choices=(('-modified','date'), ('path__path_txt','path')))
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
                q = Q()
                for i in d['attr_name'].split(','):
                    q = q | Q(attribute__name=i.strip())
                
                selection = selection.filter(q)
                
            if d['asset_name']:
                q = Q()
                for i in d['asset_name'].split(','):
                    q = q | Q(name=i.strip())
                
                selection = selection.filter(q)
            
            if d['path_txt']:
                q = Q()
                for i in d['path_txt'].split(','):
                    q = q | Q(path__path_txt__icontains=i.strip())
                
                selection = selection.filter(q)
                
            if d['min_records']:
                selection = selection.filter(records__gte=d['min_records'])
            if d['max_records']:
                selection = selection.filter(records__lte=d['max_records'])
            if d['min_date']:
                selection = selection.filter(modified__gte=d['min_date'])
            if d['max_date']:
                selection = selection.filter(modified__lte=d['max_date'])

            selection = selection.distinct()
            
            prev_selection = request.session.get('selected', [])
            
            request.session['selected'] = [i[0] 
                for i in selection.values_list('asset')
                if not prev_selection or not d['search_within_selected'] or
                       i[0] in prev_selection]
                
            selected_count = len(request.session['selected'])
            
            if selected_count < 101:
                selected = [[i[0], translate_path(i[1]), i[1], i[2]]
                    for i in selection.order_by(d['sort_by']).values_list(
                        'pk', 'path__path_txt', 'modified')
                    if not prev_selection or not d['search_within_selected'] or
                       i[0] in prev_selection]
                        
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

def drives(request):
    
    return HttpResponse('\n'.join([str(i) 
        for i in Drive.objects.order_by('letter', 'machine', 'share')]),
        mimetype="text/plain")
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
