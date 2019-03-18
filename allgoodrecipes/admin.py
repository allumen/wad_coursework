from django.contrib import admin
from allgoodrecipes.models import Recipe, Tip, UserProfile, Comment

# Register your models here.
# Register your models here.
#class CategoryAdmin(admin.ModelAdmin):
#    prepopulated_fields = {'slug': ('name',)}

#class PageAdmin(admin.ModelAdmin):
#    list_display = ('title', 'category', 'url')

#admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe)
admin.site.register(Tip)
admin.site.register(UserProfile)
admin.site.register(Comment)