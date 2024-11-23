from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'admin_portal'

urlpatterns = [
    path('landingpage/', views.landingpage, name = 'landingpage'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('forgot_password/', views.forgot_password, name = 'forgot_password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('reset_password/', views.reset_password, name='reset_password'), 
    path('dashboard/approve_request/', views.approve_request, name='approve_request'),
    # path('dashboard/no_due_slip/', views.no_due_slip, name='no_due_slip'),
    # path('dashboard/lor_request/', views.lor_request, name='lor_request'),
    # path('dashboard/submit/', views.success_page, name='success_page')
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)