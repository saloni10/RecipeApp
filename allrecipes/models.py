from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.

class Recipe(models.Model):
    name=models.CharField(max_length=100)
    chef=models.CharField(max_length=100)
    ingredients=models.CharField(max_length=500)
    steps=models.CharField(max_length=2000)
    def __unicode__(self):
        return unicode(self.name)
     
class Image(models.Model):
    name = models.ForeignKey(Recipe)
    image = models.ImageField(upload_to='.', blank = True)
    def __unicode__(self):
       return self.image.name
       
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='.', blank=True, default='/default_user.jpg')

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
       
class SubmitForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ['chef']
        fields = ('name','ingredients','steps')
        
class ImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = ['name']
        fields = ('image',)
        
        

    

