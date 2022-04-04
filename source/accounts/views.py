from django.contrib.auth import login
from django.shortcuts import render, redirect



from accounts.forms import MyUserCreateForm


def register_view(request):
    form = MyUserCreateForm()
    if request.method == 'POST':
        form = MyUserCreateForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            url = request.GET.get('next')
            if url:
                return redirect(url)
            return redirect('webapp:home_page')
    return render(request, 'registration/registration.html', {'form' : form})