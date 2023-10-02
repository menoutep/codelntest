from django.db import models
from django.utils import timezone
# Create your models here.
from django.db import models
from base.models import Badge,UserBadge
from django.contrib.auth.models import User

class MyCustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    upload_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de vues")  # Champ pour le nombre de fichiers uploadé

    # Ajoutez d'autres champs personnalisés si nécessaire

    def __str__(self):
        return self.user.username
    
    def check_upload(self):
        if self.upload_count<=5:
            return False
        else:
            print(self.upload_count)
            return True
        
    def increment_upload_count(self):
        
        self.upload_count += 1
        print(self.upload_count)
        self.save()
    
        
    def award_badge(self):
        
        if self.check_upload():
            if not UserBadge.objects.filter(user=self.user, badge__name='collector').exists():
                badge_collector,created = Badge.objects.get_or_create(name="collector")
                if created :
                    badge_collector.save()
                user_badge_collector = UserBadge.objects.create(user=self.user,badge=badge_collector)
                user_badge_collector.save()  
                print(f'Successfully assigned "Collector" badge to user {self.user.username}.')
             

  