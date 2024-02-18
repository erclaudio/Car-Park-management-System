from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def register(requests):
	if requests.method == 'POST':
		form = UserRegisterForm(requests.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(requests, f'Account created for {username}! You can now login')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(requests, 'users/register.html',  {'form': form})

@login_required
def profile(requests):
	if requests.method == 'POST':
		u_form = UserUpdateForm(requests.POST, instance=requests.user)
		p_form = ProfileUpdateForm(requests.POST,
								   requests.FILES,
								   instance=requests.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(requests, f'Your account has been updated')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=requests.user)
		p_form = ProfileUpdateForm(instance=requests.user.profile)


	context = {
		'u_form' : u_form,
		'p_form' : p_form
	}
	return render(requests, 'users/profile.html', context)

