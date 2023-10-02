# badge_assigner.py
import schedule
import time
from base.models import UserBadge, Badge,Model3D
from django.contrib.auth.models import User
from django.utils import timezone



def assign_pionneer_badge():
    one_year_ago = timezone.now() - timezone.timedelta(days=365)
    eligible_users = User.objects.filter(date_joined__lte=one_year_ago)

    pionneer_badge, _ = Badge.objects.get_or_create(
            name='pionneer',
            description='User is a pioneer on the site.',
            criteria = 'pioneer_criteria')
    try:
        for user in eligible_users:
            if not UserBadge.objects.filter(user=user, badge__name='pionneer').exists():
                UserBadge.objects.create(user=user, badge=pionneer_badge)
                print(f'Successfully assigned "Pionneer" badge to user {user.username}.')

        return True
    except:
        return False
                

def assign_star_badge():
    
    models_with_high_views = Model3D.objects.filter(views_count=1000)
    star_badge, _ = Badge.objects.get_or_create(name='star', description='Model has more than 1000 views', criteria='star_criteria')
    
# Maintenant, vous pouvez parcourir les modèles avec leurs utilisateurs associés
    try:
        for model in models_with_high_views:
            if not UserBadge.objects.filter(user=model.author, badge=star_badge).exists():
                user = model.author
                UserBadge.objects.create(user=user, badge=star_badge)
                print(f'Successfully assigned "Star" badge to user {user.username}.')

        return True
    
    except Exception as e:

        return False



# Planifiez l'exécution de la fonction toutes les 24 heures

#schedule.every(30).seconds.do(assign_pionneer_badge)
#schedule.every(30).seconds.do(assign_star_badge)

#while True:
    #schedule.run_pending()
    #time.sleep(5)  # Attendez 60 secondes avant de vérifier à nouveau
