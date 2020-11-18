from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Quote, User
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    validation_errors = User.objects.basic_validator(request.POST)
    if len(validation_errors) > 0:
        for key, value in validation_errors.items():
            messages.error(request, value)
        return redirect('/') 
    
    first_name_from_form = request.POST['first_name']
    last_name_from_form = request.POST['last_name']
    email_from_form = request.POST['email']
    password_from_form = request.POST['password']
    
    pw_hash = bcrypt.hashpw(password_from_form.encode(), bcrypt.gensalt()).decode()   
    print(pw_hash)
    
    this_user = User.objects.create(first_name=first_name_from_form,last_name=last_name_from_form, email=email_from_form, password=pw_hash)
    print('this is before request session')
    request.session['id'] = this_user.id
    print(this_user.id)
    return redirect('/quotes')
    
def quotes(request):
    if 'id' not in request.session:
        messages.error(request,'an error message')
        return redirect('/')
    context = {
        'all_the_quotes' : Quote.objects.all(),
        'all_the_users' : User.objects.all(),
        'username' : User.objects.filter(id=request.session['id'])[0]
    }
    # print(context)
    return render(request, 'quotes.html' , context) 

def add_quote(request):
    validation_errors = User.objects.quote_validator(request.POST)
    if len(validation_errors) > 0:
        for key, value in validation_errors.items():
            messages.error(request, value)
        return redirect('/quotes')   
    
    author_from_form = request.POST['author']
    desc_from_form = request.POST['desc']
    
    this_user = User.objects.get(id=request.session['id'])
    print(this_user)
    this_quote = Quote.objects.create(author=author_from_form, desc=desc_from_form, posted_by=this_user)
    this_quote.liked_quotes.add(this_user) 
    
    print(Quote.objects.all())
    return redirect("/quotes")


def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if len(user) == 0:
        messages.error(request, 'user not found')
        return redirect('/')
    elif len(user) != 0:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['id'] = logged_user.id #'id' is key name
            return redirect('/quotes')                    
        else: 
            messages.error(request, 'login/pw error')
        return redirect('/')                   
    else:
        messages.error(request, 'login error')
        return redirect('/')

def logout(request):
    if 'id' not in request.session:
        messages.error(request,'error: please login')
        return redirect('/')
    else:
        request.session.clear()
        return redirect("/") 
    
def delete_quote(request, quote_id):
    quote_to_delete = Quote.objects.get(id=quote_id)
    quote_to_delete.delete()
    return redirect('/quotes')   

def user(request, username_id):
    all_the_quotes = Quote.objects.all()
    
    # if request.session['id'] == quote_uploade
    # user_to_get = User.objects.get(id=username_id)
    # user_to_get.liked_quotes.all()
    this_user = User.objects.get(id=request.session['id'])
    all_users = User.objects.all()    
    all_quotes = Quote.objects.all()
    
    # the_quotes = Quote.objects.get(id=id)
    # the_quotes_posted_by = the_quotes.posted_by_id
    context = {
        'user' : this_user,
        'all_quotes' : all_quotes,
        'username' : User.objects.filter(id=request.session['id'])[0],
        'uploaded_by' : User.objects.first().quotes_uploaded.all(), 
        'usertoshow' : User.objects.get(id=username_id),
        
        # 'the_quotes' : the_quotes,
        # 'posted_by' : the_quotes_posted_by,
        # 'users_who_posted' : User.objects.first().quotes_uploaded.all(),
        
         
    }
    return render(request, 'showuser.html', context)

def showuser(request, quote_posted_by_id):
    return render(request, 'showuser.html', context)
    

def account(request, username_id):
    context = {
        'all_the_quotes' : Quote.objects.all(),
        'username' : User.objects.filter(id=request.session['id'])[0]
    }
    return render(request, 'account.html', context)
    
def account_edit(request, username_id):
    validation_errors = User.objects.account_validator(request.POST)
    if len(validation_errors) > 0:
        for key, value in validation_errors.items():
            messages.error(request, value)
        return redirect(f'/account/{username_id}')
    
    user_to_edit = User.objects.get(id=username_id)
    user_to_edit.first_name = request.POST['first_name']
    user_to_edit.last_name = request.POST['last_name']
    user_to_edit.email = request.POST['email']
    user_to_edit.save()
    return redirect(f'/account/{username_id}')
    
    
# Create your views here.
