from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('landing/',views.landing,name='landing'),
    path('logout',views.logout,name='logout'),
    path('change_pin',views.change_pin,name='change_pin'),
    path('check_balance/<str:username>/',views.check_balance,name='check_balance'),
    path('deposit',views.deposit,name="deposit"),
    path('success',views.success,name="success"),
    path('withdraw',views.withdraw,name="withdraw"),
    path('transactions/<str:username>/',views.transactions,name="transactions"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('transfer',views.transfer,name="transfer")
]