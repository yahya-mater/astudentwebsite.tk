from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse
from .models import workers,users
from .models import orders
import datetime
import json
# Create your views here.


#fun for internal use
def CheckIfLoged(request):
    if request.session["user_info"] == {
            'name' : '',
            'gmail' : '',
            'password' : ''
        }:
        return HttpResponseRedirect('/login')
    
    return None

def ConCh(thing:dict,changes:dict):
    CopyOfThing = thing
    CopyOfThing.update(changes)
    return CopyOfThing



#fun for external use

#main page
def home_views(request):
    if "user_info" not in request.session:
        request.session["user_info"] = dict({
            'name' : '',
            'gmail' : '',
            'password' : '',
            'mainColor' : '',
            'subColor' : ''
        })
    
    response = render(request, "YWS1/home.html", {
        "user_info": request.session["user_info"]
    })
    
    
    #if "user_colors" in request.COOKIES:
     #   cookie_dict:dict = json.loads(request.COOKIES['user_colors'])
      #  request.session["user_info"] = ConCh(request.session["user_info"],{
       #         'mainColor' : cookie_dict.get("mainColor"),
        #        'subColor' : cookie_dict.get("subColor")
         #   })

    
    #if form is not right or the user is not loged-in then do this VVVV
    return response

class add_order(forms.Form):
    order_name = forms.CharField(max_length=64, label="", widget=forms.TextInput(attrs={
        "placeholder" : "order name",
        "type" : "text",
    }))


#sub pages
def sub1(request):
    return render(request, "YWS1/sub1.html", {
        "user_info" : request.session["user_info"],
        "workers": workers.objects.all()
    })

def sub2(request):
    if request.method == "POST":
        form = add_worker(request.POST)
        if form.is_valid():
            Name = form.cleaned_data["name"]
            Age = form.cleaned_data["age"]
            workers(name=Name,age=Age).save()
        else:
            return render(request, "YWS1/sub2.html", {
                "form": form,
                "user_info" : request.session["user_info"]
            })
    return render(request, "YWS1/sub2.html", {
        "form": add_worker(),
        "user_info" : request.session["user_info"]
    })
class add_worker(forms.Form):
    name = forms.CharField(max_length=64,label="worker name")
    age = forms.IntegerField(max_value=99,min_value=0,label="worker age")


def login(request):
    #if method is not POST then do this VVVV
    if not request.method == "POST":
        return render(request, "YWS1/login.html", {
        "form": login_user(),
        "user_info" : request.session["user_info"],
        "massage": ""
        })
    
    form = login_user(request.POST)
    #if form not valid then do this VVVV
    if not form.is_valid():
        return render(request, "YWS1/login.html", {
            "form": form,
            "user_info" : request.session["user_info"],
            "massage": ""
        })
    
    filter_test = users.objects.filter(user_gmail = form.cleaned_data["UserGmail"])
    #if account exists then do this VVVV
    if filter_test.exists():
        get_test = users.objects.get(user_gmail = form.cleaned_data["UserGmail"])
        if get_test.user_password == form.cleaned_data["UserPassword"]:
            #change user name + redirect to home
            #if "user_colors" in request.COOKIES:
            #    Mcolor = json.loads(request.COOKIES['user_colors']).get("mainColor")
            #    Scolor = json.loads(request.COOKIES['user_colors']).get("mainColor")
            #else:
            #    Mcolor = Scolor = ''
            request.session["user_info"] = ConCh(request.session["user_info"],{
                'name' : get_test.user_name,
                'gmail' : get_test.user_gmail,
                'password' : get_test.user_password,
                'mainColor' : '',
                'subColor' : ''
            })

            respones = HttpResponseRedirect("/")
            respones.set_cookie("cookie", "some cookies")
            return respones

    #if the account does not exists then do this VVVV
    return render(request, "YWS1/login.html", {
                "form": form,
                "user_info" : request.session["user_info"],
                "massage": "incorrcet email or password"
            })

