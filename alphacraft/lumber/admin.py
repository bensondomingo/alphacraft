from django.contrib import admin

from .models import Log, Lumber, PurchaseItem, PurchaseOrder, Supplier

admin.site.register(Log)
admin.site.register(Lumber)
admin.site.register(Supplier)
admin.site.register(PurchaseItem)
admin.site.register(PurchaseOrder)
