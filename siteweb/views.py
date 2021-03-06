from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.conf import settings
from siteweb.models import Caracteristiques
from siteweb.models import Equipement
from siteweb.models import Objet
from siteweb.models import Inventaire
from siteweb.models import Inventaire
from siteweb.models import Prof_TP
from siteweb.models import Shop
from siteweb.models import Competence_Module
from siteweb.models import Etudiant_TP
from siteweb.models import Module
from siteweb.models import Prof
from siteweb.models import Combat
from PIL import ImageTk, Image
from django.db.models import Value
from django.db.models import Max
from django.db.models.functions import Replace
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import random
from django.utils import timezone
from django.contrib import messages
from django.http import JsonResponse
import json
import os.path
from django.contrib.staticfiles import finders
from ryntel.settings import SITE_ROOT
import time
import requests
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator

def etudiant_check(user):
    return user.id and Caracteristiques.objects.filter(id_id=user.id).count() > 0

def prof_check(user):
    return user.id and Prof.objects.filter(id_id=user.id).count() > 0

class reload_sprite_profile():
  def reload(id,f):
    start = time.time()
    if(f!=5):
      background = Image.open(os.path.join(SITE_ROOT,'static','img','sprites','homme_corps','homme-f'+str(f)+'-fullbody.png'))
      background.draft('RGB',(300,400))   
      cheveux = Image.open(os.path.join(SITE_ROOT,'static','img','sprites','cheveux',"cheveux-t3-f"+str(f)+".png"))
      cheveux.draft('RGB',(300,400))   
      background.paste(cheveux, (0, 0), cheveux)
      if(Equipement.objects.get(id_id=id).casque != -1):
        casque = Image.open(os.path.join(SITE_ROOT,'static','img','sprites','casque',str(Objet.objects.get(id=Equipement.objects.get(id_id=id).casque).nom)+"-f"+str(f)+".png"))
        casque.draft('RGB',(300,400))   
        background.paste(casque, (0, 0), casque)
      if(Equipement.objects.get(id_id=id).pantalon != -1):
        jambiere = Image.open(os.path.join(SITE_ROOT,'static','img','sprites','jambiere',str(Objet.objects.get(id=Equipement.objects.get(id_id=id).pantalon).nom)+"-f"+str(f)+".png"))
        jambiere.draft('RGB',(300,400))  
        background.paste(jambiere, (0, 0), jambiere)
      if(Equipement.objects.get(id_id=id).armure != -1):
        plastron = Image.open(os.path.join(SITE_ROOT,'static','img','sprites','plastron',str(Objet.objects.get(id=Equipement.objects.get(id_id=id).armure).nom)+"-f"+str(f)+".png"))
        plastron.draft('RGB',(300,400))  
        background.paste(plastron, (0, 0), plastron)
      if(Equipement.objects.get(id_id=id).chaussures != -1):
        chaussures = Image.open(os.path.join(SITE_ROOT,'static','img','sprites','bottes',str(Objet.objects.get(id=Equipement.objects.get(id_id=id).chaussures).nom)+"-f"+str(f)+".png"))
        chaussures.draft('RGB',(300,400))  
        background.paste(chaussures, (0, 0), chaussures)
      if(Equipement.objects.get(id_id=id).arme != -1):
        arme = Image.open(os.path.join(SITE_ROOT,'static','img','sprites','epee',str(Objet.objects.get(id=Equipement.objects.get(id_id=id).arme).nom)+"-f"+str(f)+".png"))
        arme.draft('RGB',(300,400))
        background.paste(arme, (0, 0), arme)
      print("save: ", time.time() - start)
      background.save(os.path.join(SITE_ROOT,"static","img","sprites","user",id+"-f"+str(f)+".png"))
      print("loading: ", time.time() - start)
    else:
      background = Image.open(os.path.join(SITE_ROOT,'static','img','sprites','homme_corps','homme-f1-bis-fullbody.png'))
      background.draft('RGB',(300,400))   
      cheveux = Image.open(os.path.join(SITE_ROOT,'static','img','sprites','cheveux',"cheveux-t3-f1-bis.png"))
      cheveux.draft('RGB',(300,400))   
      background.paste(cheveux, (0, 0), cheveux)
      if(Equipement.objects.get(id_id=id).casque != -1):
        casque = Image.open(os.path.join(SITE_ROOT,'static','img','sprites','casque',str(Objet.objects.get(id=Equipement.objects.get(id_id=id).casque).nom)+"-f1-bis.png"))
        casque.draft('RGB',(300,400))   
        background.paste(casque, (0, 0), casque)
      if(Equipement.objects.get(id_id=id).pantalon != -1):
        jambiere = Image.open(os.path.join(SITE_ROOT,'static','img','sprites','jambiere',str(Objet.objects.get(id=Equipement.objects.get(id_id=id).pantalon).nom)+"-f1-bis.png"))
        jambiere.draft('RGB',(300,400))  
        background.paste(jambiere, (0, 0), jambiere)
      if(Equipement.objects.get(id_id=id).armure != -1):
        plastron = Image.open(os.path.join(SITE_ROOT,'static','img','sprites','plastron',str(Objet.objects.get(id=Equipement.objects.get(id_id=id).armure).nom)+"-f1-bis.png"))
        plastron.draft('RGB',(300,400))  
        background.paste(plastron, (0, 0), plastron)
      if(Equipement.objects.get(id_id=id).chaussures != -1):
        chaussures = Image.open(os.path.join(SITE_ROOT,'static','img','sprites','bottes',str(Objet.objects.get(id=Equipement.objects.get(id_id=id).chaussures).nom)+"-f1-bis.png"))
        chaussures.draft('RGB',(300,400))  
        background.paste(chaussures, (0, 0), chaussures)
      if(Equipement.objects.get(id_id=id).arme != -1):
        arme = Image.open(os.path.join(SITE_ROOT,'static','img','sprites','epee',str(Objet.objects.get(id=Equipement.objects.get(id_id=id).arme).nom)+"-f1-bis.png"))
        arme.draft('RGB',(300,400))
        background.paste(arme, (0, 0), arme)
      print("save: ", time.time() - start)
      background.save(os.path.join(SITE_ROOT,"static","img","sprites","user",id+"-f1-bis.png"))
      print("loading: ", time.time() - start)


