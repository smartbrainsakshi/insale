from django import forms


class AdForm(forms.Form):
	fcat= forms.CharField(max_length=50)
	fdesc = forms.CharField(max_length=200)
	ftitle = forms.CharField(max_length=50)
	
	fprice= forms.CharField(max_length=50)
	fname = forms.CharField(max_length=50)
	fmobile= forms.CharField(max_length=50)
	flocation= forms.CharField(max_length=50)
	femail = forms.EmailField(max_length=50)
	fdate=forms.CharField(max_length=50)
	froom= forms.CharField(max_length=50)
	pica=forms.FileField(widget=forms.FileInput(attrs={'required':'yes'}))	
	picb=forms.FileField(widget=forms.FileInput(attrs={'required':'yes'}))	
	picc=forms.FileField(widget=forms.FileInput(attrs={'required':'yes'}))	




class CatForm(forms.Form):
	location=forms.CharField(max_length=50)
	category=forms.CharField(max_length=50)



class ProdForm(forms.Form):
	fcat= forms.CharField(max_length=50)
	fdesc = forms.CharField(max_length=200)
	ftitle = forms.CharField(max_length=50)
	
	fprice= forms.CharField(max_length=50)
	fname = forms.CharField(max_length=50)
	fmobile= forms.CharField(max_length=50)
	flocation= forms.CharField(max_length=50)
	femail = forms.EmailField(max_length=50)
	fdate=forms.CharField(max_length=50)
	froom= forms.CharField(max_length=50)




class FeedForm(forms.Form):
	fmail= forms.EmailField(max_length=50)
	fname = forms.CharField(max_length=200)
	flname= forms.CharField(max_length=50)
	
	fmsg= forms.CharField(max_length=200)



class NameForm(forms.Form):
	fsearch= forms.CharField(max_length=50)




class LoginForm(forms.Form):
	fail=forms.CharField(label="Email",max_length=50,widget=forms.TextInput(attrs={'class':'form-control','required':'yes'}))
	fswd=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control','required':'yes'}))