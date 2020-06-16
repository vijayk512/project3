from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from rest_framework.utils import json
from django.contrib.auth.decorators import login_required

from . import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Pizza, Toppings, Subs, Pasta, Dinner_Platters, Salads, Orders
from django.core.mail import send_mail


# Create your views here.
def index(request):
    return render(request, "orders/index.html")


def login_view(request):
    if request.method == "POST":
        #  created a form in form.py file for login
        form = forms.LoginForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        #  it's match the username and password.
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            orders = Orders.objects.filter(status='Pending', user_id=request.user.id).order_by('-id')[:1]
            if orders:
                request.session['order_id'] = orders[0].id
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"message": "Invalid credential", "form": form})
    else:
        form = forms.LoginForm(None)
    return render(request, "orders/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        #  form is created in form.py and validation also handled in form file.
        form = forms.Register(request.POST)
        if form.is_valid():
            user = User()
            user.username = request.POST["username"]
            user.password = make_password(request.POST["password"])
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.email = request.POST["email"]
            user.save()
            return HttpResponseRedirect("/login")
        else:
            for field in form.errors:
                form[field].field.widget.attrs["class"] += " is-invalid"
            return render(request, "orders/register.html", {"form": form})
    else:
        form = forms.Register(None)
        return render(request, "orders/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return render(request, "orders/index.html")


def hours_view(request):
    return render(request, "orders/hours.html")


def contact_us_view(request):
    return render(request, "orders/contact-us.html")


@login_required(login_url='/login')
def menu_view(request):
    #  fetching data from the tables as created in models.py.
    salad = Salads.objects.all()
    toppings = Toppings.objects.all()
    subs = Subs.objects.all().order_by('id')
    pastas = Pasta.objects.all()
    dinner_platters = Dinner_Platters.objects.all()
    pizzas = Pizza.objects.all().order_by('id')

    context = {
        'pizzas': pizzas,
        'salads': salad,
        'toppings': toppings,
        'subs': subs,
        'pastas': pastas,
        'dinner_platters': dinner_platters
    }
    return render(request, "orders/menu.html", context)


@login_required(login_url='/login')
def orders_view(request):
    if request.method == "POST":
        #  defined the default dict as data when form request happen all the data is stored and converted in
        #  json and store in data base.
        data = {'toppings': [], 'subs': [], 'pastas': [], 'dinner_platters': [], 'salads': []}
        # adding multiple subs in dict
        for sub in request.POST.getlist("subs[]"):
            data['subs'].append(sub)
        # adding a dinner platter in dict
        for dinner_platter in request.POST.getlist("dinner_platters[]"):
            data['dinner_platters'].append(dinner_platter)
        # adding a pasta in dict
        for pasta in request.POST.getlist("pastas[]"):
            data['pastas'].append(pasta)
        # adding a toppings
        for topping in request.POST.getlist("toppings[]"):
            data['toppings'].append(topping)
        # adding a salad
        for salad in request.POST.getlist("salads[]"):
            data['salads'].append(salad)

        data['pizza_type'] = request.POST["pizza_type"]
        data['size'] = request.POST["size"]
        data['type'] = request.POST["type"]
        # checking if there is sub_type or not.
        if request.POST.get("sub_type") != '':
            data['sub_type'] = request.POST.get("sub_type")
        # checking if dinner_type or not means large and small.
        if request.POST.get('dinner_type') != '':
            data['dinner_type'] = request.POST.get('dinner_type')
        orders = Orders()
        orders.user_id = request.user.id
        orders.status = "Pending"
        orders.cart_detail = json.dumps([data])  # converted into json format and storing into Table.
        orders.save()
        request.session['order_id'] = orders.id
        return HttpResponseRedirect("checkout/%d" % orders.id)
    else:
        # for get call fetching all the data from the table and relevant content as well.
        veg_toppings = Toppings.objects.all().filter(type=1)
        meat_toppings = Toppings.objects.all().filter(type=0)
        subs = Subs.objects.all().order_by('id')
        salad = Salads.objects.all()
        pastas = Pasta.objects.all()
        dinner_platters = Dinner_Platters.objects.all()
        context = {
            'veg_toppings': veg_toppings,
            'meat_toppings': meat_toppings,
            'subs': subs,
            'salads': salad,
            'pastas': pastas,
            'dinner_platters': dinner_platters

        }
        return render(request, "orders/order.html", context)


@login_required(login_url='/login')
def checkout_view(request, order_id):
    if request.method == "POST":
        orders = Orders.objects.get(pk=order_id)
        orders.total = request.POST["total"]
        orders.status = "Complete"
        orders.save()
        msg = "Thank you for ordering you Pizza"
        request.session['thank-you'] = msg
        # sending a message to a user who order related to the information, like order no, amount
        # to the registered email address.
        send_mail(
            'Order Placed Successfully',
            'Thank you for placing your'
            ' order : ' + request.user.username + '<br> - here is your '
                                                  'order no is - ' + str(
                order_id) + ' And your total amount is - $' + str(request.POST["total"]),
            'vijayk512@gmail.com',
            [request.user.email],
            fail_silently=False,
        )

        return HttpResponseRedirect("/thank-you")
    else:
        if not order_id:
            return HttpResponseRedirect("/orders")
        data = Orders.objects.get(pk=order_id)  # fetching data from order with order_id
        if data.status == 'Complete':  # if accidently fetch the completed order will redirect to orders page
            return HttpResponseRedirect("/orders")

        cart_data = json.loads(data.cart_detail)
        total = 0  # default total to 0 amount
        if cart_data[0]['pizza_type'] == '1':  # checking the type of pizza is selected
            pizza_type = 'regular'
        else:
            pizza_type = 'sicilian'

        pizza_size = cart_data[0]['size']

        if pizza_type == 'sicilian':  # if type is sicilian and change the pizza size.
            if pizza_size == '1 toppings':
                pizza_size = '1 item'
            elif pizza_size == '2 toppings':
                pizza_size = '2 items'
            elif pizza_size == '3 toppings':
                pizza_size = '3 items'

        pizza_price = Pizza.objects.filter(type=pizza_type, pizza_type=pizza_size)
        # checking the price for the pizza you selected.

        if cart_data[0]['type'] == 'large':
            pz = pizza_price[0].price_l
            total = float(total) + float(pizza_price[0].price_l)
        else:
            pz = pizza_price[0].price_m
            total = float(total) + float(pizza_price[0].price_m)

        salad_total = 0
        # adding how many salad are selected and calculating total and salad total amount.
        for salad in cart_data[0]['salads']:
            s = Salads.objects.filter(name=salad)
            salad_total = salad_total + float(s[0].price)
            total = float(total) + float(s[0].price)

        pasta_total = 0
        # adding how many pasta are selected and calculating total and salad total amount.
        for pasta in cart_data[0]['pastas']:
            p = Pasta.objects.filter(name=pasta)
            pasta_total = pasta_total + float(p[0].price)
            total = float(total) + float(p[0].price)

        dinner_total = 0
        # adding how many dinner are selected and calculating total and salad total amount.
        for dinner_platter in cart_data[0]['dinner_platters']:
            d = Dinner_Platters.objects.filter(name=dinner_platter)
            if cart_data[0]['dinner_type'] == 'large':
                dinner_total = dinner_total + float(d[0].price_l)
                total = float(total) + float(d[0].price_l)
            else:
                dinner_total = dinner_total + float(d[0].price_m)
                total = float(total) + float(d[0].price_m)

        su_price = 0
        # adding how many subs are selected and calculating total and salad total amount.
        for sub in cart_data[0]['subs']:
            su = Subs.objects.filter(name=sub)
            if cart_data[0]['sub_type'] == 'large':
                su_price = su_price + float(su[0].price_l)
                total = float(total) + float(su[0].price_l)
            else:
                su_price = su_price + float(su[0].price_m)
                total = float(total) + float(su[0].price_m)

        total_toppings = 0
        if pizza_size == 'special':
            total_toppings = 5
        elif pizza_size == 'cheese':
            total_toppings = 0
        else:
            total_toppings = int(list(filter(str.isdigit, pizza_size))[0])

        # return HttpResponse(pizza_size)
        if pizza_size not in 'special' or pizza_size not in 'cheese':
            for i in range(len(cart_data[0]['toppings']) - total_toppings):
                total = float(total) + 1
        extra = 0
        if len(cart_data[0]['toppings']) - total_toppings > 0:
            extra = len(cart_data[0]['toppings']) - total_toppings

        context = {
            'cart_data': cart_data[0],
            'pizza_price': pz,
            'pizza_type': pizza_type,
            'total': str(round(total, 2)),
            'sub_price': su_price,
            'dinner_total': dinner_total,
            'salad_total': salad_total,
            'pasta_total': pasta_total,
            'order_id': order_id,
            'total_toppings': extra

        }
        return render(request, "orders/checkout.html", context)


def thank_you_view(request):
    # checking session and destroying once msg is fetched.
    if 'thank-you' not in request.session:
        return HttpResponseRedirect("/")
    else:
        msg = request.session['thank-you']
    if request.session['thank-you']:
        del request.session['thank-you']
        del request.session['order_id']

    return render(request, "orders/thank-you.html", {'msg': msg})