# Create your views here.
def index(request):
    return render(request, 'index.html')

class LoginView(TemplateView):

  template_name = 'index.html'

  def post(self, request, **kwargs):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    r = requests.post(url = "http://iic0e.univ-littoral.fr/moodle/login/index.php" , data = {'username': username,'password' : password, 'rememberusername':1}, allow_redirects=False) 
    if(r.status_code == 303):
      user = authenticate(username=username, password=password)
      if user is not None and user.is_active:
          if(Caracteristiques.objects.filter(id_id=user.id).count() > 0):
            login(request, user)
            messages.success(request, 'Connexion réussie')
            return HttpResponseRedirect( settings.LOGIN_REDIRECT_URL_ETU )
          else:
            messages.error(request, "Vous n'êtes pas élève!")
      else: #si l'user n'est pas inscrit, on créer un compte
        info = username.split(".")
        user = User.objects.create_user(username=username, email=info[1]+"."+info[0]+"@etu.univ-littoral.fr", password=password, first_name = info[1], last_name=info[0])
        user.save()
        user = User.objects.create_user(username=username, email=username+"@etu.univ-littoral.fr", password=password)
        user.save()
        car = Caracteristiques(id=User.objects.get(id=user.id),niveau=1, gold=100, attaque=0, defense=0, vitesse=90, precision=90, effet=0, last_attack='2020-01-01',exp=100)
        car.save()
        shop = Shop(id=User.objects.get(id=user.id),objet0=-1, objet1=-1, objet2=-1, objet3=-1 ,objet4=-1, objet5=-1, dateupdate='2020-01-01')
        shop.save()
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.success(request, 'Votre compte a bien été créer')
            return HttpResponseRedirect( settings.LOGIN_REDIRECT_URL_ETU )
    else:
        messages.error(request, 'Mauvais mot de passe moodle')
    return render(request, self.template_name)

class LoginProfView(TemplateView):
  template_name = 'index.html'
  def post(self, request, **kwargs):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    r = requests.post(url = "http://iic0e.univ-littoral.fr/moodle/login/index.php" , data = {'username': username,'password' : password, 'rememberusername':1}, allow_redirects=False) 
    if(r.status_code == 303):
      user = authenticate(username=username, password=password)
      if user is not None and user.is_active:
          if(Prof.objects.filter(id_id=user.id).count() > 0):
            login(request, user)
            messages.success(request, 'Connexion réussie')
            return HttpResponseRedirect( settings.LOGIN_REDIRECT_URL_PROF )
          else:
            messages.error(request, "Bien essayé, mais vous n'êtes pas prof")
      else: #si l'user n'est pas inscrit, on créer un compte
        messages.error(request, "Votre compte prof n'est pas actif sur Jenky, veuillez contacter un administrateur")
    else:
        messages.error(request, 'Mauvais mot de passe moodle')
    return render(request, self.template_name)

class LogoutView(TemplateView):
  template_name = 'index.html'
  def get(self, request, **kwargs):
    logout(request)
    return render(request, self.template_name)

class IndexView(TemplateView):
  template_name = "dashboard/index.html"
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)
  def get(self, request, **kwargs):
    caracteristiques = Caracteristiques.objects.get(id_id=request.user.id)
    return render(request, self.template_name, {'caracteristiques' : caracteristiques})

class ProfView(TemplateView):
  def get(self, request, **kwargs):
    modules = Prof_TP.objects.filter(prof_id=request.user.id)
    objectif = Competence_Module.objects.all()
    competence=[]
    for i in modules:
      print(i.nom_module_id)
      competence.append([i.id,Competence_Module.objects.filter(nom_module_id=i.nom_module_id).distinct("nom_competence").count()])
    return render(request, 'prof/index.html', {'modules':modules,'competence':competence,'objectif':objectif}) 

