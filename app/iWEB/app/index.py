from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Location, Item, UserProfile
from .forms import LocationForm
from .utils.mapUtilities import read_map

def main(request):
    """This is the main page - everything but the login/register screen should be in this view going forward"""

    #add location
    submitted = False
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/addLocation?submitted=True') #This should probably be changed to avoid redirects to a dead page
    else:
        form = LocationForm
        if 'submitted' in request.GET:
            submitted = True
    form = LocationForm

    #context setup
    fountain_locations = Location.objects.filter(type='Fountain')
    bus_stop_locations = Location.objects.filter(type='BusStop')
    bin_locations = Location.objects.filter(type='Bin')
    
    fountain_coordinates = []
    bus_stop_coordinates = []
    bin_coordinates = []
    
    for fountain in fountain_locations:
        fountain_coordinates.append([fountain.latitude, fountain.longitude, fountain.building, fountain.information])
    for bus_stop in bus_stop_locations:
        bus_stop_coordinates.append([bus_stop.latitude, bus_stop.longitude, bus_stop.building, bus_stop.information])
    for bin in bin_locations:
        bin_coordinates.append([bin.latitude, bin.longitude, bin.building, bin.information])
    
    map = read_map()

    leaderboard_list = UserProfile.objects.values().order_by("-score")
    leaderboard_list = leaderboard_list[:5]
    for profile in leaderboard_list:
        profile["username"] = User.objects.get(pk=profile["user_id"]).username
            
    loc_list = Location.objects.values()
    item_list = Item.objects.all
    
    current_user = request.user
    current_user_data = UserProfile.objects.get(user = current_user)
    
    context = {
    'fountain_locations': fountain_coordinates,
    'bus_stop_locations': bus_stop_coordinates,
    'bin_locations': bin_coordinates,
    'maze': map,
    'points': getattr(current_user_data, "score"),
    'item_list': item_list,
    'scores': leaderboard_list,
    'closest_things': loc_list,
    'location_form': LocationForm,
    'submitted': submitted,
    'streak':'100', #get streak of current user
    'theme_colours': {'main':'#000000', 'second':'#7t12dd', 'icons':'#000000','background':'#000000'},
    'theme_dark': {'main':'999999', 'second':'333333', 'icons':'666666', 'background':'99999'},
    'theme_pink': {'main':'#ffcccc', 'second':'#993366', 'icons':'#ff9999', 'background':'#ffcccc'},
    'theme_summer':{'main':'#ffcc66', 'second':'#ff6600', 'icons':'#ff9900', 'background':'#ffcc66'},
    'theme_winter':{'main':'#99ccff', 'second':'#6699cc', 'icons':'#6656ff', 'background':'#99ccff'},
    'theme_spring':{'main':'#ccff99', 'second':'#66cc99', 'icons':'#66cc99', 'background':'#ccff99'},
    'theme_autumn':{'main':'#ffcc99', 'second':'#cc6800', 'icons':'cc6800', 'background':'ffcc99'},
    } 
    print(bin_coordinates)
    return render(request, 'index.html', context)