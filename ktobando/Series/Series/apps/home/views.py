from django.shortcuts import render_to_response
from django.template import RequestContext
from Series.apps.home.forms import *
from Series.apps.home.models import Manga,Editorial,Genero,Idioma, Series, Marca, Figuras
from Series.apps.home.forms import login_form
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage,InvalidPage

def index_view (request) :
	return render_to_response('home/index.html', context_instance = RequestContext(request))

def single_series_view(request, id_prod):
	prod = Series.objects.get(id = id_prod)
	ctx = {'series':prod}
	return render_to_response('home/single_series.html',ctx,context_instance = RequestContext(request))


def single_figuras_view(request, id_prod):
	prod = Figuras.objects.get(id = id_prod)
	ctx = {'figuras':prod}
	return render_to_response('home/single_figuras.html',ctx,context_instance = RequestContext(request))


def single_manga_view(request, id_prod):
	prod = Manga.objects.get(id = id_prod)
	ctx = {'manga':prod}
	return render_to_response('home/single_manga.html',ctx,context_instance = RequestContext(request))


def series_view(request, pagina):
	lista_prod = Series.objects.filter(status = True)
	paginator = Paginator(lista_prod, 3)
	try:
		page = int(pagina)
	except:
		page = 1
	try:
		series = paginator.page(page)
	except (EmptyPage,InvalidPage):
		series = paginator.page(paginator.num_pages)

	ctx = {"series":series}
	return render_to_response ('home/series.html', ctx, context_instance = RequestContext(request))


def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else: 
		if request.method == "POST":
			formulario = login_form(request.POST)
			if formulario.is_valid():
				usu = formulario.cleaned_data['usuario']
				pas = formulario.cleaned_data['clave']
				usuario = authenticate(username = usu, password = pas)
				if usuario is not None and usuario.is_active:
					login(request, usuario)
					return HttpResponseRedirect('/')
				else:
					mensaje = "usuario y/o clave incorrecta"
		formulario = login_form()
		ctx = {'form':formulario, 'mensaje':mensaje}
		return render_to_response('home/login.html', ctx, context_instance = RequestContext(request))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def register_view(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			usuario = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			u = User.objects.create_user(username=usuario,email=email,password=password_one)
			u.save()
			return render_to_response('home/thanks_register.html',context_instance=RequestContext(request))
		else:
			ctx = {'form':form}
			return render_to_response('home/register.html',ctx,context_instance=RequestContext(request))
	ctx = {'form':form}
	return render_to_response('home/register.html', ctx,context_instance=RequestContext(request))

