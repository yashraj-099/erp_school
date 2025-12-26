from django.contrib import admin
from django.urls import path, include
from core import views
# from django.conf.urls import handler404, handler500, handler403, handler400

# handler404 = "core.views.error_404"
# # handler500 = "core.views.error_500"
# handler403 = "core.views.error_403"
# handler400 = "core.views.error_400"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # path('api/', include('core.api_urls')),
    # path('api-auth/', include('rest_framework.urls')),
    # path('api/token/', include('core.api_token_urls')),
    # path('login/', views.login_view, name='login'),
]
