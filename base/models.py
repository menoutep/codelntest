from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Model3D(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom du modèle")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    image = models.ImageField(upload_to='model3d_images/', verbose_name="Image 3D")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de vues")  # Champ pour le nombre de vues

    def __str__(self):
        return self.name

    def increment_views(self):
        
        self.views_count += 1
        self.save()

    class Meta:
        verbose_name = "Modèle 3D"
        verbose_name_plural = "Modèles 3D"



class Badge(models.Model):
    # Champ pour le nom du badge
    name = models.CharField(max_length=255)
    
    # Champ pour la description du badge
    description = models.TextField()
    
    # Champ pour les critères d'attribution du badge
    criteria = models.TextField()
    
    def __str__(self):
        return self.name
    
    def criteria_check(self, user):
        # Vérifiez si l'utilisateur répond aux critères du badge
        if self.criteria == 'pioneer_criteria':
            # Si le badge est attribué aux pionniers (inscrits depuis plus d'un an)
            one_year_ago = timezone.now() - timezone.timedelta(days=365)
            print(one_year_ago)
            print(user.date_joined)
            return user.date_joined <= one_year_ago
        # Ajoutez d'autres critères ici si nécessaire

        return False  # Par défaut, le badge n'est pas attribué


class UserBadge(models.Model):
    # Champ pour l'utilisateur qui a obtenu le badge
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Champ pour le badge obtenu par l'utilisateur
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    
    # Champ pour la date à laquelle le badge a été obtenu
    date_awarded = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"