class ApiProf(TemplateView):
  @method_decorator(user_passes_test(prof_check))
  def dispatch(self, *args, **kwargs):
    return super(ApiProf, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs):
    if request.POST.get('toDownload') == 'module':
      print (request.POST.get('valeur'))
      module = Module.objects.get(nom_module=request.POST.get('valeur'))
      objectif = Competence_Module.objects.filter(nom_module_id=module.id)
      objectifs=[]
      for i in objectif:
        if([i.nom_competence,i.nombre_exp_gagne] not in objectifs):
          objectifs.append([i.nom_competence,i.nombre_exp_gagne])
      tosend = {
        'objectif' : objectifs,
        'nom_module' : module.nom_module,
      }
    elif request.POST.get('toDownload') == 'objectif':
      objectif=Competence_Module.objects.filter(nom_competence=request.POST.get('valeur'))
      etudiant=[]
      for i in objectif:
        nom_etu = User.objects.get(id=i.etudiant_id).last_name
        prenom_etu = User.objects.get(id=i.etudiant_id).first_name
        etudiant.append([nom_etu,prenom_etu,i.valide])
      tosend = {
        'nom_objectif' : request.POST.get('valeur'),
        'etudiant' : etudiant,
      }
    elif request.POST.get('toDownload') == 'valider':
      objectif = request.POST.get('obj')
      last_name = request.POST.get('name').split('.')[0]
      first_name = request.POST.get('name').split('.')[1]
      us = User.objects.get(first_name = first_name, last_name=last_name)
      Competence_Module.objects.filter(nom_competence=objectif,etudiant_id=us.id).update(valide=True)
      tosend={'ok':'ok'}
    elif request.POST.get('toDownload') == 'refuser':
      objectif = request.POST.get('obj')
      last_name = request.POST.get('name').split('.')[0]
      first_name = request.POST.get('name').split('.')[1]
      us = User.objects.get(first_name = first_name, last_name=last_name)
      Competence_Module.objects.filter(nom_competence=objectif,etudiant_id=us.id).update(valide=False)
      tosend={'ok':'ok'}
    return JsonResponse(tosend, safe=False)
  def get(self, request, **kwargs):
    return render(request, 'dashboardProf/empty.html') 

class AjouterObjectif(TemplateView):
  @method_decorator(user_passes_test(prof_check))
  def dispatch(self, *args, **kwargs):
        return super(AjouterObjectif, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs):
    objectif = request.POST.get('objectif')
    experience = request.POST.get('experience')
    module = request.POST.get('module')
    etudiant = Etudiant_TP.objects.filter(nom_module_id=Module.objects.get(nom_module=module).id)
    to_send = []
    for i in etudiant:
      ajoutBDD = Competence_Module(nom_competence=objectif,nombre_exp_gagne=experience,valide=False,etudiant_id=i.etudiant_id,nom_module_id=Module.objects.get(nom_module=module).id)
      ajoutBDD.save()
    return JsonResponse("{'ok':'ok'}", safe=False)

class MonJenkyView(TemplateView):
  template_name = "dashboard/monjenky.html"
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(MonJenkyView, self).dispatch(*args, **kwargs)
  def get(self, request, **kwargs):
    list = {}
    caracteristiques = Caracteristiques.objects.get(id_id=request.user.id)
    list.update({'caracteristiques' : caracteristiques})
    try:
      obj = Equipement.objects.get(id_id=request.user.id)
      list.update({'obj' : obj})
      casque = Objet.objects.get(id=obj.casque)
      list.update({'casque' : casque})
      armure = Objet.objects.get(id=obj.armure)
      list.update({'armure' : armure})
      pantalon = Objet.objects.get(id=obj.pantalon)
      list.update({'pantalon' : pantalon})
      chaussures = Objet.objects.get(id=obj.chaussures)
      list.update({'chaussures' : chaussures})
      arme = Objet.objects.get(id=obj.arme)
      list.update({'arme' : arme})
      idinv = Inventaire.objects.filter(idjoueur_id=request.user.id)
      list.update({'idinv' : idinv})
      inv = Objet.objects.filter(id__in = [objet.objet for objet in idinv] )
      list.update({'inv' : inv})
    except Exception as e:
      print("euh ah oe chaud y'a une erreur"+str(e))
    return render(request, self.template_name, list)

