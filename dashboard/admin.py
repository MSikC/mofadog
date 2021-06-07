from django.contrib import admin
from .models import Order, Node, Question, Notice
# Register your models here.
admin.site.register(Order)
admin.site.register(Node)
admin.site.register(Question)
admin.site.register(Notice)