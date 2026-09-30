from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("authentication.urls")),
    path("api/cards/", include("cards.urls")),
    path("api/transactions/", include("transactions.urls")),
    path("api/admin-panel/", include("adminpanel.urls")),
]
