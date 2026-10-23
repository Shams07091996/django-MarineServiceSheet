from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record
from .forms import AddRecordForm

def home(request):
    records = Record.objects.all()
    
    # Check to see if loggin in
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged In")
            return redirect('home')
        else:
            messages.success(request, "There was an Error Loggin in, Please Try Again ...")
            return redirect('home')
        
    else: 
        return render(request, 'home.html', {'records':records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out ...")
    return redirect('home')

def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look up Records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
       messages.success(request, "You must be Logged in to view that page ...") 
       return redirect('home')
   

def delete_customer(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully ...") 
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to do that ...") 
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()   
                messages.success(request, "Record Added ...") 
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in ...") 
        return redirect('home') 
    
def update_record(request, pk):
    if request.user.is_authenticated:
        currect_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=currect_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated! ...") 
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "You must be logged in ...")
        return redirect('home') 