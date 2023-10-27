from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.hashers import make_password, check_password


def register(request):
    if request.method == "GET":
        if "user_id" in request.session:
            return redirect("/user/dashboard")
        return render(request, "login.html")
    elif request.method == "POST":
        name = request.POST["name"]
        phone = request.POST["phone"]
        dob = request.POST["dob"]
        aadhar = request.POST["aaadhar"]
        address = request.POST["address"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        emer1_name = request.POST["emer1_name"]
        emer1_number = request.POST["emer1_number"]
        emer1_address = request.POST["emer1_address"]
        emer2_name = request.POST["emer2_name"]
        emer2_number = request.POST["emer2_number"]
        emer2_address = request.POST["emer2_address"]
        if password == confirm_password:
            if User.objects.filter(aaadhar=aadhar).exists():
                return render(
                    request,
                    "login.html",
                    {"message": "Already registered! Please log in!"},
                )
            print(name, phone, dob, aadhar, address, password)
            print(emer1_name, emer1_number, emer1_address)
            print(emer2_name, emer2_number, emer2_address)
            password = make_password(password)
            user = User(
                name=name,
                phone=phone,
                dob=dob,
                aaadhar=aadhar,
                address=address,
                password=password,
                emer1_name=emer1_name,
                emer1_number=emer1_number,
                emer1_address=emer1_address,
                emer2_name=emer2_name,
                emer2_number=emer2_number,
                emer2_address=emer2_address,
            )
            user.save()
            id = User.objects.get(aaadhar=aadhar).user_id
            request.session["user_id"] = id
            return render(
                request, "login.html", {"message": "Successfully Registered!"}
            )
        else:
            return render(
                request,
                "login.html",
                {"message": "Password and Confirmation do not match!"},
            )


def login(request):
    if request.method == "GET":
        if "user_id" in request.session:
            return redirect("/user/dashboard")
        return render(request, "login.html")
    else:
        name = request.POST["name"]
        password = request.POST["password"]
        aadhar = request.POST["aadhar"]
        print(name, password, aadhar)
        try:
            user = User.objects.get(aaadhar=aadhar)
        except User.DoesNotExist:
            print("Does not exist")
            return render(
                request, "login.html", {"message": "Invalid Name or Password"}
            )
        if check_password(password, user.password) and user.name == name:
            request.session["user_id"] = user.user_id
            return redirect("/user/dashboard")
        else:
            return render(
                request, "login.html", {"message": "Invalid Name or Password"}
            )
        

def logout(request):
    if "user_id" in request.session:
        del request.session["user_id"]
    return redirect("/user/login")
