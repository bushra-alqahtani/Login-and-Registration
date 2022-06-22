from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Users
import bcrypt



# Create your views here.

def index(request):
    return render(request,"index.html")


def register(request):
    if request.method == "POST":
    #check for errors
        errors=Users.objects.validatorRe(request.POST)
        if len(errors) > 0:
            for key ,value in errors.items():
                messages.error(request,value)
            return redirect("/") # idf ther is any error redirect me to the registeraion forms page
        
        else:
            First_Name=request.POST['First_Name']
            Last_Name=request.POST['Last_Name']
            Email=request.POST['Email']
            Password=request.POST['Password']
            #use "bcrypt" to hash password
            pwHash=bcrypt.hashpw(Password.encode(),bcrypt.gensalt()).decode()

            #create user 
            newUser =Users.objects.create(First_Name=First_Name,Last_Name=Last_Name,Email=Email,Password=pwHash)
            newUser.save()

            #(save user id in session to access to user ) 
            request.session['loginID']=newUser.id
        return redirect("/success")
    else:
        return redirect('/')


def login(request):
    if request.method == "POST":
        #check for errors 
        errors=Users.objects.validatorLo(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect("/")
        #fetching for the id to redirect user to success page.
        request.session['loginID'] = Users.objects.get(Email=request.POST['Email']).id
        return redirect('/success')


def success(request):
    try:
        id = request.session['loginID']   
    except:
        messages.error(request, "Need to login first")
        return render(request,'success.html')
    context={
       'loginUser':Users.objects.get(id=request.session['loginID'])
    }
    return render(request,"success.html",context)


def logout (request):
    del request.session['loginID']
    return redirect('/')

