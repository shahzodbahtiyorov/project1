from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django import forms

from apps.accounts.models import Account


@user_passes_test(lambda u: u.is_superuser)
def create_permission(request):
    class ContentTypeForm(forms.ModelForm):
        class Meta:
            model = ContentType
            fields = ['model']  # content_type ni yaratish uchun

    class PermissionForm(forms.ModelForm):
        class Meta:
            model = Permission
            fields = ['name', 'codename']

    if request.method == 'POST':
        # ContentType yaratish
        content_type_name = request.POST.get('content_type_name')
        if content_type_name:
            content_type = ContentType.objects.create(
                app_label='super_app',
                model=content_type_name.lower()
            )


            permission_name = request.POST.get('name')
            permission_codename = request.POST.get('codename')

            if permission_name and permission_codename:
                Permission.objects.create(
                    name=permission_name,
                    codename=permission_codename,
                    content_type=content_type
                )
                return redirect('account_api:user_page')


    user_content_type = ContentType.objects.get_for_model(Account)

    context = {
        'content_type_form': ContentTypeForm(),
        'permission_form': PermissionForm(),
    }
    return render(request, 'users/permisssions_create.html', context)