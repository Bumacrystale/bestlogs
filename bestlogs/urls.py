from django.contrib import admin
from django.urls import path, include
from main import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.user_login, name='root'),
    path('home/', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('orders/', views.orders, name='orders'),
    path('add-funds/', views.add_funds, name='add_funds'),
    path('transactions/', views.transaction_page, name='transaction_page'),
    path('wallet/', views.wallet, name='wallet'),
    path('profile/', views.profile, name='profile'),
    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

    # FLUTTERWAVE
    path('flutterwave/initialize/', views.initialize_payment, name='initialize_payment'),
    path('flutterwave/callback/', views.payment_callback, name='payment_callback'),

    # PASSWORD RESET
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
