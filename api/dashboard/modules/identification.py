from django.shortcuts import render, redirect

from apps.wallet.models import Identification
from django.core.paginator import Paginator




def idenfication_view(request):
    identification = Identification.objects.all().order_by('-pk')
    paginator = Paginator(identification, 10)
    page_number = request.GET.get('page')
    identification = paginator.get_page(page_number)
    start_index = (identification.number - 1) * paginator.per_page + 1
    context = {
        'identification': identification,
        'active': 'identification'
    }
    return render(request, template_name='users/identification.html', context=context)
def identification_detail(request,pk):
    identification = Identification.objects.filter(pk=pk).first()
    if not identification:
         return render(request, 'users/identification.html', {"error": "User not found"})

    content = {
        'identification': identification,
        'active': 'identification'
    }
    return render(request, 'users/identification_detail.html', content)