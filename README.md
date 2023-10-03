le projet est divisé en trois applications. 
une application accounts : ayant pour role la gestion des utilisateurs , la logique pour l'attribution du badge collector ese trouve dans cette partie.
une application base : ayant pour role la gestion de la logique du projet(affichage des modele3D, page de detail d'un modele et un formulaire de creation pour les model3D, attribution des badge pionneer et star)
une application api : ayant pour role la gestion de la logique de l'api (liste des badges d'un utilisateur, liste de tout les badges)

Chaque application a ses test ecris dans le fichier test.py se trouvant dans chaque application.
Pour demarrer le projet : 
-telecharger le projet
-installer django 4.2
-installer django-rest-framework
-python manage.py runserver pour lancer le projet
-python manage.py test (pour lancer les test )
j'ai utilisé une base donnée sqlite, pas donc de configuration requise au niveau de la bd.

