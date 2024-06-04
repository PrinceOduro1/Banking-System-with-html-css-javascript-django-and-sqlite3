from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import BankUser,Transaction
import re
from decimal import Decimal


# Create your views here.
def index(request):

    return render(request, 'index.html')
def landing(request):
    if request.user.is_authenticated:
        user_name = request.user.username 
        return render(request, 'landing.html', {'user_name': user_name})
    else:
        return render(request, 'landing.html')
def logout(request):
    auth.logout(request)
    return redirect('/dashboard')
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('dashboard')
        else:
            messages.info(request,'Invalid credentials...Try again')
            return redirect('login')
    else:
        return render(request,'slide.html')
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        initial_deposit = request.POST['initial_deposit']
        pass_confirm = request.POST['confirm_password']
        pass_len = len(password)
        
        if (pass_len == 4):
            if password == pass_confirm:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists')
                    return redirect('signup')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                    return redirect('signup')
                else:
                    # Create the user
                    user = User.objects.create_user(username=username, email=email, password=password)
                    # Create BankUser with initial deposit
                    bank_user = BankUser(username=username, email=email, initial_deposit=initial_deposit,pin=password)
                    bank_user.save()
                    messages.success(request, 'Account created successfully. Please log in.')
                    return redirect('login')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('signup')
        else:
            messages.error(request, 'Pin should contain four digits')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

from django.contrib.auth.decorators import login_required

@login_required
def change_pin(request):
    if request.method == 'POST':
        new_pin = request.POST['new-pin']
        confirm_pin = request.POST['confirm-new-pin']
        print("New PIN:", new_pin) 
        if new_pin == confirm_pin:

            if len(new_pin) == 4 :
                user = request.user
                user.set_password(new_pin)  # Update password for Django user
                user.save()
                bank_user = BankUser.objects.get(username=user.username)
                bank_user.pin = new_pin
                bank_user.save()
                messages.success(request, 'Your PIN was successfully updated!')
                return redirect('dashboard')
               
            else:
                messages.error(request, 'Invalid PIN. Please enter a 4-digit number.')
        else:
            messages.error(request, 'PINs do not match. Please make sure they are the same.')
            return redirect('change_pin')
    return render(request, 'changePin.html')
from django.shortcuts import render

@login_required
def check_balance(request,username):
    # Get the currently logged-in user's username
    #username = request.user.username
    
    # Query the BankUser model to get the corresponding bank user
    try:
        bank_user = BankUser.objects.get(pk=username)
        context={
            'username':bank_user.username,
            'balance':bank_user.initial_deposit
        }
        balance = bank_user.initial_deposit
    except BankUser.DoesNotExist:
        balance = None  # or handle the case where the user doesn't have a bank account
    
    return render(request, 'checkbalance.html', context)
@login_required
def deposit(request):
    if request.method == 'POST':
        print('user logged:',request.user.username)
        amount = Decimal(request.POST.get('amount'))
        print('amount',amount)
        if amount<=0:
            return HttpResponse('invalid deposit')
        try:
            
            bank_user = BankUser.objects.get(username=request.user.username)
            print('bank user',bank_user.username)
            bank_user.initial_deposit +=amount
            bank_user.save()
            transaction = Transaction.objects.create(bank_user=bank_user,transaction_type='Deposit',amount=amount)
            transaction.save()
            return redirect('dashboard')
        except BankUser.DoesNotExist:
            all_user = BankUser.objects.all()
            print('all user:',[user.username for user in all_user])
            return HttpResponse('User account not found')
        except ValueError as e:
            print('ValueError:',e)
            return HttpResponse('Invalid input')
    else:
        return render(request, 'deposit.html')
def success(request):
    return render(request,'success.html')



def withdraw(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('with_amount'))
        bank_user = BankUser.objects.get(username=request.user.username)
        if amount>0:

            if amount > bank_user.initial_deposit:
                messages.error(request,'Amount greater than your balance.Invalid withdrawal')
                return redirect('withdraw')
            else:
                bank_user.initial_deposit = bank_user.initial_deposit - amount
                bank_user.save()
                transaction = Transaction.objects.create(bank_user=bank_user,transaction_type='Withdrawal',amount=amount)
                transaction.save()
                messages.success(request,'Successfull')
                return redirect('dashboard')
        else:
            messages.error(request,'Invalid amount')
            return redirect('withdraw')
    else:
        return render(request,'withdraw.html')
    


def transactions(request,username):
    transaction = Transaction.objects.filter(bank_user=username)
    print('user',transaction)
    return render(request,'transactions.html',{'transaction':transaction})

from django.http import JsonResponse

@login_required
def dashboard(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            bank_user = BankUser.objects.get(username=request.user.username)
            balance = bank_user.initial_deposit
            transactions = Transaction.objects.filter(bank_user=bank_user)
            transactions_data = [
                {
                    'transaction_type': trans.transaction_type,
                    'amount': trans.amount,
                    'timestamp': trans.timestamp
                } for trans in transactions
            ]
            return JsonResponse({'balance': balance, 'transactions': transactions_data})
        except BankUser.DoesNotExist:
            return JsonResponse({'balance': 0, 'transactions': []}, status=404)
    else:
        try:
            bank_user = BankUser.objects.get(username=request.user.username)
            balance = bank_user.initial_deposit
        except BankUser.DoesNotExist:
            balance = 0
        return render(request, 'dashboard.html', {'balance': balance})


@login_required
def transfer(request):
    if request.method == 'POST':
        recipient_username = request.POST['username']
        amount = Decimal(request.POST['amount'])

        try:
            sender = BankUser.objects.get(username=request.user.username)
            recipient = BankUser.objects.get(username=recipient_username)

            if sender.initial_deposit >= amount:
                # Subtract the amount from the sender's balance
                sender.initial_deposit -= amount
                sender.save()

                # Add the amount to the recipient's balance
                recipient.initial_deposit += amount
                recipient.save()

                # Create transaction records for both sender and recipient
                Transaction.objects.create(
                    bank_user=sender,
                    transaction_type='Transfer Out',
                    amount=amount
                )
                Transaction.objects.create(
                    bank_user=recipient,
                    transaction_type='Transfer In',
                    amount=amount
                )

                messages.success(request, 'Transfer successful.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Insufficient balance.')
        except BankUser.DoesNotExist:
            messages.error(request, 'Recipient does not exist.')

    return render(request, 'transfer.html')