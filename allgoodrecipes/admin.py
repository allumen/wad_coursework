from django.contrib import admin
from allgoodrecipes.models import Recipe, Tip, UserProfile, Comment, Ingredient, Unit, RecipeCategory

# Register your models here.
# Register your models here.
#class CategoryAdmin(admin.ModelAdmin):
#    prepopulated_fields = {'slug': ('name',)}

#class PageAdmin(admin.ModelAdmin):
#    list_display = ('title', 'category', 'url')

#admin.site.register(Category, CategoryAdmin)

class IngredientInline(admin.TabularInline):
    model = Ingredient
    
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientInline,
    ]
    
    exclude = ('url_chosen',)

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tip)
admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Unit)
admin.site.register(RecipeCategory)