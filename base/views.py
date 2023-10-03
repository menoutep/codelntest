from django.shortcuts import render, redirect
from base.models import Model3D
from base.forms import Model3DForm
from accounts.models import MyCustomUser
from django.core.paginator import Paginator
from base.badge_assigner import assign_pionneer_badge,assign_star_badge
# Create your views here.
def home(request):
    models = Model3D.objects.all().order_by('-created_at')
    assign_pionneer_badge()
    paginator = Paginator(models, 10)  #  10 actualités par page
    page = request.GET.get('page')
    models = paginator.get_page(page)

    context = {'models':models}
  
    return render (request, 'base/home.html',context)

 
def create_model3d(request):
    if request.method == 'POST':
        form = Model3DForm(request.POST, request.FILES)
  
        if form.is_valid():
            # Créez une instance de Model3d à partir des données du formulaire
            model3d = form.save(commit=False)
            model3d.author = request.user  # Assurez-vous d'attribuer le propriétaire actuel de la session
            model3d.save()
            if MyCustomUser.objects.filter(user=request.user).exists() : 
                my_custom_user = MyCustomUser.objects.get(user=request.user)
                
                my_custom_user.increment_upload_count()
                my_custom_user.award_badge()
            return redirect('base:home')  # Redirigez vers la page de détail du modèle 3D créé
    else:
        form = Model3DForm()

    return render(request, 'base/create_model3d.html', {'form': form})


def detail_model(request,pk):
    model = Model3D.objects.get(id=pk)
    model.increment_views()
    assign_star_badge()

    context ={'model':model}

    return render(request, 'base/detail.html',context )
