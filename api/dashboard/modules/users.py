from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from twisted.names.client import query
from django.contrib.auth.models import Permission

from api.dashboard.forms.user import UserEditForm
from api.wallet.modules.identification import identification
from apps.accounts.models import Account
from apps.wallet.models import Identification, CardModel
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password



def user_page(request):
    query = request.GET.get('query', '')
    if query:
        users = Account.objects.filter(
            Q(email__icontains=query) | Q(phone_number=query)
        )
    else:
        users = Account.objects.all().order_by('-pk')


    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query
    }

    return render(request, template_name='users/user_permission.html', context=context)
def user_permissions(request, user_id):
    user = get_object_or_404(Account, id=user_id)
    permissions = Permission.objects.all()

    if request.method == 'POST':

        user.user_permissions.clear()
        selected_permissions = request.POST.getlist('permissions')

        for perm_id in selected_permissions:
            permission = Permission.objects.get(id=perm_id)
            user.user_permissions.add(permission)

        user.save()

        return redirect('account_api:user_page')

    context = {
        'user': user,
        'permissions': permissions,
    }
    return render(request, 'users/user_role.html', context)


def user_view(request, user_id):
    user = Account.objects.filter(id=user_id).first()

    if not user:
        return redirect('account_api:user_page')

    card = CardModel.objects.filter(owner=user.id).first()

    if not card:
        return render(request, 'users/user_profile.html', {'error': 'No card found'})

    identification = Identification.objects.filter(user=user.id).first()

    if not identification:
        return render(request, 'users/user_profile.html', {'error': 'No identification found'})


    profile_data = identification.response

    common_data = profile_data.get('profile', {}).get('common_data', {})

    first_name = common_data.get('first_name', 'N/A')
    last_name = common_data.get('last_name', 'N/A')
    middle_name = common_data.get('middle_name', 'N/A')

    context = {
        'card': card,
        'user': user,
        'identification': identification,
        'first_name': first_name,
        'last_name': last_name,
        'middle_name': middle_name,
    }

    return render(request, 'users/user_profile.html', context)

def edit_user(request, user_id):
    print(user_id, "^^^^^^^^")
    user = get_object_or_404(Account, id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():

            password = form.cleaned_data.get('password')
            if password:
                user.password = make_password(password)
            form.save()
            return redirect('account_api:user_page')
    else:
        form = UserEditForm(instance=user)

    return render(request, 'users/user_permission.html', {'form': form, 'user': user})


def user_delete(request, user_id):
    user = Account.objects.filter(id=user_id).first()
    user.delete()
    return redirect('account_api:user_page')