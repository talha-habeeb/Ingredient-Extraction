from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.http import require_http_methods
import re
from django.contrib import messages




@login_required(login_url='login')
def HomePage(request):
    return render (request,'home.html')



def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if not (uname and email and pass1 and pass2):
            messages.error(request, "Please fill in all fields.")
            return render(request, 'signup.html', {'username': uname, 'email': email})

            #return HttpResponse("Please fill in all fields.")

        if pass1!=pass2:
            messages.error(request, "Your password and confirm password are not the same!!")
            return render(request, 'signup.html', {'username': uname, 'email': email})
            #return HttpResponse("Your password and confirm password are not Same!!")
        

        my_user=User.objects.create_user(uname,email,pass1)
        my_user.save()
        return redirect('login')
    return render (request,'signup.html')


def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')


@require_http_methods(["POST", "GET"])
def extract_ingredients(request):
    if request.method == "POST":
        # Extract the recipe text 
        recipe_text = request.POST.get('recipe_text', '').strip()
        if not recipe_text:
            # when no text is entered
            return render(request, 'results.html', {'error': 'No text was entered.'})
        # ingredient extract
        pattern = r'(\d+\/\d+|\d+\.?\d*)\s?(cups?|teaspoons?|tablespoons?|tbsps?|tsps?|grams?|ounces?|oz|pounds?|lbs?|kilograms?|kgs?|liters?|l|mls?|milliliters?|pinch(es)?|to taste)?\s([a-zA-Z ]+)(?=(,|\.|\n|$|\d))'
        ingredients = re.findall(pattern, recipe_text)
        if not ingredients:
            #  when no ingredients are found
            return render(request, 'results.html', {'error': 'No ingredients were found.'})
        
        

        # Render the results to an HTML page
        return render(request, 'results.html', {'ingredients': ingredients})
    # For GET request render the form
    return render(request, 'ingredient_form.html')

