from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Authentication
    path('accounts/', include('apps.accounts.urls')),

    # Core/Dashboard
    path('', include('apps.core.urls')),

    # Students
    path('students/', include('apps.students.urls')),

    # Academics
    path('academics/', include('apps.academics.urls')),

    # Staff
    path('staff/', include('apps.staff.urls')),

    # Accounting
    path('accounting/', include('apps.accounting.urls')),

    # Attendance
    path('attendance/', include('apps.attendance.urls')),

    # Examination
    path('examination/', include('apps.examination.urls')),

    # Donation
    path('donation/', include('apps.donation.urls')),

    # Library
    path('library/', include('apps.library.urls')),

    # Canteen
    path('canteen/', include('apps.canteen.urls')),

    # Branch
    path('branch/', include('apps.branch.urls')),

    # Portal
    path('portal/', include('apps.portal.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)