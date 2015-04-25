from django import forms
from django.contrib import admin
from models import Recipe
from models import Image
from models import UserProfile
# Register your models here.

class RecipeModelForm( forms.ModelForm ):
    ingredients = forms.CharField( widget=forms.Textarea )
    steps = forms.CharField( widget=forms.Textarea )
    class Meta:
        model = Recipe
       
class InlineImage(admin.TabularInline):
    model = Image

class RecipeAdmin(admin.ModelAdmin):
    form = RecipeModelForm
    list_display= ('name', 'chef')
    inlines = [InlineImage]
    
admin.site.register(Recipe, RecipeAdmin)
