from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Location, Item, UserProfile
from .forms import LocationForm, ThemeChangeForm
from .utils.mapUtilities import read_map
import json

def setTheme(themeName):
    print(themeName)


def main(request):
    """This is the main page - everything but the login/register screen should be in this view going forward"""
    # add location
    # load user info from request
    current_user = request.user
    current_user_data = UserProfile.objects.get(user = current_user)
    
    #add location
    submitted = False
    if request.method == "POST":
        data = json.loads(request.body)
        points = data.get("points")
        current_user_data.score += points
        current_user_data.save()

        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/addLocation?submitted=True') #This should probably be changed to avoid redirects to a dead page
    else:
        form = LocationForm
        if 'submitted' in request.GET:
            submitted = True
    
    # context setup
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
    

    themes = {
        'default':{'name':'default','main':'#3776ac', 'second':'#7a12dd', 'icons':'#3776ac','background':'#ffffff','font':'#ffffff'},
        'first':{'name':'first','main':'#ffcccc', 'second':'#993366', 'icons':'#ff9999', 'background':'#ffcccc','font':'#ffffff'},
        'second':{'name':'second','main':'#ffcc66', 'second':'#ff6600', 'icons':'#ff9900', 'background':'#ffcc66','font':'#ffffff'},
        'third':{'name':'third','main':'#99ccff', 'second':'#6699cc', 'icons':'#6656ff', 'background':'#99ccff','font':'#ffffff'},
        'fourth':{'name':'fourth','main':'#ccff99', 'second':'#66cc99', 'icons':'#66cc99', 'background':'#ccff99','font':'#ffffff'},
        'fifth':{'name':'fifth','main':'#ffcc99', 'second':'#cc6800', 'icons':'cc6800', 'background':'ffcc99','font':'#ffffff'},
    }

    totalThemes = ['default','first','second','third','fourth','fifth']
    ownedThemes = current_user_data.owned_templates
    themeList = themes
    counter = 0
    for counter in range(0,4):
        if totalThemes[counter] not in ownedThemes:
            themeList.popitem(totalThemes[counter])
        counter += 1
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
    'streak':current_user_data.streak, #get streak of current user
    'themes': themeList,
    'colour': themes[current_user_data.current_template],
    }

    print(bin_coordinates)
    return render(request, 'index.html', context)