from django import forms
from django.contrib.auth import (
		authenticate,
		get_user_model,
		login,
		logout,
	)

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)


	def clean(self,*args,**kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		user = authenticate(username=username,password=password)
		if username and password:
			if not user:
				raise forms.ValidationError("This user does not exists.")
			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")
			if not user.is_active:
				raise forms.ValidationError("This user is not longer active.")

		return super(UserLoginForm,self).clean(*args,**kwargs)



class UserRegisterForm(forms.ModelForm):
	email = forms.EmailField(label='Email Address')
	email2 = forms.EmailField(label="Confirm Email")
	password = forms.CharField(widget = forms.PasswordInput)
	
	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'email2',
			'password',

		]


	def clean_email2(self):
		email = self.cleaned_data.get("email")
		email2 = self.cleaned_data.get("email2")
		if email != email2:
			raise forms.ValidationError("Emails must match")
		email_qs = User.objects.filter()
		return email
