from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from base.models import Badge, UserBadge

class UserBadgeTests(TestCase):
    def setUp(self):
        # Créer un utilisateur pour les tests
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Créer un badge pour les tests
        self.badge = Badge.objects.create(name='TestBadge', description='Test Badge Description', criteria='test_criteria')

        # Créer un UserBadge associé à l'utilisateur et au badge pour les tests
        self.user_badge = UserBadge.objects.create(user=self.user, badge=self.badge)

        # Créer un client API pour effectuer des requêtes
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')


    def test_user_badge_list_all(self):
        # Créer une URL pour la vue UserBadgeListAll
        url = reverse('api:userbadge-list-all')

        # Effectuer une requête GET
        response = self.client.get(url)

        # Vérifier que la réponse a un code de statut HTTP 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérifier que le nombre d'objets UserBadge dans la réponse correspond au nombre d'objets créés
        self.assertEqual(len(response.data), 1)

    def test_user_badge_list(self):
        # Créer une URL pour la vue UserBadgeList avec le nom d'utilisateur en tant que paramètre
        url = reverse('api:userbadge-list')
        username = 'testuser'

        # Effectuer une requête GET avec le nom d'utilisateur en tant que paramètre
        response = self.client.get(url, {'username': username})

        # Vérifier que la réponse a un code de statut HTTP 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérifier que le nombre d'objets UserBadge dans la réponse correspond au nombre d'objets créés pour cet utilisateur
        self.assertEqual(len(response.data), 1)

    def test_user_badge_list_user_not_found(self):
        # Créer une URL pour la vue UserBadgeList avec un nom d'utilisateur inexistant en tant que paramètre
        url = reverse('api:userbadge-list')
        username = 'nonexistentuser'

        # Effectuer une requête GET avec un nom d'utilisateur inexistant en tant que paramètre
        response = self.client.get(url, {'username': username})

        # Vérifier que la réponse a un code de statut HTTP 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérifier que la réponse ne contient aucun objet UserBadge car l'utilisateur n'existe pas
        self.assertEqual(len(response.data), 0)

    def test_user_badge_detail(self):
        # Créer une URL pour la vue UserBadgeDetail avec le nom d'utilisateur et le nom du badge en tant que paramètres
        url = reverse('api:userbadge-detail')
        username = 'testuser'
        badge_name = 'TestBadge'

        # Effectuer une requête GET avec le nom d'utilisateur et le nom du badge en tant que paramètres
        response = self.client.get(url, {'username': username, 'badge_name': badge_name})

        # Vérifier que la réponse a un code de statut HTTP 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérifier que les données de la réponse correspondent aux données de l'objet UserBadge créé
        self.assertEqual(response.data['user']['username'], self.user.username)
        self.assertEqual(response.data['badge']['name'], badge_name)

    def test_user_badge_detail_user_not_found(self):
        # Créer une URL pour la vue UserBadgeDetail avec un nom d'utilisateur inexistant et le nom du badge en tant que paramètres
        url = reverse('api:userbadge-detail')
        username = 'nonexistentuser'
        badge_name = 'TestBadge'

        # Effectuer une requête GET avec un nom d'utilisateur inexistant et le nom du badge en tant que paramètres
        response = self.client.get(url, {'username': username, 'badge_name': badge_name})

        # Vérifier que la réponse a un code de statut HTTP 404 (Non trouvé) car l'utilisateur n'existe pas
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_badge_detail_badge_not_found(self):
        # Créer une URL pour la vue UserBadgeDetail avec le nom d'utilisateur et un nom de badge inexistant en tant que paramètres
        url = reverse('api:userbadge-detail')
        username = 'testuser'
        badge_name = 'NonexistentBadge'

        # Effectuer une requête GET avec le nom d'utilisateur et un nom de badge inexistant en tant que paramètres
        response = self.client.get(url, {'username': username, 'badge_name': badge_name})

        # Vérifier que la réponse a un code de statut HTTP 404 (Non trouvé) car le badge n'existe pas
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
