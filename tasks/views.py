from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django.db.models import Count
from tasks import helper
import pandas as pd
from tasks.models import Data
from tasks.models import Credit
from datetime import datetime
from django.core.paginator import Paginator
import io
from django.contrib.auth.decorators import login_required

from django.contrib.auth import update_session_auth_hash



# Create a custom form for user signup that includes an email field
class SignupForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# Create a custom form for user login that includes fields for username and password
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())



#View to render a main "index.html" page
def helloword(request):
    
    title = User.objects.get(pk=1)
    return render(request, 'index.html', {
        'user': request.user
    })


@login_required
def profile(request):
    user = request.user
    
    if request.method == 'POST':
        old_password = request.POST.get('oldpassword')
        new_password1 = request.POST.get('password')
        new_password2 = request.POST.get('password2')
        
        # Verify if the password if correct
        if not user.check_password(old_password):
            return render(request, 'dashboard/profile.html', {
            'user': user,
            'credit': helper.value_credits(request),
            'error': 'The current password is incorrect '
        })
        # Verify if the password match
        elif new_password1 != new_password2:
            return render(request, 'dashboard/profile.html', {
            'user': user,
            'credit': helper.value_credits(request),
            'error': 'The password news no match '
        })
        else:
            # update the password
            user.set_password(new_password1)
            user.save()
            
            # Authenticate the user with the new password
            new_user = authenticate(username=user.username, password=new_password1)
            if new_user:
                login(request, new_user)
            
            # Redirigir al usuario a la página de perfil
            return render(request, 'dashboard/profile.html', {
            'user': user,
            'credit': helper.value_credits(request),
            'success': 'The password was change successfully'
        })
    
    return render(request, 'dashboard/profile.html', {
        'user': user,
        'credit': helper.value_credits(request),
    })



# View for the dashboard page
@login_required
def dashboard(request):
    if request.method == 'POST': #Verify if the user delete all the data
        number_user = User.objects.count()
        search_count = Data.objects.values('search').filter(user=request.user).distinct().count()
        data_count = Data.objects.filter(user=request.user).count()
        user = User.objects.get(username=request.user)
        credit = Credit.objects.get(user=user)
        Data.objects.filter(user=request.user).delete()
        return render(request, 'dashboard/index.html', {
        'user': request.user,
        'id': number_user,
        'search': search_count,
        'data': data_count,
        'credit': credit.value,
        'delete': 'Data deletion was successful'
        
    })
    else:
        number_user = User.objects.count()
        search_count = Data.objects.values('search').filter(user=request.user).distinct().count()
        data_count = Data.objects.filter(user=request.user).count()
        user = User.objects.get(username=request.user)
        credit = Credit.objects.get(user=user)
        return render(request, 'dashboard/index.html', {
            'user': request.user,
            'id': number_user,
            'search': search_count,
            'data': data_count,
            'credit': credit.value,
            
        })
# View for the data page
@login_required
def data(request):
    if request.method == 'GET':
        # Get a list of unique values in the "search" field of the "Data" model, along with the number of times each value appears.
        search = Data.objects.values('search').annotate(Count('search')).order_by('-search__count')
        data = Data.objects.filter(user=request.user)
        paginator = Paginator(data, 10)  # Show 10 items per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        # Render the "data.html" template, passing in the logged-in user and the search data for that user.
        return render(request, 'dashboard/data.html', {
            'user': request.user,
            'search': search.filter(user=request.user),
            'data': page_obj,
            'pagination': True,
            'credit': helper.value_credits(request),
        })
    else:
    # Get a list of unique values in the "search" field of the "Data" model, along with the number of times each value appears.
        search = Data.objects.values('search').annotate(Count('search')).order_by('-search__count')
        data = Data.objects.filter(user=request.user, search=request.POST['request'].split(",")[0])
        # Render the "data.html" template, passing in the logged-in user and the search data for that user.
        return render(request, 'dashboard/data.html', {
            'user': request.user,
            'search': search.filter(user=request.user),
            'data': data,
            'pagination': False,
            'credit': helper.value_credits(request),
        })

