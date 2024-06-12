from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, PreferenceForm
from .models import User, Preference

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('preferences', user_id=user.id)
    else:
        form = UserForm()
    return render(request, 'registration/register.html', {'form': form})

def preferences(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        preference = Preference.objects.get(user=user)
    except Preference.DoesNotExist:
        preference = None

    if request.method == 'POST':
        form = PreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            pref = form.save(commit=False)
            pref.user = user
            pref.save()
            return redirect('suggestions', user_id=user.id)
    else:
        form = PreferenceForm(instance=preference)
    return render(request, 'registration/preferences.html', {'form': form})

def suggestions(request, user_id):
    user = get_object_or_404(User, id=user_id)
    preferences = Preference.objects.filter(user=user).first()
    if preferences:
        suggestions = User.objects.filter(
           
            age__gte=preferences.age_min,
            age__lte=preferences.age_max
        ).exclude(id=user_id)
        
        suggestions = [s for s in suggestions if preferences.description_partner in s.description]
    else:
        suggestions = User.objects.none()
    
    # Debugging: Print suggestions to the console
    print(f"User: {user}")
    print(f"Preferences: {preferences}")
    print(f"Suggestions: {suggestions}")

    return render(request, 'registration/suggestions.html', {'suggestions': suggestions})

from django.shortcuts import render
from .models import User

def user_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, 'registration/user_profile.html', {'user': user})
