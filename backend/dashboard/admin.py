from django.contrib import admin
from .models import ScamPattern

class ScamPatternAdmin(admin.ModelAdmin):
    list_display = ('template_text', 'category', 'normalized_text', 'sighting_count')
    list_editable = ('category', )
    search_fields = ('category', 'template_text', 'sighting_count')

admin.site.register(ScamPattern, ScamPatternAdmin)