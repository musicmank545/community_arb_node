from django.contrib import admin
from .models import Node

# Register your models here.
class NodeAdmin(admin.ModelAdmin):
    model = Node
    list_display = ("name","address","port","currentBlockHeight","healthy","default")
    list_filter = ("name","address","port","currentBlockHeight","healthy","default")
    
admin.site.register(Node, NodeAdmin)