@login_required
def download_all_data(request):
    # Obtener todos los datos del modelo
    data = Data.objects.filter(user=request.user)

    # Crear un objeto DataFrame
    df = pd.DataFrame(list(data.values()))

    # Crear un archivo CSV en memoria
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)

    # Configurar la respuesta HTTP
    response = HttpResponse(buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="my_data.csv"'

    return response

@login_required
def improve(request):
    if request.method == 'GET':
        # Get a list of unique values in the "search" field of the "Data" model, along with the number of times each value appears.
        title = Data.objects.values('title').filter(user=request.user)
        # Render the "data.html" template, passing in the logged-in user and the search data for that user.
        return render(request, 'dashboard/improve.html', {
            'user': request.user,
            'title': title,
            'show': False,
            'credit': helper.value_credits(request),
        })
    else:
        credit = helper.value_credits(request)
        if credit >= 5: # The user must to have 5 credits
        # Get a list of unique values in the "search" field of the "Data" model, along with the number of times each value appears.
            title = Data.objects.values('title').filter(user=request.user)
            old_title = str(request.POST['title'])
            new_title = helper.title_improve(old_title)
            new_credits = helper.value_credits(request, 5) # we subtract the credits
            # Render the "data.html" template, passing in the logged-in user and the search data for that user.
            return render(request, 'dashboard/improve.html', {
                'user': request.user,
                'title': title,
                'new_title': new_title,
                'old_title': old_title,
                'show': True,
                'credit': new_credits,
            })
        else:
                        return render(request, 'dashboard/improve.html', {
                'user': request.user,
                'error': "You don't have enough credits",
                'show': False,
                'credit': helper.value_credits(request),
            })



#View for the analytics page
@login_required
def analytics(request):
    # If the request method is GET, render the "analytics.html" template, passing in the logged-in user.
    if request.method == 'GET':
        return render(request, 'dashboard/analytics.html', {
            'user': request.user,
            'credit': helper.value_credits(request),

        })
    # If the request method is not GET, process the search results and store them in the database.
    else:
        # Get the logged-in user and process the search results submitted by the user.
            user = request.user
            # Extract public information of youtube
            data = helper.process_results(request.POST['search'], int(request.POST['number']))
            # Convert the search results to a Pandas dataframe.
            df = pd.DataFrame.from_dict(data, orient='index')
            # Define a date format string for parsing the "Upload Date" field.
            date_format = "%Y-%m-%d"
            # Loop over the search results and convert the data to database compatible
            for i in range(len(data)):
                try:
                    date_object = datetime.strptime(data[i]['Upload Date'], date_format)
                    views = data[i]['Channel Total Views'].replace(" views", "").replace(',', '')
                    keywords_tags = data[i]['Keywords Tags']
                    if keywords_tags:
                        keywords_tags = ', '.join([x for x in keywords_tags if x])
                    else:
                        keywords_tags = 'Nothing'
                    # Create a new "Data" object with the extracted information and save it to the database but first verify if the object already exist 
                    if Data.objects.filter(user=user, link=data[i]['Link']).exists():
                        pass
                    else:
                        Data.objects.create(
                            title=data[i]['Title'],
                            search=data[i]['Search'],
                            link=data[i]['Link'],
                            thumbnail=data[i]['Thumbnail'],
                            view_count=int(data[i]['View Count:']),
                            keywords_tags=keywords_tags,
                            duration_seconds=int(data[i]['Duration Seconds']),
                            upload_date=date_object,
                            published_time=data[i]['published Time'],
                            category=data[i]['Category'],
                            all_video_description=data[i]['All Video Description'],
                            channel=data[i]['Channel'],
                            subscribers=data[i]['Subscribers'],
                            channel_description=data[i]['Channel Description'],
                            keywords_channel=data[i]['Keywords channel'],
                            channel_total_views=int(views),
                            channel_join=data[i]['Channel Join'],
                            country=data[i]['Country'],
                            user=user
                        )
                except (TypeError, KeyError) as error:
                    print("Error:", error)
            # Improve the titles of the videos, count the most common words in the titles and keyword tags,
            # and render the "analytics.html" template with the search data and charts, passing in the logged-in user.
            checkbox = request.POST.get('ai_improve_title', False) # verify if the checkbox is true for return the title
            credit = helper.value_credits(request)
            error = None
            if checkbox == False:
                new, new2 = None, None
            elif credit >= 10: # Verify if the user have the credits
                subtract_credits = helper.value_credits(request, 10) # we subtract the credits
                new, new2 = helper.improve_title(df)
            else:
                error = "You don't have enough credits"
                new, new2 = None, None
            #Count The words for de charts
            dictionary = helper.count_words(list(df['Title'].values))
            dictionary2 = helper.count_words2(list(df['Keywords Tags'].values))
            return render(request, 'dashboard/analytics.html', {
                'user': user,
                'data': data,
                'chart': helper.chart(df),
                'chart2': helper.chart2(df),
                'chart3': helper.chart3(df, dictionary),
                'chart4': helper.chart3(df, dictionary2),
                'showresult': True,
                'newtitle1': new,
                'newtitle2': new2,
                'checkbox': checkbox,
                'error': error,
                'credit': helper.value_credits(request),
            })





#user signout
def signout(request):
    logout(request)
    return redirect('home')


#View for user signup
def create(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():  # Validate the form
            if request.POST['password1'] == request.POST['password2']:
                if User.objects.filter(username=request.POST['username']).exists():
                    return render(request, 'create.html', {
                        'form': form,
                        'error': 'Username Already exists '
                    })
                if User.objects.filter(email=request.POST['email']).exists():
                    return render(request, 'create.html', {
                        'form': form,
                        'error': 'Email Already exists '
                    })
                try:
                    user = User.objects.create_user(
                        username=request.POST['username'],
                        first_name=request.POST['fname'],
                        email=request.POST['email'],
                        password=request.POST['password1'])
                    user.save()
                    credit = Credit(user=user, value=1000)
                    credit.save()
                    login(request, user)
                    return redirect('/dashboard/')
                except IntegrityError:
                    return render(request, 'create.html', {
                        'form': form,
                        'error': 'Username or email Already exists '
                    })
            else:
                return render(request, 'create.html', {
                    'form': form,
                    'error': 'Password no match '
                })
        else:
            # Retrieve form errors and display them in the template.
            errors = form.errors.as_data()
            error_messages = []
            for field, errors in errors.items():
                for error in errors:
                    error_messages.append(error.message)
            return render(request, 'create.html', {
                'form': form,
                'error': error_messages[0]
            })
    else:
        #Verify if the user already is authenticated if is true redirect to dashboard
        if request.user.is_authenticated:
            return redirect("/dashboard/")
        form = SignupForm()
        return render(request, 'create.html', {
            'form': form
        })




def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Validate and authenticate the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Verify reCAPTCHA
                recaptcha_response = request.POST.get('g-recaptcha-response')
                if not recaptcha_response:
                    error = 'Please complete the reCAPTCHA challenge.'
                    return render(request, 'login.html', {'form': form, 'error': error})
                else:
                    # Validate reCAPTCHA response with `captcha` package
                    captcha = form.cleaned_data['captcha']
                    if not captcha:
                        error = 'reCAPTCHA validation failed. Please try again.'
                        return render(request, 'login.html', {'form': form, 'error': error})
                    else:
                        # Log the user in and redirect them to the homepage
                        login(request, user)
                        return redirect('/dashboard/')
            else:
                # Return an error message
                error = 'Invalid login credentials. Please try again.'
                return render(request, 'login.html', {'form': form, 'error': error})
    else:
        # Verify if the user already is authenticated if is true redirect to dashboard
        if request.user.is_authenticated:
            return redirect("/dashboard/")
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
