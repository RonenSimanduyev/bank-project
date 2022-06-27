from django.urls import path
from . import views

urlpatterns=[
    path('',views.home, name='home'),
    path('transaction',views.transaction ,name='transaction'),
    path('transfers',views.transfers ,name='transfers'),
    path('withdraw',views.withdraw , name='withdraw'),
    path('login',views.login_user, name='login'),
    path('logout',views.logout_user, name='logout'),
    path('sighnup',views.sighnup_user , name='sighnup'),
    
]