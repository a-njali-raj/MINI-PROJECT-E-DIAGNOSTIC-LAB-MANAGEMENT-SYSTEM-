from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib.auth.decorators import login_required
from tests.models import User 
from django.views.decorators.cache import never_cache
from tests.models import Test
from django.contrib.auth import authenticate, login
from django.contrib import messages
@never_cache
@login_required(login_url='login')
def staff_dashboard(request):
    if request.user.is_staff and not request.user.is_superuser:
        
        return render(request, "staff_dashboard.html")
    return redirect("home")

@never_cache
@login_required(login_url='login')
def admin_dashboard(request):
    if request.user.is_superuser:
        users = User.objects.filter(is_superuser=False)
        return render(request, "admin_dashboard.html", {"users": users})
    return redirect("home")

@never_cache
@login_required(login_url='login')
def userdetails(request):
    if request.user.is_superuser:
        users = User.objects.filter(is_superuser=False, is_staff=False, is_active=True)
        return render(request, "userdetails.html", {"users": users})
    return redirect("home")
   
@never_cache
@login_required(login_url='login')
def admintest(request):
    tests = Test.objects.all() 
    return render(request, "admintest.html", {'tests': tests}) # Retrieve all Test objects from the database
@never_cache
@login_required(login_url='login')
def addtest(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        is_available = request.POST.get('is_available')  # Get the checkbox value

        # If the checkbox is not checked, set is_available to False
        if is_available is None:
            is_available = False
        else:
            is_available = True

        if name and price:
            Test.objects.create(name=name, price=price, is_available=is_available)
            messages.success(request, "Test  added successfully.")
            return redirect("admintest")  # Redirect to a success page or any other page
    return render(request, "addtest.html")
@never_cache
@login_required(login_url='login')
def delete_test(request,test_id):
    test = get_object_or_404(Test, id=test_id)

    # Instead of deleting, change the availability status to False
    test.is_available = False
    test.save()
    messages.success(request, "test deleted successfully.")

    return redirect("admintest")
@never_cache
@login_required(login_url='login')
def updatetest(request):
    # Retrieve 'test_id' from the query parameter 'test_id'
    test_id = request.GET.get('test_id')

    if request.method == 'POST':
        # Get the updated data from the form
        name = request.POST.get('name')
        price = request.POST.get('price')
        availability = request.POST.get('availability')

        # Retrieve the test instance based on the 'test_id'
        test = Test.objects.get(pk=test_id)

        # Update the test's attributes
        test.name = name
        test.price = price
        test.is_available = availability == "True"  # Convert to boolean

        # Save the updated test
        test.save()

        # Redirect to a success page or return a response
        messages.success(request, "Test updated successfully.")
        return redirect('admintest')  # Replace 'success_page' with the appropriate URL

    # Handle GET requests for editing the test details
    else:
        # Retrieve the test instance based on the 'test_id'
        test = Test.objects.get(pk=test_id)
        context = {
            'test': test,
        }
        return render(request, "updatetest.html", context)
@never_cache
@login_required(login_url='login')
def adminstaff(request):
    staff_users = User.objects.filter(is_staff=True,is_superuser=False)
    context = {'staff_users': staff_users}
    return render(request, 'adminstaff.html', context)
@never_cache
@login_required(login_url='login')
def addstaff(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST["first-name"]

        # Create the user and set is_staff to True
        user = User.objects.create_user(username=username, password=password)
        user.is_staff = True
        user.first_name = first_name

        user.save()

        # Log in the new staff member
        
        messages.success(request, "Staff is added successfully.")
        return redirect('admin_dashboard')  # Redirect to staff_dashboard

    return render(request, 'addstaff.html')
@never_cache
@login_required(login_url='login')
def delete_staff(request, user_id):
    # Get the user object to delete
    user = get_object_or_404(User, id=user_id)

    # Set is_staff status to 0
    user.is_staff = False
    user.is_active = False
    user.save()

    # You can add a confirmation message if needed
    messages.success(request, "staff is removed successfully.")

    # Redirect to a staff list page or wherever you need to go
    return redirect('admin_dashboard')  # Replace 'staff_list' with the actual URL name for your staff list page
@never_cache
@login_required(login_url='login')
def stafftest(request):
    tests = Test.objects.all() 
    return render(request, "stafftest.html", {'tests': tests}) # Retrieve all Test objects from the database