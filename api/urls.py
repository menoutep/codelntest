from django.urls import path
from . import views
app_name="api"
urlpatterns = [
    path('userbadgesall/', views.UserBadgeListAll.as_view(), name='userbadge-list-all'),
    path('userbadges/', views.UserBadgeList.as_view(), name='userbadge-list'),
    path('userbadge/', views.UserBadgeDetail.as_view(), name='userbadge-detail'),
    # Ajoutez d'autres URL pour les badges et les utilisateurs ici
]
