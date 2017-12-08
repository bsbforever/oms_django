from django.contrib import admin

# Register your models here.

from monitor.models import oraclelist
from monitor.models import oraclestatus
from monitor.models import oracle_buffergets
from monitor.models import oracle_diskreads
from monitor.models import oracle_elapsedtime
from monitor.models import oracle_cputime
from monitor.models import oracle_topevent
from monitor.models import linuxlist


admin.site.register(oraclelist)
admin.site.register(oraclestatus)
admin.site.register(oracle_buffergets)
admin.site.register(oracle_diskreads)
admin.site.register(oracle_elapsedtime)
admin.site.register(oracle_cputime)
admin.site.register(oracle_topevent)
admin.site.register(linuxlist)
