from django.contrib import admin
from .models import Note



# Register your models here.
class myModelAdmin(admin.ModelAdmin):
    list_display = ['image_tag','title', 'short_content', 'created_at', 'updated_at', 'status', 'user']
    search_fields = ['title',"user__username",]
    list_filter = ['status', 'user']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}

    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    short_content.short_description = "Content"






admin.site.register(Note, myModelAdmin)