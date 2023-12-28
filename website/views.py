from django.shortcuts import render
from .temp_data import data, team_member


def home_page_view(request):
    return render(request, 'website/home_page.html')


def about_page_view(request):
    return render(request, 'website/about_page.html')


def services_list_page_view(request):
    return render(request, 'website/services/services_list_page.html', {'service_items': data})


def services_detail_page_view(request, pk):
    service = next((item for item in data if item['id'] == pk), None)
	
    if not service:
        return render(request, '404.html')
    
    context = {
        'services': data,
        'service': service,
    }
    return render(request, 'website/services/service_detail_page.html', context)


def teams_page_view(request):
    return render(request, 'website/teams/teams_page.html', {'teams': team_member})


def contact_page_view(request):
    return render(request, 'website/contact/contact_page.html')