from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from api.wallet.modules.identification import identification
from apps.accounts.models.account import Account
from apps.wallet.models import TransactionsModel, Identification
from django.core.paginator import Paginator

@login_required(login_url='account_api:login')
def index(request):

    permissions = {
        'user_permission': request.user.has_perm('super_app.user_permission'),


    }
    return render(request, 'index.html', {'permissions': permissions})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = Account.objects.filter(email=email).first()

        if not user:
            return render(request, 'login.html', {"error": "User not found"})

        if check_password(password, user.password):

            login(request, user)
            return redirect('account_api:index')
        else:
            return render(request, 'login.html', {"error": "Wrong password"})

    return render(request, 'login.html')

def logout_view(request):
    login(request)
    return redirect('account_api:login')


def transcation_view(request):
    query = request.GET.get('query', '')  # Qidiruv so'zini olish
    transactions_list = TransactionsModel.objects.all().order_by('-pk')

    if query:

        transactions_list = transactions_list.filter(
            Q(sender_ext_id=query) | Q(cr_ext_id=query)
        ).distinct()

    paginator = Paginator(transactions_list, 10)
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)
    start_index = (transactions.number - 1) * paginator.per_page + 1

    context = {
        'transactions': transactions,
        'active': 'transcation',
        'query': query,
    }

    return render(request, 'content/transcations.html', context)
def delete_transactions_view(request):
    if request.method == "POST":
        transaction_ids = request.POST.getlist('transaction_ids')
        TransactionsModel.objects.filter(id__in=transaction_ids).delete()
        return redirect('account_api:transcation')  # Redirect to the transactions view after deletion

def user_view(request):
    user_list = Account.objects.all().order_by('-pk')
    paginator = Paginator(user_list, 10)

    page_number = request.GET.get('page')
    user = paginator.get_page(page_number)
    start_index = (user.number - 1) * paginator.per_page + 1
    context = {
        'users': user,
    }
    return  render(request,template_name='users/users.html',context=context)
