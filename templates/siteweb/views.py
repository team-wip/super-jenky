from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.conf import settings
from siteweb.models import Caracteristiques
from siteweb.models import Equipement
from siteweb.models import Objet
from siteweb.models import Inventaire
from siteweb.models import Shop
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

# Create your views here.
def index(request):
    return render(request, 'index.html')

class LoginView(TemplateView):

  template_name = 'index.html'

  def post(self, request, **kwargs):
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    user = authenticate(username=username, password=password)
    if user is not None and user.is_active:
        login(request, user)
        messages.success(request, 'Connexion réussie')
        return HttpResponseRedirect( settings.LOGIN_REDIRECT_URL )
    else:
      messages.error(request, 'Mauvais mot de passe')
    return render(request, self.template_name)


class LogoutView(TemplateView):

  template_name = 'index.html'
  def get(self, request, **kwargs):
    logout(request)
    return render(request, self.template_name)

class IndexView(TemplateView):
  template_name = "dashboard/index.html"
  def get(self, request, **kwargs):
    caracteristiques = Caracteristiques.objects.get(id_id=request.user.id)
    return render(request, self.template_name, {'caracteristiques' : caracteristiques})

class MonJenkyView(TemplateView):
  template_name = "dashboard/monjenky.html"
  def get(self, request, **kwargs):
    list = {}
    caracteristiques = Caracteristiques.objects.get(id_id=request.user.id)
    list.update({'caracteristiques' : caracteristiques})
    try:
      obj = Equipement.objects.get(id_id=request.user.id)
      list.update({'obj' : obj})
      casque = Objet.objects.get(typeobjet=obj.casque)
      list.update({'casque' : casque})
      armure = Objet.objects.get(typeobjet=obj.armure)
      list.update({'armure' : armure})
      pantalon = Objet.objects.get(typeobjet=obj.pantalon)
      list.update({'pantalon' : pantalon})
      chaussures = Objet.objects.get(typeobjet=obj.chaussures)
      list.update({'chaussures' : chaussures})
      arme = Objet.objects.get(typeobjet=obj.arme)
      list.update({'arme' : arme})
      idinv = Inventaire.objects.filter(idjoueur_id=request.user.id)
      list.update({'idinv' : idinv})
      inv = Objet.objects.filter(id__in = [objet.objet for objet in idinv] )
      list.update({'inv' : inv})
    except:
      print("euh ah oe chaud y'a une erreur")
    return render(request, self.template_name, list)

class MonJenkyItemVendre(TemplateView):
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
        messages.success(request, 'Le casque a bien été équipé')
    elif typeobjet == 2 : # si c'est une armure
      if not (stuff.armure >= 0):
        Equipement.objects.filter(id_id = request.user.id).update(armure=inv.objet)
        Inventaire.objects.filter(objet = request.POST.get('item'), idjoueur_id=request.user.id).delete()
        messages.success(request, 'L\'armure a bien été équipée')
    elif typeobjet == 3 : # si c'est un pantalon
      if not (stuff.pantalon >= 0):
        Equipement.objects.filter(id_id = request.user.id).update(pantalon=inv.objet)
        Inventaire.objects.filter(objet = request.POST.get('item'), idjoueur_id=request.user.id).delete()
        messages.success(request, 'Le pantalon a bien été équipé')
    elif typeobjet == 4 : # si c'est des chaussures
      if not (stuff.chaussures >= 0):
        Equipement.objects.filter(id_id = request.user.id).update(chaussures=inv.objet)
        Inventaire.objects.filter(objet = request.POST.get('item'), idjoueur_id=request.user.id).delete()
        messages.success(request, 'Les chaussures ont bien été équipées')
    else: 
      messages.error(request, 'Type d\'objet non trouvé')
    return HttpResponseRedirect('/dashboard/monjenky/#inventaire')
  def get(self, request, **kwargs):
    return render(request, 'layouts/empty.html')

class MonJenkyItemDesequipArme(TemplateView):
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
  def post(self, request, **kwargs):
    if request.POST.get('casque') != '-1':
      if Inventaire.objects.filter(idjoueur_id=request.user.id, objet=request.POST.get('casque')).count() == 0:
        Equipement.objects.filter().update(casque=-1)
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
  def post(self, request, **kwargs):
    if request.POST.get('armure') != '-1':
      if Inventaire.objects.filter(idjoueur_id=request.user.id, objet=request.POST.get('armure')).count() == 0:
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
  def post(self, request, **kwargs):
    if request.POST.get('pantalon') != '-1':
      if Inventaire.objects.filter(idjoueur_id=request.user.id, objet=request.POST.get('pantalon')).count() == 0:
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
  def post(self, request, **kwargs):
    if request.POST.get('chaussures') != '-1': # Si l'objet n'est pas nul
      if Inventaire.objects.filter(idjoueur_id=request.user.id, objet=request.POST.get('chaussures')).count() == 0:
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
  def get(self, request, **kwargs):
    caracteristiques = Caracteristiques.objects.get(id_id=request.user.id)
    return render(request, self.template_name, {'caracteristiques' : caracteristiques})

class ProfileUpdate(TemplateView):
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

class ShopView(TemplateView):
  template_name = 'dashboard/shop.html'
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
  def get(self, request, **kwargs):
    caracteristiques = Caracteristiques.objects.get(id_id=request.user.id)
    listuser = User.objects.all()
    listusercar = Caracteristiques.objects.all()
    return render(request, self.template_name, {'caracteristiques' : caracteristiques,'listuser': listuser, 'listusercar':listusercar})


class ApiInfoUser(TemplateView):
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

    