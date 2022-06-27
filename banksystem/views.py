from django.shortcuts import redirect, render
from .models import Client,Transaction
from django.db.models import Q
from django.db.models import Sum
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
@login_required(login_url='login')
def home(request):
    income=Transaction.objects.filter(transferTo=request.user.client).aggregate(Sum('amount'))
    expenses = Transaction.objects.filter(transferFrom=request.user.client).aggregate(Sum('amount'))
    try:
        total=income['amount__sum']- expenses['amount__sum']
    except:
        total=0
    transactions=Transaction.objects.filter(
        Q(transferFrom=request.user.client) |
        Q(transferTo=request.user.client)
    ).order_by('-created')
    return render(request,'banksystem/home.html',{"transactions":transactions,"total":total})



@login_required(login_url='login')
def transaction(request):
    return render(request,'banksystem/transaction.html')



@login_required(login_url='login')
def transfers(request):
    clients=Client.objects.all
    if request.method == 'POST':
        transferTo=Client.objects.get(id =request.POST['transferTo'])
        Transaction.objects.create(
            transferFrom=request.user.client,
            transferTo=transferTo,
            amount=request.POST['amount'],
            title=request.POST['title']

        )
        return redirect ('home')
    return render(request,'banksystem/transfers.html',{"clients":clients})


@login_required(login_url='login')
def withdraw(request):
    if request.method == 'POST':
        Transaction.objects.create(
            transferFrom=request.user.client,
            transferTo=None,
            amount=request.POST['amount'],
            title='ATM withdraw'
        )
        return redirect ('home')
    return render(request,'banksystem/withdraw.html')



def login_user(request):
    error=''
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        
        try:
            user=User.objects.get(username=username)

        except:
            error='Username not found'

        user=authenticate(request,username=username ,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            error='Username or password incorrect'
    return render(request,'banksystem/login.html',{"error":error})



def logout_user(request):
    logout (request)
    return redirect('login')



def sighnup_user(request):
    form=UserCreationForm()
    if request.method =='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=request.POST['username']
            password=request.POST['password1']
            try:
                user=authenticate(username=username ,password=password)
                Client.objects.create(
                    user=user,
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name']
                )
                login(request,user)
                return redirect('home')
            except:
                 return render(request,'banksystem/sighnup.html',{'error':'error creating user'})

    return render(request,'banksystem/sighnup.html',dict({'form':form}))
