from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm
from .models import InvestmentPlan, Transaction
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    return render(request, 'XinvestApp/index.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                error_message = "Invalid Username or Password"
                return render(request, 'XinvestApp/login.html', {"error_message": error_message})

    return render(request, 'XinvestApp/login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.status = 'investor'
                user.save()  # Save the user before authenticating
                login(request, user)
                messages.success(request, f'Account created for {user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Error creating account. Please check the form.')
        else:
            form = RegisterForm()
    return render(request, 'XinvestApp/register.html', {'form': form})


@login_required(login_url='/login_user')
def packages(request):
    packages = InvestmentPlan.objects.all()
    context = {'packages': packages}  # Corrected line
    return render(request, 'XinvestApp/dashboard/packages.html', context)




def transaction_history(request):
    transactions = Transaction.objects.filter(user=request.user)
    context = {'transactions': transactions}  # Corrected line
    return render(request, 'XinvestApp/dashboard/transaction_history.html', context)
    

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/login_user')
def dashboard(request):
    user = request.user
    try:
        # Get the most recent transaction of type 'deposit' for the given user
        transaction = Transaction.objects.filter(transaction_type='deposit', user=user).order_by('-transaction_date').first()
        
        # Check if a transaction exists and if its status is approved
        if transaction and transaction.transaction_status == 'approved':
            user.balance = transaction.amount  # Adjust balance based on the transaction amount
        else:
            user.balance = 0
    except ObjectDoesNotExist:
        user.balance = user.balance  
    # Save the user instance after updating the balance
    user.save()

    return render(request, 'XinvestApp/dashboard/index_2.html')

               
@login_required(login_url='/login_user')
def deposit(request,package):
    user = request.user
    if user.investment_plan is not None:
        return redirect('dashboard')
    else:
        package = InvestmentPlan.objects.get(name = package)
        amount = package.amount
        context = {'amount': amount,'package':package}
    return render(request, 'XinvestApp/dashboard/PayOut.html',context)

@login_required(login_url='/login_user')
def pending(request,):
    # investment_plan = get_object_or_404(InvestmentPlan, id=package_id)
    # user = request.user
    # if user.investment_plan is None:
    #     user.investment_plan = investment_plan
    #     user.balance = investment_plan.amount
    #     user.save()
    #     transaction = Transaction.objects.create(
    #     user=user,
    #     amount= investment_plan.amount,
    #     transaction_type= 'deposit',
    #     transaction_status='pending'
    # )
    #     transaction.save()
    # else:
    #     messages.error(request, 'You already have an investment plan.')
    #     return redirect('dashboard')
    return render(request, 'XinvestApp/dashboard/pending.html')

@login_required(login_url='/login_user')
def upload_proof(request,package):
    investment_plan = get_object_or_404(InvestmentPlan, name = package)
    plan = InvestmentPlan.objects.get(name = package)
    user = request.user
    if request.method == 'POST' and request.FILES['proof_of_payment']:
        proof_of_payment = request.FILES['proof_of_payment']    
        if user.investment_plan is None:
            user.investment_plan = investment_plan
            user.balance = investment_plan.amount
            user.save()

            transaction = Transaction.objects.create(
            user=user,
            amount= investment_plan.amount,
            transaction_type= 'deposit',
            transaction_status='pending',
            proof_of_payment=proof_of_payment  
        )
            transaction.save()
        else:
            messages.error(request, 'You already have an investment plan.')
            return redirect('dashboard')
        
        return redirect('dashboard')
    
    return render(request, 'XinvestApp/dashboard/upload_proof.html',{'package':package})

















def earnings(request):
    return render(request, 'XinvestApp/dashboard/Earning.html')

def investment_plans(request):
    return render(request, 'XinvestApp/plan.html')

def about(request):
    return render(request, 'XinvestApp/about.html')

def contact(request):
    return render(request, 'XinvestApp/contact.html')

def blogs(request):
    return render(request, 'XinvestApp/blogs.html')

# Add more views as needed
