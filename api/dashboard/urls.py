from django.urls import  path


from api.dashboard import views
from api.dashboard.modules.permissions import create_permission
from api.dashboard.modules.users import user_page, user_permissions, user_view as user_profile, user_delete, edit_user
from api.dashboard.views import  *
from api.dashboard.modules.identification import idenfication_view, identification_detail

urlpatterns = [
    path('home_page/', index, name='index'),
    path('',login_view,name='login'),
    path('transaction/view/',transcation_view,name='transcation'),
    path('transaction/delete',delete_transactions_view,name = 'transaction_delete'),
    path('user/all/',user_view,name='users'),
    path('idenfications/user',idenfication_view,name='idencations'),
    path('idenfications/<int:pk>',identification_detail,name='idencation_detail'),
    path('user/page/',user_page,name='user_page'),
    path('user/role/<int:user_id>/',user_permissions,name='user_role'),
    path('permission/create',create_permission,name='manage_permissions'),
    path('user/profile/<int:user_id>/',user_profile,name='user_profile'),
    path('user/delete/<int:user_id>',user_delete,name='user_delete'),
    path('user/edit/<int:user_id>',edit_user,name='edit_user'),


]