from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from . models import Profile
from core.forms import ContactForm, ProfileForm
from django.contrib import messages
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, "index.html")

def classes(request):
    return render(request, "class.html")

def contact(request):
    if request.method =="POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Thanks for your message.")
    return render(request, "contact.html")

def profile(request):
    user = get_object_or_404(Profile, user=request.user)
    return render(request, "profile.html", {"profile":user})

def editprofile(request):
    form = ProfileForm()
    return render(request, "editprofile.html", {"form":form})

def subscribe(request):
    return render(request, "subscribe.html")

@login_required(login_url='/authentication/login/')
def payment(request, choice):
    if choice == "all":
        name = "All round fitness"
        price = 30
    elif choice == "body_building":
        name = "Body Building"
        price = 25
    elif choice == "muscle_building":
        name = "Muscle Building"
        price = 20

    data = {
        "name":name,
        "price":price,
        "choice":choice
        }
    return render(request, "payment.html", {"data":data})


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request, choice):
    user = get_object_or_404(Profile, user=request.user)
    user.subscribed_type = choice
    user.save()
    if choice == "all":
        price = 3000
    elif choice == "body_building":
        price = 2500
    elif choice == "muscle_building":
        price = 2000
    if request.method == 'GET':
        domain_url = settings.DOMAIN_URL
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success/{CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        "quantity":1,
                        "price_data":{
                            "unit_amount":price,
                            "product_data":{
                                "name":"muscle"
                            },
                            "currency":"usd"
                        }
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

def success(request, session_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status == "paid":
        user = get_object_or_404(Profile, user=request.user)
        user.is_subscribed = True
        user.subscribed_type
        user.checkout_session = session_id
        user.payment_id = session.payment_intent
        user.save()
    messages.success(
                request, "Thanks for your payment.")
    return redirect("subscribe")
def canceled(request):
    return HttpResponse("sorry something went wrong")