class login_user(forms.Form):
    UserGmail = forms.EmailField(max_length=64, label="", widget=forms.TextInput(attrs={
        "placeholder" : "user gmail",
        "type" : "email"
    }))
    UserPassword = forms.CharField(max_length=64, label="", widget=forms.TextInput(attrs={
        "placeholder" : "user password",
        "type" : "password"
    }))

def signin(request):
    if request.method == "POST":
        form = signin_user(request.POST)
        if form.is_valid():
            filter_test = users.objects.filter(user_gmail = form.cleaned_data["UserGmail"])
            if filter_test.exists():
                massage = "email already exists"
                return render(request, "YWS1/signin.html", {
                    "massage" : massage,
                    "user_info" : request.session["user_info"],
                    "form" : form
                })
            else:
                massage = ""
                Name = form.cleaned_data["UserName"]
                Gmail = form.cleaned_data["UserGmail"]
                Password = form.cleaned_data["UserPassword"]
                users(user_name=Name,user_gmail=Gmail,user_password=Password).save()
                request.session["user_info"] = ConCh(request.session["user_info"],{
                        'name' : Name,
                        'gmail' : Gmail,
                        'password' : Password,
                })
                return HttpResponseRedirect("/")
        else:
            return render(request, "YWS1/signin.html", {
                    "massage" : "",
                    "user_info" : request.session["user_info"],
                    "form" : form
                })
    else:
        return render(request, "YWS1/signin.html", {
            "massage" : "",
            "user_info" : request.session["user_info"],
            "form" : signin_user()
        })
class signin_user(forms.Form):
    UserName = forms.CharField(max_length=64, label="", widget=forms.TextInput(attrs={
        "placeholder" : "user name",
        "type" : "text"
    }))
    UserGmail = forms.EmailField(max_length=64, label="", widget=forms.TextInput(attrs={
        "placeholder" : "user gmail",
        "type" : "email"
    }))
    UserPassword = forms.CharField(max_length=64, label="", widget=forms.TextInput(attrs={
        "placeholder" : "user password",
        "type" : "password"
    }))


#side bar(setting)
def about(request):
    if CheckIfLoged(request) != None :
        return CheckIfLoged(request)
    
    return render(request, "YWS1/about.html", {
        "user_info" : request.session["user_info"]
    })

def Orders(request):
    if CheckIfLoged(request) != None :
        return CheckIfLoged(request)
    

    filter_orders = orders.objects.filter(user_gmail = request.session["user_info"].get("gmail"))
    
    #if method is not POST then do this VVVV
    if not request.method == "POST":
        return render(request, "YWS1/orders.html", {
            "form": add_order(),
            "user_info" : request.session["user_info"],
            "massage" : "order has been added",
            "orders" : filter_orders
        })
    
    form = add_order(request.POST)
    #if form is right and user loged-in then do this VVVV
    if form.is_valid() and request.session["user_info"].get("name") != '':
            date = datetime.datetime.now()
            orders(user_gmail=request.session["user_info"].get("gmail"),
                   user_order=form.cleaned_data["order_name"],
                   user_order_date_month=date.strftime("%m"),
                   user_order_date_day=date.strftime("%d"),
                   user_order_date_hour=date.strftime("%H")).save()
            

            
            return render(request, "YWS1/orders.html", {
                # i change it from form to the corrent one so that input value is empty 
                "form": add_order(),
                "user_info" : request.session["user_info"],
                "massage" : "order has been added",
                "orders" : filter_orders
            })
    
    #if form is not right or the user is not loged-in then do this VVVV
    return HttpResponseRedirect('/login')

def OrdersDelete(request, id):
  member = orders.objects.get(id=id)
  member.delete()
  return HttpResponseRedirect('/orders')


def logout(request):
    request.session.pop("user_info")
    
    response = HttpResponseRedirect('/')
    response.delete_cookie('cookie')
    return response


def admin(request):
    if CheckIfLoged(request) != None :
        return CheckIfLoged(request)
    
    if not request.session["user_info"].get("gmail") == "admin@gmail.com":
        return HttpResponseRedirect('/')
    


    return render(request,"YWS1/adminPage.html",{
        "users_orders": orders.objects.all(),
        "user_info" : request.session["user_info"],
        "form":add_order(),
        "massage":"",
    })


def test(request):
    return 