class MonJenkyItemVendre(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(MonJenkyItemVendre, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs): 
    if Inventaire.objects.filter(objet = request.POST.get('item'), idjoueur_id=request.user.id).delete()[0] == 1: # si on réussi à supprimer l'item, on peut rajouter des golds
      Caracteristiques.objects.filter(id=request.user.id).update(gold = Caracteristiques.objects.get(id=request.user.id).gold + Objet.objects.get(id=request.POST.get('item')).prix_vente)
      messages.success(request, 'Objet bien vendu')
    else:
      messages.error(request, 'Triche possible')
    return HttpResponseRedirect('/dashboard/monjenky/#inventaire')
  def get(self, request, **kwargs):
    return render(request, 'layouts/empty.html')

class MonJenkyItemEquip(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(MonJenkyItemEquip, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs): # Vérification si l'user n'a pas déjà un item équipé sur lui
    inv = Inventaire.objects.get(idjoueur_id=request.user.id, objet=request.POST.get('item')) # on fetch l'item qui veut equiper
    typeobjet = Objet.objects.get(id=inv.objet).typeobjet
    detailobjet = Objet.objects.get(id=inv.objet)
    stuff = Equipement.objects.get(id_id = request.user.id) # recupère le stuff du joueur
    if typeobjet == 0 : # si c'est une épée
      if not (stuff.arme >= 0): # on peut ajouter l'arme
        Equipement.objects.filter(id_id = request.user.id).update(arme=inv.objet)
        Inventaire.objects.filter(objet = request.POST.get('item'), idjoueur_id=request.user.id).delete()
        Caracteristiques.objects.filter(id_id=request.user.id).update(attaque=detailobjet.pa)
        messages.success(request, 'L\'arme a bien été équipée')
    elif typeobjet == 1 : # si c'est un casque
      if not (stuff.casque >= 0):
        Equipement.objects.filter(id_id = request.user.id).update(casque=inv.objet)
        Inventaire.objects.filter(objet = request.POST.get('item'), idjoueur_id=request.user.id).delete()
        Caracteristiques.objects.filter(id_id=request.user.id).update(defense=Caracteristiques.objects.get(id_id=request.user.id).defense+Objet.objects.get(id=Equipement.objects.get(id_id=request.user.id).casque).pd)
        Caracteristiques.objects.filter(id_id=request.user.id).update(precision=Caracteristiques.objects.get(id_id=request.user.id).precision+Objet.objects.get(id=Equipement.objects.get(id_id=request.user.id).casque).pa)
        messages.success(request, 'Le casque a bien été équipé')
    elif typeobjet == 2 : # si c'est une armure
      if not (stuff.armure >= 0):
        Equipement.objects.filter(id_id = request.user.id).update(armure=inv.objet)
        Inventaire.objects.filter(objet = request.POST.get('item'), idjoueur_id=request.user.id).delete()
        Caracteristiques.objects.filter(id_id=request.user.id).update(defense=Caracteristiques.objects.get(id_id=request.user.id).defense+Objet.objects.get(id=Equipement.objects.get(id_id=request.user.id).armure).pd)
        messages.success(request, 'L\'armure a bien été équipée')
    elif typeobjet == 3 : # si c'est un pantalon
      if not (stuff.pantalon >= 0):
        Equipement.objects.filter(id_id = request.user.id).update(pantalon=inv.objet)
        Inventaire.objects.filter(objet = request.POST.get('item'), idjoueur_id=request.user.id).delete()
        Caracteristiques.objects.filter(id_id=request.user.id).update(defense=Caracteristiques.objects.get(id_id=request.user.id).defense+Objet.objects.get(id=Equipement.objects.get(id_id=request.user.id).pantalon).pd)
        messages.success(request, 'Le pantalon a bien été équipé')
    elif typeobjet == 4 : # si c'est des chaussures
      if not (stuff.chaussures >= 0):
        Equipement.objects.filter(id_id = request.user.id).update(chaussures=inv.objet)
        Inventaire.objects.filter(objet = request.POST.get('item'), idjoueur_id=request.user.id).delete()
        Caracteristiques.objects.filter(id_id=request.user.id).update(defense=Caracteristiques.objects.get(id_id=request.user.id).defense+Objet.objects.get(id=Equipement.objects.get(id_id=request.user.id).chaussures).pd)
        Caracteristiques.objects.filter(id_id=request.user.id).update(vitesse=Caracteristiques.objects.get(id_id=request.user.id).vitesse+Objet.objects.get(id=Equipement.objects.get(id_id=request.user.id).chaussures).pa)
        messages.success(request, 'Les chaussures ont bien été équipées')
    else: 
      messages.error(request, 'Type d\'objet non trouvé')
    return HttpResponseRedirect('/dashboard/monjenky/#inventaire')
  def get(self, request, **kwargs):
    return render(request, 'layouts/empty.html')

class MonJenkyItemDesequipArme(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(MonJenkyItemDesequipArme, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs):
    if request.POST.get('arme') != '-1':
      if Inventaire.objects.filter(idjoueur_id=request.user.id, objet=request.POST.get('arme')).count() == 0:
        Equipement.objects.filter(id_id=request.user.id).update(arme=-1)
        Caracteristiques.objects.filter(id_id=request.user.id).update(attaque=0)
        Inventaire.objects.create(objet=request.POST.get('arme'), idjoueur_id=request.user.id)
        messages.success(request, 'L\'objet a bien été transféré vers l\'inventaire')
      else:
        messages.error(request, 'Objet déjà dans l\'inventaire')
    else:
      messages.error(request, 'Contactez l\'administrateur du site')
    return HttpResponseRedirect('/dashboard/monjenky/#')
  def get(self, request, **kwargs):
    return render(request, 'layouts/empty.html')

class MonJenkyItemDesequipCasque(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(MonJenkyItemDesequipCasque, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs):
    if request.POST.get('casque') != '-1':
      if Inventaire.objects.filter(idjoueur_id=request.user.id, objet=request.POST.get('casque')).count() == 0:
        Caracteristiques.objects.filter(id_id=request.user.id).update(defense=Caracteristiques.objects.get(id_id=request.user.id).defense-Objet.objects.get(id=Equipement.objects.get(id_id=request.user.id).casque).pd)
        Caracteristiques.objects.filter(id_id=request.user.id).update(precision=Caracteristiques.objects.get(id_id=request.user.id).precision-Objet.objects.get(id=Equipement.objects.get(id_id=request.user.id).casque).pa)
        Equipement.objects.filter(id_id=request.user.id).update(casque=-1)
        Inventaire.objects.create(objet=request.POST.get('casque'), idjoueur_id=request.user.id)
        messages.success(request, 'L\'objet a bien été transféré vers l\'inventaire')
      else:
        messages.error(request, 'Objet déjà dans l\'inventaire')
    else:
      messages.error(request, 'Contactez l\'administrateur du site')
    return HttpResponseRedirect('/dashboard/monjenky/#')
  def get(self, request, **kwargs):
    return render(request, 'layouts/empty.html')

class MonJenkyItemDesequipArmure(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(MonJenkyItemDesequipArmure, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs):
    if request.POST.get('armure') != '-1':
      if Inventaire.objects.filter(idjoueur_id=request.user.id, objet=request.POST.get('armure')).count() == 0:
        Caracteristiques.objects.filter(id_id=request.user.id).update(defense=Caracteristiques.objects.get(id_id=request.user.id).defense-Objet.objects.get(id=Equipement.objects.get(id_id=request.user.id).armure).pd)
        Equipement.objects.filter().update(armure=-1)
        Inventaire.objects.create(objet=request.POST.get('armure'), idjoueur_id=request.user.id)
        messages.success(request, 'L\'objet a bien été transféré vers l\'inventaire')
      else:
        messages.error(request, 'Objet déjà dans l\'inventaire')
    else:
      messages.error(request, 'Contactez l\'administrateur du site')
    return HttpResponseRedirect('/dashboard/monjenky/#')
  def get(self, request, **kwargs):
    return render(request, 'layouts/empty.html')

class MonJenkyItemDesequipPantalon(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(MonJenkyItemDesequipPantalon, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs):
    if request.POST.get('pantalon') != '-1':
      if Inventaire.objects.filter(idjoueur_id=request.user.id, objet=request.POST.get('pantalon')).count() == 0:
        Caracteristiques.objects.filter(id_id=request.user.id).update(defense=Caracteristiques.objects.get(id_id=request.user.id).defense-Objet.objects.get(id=Equipement.objects.get(id_id=request.user.id).pantalon).pd)
        Equipement.objects.filter().update(pantalon=-1)
        Inventaire.objects.create(objet=request.POST.get('pantalon'), idjoueur_id=request.user.id)
        messages.success(request, 'L\'objet a bien été transféré vers l\'inventaire')
      else:
        messages.error(request, 'Objet déjà dans l\'inventaire')
    else:
      messages.error(request, 'Contactez l\'administrateur du site')
    return HttpResponseRedirect('/dashboard/monjenky/#')
  def get(self, request, **kwargs):
    return render(request, 'layouts/empty.html')

class MonJenkyItemDesequipChaussures(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(MonJenkyItemDesequipChaussures, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs):
    if request.POST.get('chaussures') != '-1': # Si l'objet n'est pas nul
      if Inventaire.objects.filter(idjoueur_id=request.user.id, objet=request.POST.get('chaussures')).count() == 0:
        Caracteristiques.objects.filter(id_id=request.user.id).update(vitesse=Caracteristiques.objects.get(id_id=request.user.id).vitesse-Objet.objects.get(id=Equipement.objects.get(id_id=request.user.id).chaussures).pa)
        Caracteristiques.objects.filter(id_id=request.user.id).update(defense=Caracteristiques.objects.get(id_id=request.user.id).defense-Objet.objects.get(id=Equipement.objects.get(id_id=request.user.id).chaussures).pd)
        Equipement.objects.filter().update(chaussures=-1)
        Inventaire.objects.create(objet=request.POST.get('chaussures'), idjoueur_id=request.user.id)
        messages.success(request, 'L\'objet a bien été transféré vers l\'inventaire')
      else:
        messages.error(request, 'Objet déjà dans l\'inventaire')
    else:
      messages.error(request, 'Contactez l\'administrateur du site')
    return HttpResponseRedirect('/dashboard/monjenky/#')
  def get(self, request, **kwargs):
    return render(request, 'layouts/empty.html')
    
class ProfileView(TemplateView):
  template_name = 'dashboard/profile.html'
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(ProfileView, self).dispatch(*args, **kwargs)
  def get(self, request, **kwargs):
    caracteristiques = Caracteristiques.objects.get(id_id=request.user.id)
    return render(request, self.template_name, {'caracteristiques' : caracteristiques})

class ProfilProf(TemplateView):
  template_name = 'prof/profile.html'
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(ProfilProf, self).dispatch(*args, **kwargs)
  def get(self, request, **kwargs):
    return render(request, self.template_name)

class ProfileUpdate(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(ProfileUpdate, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs):
    if request.POST.get('ln') != '' and request.POST.get('fn') != '' and request.POST.get('mdpactuel') != ''  and request.POST.get('mail') != '': # si la requete n'est pas nulle
      if(request.user.check_password(request.POST.get('mdpactuel'))):
        User.objects.filter(id=request.user.id).update(email = request.POST.get('mail'), first_name = request.POST.get('fn'), last_name = request.POST.get('ln'))
        if(request.POST.get('mdpnouveau') != ''):
          request.user.set_password(request.POST.get('mdpnouveau'))
          request.user.save()
        messages.success(request, 'Profil bien mis à jour')
      else:
        messages.error(request, 'Mauvais mot de passe fourni')
    else:
      messages.error(request, 'Veuillez remplir tous les champs !')
    return HttpResponseRedirect('/dashboard/profile/')
  def get(self, request, **kwargs):
    return render(request, 'layouts/empty.html')


class ProfileProfUpdate(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(ProfileProfUpdate, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs):
    if request.POST.get('ln') != '' and request.POST.get('fn') != '' and request.POST.get('mdpactuel') != ''  and request.POST.get('mail') != '': # si la requete n'est pas nulle
      if(request.user.check_password(request.POST.get('mdpactuel'))):
        User.objects.filter(id=request.user.id).update(email = request.POST.get('mail'), first_name = request.POST.get('fn'), last_name = request.POST.get('ln'))
        if(request.POST.get('mdpnouveau') != ''):
          request.user.set_password(request.POST.get('mdpnouveau'))
          request.user.save()
        messages.success(request, 'Profil bien mis à jour')
      else:
        messages.error(request, 'Mauvais mot de passe fourni')
    else:
      messages.error(request, 'Veuillez remplir tous les champs !')
    return HttpResponseRedirect('/prof/profile/')
  def get(self, request, **kwargs):
    return render(request, 'layouts/empty.html')

class ShopView(TemplateView):
  template_name = 'dashboard/shop.html'
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(ShopView, self).dispatch(*args, **kwargs)
  def get(self, request, **kwargs):
    shop = Shop.objects.get(id=request.user.id)
    caracteristiques = Caracteristiques.objects.get(id_id=request.user.id)
    if(datetime.now(tz=timezone.utc) < (shop.dateupdate + timedelta(hours=1))):
      can_update = False
    else:
      can_update = True
    liste_items = []
    if shop.objet0 != -1:
      liste_items.append(Objet.objects.get(id=shop.objet0))
    else:
      liste_items.append(-1)
    if shop.objet1 != -1:
      liste_items.append(Objet.objects.get(id=shop.objet1))
    else:
      liste_items.append(-1)
    if shop.objet2 != -1:
      liste_items.append(Objet.objects.get(id=shop.objet2))
    else:
      liste_items.append(-1)
    if shop.objet3 != -1:
      liste_items.append(Objet.objects.get(id=shop.objet3))
    else:
      liste_items.append(-1)
    if shop.objet4 != -1:
      liste_items.append(Objet.objects.get(id=shop.objet4))
    else:
      liste_items.append(-1)
    if shop.objet5 != -1:
      liste_items.append(Objet.objects.get(id=shop.objet5))
    else:
      liste_items.append(-1)
    minute = round(((shop.dateupdate + timedelta(hours=1)) - datetime.now(tz=timezone.utc)).total_seconds()/60)
    return render(request, self.template_name, {'shop': shop, 'caracteristiques' : caracteristiques, 'can_update' : can_update, 'liste_items': liste_items, 'minute' :  minute})



class ShopUpdate(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(ShopUpdate, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs):
    shop = Shop.objects.get(id=request.user.id)
    if(datetime.now(tz=timezone.utc) > (shop.dateupdate + timedelta(hours=1))): # si l'utilisateur a envoyé une requete alors qu'il n'a pas le droit
      nbmax = Objet.objects.aggregate(Max('id'))['id__max']
      Shop.objects.filter(id=request.user.id).update(objet0 = random.randint(0,nbmax), objet1 = random.randint(0,nbmax), objet2 = random.randint(0,nbmax), objet3 = random.randint(0,nbmax), objet4 = random.randint(0,nbmax), objet5 = random.randint(0,nbmax), dateupdate = datetime.now(tz=timezone.utc))
    else: # triche
      messages.error(request, 'Triche possible, tu n\'a pas été autorisé à mettre à jour le shop')
    return HttpResponseRedirect('/dashboard/shop/')
  def get(self, request, **kwargs):
    return render(request, 'layouts/empty.html')

class ShopEquip(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(ShopEquip, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs):
    pos_item = request.POST.get('item')
    id_item = request.POST.get('item'+pos_item)
    shop = Shop.objects.get(id=request.user.id)
    if int(eval('shop.objet'+pos_item)) == int(id_item): # verif si l'user a l'objet en question dans le shop
      if Inventaire.objects.filter(idjoueur_id=request.user.id, objet=id_item).count() == 0: # si l'user n'a pas l'objet dans son inventaire
        if Equipement.objects.filter(id_id=request.user.id, arme=id_item).count() == 0 and Equipement.objects.filter(id_id=request.user.id, casque=id_item).count() == 0 and Equipement.objects.filter(id_id=request.user.id, armure=id_item).count() == 0 and Equipement.objects.filter(id_id=request.user.id, pantalon=id_item).count() == 0 and Equipement.objects.filter(id_id=request.user.id, chaussures=id_item).count() == 0:
          if Caracteristiques.objects.get(id=request.user.id).gold - Objet.objects.get(id=id_item).prix_achat >= 0: # si l'user peut l'acheter
            pos_item = int(pos_item)
            if(pos_item == 0):
              Shop.objects.filter(id=request.user.id).update(objet0 = -1)
            elif(pos_item == 1):
              Shop.objects.filter(id=request.user.id).update(objet1 = -1)
            elif(pos_item == 2):
              Shop.objects.filter(id=request.user.id).update(objet2 = -1)
            elif(pos_item == 3):
              Shop.objects.filter(id=request.user.id).update(objet3 = -1)
            elif(pos_item == 4):
              Shop.objects.filter(id=request.user.id).update(objet4 = -1)
            elif(pos_item == 5):
              Shop.objects.filter(id=request.user.id).update(objet5 = -1)
            Caracteristiques.objects.filter(id=request.user.id).update(gold = Caracteristiques.objects.get(id=request.user.id).gold-Objet.objects.get(id=id_item).prix_achat)
            Inventaire.objects.create(objet=id_item, idjoueur_id=request.user.id)
            messages.success(request, 'Objet bien ajouté à l\'inventaire')
          else:
            messages.error(request, 'Pas assez de golds')
        else:
          messages.error(request, 'Objet déjà équipé')
      else:
        messages.error(request, 'Objet déjà dans l\'inventaire')
    else:
      messages.error(request, 'Objet non trouvé dans le shop, triche possible')
    return HttpResponseRedirect('/dashboard/shop/')
  def get(self, request, **kwargs):
    return render(request, 'layouts/empty.html')
  

class AreneView(TemplateView):
  template_name = 'dashboard/arene.html'
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(AreneView, self).dispatch(*args, **kwargs)
  def get(self, request, **kwargs):
    caracteristiques = Caracteristiques.objects.get(id_id=request.user.id)
    listuser = User.objects.all()
    listusercar = Caracteristiques.objects.all()
    check_user_attacked = []
    for user in listuser:
      if(datetime.now(tz=timezone.utc) < (Caracteristiques.objects.get(id_id=user.id).last_attack + timedelta(hours=1))):
        check_user_attacked.append({'userid' : user.id, 'update' :False})
      else:
        check_user_attacked.append({'userid' : user.id, 'update' :True})
    return render(request, self.template_name, {'caracteristiques' : caracteristiques,'listuser': listuser, 'listusercar':listusercar, 'check_user_attacked' : check_user_attacked})


class ApiInfoUser(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(ApiInfoUser, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs):
    req=Caracteristiques.objects.get(id_id=request.POST.get('id'))
    tosend = {
      'id' : req.id.id,
      'atq' : req.attaque,
      'def' : req.defense,
      'spd' : req.vitesse,
      'acc' : req.precision,
    }
    return JsonResponse(tosend, safe=False)
  def get(self, request, **kwargs):
    return render(request, 'layouts/empty.html') 


class ApiInfoHistorique(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(ApiInfoHistorique, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs):
    req1=Combat.objects.filter(joueur_attaque=request.POST.get('id'))
    req2=Combat.objects.filter(joueur_defense=request.POST.get('id'))
    req = req1 | req2
    tosend = {}
    i=0
    for r in req:
      subr = {}
      subr['id_match'] = r.id
      subr['joueur_attaque'] = r.joueur_attaque.username
      subr['joueur_defense'] = r.joueur_defense.username
      subr['gold_obtenu'] = r.gold_obtenu
      subr['date_attaque'] = r.date_attaque
      subr['gagnant'] = r.gagnant.username
      i+=1
      tosend[i] = subr
    return JsonResponse(tosend, safe=False)
  def get(self, request, **kwargs):
    return render(request, 'layouts/empty.html') 

class ApiResultArene(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(ApiResultArene, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs): # partie pas du tout sécurisé, faut absolument bosser dessus
    #récupération info joueur
    id_gagnant = int(request.POST.get('vainqueur'))
    id_attaque = int(request.POST.get('attaque'))
    id_defense = int(request.POST.get('defense'))
    nb_gold = int(request.POST.get('golds'))
    paj1,paj2 = Caracteristiques.objects.get(id_id=id_attaque).attaque,Caracteristiques.objects.get(id_id=id_defense).attaque
    pdj1,pdj2 = Caracteristiques.objects.get(id_id=id_attaque).defense,Caracteristiques.objects.get(id_id=id_defense).defense
    spdj1,spdj2 = Caracteristiques.objects.get(id_id=id_attaque).vitesse,Caracteristiques.objects.get(id_id=id_defense).vitesse
    #fix pour les défenses nulles
    if(pdj1 != 0):
      dgtj2 = ((paj2*4) / pdj1)*10
    else: #dégat brut
      dgtj2 = (paj2*4)
    if(pdj2 != 0):
      dgtj1 = ((paj1*4) / pdj2)*10
    else: #dégat brut
      dgtj1 = (paj1*4)
    #simulation partie
    hpj1,hpj2 = 100,100
    if(spdj2>spdj1):
      while(hpj1 > 0 and hpj2 > 0):
        hpj1-=dgtj2
        hpj2-=dgtj1
    else:
      while(hpj1 > 0 and hpj2 > 0):
        hpj2-=dgtj1
        hpj1-=dgtj2
    #récuperation resultat
    if(hpj1<=0):
      vainqueur=2
    else:
      vainqueur=1
    if(vainqueur == 1 and id_gagnant == id_attaque or vainqueur == 2 and id_gagnant == id_defense): 
      Caracteristiques.objects.filter(id=request.user.id).update(gold = Caracteristiques.objects.get(id=request.user.id).gold + nb_gold)
      Caracteristiques.objects.filter(id=id_defense).update(last_attack = datetime.now(tz=timezone.utc))
      Combat.objects.create(joueur_attaque = User.objects.get(id=id_attaque), joueur_defense = User.objects.get(id=id_defense), gold_obtenu = nb_gold, gagnant = User.objects.get(id=id_gagnant), date_attaque = datetime.now(tz=timezone.utc))
      return HttpResponse(json.dumps("{ok}"), content_type='application/json')
    else:
      return HttpResponse(json.dumps("{triche détectée}"), content_type='application/json')
  def get(self, request, **kwargs):
    return render(request, 'layouts/empty.html') 

class ApiChargeSprite(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
        return super(ApiChargeSprite, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs):
    joueur1, joueur2 = request.POST.get('joueur1'), request.POST.get('joueur2')
    for i in range(1,6):
      reload_sprite_profile.reload(joueur1,i)
      reload_sprite_profile.reload(joueur2,i)
    return JsonResponse({"ok":"ok"}, safe=False)

class ObjectifView(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
    return super(ObjectifView, self).dispatch(*args, **kwargs)
  def get(self, request, **kwargs):
    modules = Prof_TP.objects.filter(prof_id=request.user.id)
    objectif = Competence_Module.objects.all()
    competence=[]
    caracteristiques = Caracteristiques.objects.get(id_id=request.user.id)
    for i in modules:
      competence.append([i.id,Competence_Module.objects.filter(nom_module_id=i.nom_module_id).distinct("nom_competence").count()])
    return render(request, 'dashboard/objectifs.html', {'caracteristiques':caracteristiques, 'modules':modules,'competence':competence,'objectif':objectif}) 

class ObjectifApi(TemplateView):
  @method_decorator(user_passes_test(etudiant_check))
  def dispatch(self, *args, **kwargs):
    return super(ObjectifApi, self).dispatch(*args, **kwargs)
  def post(self, request, **kwargs):
    if request.POST.get('toDownload') == 'module':
      print (request.POST.get('valeur'))
      module = Module.objects.get(nom_module=request.POST.get('valeur'))
      objectif = Competence_Module.objects.filter(nom_module_id=module.id, etudiant_id=request.user.id)
      objectifs=[]
      for i in objectif:
        if([i.nom_competence,i.nombre_exp_gagne] not in objectifs):
          objectifs.append([i.nom_competence,i.nombre_exp_gagne,i.valide])
      tosend = {
        'objectif' : objectifs,
        'nom_module' : module.nom_module,
      }
    elif request.POST.get('toDownload') == 'valider':
      objectif = request.POST.get('obj')
      last_name = request.POST.get('name').split('.')[0]
      first_name = request.POST.get('name').split('.')[1]
      us = User.objects.get(first_name = first_name, last_name=last_name)
      Competence_Module.objects.filter(nom_competence=objectif,etudiant_id=us.id).update(valide=True)
      tosend={'ok':'ok'}
    elif request.POST.get('toDownload') == 'refuser':
      objectif = request.POST.get('obj')
      last_name = request.POST.get('name').split('.')[0]
      first_name = request.POST.get('name').split('.')[1]
      us = User.objects.get(first_name = first_name, last_name=last_name)
      Competence_Module.objects.filter(nom_competence=objectif,etudiant_id=us.id).update(valide=False)
      tosend={'ok':'ok'}
    return JsonResponse(tosend, safe=False)
  def get(self, request, **kwargs):
    return render(request, 'dashboardProf/empty.html') 