from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from plants.models import Plant
from plants.entities import RichPlant
from plants.services import check_is_user_owner_of_plant
from .services import generate_labels_pdf

@login_required
def get_labels_pdf(request):

    # processing user data
    if request.method == 'POST':

        if request.POST['plant_ids']:
            plant_ids = request.POST.getlist('plant_ids')

        current_user = request.user

        plants = Plant.objects.filter(id__in=plant_ids)
        rich_plants = []
        for plant in plants: 
            rich_plants.append(RichPlant(plant))

        # check access (is owner) for all plants
        for rich_plant in rich_plants: 
            user_is_owner = check_is_user_owner_of_plant(current_user, rich_plant)
            if not user_is_owner:
                return HttpResponseForbidden()

        
        # generate pdf and take path to it
        path_to_pdf = generate_labels_pdf(rich_plants)
        if path_to_pdf:
            filename = 'user_labels.pdf'
            pdf_file = open(path_to_pdf, 'rb')
            response = HttpResponse(content=pdf_file)
            response['Content-Type'] = 'application/pdf'
            response['Content-Disposition'] = 'attachment; filename="%s.pdf"' % filename
            return response

    
    else:
        return Http404("No plants was received")
