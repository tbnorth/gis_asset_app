# Create your views here.
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django import forms
from django.db.models import Q
from django.http import Http404

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
        help_text = """Show datasets in <strong>any</strong> of 
            these formats, use '(all)' to clear selection,  
            'esri shapefile' used for both shapefiles and .dbfs, 
            use geom_types=none to isolate plain .dbfs""")
        
    geom_types = forms.MultipleChoiceField(required=False, 
        choices=geom_type_list,
        help_text = """Show datasets with <strong>any</strong> of
            these geomtry types, use '(all)' to clear selection,
            none indicates plain .dbf""")
        
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
        help_text = 'Check to search within selected - search previous conditions <strong>AND</strong> these conditions')  
            
    use_regex = forms.BooleanField(required=False,
        help_text = 'Interpret search strings and case insensitive regular expressions')      
    
    sort_by = forms.ChoiceField(required=True, initial='modified',
        help_text = 'Show results (when &lt;= 100) by date/path',
        choices=(('-modified','date'), ('path__path_txt','path')))
def check_origin(request):
    
    if not '131.212.123' in request.META.get('REMOTE_ADDR', ''):
        raise Http404
def search(request):
    
    check_origin(request)
    
    total_assets = Asset.objects.count()
    selected_count = 0
    selected = []
    
    if request.method == 'POST':
        
        form =  SearchForm(request.POST)
        
        if form.is_valid():
            
            d = form.cleaned_data
            
            regex = d['use_regex']
            
            filters = request.session['filters']
            request.session.modified = True
            if not d['search_within_selected']:
                filters.clear()
        
            selection = Asset.objects.all()
            
            # *partial* *alternative* to selection filtering on session below
            # if (d['search_within_selected'] and 
            #     request.session.get('selected', [])):
            #     selection = selection.filter(asset__in=request.session.get(
            #         'selected', []))
            
            if d['attr_name']:
                q = Q()
                for i in d['attr_name'].split(','):
                    if regex:
                        q = q | Q(attribute__name__iregex=i.strip())
                    else:
                        q = q | Q(attribute__name=i.strip())
                
                selection = selection.filter(q)
                filters.add("Has an attribute %s"%' or '.join(d['attr_name'].split(',')))
                
            if d['asset_name']:
                q = Q()
                for i in d['asset_name'].split(','):
                    if regex:
                        q = q | Q(name__iregex=i.strip())
                    else:
                        q = q | Q(name=i.strip())
                
                selection = selection.filter(q)
                filters.add("Dataset name in %s"%' or '.join(d['asset_name'].split(',')))
            
            if d['path_txt']:
                q = Q()
                for i in d['path_txt'].split(','):
                    if regex:
                        q = q | Q(path__path_txt__iregex=i.strip())
                    else:
                        q = q | Q(path__path_txt__icontains=i.strip())
                
                selection = selection.filter(q)
                filters.add("Path contains %s"%' or '.join(d['path_txt'].split(',')))
                
            if d['min_records']:
                selection = selection.filter(records__gte=d['min_records'])
                filters.add("At least %s records"%d['min_records'])
            if d['max_records']:
                selection = selection.filter(records__lte=d['max_records'])
                filters.add("At most %s records"%d['max_records'])
            if d['min_date']:
                selection = selection.filter(modified__gte=d['min_date'])
                filters.add("Modified on or after %s"%d['min_date'])
            if d['max_date']:
                selection = selection.filter(modified__lte=d['max_date'])
                filters.add("Modified on or before %s"%d['max_date'])
                
            if d['formats']:
                q = Q()
                for f in d['formats']:
                    if not f:  # "(all)" is selected
                        q = Q()
                        break
                    q = q | Q(format__name=f)
                selection = selection.filter(q)
                filters.add("Format is %s"%' or '.join(d['formats']))
                
            if d['geom_types']:
                q = Q()
                for f in d['geom_types']:
                    if not f:  # "(all)" is selected
                        q = Q()
                        break
                    q = q | Q(geom_type__name=f)
                selection = selection.filter(q)
                filters.add("Geometry type is %s"%' or '.join(d['geom_types']))
                
            selection = selection.distinct()
            
            prev_selection = list( request.session.get('selected', []) )
            
            request.session['selected'] = [i[0] 
                for i in selection.values_list('asset')
                if not prev_selection or not d['search_within_selected'] or
                    i[0] in prev_selection]
                
            selected_count = len(request.session['selected'])
            
            selected = [[i[0], translate_path(i[1]), i[1], i[2]]
                for i in selection.order_by(d['sort_by']).values_list(
                    'pk', 'path__path_txt', 'modified')[:200]
                if not prev_selection or not d['search_within_selected'] or
                   i[0] in prev_selection]
                        
    else:
        
        form = SearchForm()
        request.session['filters'] = set()
    
    return render_to_response(
        "gis_asset/search.html",
        {   'total_assets': total_assets,
            'selected_count': selected_count,
            'form': form,
            'selected': selected,
            'filters': request.session['filters'],
        },
        RequestContext(request),
    )

def translate_path(path):
    
    path = path.strip('/').split('/')
    
    path[0] += '.nrri.umn.edu'
    path.pop(0)  # discard machine
    path[0] = 'file:///%s:' % path[0][0].upper()  # assume drive
        
    return '/'.join(path[:-1])  # drop last to open directory
def asset(request, pk):
    
    check_origin(request)
    
    asset = Asset.objects.get(pk=pk)

    return render_to_response(
        "gis_asset/asset_core.html" 
        if request.is_ajax() else "gis_asset/asset.html",
        {   'asset': asset,
        },
        RequestContext(request),
    )

def drives(request):
    
    check_origin(request)
    
    return HttpResponse('\n'.join([str(i) 
        for i in Drive.objects.order_by('letter', 'machine', 'share')]),
        mimetype="text/plain")
def autocomplete(request):
    
    check_origin(request)
    
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
        
    if request.session.get('selected', []):
        suggestions = suggestions.filter(
            asset__in=request.session.get('selected', []))
            
    suggestions = suggestions.distinct()
        
    suggestions = [i[0] for i in suggestions.values_list(field)[:250]]
    suggestions.sort()  # django can't sort *and* slice

    return HttpResponse(
        json.dumps({
            'query': query,
            'suggestions': suggestions,
        }),
        mimetype='text/plain'
    )
