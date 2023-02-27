from django.shortcuts import HttpResponseRedirect, render
from .models import users


def check(request):
    if request.session["user_info"].get("name") == '':
        return HttpResponseRedirect('/log-in')
    return None

def updateDict(thing:dict,changes:dict):
    CopyOfThing = thing
    CopyOfThing.update(changes)
    return CopyOfThing


# Create your views here.
a = [1,1,1,1,1,1,1,1,1,1,1,1,1]
def home(request):
    if "user_info" not in request.session:
        request.session["user_info"] = dict({
            'name' : '',
            'email' : '',
        })

    response = render(request, "YWS2/home.html", {
        'user' : request.session['user_info'],
        'a' : a,
    })
    return response

def log_in(request):
    response = render(request, "YWS2/log-in.html", {
        'user' : request.session['user_info'],
    })
    if not request.method == "POST":
        return response
    
    item = request.POST
    test = users.objects.filter(email=item['email'])
    if test.exists():
        test = users.objects.get(email=item['email'])
        if item['password'] == test.password:
            request.session['user_info'] = updateDict(request.session['user_info'],{
                'name' : test.name,
                'email' : test.email,
            })
            return HttpResponseRedirect('/')
    

    response = render(request, "YWS2/log-in.html", {
        'user' : request.session['user_info'],
        'massage' : 'incorrect email or password',
    })
    return response

def sign_in(request):
    response = render(request, "YWS2/sign-in.html", {
        'user' : request.session['user_info'],
    })
    if not request.method == "POST":
        return response
    
    item = request.POST
    test = users.objects.filter(email=item['email'])
    if test.exists():
        return render(request, "YWS2/sign-in.html", {
        'user' : request.session['user_info'],
        'massage' : 'this email already in use',
    })

    users(name=item['userName'], email=item['email'], password=item['password'], authorised=0).save()
    request.session['user_info'] = updateDict(request.session['user_info'],{
        'name' : item['userName'],
        'email' : item['email'],
    })
    response = HttpResponseRedirect('/')
    return response

def log_out(request):
    request.session['user_info'] = updateDict(request.session['user_info'],{
        'name' : '',
        'email' : '',
    })
    return HttpResponseRedirect('/')

def setting(request):
    if check(request) != None :
        return check(request)
    
    response = render(request, "YWS2/setting.html", {
        'user' : request.session['user_info'],
    })
    return response

