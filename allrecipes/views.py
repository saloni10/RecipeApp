from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from models import Recipe
from models import Image
from models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from forms import ContactForm
from forms import UserForm, UserProfileForm
from forms import SubmitRecipeForm, SubmitRimageForm,LoginForm
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from recipes.settings import DEFAULT_FROM_EMAIL
from django.views.generic import *
from forms import PasswordResetRequestForm,SetPasswordForm
from django.contrib import messages
from django.core.urlresolvers import reverse

# Create your views here.

def index(request):
    return render(request, 'index.html' )

def about(request):
    return render(request, 'about.html' )

def contact(request):
    if request.method == 'POST':
     contact_form=ContactForm(request.POST)
     if contact_form.is_valid():
        cd = contact_form.cleaned_data
        send_mail(
                  cd['user_name'],
                  cd['user_message'],
                  cd.get('user_email', 'noreply@example.com'),['salonibaweja10@gmail.com'],
                  )
    else:
        contact_form=ContactForm()
    return render(request, 'contact.html', {'contact_form':contact_form} )
    
def tips(request):
    return render(request, 'tips.html' )

def search(request):
    error= False
    if 'recipe' in request.GET:
        recipe= request.GET['recipe'].strip()
        if not recipe:
            error= True
        else:
            obj = Image.objects.filter(name__name__icontains=recipe)
            return render(request, 'search_recipe.html', {'obj':obj,'title': recipe} )
    return render(request, 'search_recipe.html', {'error':error}
     )
     
def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(request.POST,request.FILES)
       # p = UserProfileForm(data=request.FILES)
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():# and p.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
               # p.picture = request.FILES['picture']
               # p.save()
               profile.picture = request.FILES['picture']
            # Now we save the UserProfile model instance.
            profile.save()
                
            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'registration.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        login_form = LoginForm(data=request.POST)
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/recipes/submission/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print login_form.errors
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        login_form=LoginForm()
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {'login_form':login_form}, context)
        
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
    
# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/recipes/index')
    
@login_required    
def profile(request):
    changed=""
    username=request.user.username
    fname=request.user.first_name
    lname=request.user.last_name
    email=request.user.email
    obj = User.objects.get(username=request.user.username)
    obj1 = UserProfile.objects.get(user=obj)
    if 'changed' in request.GET : 
        changed = request.GET['changed']
    return render_to_response('profile.html', { 'username':username, 'fname':fname,'lname':lname,'email':email,'obj1':obj1,'changed':changed})
    
@login_required  
def changepwd(request):
    return render(request,'changepwdform.html')
    
@login_required   
def changepassword(request):
    changed= ""
    user = auth.models.User.objects.get(username=request.user.username)
    opwd=request.POST['opwd']
    pwd=request.POST['npwd']
    if request.user.check_password(opwd):
        user.set_password(pwd)
        user.save()
        auth.login(request, auth.authenticate(username=request.user.username, password=pwd))
        return redirect('/recipes/profile/?changed=ok') 
    else:
        #return redirect('/forum/changepwd/?changed=wr')
        changed = "wrong"
        return render(request,'changepwdform.html',{'changed':changed})
        
        
@login_required       
def submit(request):
    recipe_form = SubmitRecipeForm()
    image_form = SubmitRimageForm()
    submitted = False
    if request.method == 'POST':
        name = request.POST.get('name')
        steps=request.POST.get('steps')
        ingredients=request.POST.get('ingredients')                    
         
        image= request.POST.get('image')
        obj= Recipe(name=name,steps=steps,ingredients=ingredients)
        obj.save()
        obj1 = Image(name=obj,image=image)
        obj1.save()
        submitted = True
    return render(request, 'submit-form.html', {'recipe_form':recipe_form,'image_form':image_form,'submitted':submitted } )
   
def success(request):
    
    return render(request,'success.html')
    """
     if request.method == 'POST':
        recipe_form = SubmitRecipeForm(data=request.POST)
        image_form = SubmitRimageForm(data=request.POST)
        if recipe_form.is_valid() and image_form.is_valid():
            recipe = recipe_form.save()
          
      return render_to_response('submit-form.html', {'recipe_form':recipe_form, 'image_form':image_form })
    """


def cust_password_reset(request):
    """Used django.contrib.auth.views.password_reset view method for  forgotten password on Customer UI. This  method will send an e-mail to user's email-id which is entered in password_reset_form"""
    #path = reverse('cust_password_reset_done')
    if not request.user.is_authenticated():
        return password_reset(request,  template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        post_reset_redirect='/recipes/password_reset/done/',   from_email='recipes@localhost.com')
    else:
        return HttpResponseRedirect("/")
        
        
def cust_password_reset_done(request):
    """This will show acknowledge message to user who is seeking to reset his/her password."""
    if not request.user.is_authenticated():
        return password_reset_done(request,  template_name='registration/password_reset_done.html')
    else:
        return HttpResponseRedirect("/")        
        
def cust_password_reset_confirm(request, uidb36, token):
    """ This will allow user to reset his/her password for the system"""
    if not request.user.is_authenticated():
        return password_reset_confirm(request, uidb36=uidb36, token=token,
        template_name='registration/password_reset_confirm.html',
        post_reset_redirect='/recipes/reset/done/')
    else:
        return HttpResponseRedirect("/")  
        
def cust_password_reset_complete(request):
    """This will show acknowledge message to user after successfully resetting his/her password for the system."""
    if not request.user.is_authenticated():
        return password_reset_complete(request,
        template_name='registration/password_reset_complete.html')
    else:
        return HttpResponseRedirect("/")

class ResetPasswordRequestView(FormView):
    template_name = "registration/test_template.html"    #code for template is given below the view's code
    success_url = '/recipes/login'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        '''
        This method here validates the if the input is an email address or not. Its return type is boolean, True if the input is a email address or False if its not.
        '''
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        '''
        A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm). 
        '''
        form = self.form_class(request.POST)
        if form.is_valid():
            data= form.cleaned_data["email_or_username"]
        if self.validate_email_address(data) is True:                 #uses the method written above
            '''
            If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
            '''
          
            associated_users= User.objects.filter(email= data)
            if associated_users.exists():
                for user in associated_users:
                        c = {
                            'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'your site',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user.username,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                            }
                        subject_template_name='registration/password_reset_subject.txt' 
                        # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                        email_template_name='registration/password_reset_email.html'    
                        # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                        subject = loader.render_to_string(subject_template_name, c)
                        # Email subject *must not* contain newlines
                        subject = ''.join(subject.splitlines())
                        email = loader.render_to_string(email_template_name, c)
                        send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'An email has been sent to ' + data +". Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'No user is associated with this email address')
            return result
        else:
            '''
            If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
            '''
            associated_users= User.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': 'myjita.info',
                        'site_name': 'myjita',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                        }
                    subject_template_name='registration/password_reset_subject.txt'
                    email_template_name='registration/password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request, 'Email has been sent to ' + data +"'s email address. Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'This username does not exist in the system.')
            return result
        messages.error(request, 'Invalid Input')
        return self.form_invalid(form)    
        
        
class PasswordResetConfirmView(FormView):
    template_name = "registration/test_template.html"
    success_url = '/recipes/login'
    form_class = SetPasswordForm

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
    
        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password= form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request,'The reset password link is no longer valid.')
            return self.form_invalid(form)          
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
