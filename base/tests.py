from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from base.models import Model3D,UserBadge,Badge
from django.utils import timezone
from accounts.models import MyCustomUser
import time

class CreateModel3DViewWithNewUserTestCase(TestCase):
    def setUp(self):
        signup_url = reverse('accounts:signup')
        response = self.client.post(signup_url, {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Devrait rediriger après la création de l'utilisateur
        self.user_ = User.objects.create_user(
            username='user',
            password='password'     
        )
        self.user_pioneer = User.objects.create_user(
            username='pioneeruser',
            password='password',
            date_joined=timezone.now() - timezone.timedelta(days=365)  # Un an en arrière
        )
        user_bagde_pionner_count = UserBadge.objects.filter(user=self.user_pioneer,badge__name='pionneer').count()
        self.assertEqual(user_bagde_pionner_count, 0)
        model_ = Model3D.objects.create(name='Model with high views', author=self.user_ ,image='post2.jpg')
        model_.save()
        # Connectez-vous avec le nouvel utilisateur
        login_url = reverse('accounts:login')
        response = self.client.post(login_url, {
            'username': 'testuser',
            'password': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)
    def test_create_model3d_view_with_new_user(self):
  
        
        create_model3d_url = reverse('base:create_model3d')
        with open('media/model3d_images/post1.jpg', 'rb') as image_file:
    # Lire le contenu du fichier en bytes
            
            response = self.client.post(create_model3d_url, {
                'name': 'Test Model',
                'description': 'Test description',
                'image': image_file,
            })
            self.assertEqual(response.status_code, 302)  # Devrait rediriger après la création du modèle
            self.assertTrue(Model3D.objects.filter(name='Test Model', author=response.wsgi_request.user).exists())
            self.assertTrue(MyCustomUser.objects.filter(user=response.wsgi_request.user).exists())
            my_custom_user = MyCustomUser.objects.get(user=response.wsgi_request.user)
            self.assertEqual(my_custom_user.upload_count, 1)  # Vérifiez si le compteur d'uploads a été incrémenté
            user_bagde_pionner_count = UserBadge.objects.filter(user=self.user_pioneer,badge__name='pionneer').count()
            
            self.assertEqual(user_bagde_pionner_count, 0)

    def test_award_collector_bagde(self):
        # Créez un nouvel utilisateur via la vue signup
        # Créez un fichier factice à télécharger
       
        create_model3d_url = reverse('base:create_model3d')
        for i in range(1,7,1):
            file=f'media/model3d_images/post{i}.jpg'
            with open(file, 'rb') as image_file:
        # Lire le contenu du fichier en bytes
                name = f'Test Model{i}2'
                response = self.client.post(create_model3d_url, {
                    'name': name,
                    'description': 'Test description',
                    'image': image_file,
                })
                self.assertEqual(response.status_code, 302)  # Devrait rediriger après la création du modèle
                self.assertTrue(Model3D.objects.filter(name=name, author=response.wsgi_request.user).exists())
        self.assertTrue(Badge.objects.filter(name="collector").exists())

        self.assertTrue(UserBadge.objects.filter(user=response.wsgi_request.user, badge__name='collector').exists())
        user_bagde_pionner_count = UserBadge.objects.filter(user=self.user_pioneer,badge__name='pionneer').count()
        self.assertEqual(user_bagde_pionner_count, 0)
    def test_award_start_badge(self):
        home_url = reverse('base:home')
        for i in range(1,1005):
            response = self.client.get(home_url)
            self.assertEqual(response.status_code, 200)

        time.sleep(5)
        self.assertTrue(Badge.objects.filter(name="star").exists())
        self.assertTrue(UserBadge.objects.filter(badge__name='star').exists())
        user_bagde_pionner_count = UserBadge.objects.filter(user=self.user_pioneer,badge__name='pionneer').count()

        self.assertEqual(user_bagde_pionner_count, 1)
    def test_award_pionneer_badge(self):
        home_url = reverse('base:home')
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Badge.objects.filter(name="pionneer").exists())
        self.assertTrue(UserBadge.objects.filter(user=self.user_pioneer,badge__name='pionneer').exists())
        user_bagde_pionner_count = UserBadge.objects.filter(user=self.user_pioneer,badge__name='pionneer').count()
        self.assertEqual(user_bagde_pionner_count, 1)

        


