import requests
import uuid
from decimal import Decimal, InvalidOperation

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction as db_transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm
from .models import Product, Order, Transaction


# =========================
# HELPER FUNCTION
# =========================
def get_user_balance(user):
    transactions = Transaction.objects.filter(user=user)
    balance = Decimal("0.00")

    for t in transactions:
        tx_type = str(t.type).strip().lower()

        if tx_type in ["fund", "deposit", "credit", "add_funds"]:
            balance += Decimal(str(t.amount))
        elif tx_type in ["purchase", "debit", "withdraw"]:
            balance -= Decimal(str(t.amount))

    return balance


# =========================
# HOME
# =========================
@login_required
def home(request):
    products = Product.objects.filter(stock__gt=0).order_by("-id")[:6]

    balance = Decimal("0.00")
    if request.user.is_authenticated:
        balance = get_user_balance(request.user)

    context = {
        "products": products,
        "balance": balance,
    }
    return render(request, "home.html", context)


# =========================
# WALLET
# =========================
@login_required
def wallet(request):
    # FIXED: strong ordering so latest appears first
    transactions = Transaction.objects.filter(user=request.user).order_by("-id")
    balance = get_user_balance(request.user)

    context = {
        "balance": balance,
        "transactions": transactions,
    }
    return render(request, "wallet.html", context)


# =========================
# ADD FUNDS
# =========================
@login_required
def add_funds(request):
    return render(request, "add_funds.html")


# =========================
# SERVICES
# =========================
def services(request):
    products = Product.objects.filter(stock__gt=0).order_by("-id")
    return render(request, "services.html", {"products": products})


# =========================
# BUY PRODUCT
# =========================
@login_required
def buy_product(request, product_id):
    with db_transaction.atomic():
        product = get_object_or_404(Product.objects.select_for_update(), id=product_id)
        balance = get_user_balance(request.user)

        if product.stock <= 0:
            messages.error(request, "Product out of stock.")
            return redirect("services")

        if balance < product.price:
            messages.error(request, "Insufficient wallet balance.")
            return redirect("wallet")

        product.stock -= 1
        product.save()

        Order.objects.create(
            user=request.user,
            product=product,
            price=product.price
        )

        # FIXED: purchase transaction must be saved for history + balance deduction
        Transaction.objects.create(
            user=request.user,
            type="purchase",
            amount=product.price,
            reference=f"PUR-{uuid.uuid4().hex[:10]}"
        )

    messages.success(request, "Product purchased successfully.")
    return redirect("orders")


