from django.http import Http404
from rest_framework import generics
from base.models import UserBadge,Badge
from .serializers import UserBadgeSerializer

from rest_framework import permissions

from .serializers import UserBadgeSerializer
from django.contrib.auth.models import User

class UserBadgeListAll(generics.ListAPIView):
    queryset = UserBadge.objects.all()
    serializer_class = UserBadgeSerializer


class UserBadgeList(generics.ListAPIView):
    serializer_class = UserBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]  # Vous pouvez personnaliser les autorisations ici

    def get_queryset(self):
        # Récupérer le nom de l'utilisateur à partir des paramètres de requête
        username = self.request.query_params.get('username')

        # Rechercher l'utilisateur par nom d'utilisateur
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            # Filtrer les badges par utilisateur trouvé
            return UserBadge.objects.filter(user=user)
        else:
            # Si l'utilisateur n'est pas trouvé, renvoyer une liste vide ou une réponse d'erreur appropriée
            return UserBadge.objects.none()


class UserBadgeDetail(generics.RetrieveAPIView):
    serializer_class = UserBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]  # Vous pouvez personnaliser les autorisations ici

    def get_object(self):
        # Récupérer le nom de l'utilisateur et le nom du badge à partir des paramètres de requête
        username = self.request.query_params.get('username')
        badge_name = self.request.query_params.get('badge_name')

        # Rechercher l'utilisateur par nom d'utilisateur
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        if user:
            # Rechercher le badge par nom
            try:
                badge = Badge.objects.get(name=badge_name)
            except Badge.DoesNotExist:
                badge = None

            if badge:
                # Rechercher l'objet UserBadge correspondant à l'utilisateur et au badge
                try:
                    user_badge = UserBadge.objects.get(user=user, badge=badge)
                except UserBadge.DoesNotExist:
                    user_badge = None

                if user_badge:
                    return user_badge

        # Si l'utilisateur, le badge ou l'objet UserBadge correspondant n'est pas trouvé,
        # renvoyez une réponse d'erreur appropriée.
        raise Http404("UserBadge not found")


