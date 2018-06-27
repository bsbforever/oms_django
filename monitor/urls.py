from django.conf.urls import  url, include
from monitor import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^oracle_command/$',views.oracle_command, name='oracle_command'),
    url(r'^commandresult/$',views.commandresult, name='commandresult'),
    url(r'^oracle_status$',views.oracle_status, name='oracle_status'),
    url(r'^oracle_performance$',views.oracle_performance, name='oracle_performance'),
    url(r'^performance$',views.performance, name='performance'),
    url(r'^cpumem_day$',views.cpumem_day, name='cpumem_day'),
    url(r'^oracle_topevent$',views.oracle_topevent, name='oracle_topevent'),
    url(r'^check_topsql$',views.check_topsql, name='check_topsql'),
    url(r'^addbaseline$',views.addbaseline, name='addbaseline'),
    url(r'^check_hitratio$',views.check_hitratio, name='check_hitratio'),
    url(r'^linux_list$',views.linux_list, name='linux_list'),
]