# =========================
# ORDERS
# =========================
@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-id")
    return render(request, "orders.html", {"orders": orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_detail.html", {"order": order})


# =========================
# PROFILE
# =========================
@login_required
def profile(request):
    if request.method == "POST":
        profile_picture = request.FILES.get("profile_picture")
        if profile_picture:
            request.user.profile.profile_picture = profile_picture
            request.user.profile.save()
            messages.success(request, "Profile picture updated successfully.")
            return redirect("profile")

    return render(request, "profile.html")


# =========================
# TRANSACTION PAGE
# =========================
@login_required
def transaction_page(request):
    # FIXED: same transactions, same ordering
    transactions = Transaction.objects.filter(user=request.user).order_by("-id")
    return render(request, "transaction_page.html", {"transactions": transactions})


# =========================
# SIGNUP
# =========================
def signup(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        if not name or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, "signup.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

        if User.objects.filter(username=name).exists():
            messages.error(request, "Username already exists.")
            return render(request, "signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "signup.html")

        user = User.objects.create_user(
            username=name,
            email=email,
            password=password,
            first_name=name
        )

        login(request, user)
        messages.success(request, "Account created successfully.")
        return redirect("home")

    return render(request, "signup.html")


# =========================
# LOGIN
# =========================
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = LoginForm()

    return render(request, "registration/login.html", {"form": form})

# =========================
# LOGOUT
# =========================
def user_logout(request):
    logout(request)
    return redirect("login")


# =========================
# INITIALIZE PAYMENT
# =========================
@login_required
def initialize_payment(request):
    if request.method != "POST":
        return redirect("add_funds")

    amount = request.POST.get("amount", "").strip()

    if not amount:
        messages.error(request, "Please enter an amount.")
        return redirect("add_funds")

    try:
        amount_decimal = Decimal(amount).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        messages.error(request, "Invalid amount.")
        return redirect("add_funds")

    if amount_decimal <= 0:
        messages.error(request, "Amount must be greater than zero.")
        return redirect("add_funds")

    if not request.user.email:
        messages.error(request, "Please add an email to your account first.")
        return redirect("profile")

    tx_ref = f"bestlogs-{request.user.id}-{uuid.uuid4().hex[:10]}"

    headers = {
        "Authorization": f"Bearer {settings.FLW_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "tx_ref": tx_ref,
        "amount": str(amount_decimal),
        "currency": "NGN",
        "redirect_url": settings.FLW_REDIRECT_URL,
        "customer": {
            "email": request.user.email,
            "name": request.user.get_full_name() or request.user.username,
        },
        "meta": {
            "user_id": request.user.id,
            "expected_amount": str(amount_decimal),
        },
        "customizations": {
            "title": "Wallet Funding",
            "description": "Fund your wallet",
        },
    }

    try:
        response = requests.post(
            "https://api.flutterwave.com/v3/payments",
            json=payload,
            headers=headers,
            timeout=30,
        )
        data = response.json()
        print("INITIALIZE RESPONSE:", data)
    except Exception as e:
        print("INITIALIZE ERROR:", e)
        messages.error(request, "Could not connect to payment gateway.")
        return redirect("add_funds")

    if data.get("status") != "success":
        messages.error(request, data.get("message", "Payment initialization failed."))
        return redirect("add_funds")

    payment_link = data.get("data", {}).get("link")
    if not payment_link:
        messages.error(request, "No payment link returned.")
        return redirect("add_funds")

    return redirect(payment_link)


# =========================
# PAYMENT CALLBACK / VERIFY
# =========================
def payment_callback(request):
    status = request.GET.get("status")
    tx_ref = request.GET.get("tx_ref")
    transaction_id = request.GET.get("transaction_id")

    print("CALLBACK HIT")
    print("status:", status)
    print("tx_ref:", tx_ref)
    print("transaction_id:", transaction_id)

    # FIXED: do not stop because status is "completed"
    if status not in ["successful", "completed"]:
        messages.error(request, f"Payment was not successful. Status: {status}")
        return redirect("wallet")

    if not tx_ref or not transaction_id:
        messages.error(request, "Missing transaction details.")
        return redirect("wallet")

    headers = {
        "Authorization": f"Bearer {settings.FLW_SECRET_KEY}",
    }

    try:
        response = requests.get(
            f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify",
            headers=headers,
            timeout=30,
        )
        data = response.json()
        print("VERIFY RESPONSE:", data)
    except Exception as e:
        print("VERIFY ERROR:", e)
        messages.error(request, "Could not verify payment.")
        return redirect("wallet")

    if data.get("status") != "success":
        messages.error(request, data.get("message", "Verification failed."))
        return redirect("wallet")

    payment_data = data.get("data", {})
    verified_status = str(payment_data.get("status", "")).lower()
    verified_tx_ref = payment_data.get("tx_ref")
    currency = payment_data.get("currency")
    charged_amount = payment_data.get("charged_amount")
    meta = payment_data.get("meta") or {}

    print("verified_status:", verified_status)
    print("verified_tx_ref:", verified_tx_ref)
    print("currency:", currency)
    print("charged_amount:", charged_amount)
    print("meta:", meta)

    if verified_status != "successful":
        messages.error(request, f"Payment verification failed. Status: {verified_status}")
        return redirect("wallet")

    if verified_tx_ref != tx_ref:
        messages.error(request, "Transaction reference mismatch.")
        return redirect("wallet")

    if currency != "NGN":
        messages.error(request, "Invalid currency.")
        return redirect("wallet")

    try:
        amount_paid = Decimal(str(charged_amount)).quantize(Decimal("0.01"))
    except Exception:
        messages.error(request, "Invalid paid amount.")
        return redirect("wallet")

    expected_amount = meta.get("expected_amount")
    user_id = meta.get("user_id")

    try:
        expected_amount = Decimal(str(expected_amount)).quantize(Decimal("0.01"))
    except Exception:
        messages.error(request, "Expected amount missing.")
        return redirect("wallet")

    if str(user_id) != str(request.user.id):
        messages.error(request, "This payment does not belong to your account.")
        return redirect("wallet")

    if amount_paid < expected_amount:
        messages.error(request, "Paid amount is less than expected.")
        return redirect("wallet")

    existing_tx = Transaction.objects.filter(reference=tx_ref).first()
    if existing_tx:
        messages.info(request, "This payment has already been processed.")
        return redirect("wallet")

    Transaction.objects.create(
        user=request.user,
        type="fund",
        amount=amount_paid,
        reference=tx_ref
    )

    messages.success(request, "Wallet funded successfully.")
    return redirect("wallet")
