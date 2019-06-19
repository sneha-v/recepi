from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponse,HttpResponseRedirect
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Food,Recipes
from django.contrib.auth.decorators import login_required
import operator
from datetime import datetime
from django.core.mail import send_mail, EmailMessage

global number

def index(request):
    return render(request,"index.html")

def signin(request):
    if request.method == "POST":
        uname = request.POST.get("uname",None)
        print(uname)
        password =request.POST.get("password",None)
        print(password)
        user = authenticate(request,username=uname,password=password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect("/main")
        else:
            return render(request,"login.html",{"error":"Login error"})
    return render(request,"login.html")

def signup(request):
    if request.method=="POST":
        fullname=request.POST.get('fname',None)
        email=request.POST.get('email',None)
        username=request.POST.get('uname',None)
        password=request.POST.get('pass',None)
        user_exists=User.objects.filter(username=username).exists()
        if not user_exists:
            user=User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=fullname.split()[0],
            last_name=" ".join(fullname.split()[1:])
            )
            user.save()
            login(request,user)
            return redirect("/main")
        else:
            return HttpResponse("user already Exists. Try other User Name")
    return render(request,"signUp.html")

def signout(request):
	logout(request)
	return redirect("/")

@login_required(login_url="/signin/")
def main(request):
    return render(request,"main.html")

@login_required(login_url="/signin/")
def findrecep(request):
    if request.method=='POST':
        number = request.POST.get("items",None)
        if number == "":
            return render(request,"main.html")
        number = [i for i in range(1,int(number)+1)]
    return render(request,"findrec.html", {"number":number})

@login_required(login_url="/signin/")
def findcuisine(request, number):
    items = []
    item_dict = {}
    cuisine_count = {}
    index = {}
    maxy = {}
    number1 = [i for i in range(1,int(number)+1)]
    if request.method == "POST":
        for i in range(1,int(number)+1):
            if request.POST.get("recipe"+str(i))=='':
                return render(request, "findrec.html",{"number":number1,"error":"enter all the items"})
                break
            items.append(request.POST.get("recipe"+str(i),None).lower())
        table_items =  Recipes.objects.values_list('item','rec_name')
        for item in table_items:
            recepi_name = Food.objects.get(pk=item[1]).rec_name
            if recepi_name not in item_dict.keys():
                item_dict[recepi_name] = [item[0]]
                index[recepi_name] = item[1]
            else:
                item_dict[recepi_name].append(item[0])
        for i in items:
            temp = {}
            for j in item_dict.keys():
                if i.capitalize() in item_dict[j]:
                    cui_name = Food.objects.get(pk=index[j]).cuisine_name
                    if cui_name not in temp.keys():
                        temp[cui_name] = 1
                    else:
                        temp[cui_name] = temp[cui_name] + 1
                    cuisine_count[i] = temp
        print(cuisine_count)
        for item in cuisine_count.keys():
            maximum = max(cuisine_count[item], key=cuisine_count[item].get)
            if maximum not in maxy.keys():
                maxy[maximum] = cuisine_count[item][maximum]
            else:
                maxy[maximum] += cuisine_count[item][maximum]
        print(maxy)
        if maxy=={}:
            pred = "Indian"
        else:
            pred = max(maxy, key=maxy.get)
    return render(request, "findcuisine.html",{"prediction":pred})

@login_required(login_url="/signin/")
def reclist(request,pred):
    contri_name=[]
    proc=[]
    recepi_name = []
    item=[]
    quantity=[]
    singleitem = []
    if request.method == "POST":
        cui_name = request.POST.get("cui_name")
        rec_name = Food.objects.filter(cuisine_name = cui_name.capitalize()).values_list('rec_name','con_name','procedure','id').order_by('pub_date')
        for i in rec_name:
            lines = []
            recepi_name.append(i[0])
            item.append(Recipes.objects.filter(rec_name=i[3]).values_list('item',flat=True))
            quantity.append(Recipes.objects.filter(rec_name=i[3]).values_list('quantity',flat=True))
            contri_name.append(i[1].capitalize())
            with open(f"media/{i[2]}") as file:
                lines = [line.strip() for line in file]
            proc.append(lines)
        for i in range(len(item)):
            singleitem.append(dict(zip(item[i],quantity[i])))
        return render(request, "reclist.html" ,{"recepi_thing":zip(recepi_name,contri_name,singleitem,proc),"cuisine_name":cui_name.capitalize()} )

    else:
        rec_name = Food.objects.filter(cuisine_name = pred.capitalize()).values_list('rec_name','con_name','procedure','id').order_by('pub_date')
        for i in rec_name:
            lines = []
            recepi_name.append(i[0])
            item.append(Recipes.objects.filter(rec_name=i[3]).values_list('item',flat=True))
            quantity.append(Recipes.objects.filter(rec_name=i[3]).values_list('quantity',flat=True))
            contri_name.append(i[1].capitalize())
            with open(f"media/{i[2]}") as file:
                lines = [line.strip() for line in file]
            proc.append(lines)
        for i in range(len(item)):
            singleitem.append(dict(zip(item[i],quantity[i])))
        return render(request, "reclist.html" ,{"recepi_thing":zip(recepi_name,contri_name,singleitem,proc),"cuisine_name":pred.capitalize()} )

@login_required(login_url="/signin/")
def addrecep(request):
    if request.method == 'POST':
        number = request.POST.get("items")
        number = [i for i in range(1,int(number)+1)]
    username = None
    if request.user.is_authenticated:
        username = request.user.username
        print(username)
    return render(request,"addrecep.html",{"number":number})

@login_required(login_url="/signin/")
def adding_recep(request,number):
    number = [i for i in range(1,int(number)+1)]
    item_quantity = []
    try:

        if request.method=='POST':
            cui_name = request.POST.get("cui_name")
            reci_name = request.POST.get("rec_name")
            procedure = request.POST.get("procedure")
            for i in range(1,int(number)+1):
                if request.POST.get("recipe"+str(i))=='' or request.POST.get("recipe"+str(i))=='':
                    return render(request, "addrecep.html",{"number":number1,"error":"enter all the items"})
                    break
                item_quantity.append([request.POST.get("recipe"+str(i),None).capitalize(),request.POST.get("quantity"+str(i),None).capitalize()])
            rec_spaceless = reci_name.replace(" ","")
            with open(f"media/food/procedure/{rec_spaceless}.txt", "w") as f:
                f.write(procedure)
                f.close()
    except:
        return render(request, "addrecep.html",{"number":number,"error":"Oops something went wrong! add again!"})
        if request.user.is_authenticated:
            username = request.user.username
        try:
            recepi = Food.objects.create(
            con_name = username.capitalize(),
            rec_name = reci_name.capitalize(),
            no_of_items = number,
            cuisine_name = cui_name.capitalize(),
            pub_date = datetime.now(),
            procedure = f'food/procedure/{reci_name.replace(" ","")}.txt'
            )
            recepi.save()
        except:
            return render(request, "addrecep.html",{"number":number,"error":"Recepi name already exists"})

        for items in item_quantity:
            item = Recipes.objects.create(
            rec_name =recepi,
            item = items[0].capitalize(),
            quantity = items[1]
            )
            item.save()
    return render(request,"profile.html",{"message":"Recepi successfully added!"})

@login_required(login_url="/signin/")
def profile(request):
    proc=[]
    recepi_name = []
    item=[]
    quantity=[]
    cui_name = []
    singleitem = []
    if request.user.is_authenticated:
        username = request.user.username.capitalize()
    rec_name = Food.objects.filter(con_name = username).values_list('rec_name','con_name','procedure','id','cuisine_name').order_by('pub_date')
    for i in rec_name:
        lines = []
        recepi_name.append(i[0])
        cui_name.append(i[4])
        item.append(Recipes.objects.filter(rec_name=i[3]).values_list('item',flat=True))
        quantity.append(Recipes.objects.filter(rec_name=i[3]).values_list('quantity',flat=True))
        with open(f"media/{i[2]}") as file:
            lines = [line.strip() for line in file]
        proc.append(lines)
    for i in range(len(item)):
        singleitem.append(dict(zip(item[i],quantity[i])))
    return render(request,"profile.html",{"recepi_thing":zip(recepi_name,cui_name,singleitem,proc),"con_name":username,"rec_name":recepi_name})


@login_required(login_url="/signin/")
def search(request):
    proc=[]
    recepi_name = []
    item=[]
    quantity=[]
    cui_name = []
    singleitem = []
    contri_name = []
    if request.method=='POST':
        search = request.POST.get("search").capitalize()
        print(search)
        rec_name = Food.objects.filter(rec_name =search).values_list('rec_name','con_name','procedure','id','cuisine_name').order_by('pub_date')
        if rec_name:
            for i in rec_name:
                lines = []
                recepi_name.append(i[0])
                contri_name.append(i[1])
                cui_name.append(i[4])
                item.append(Recipes.objects.filter(rec_name=i[3]).values_list('item',flat=True))
                quantity.append(Recipes.objects.filter(rec_name=i[3]).values_list('quantity',flat=True))
                with open(f"media/{i[2]}") as file:
                    lines = [line.strip() for line in file]
                proc.append(lines)
            for i in range(len(item)):
                singleitem.append(dict(zip(item[i],quantity[i])))

            return render(request,"search.html",{"recepi_thing":zip(recepi_name,contri_name,cui_name,singleitem,proc),"rec_name":recepi_name,"bit":1})
        else:
            rec_name = Food.objects.filter(cuisine_name =search).values_list('rec_name','con_name','procedure','id','cuisine_name').order_by('pub_date')
            print(rec_name)
            for i in rec_name:
                lines = []
                recepi_name.append(i[0])
                contri_name.append(i[1])
                cui_name.append(i[4])
                item.append(Recipes.objects.filter(rec_name=i[3]).values_list('item',flat=True))
                quantity.append(Recipes.objects.filter(rec_name=i[3]).values_list('quantity',flat=True))
                with open(f"media/{i[2]}") as file:
                    lines = [line.strip() for line in file]
                proc.append(lines)
            for i in range(len(item)):
                singleitem.append(dict(zip(item[i],quantity[i])))
            return render(request,"search.html",{"recepi_thing":zip(recepi_name,contri_name,singleitem,proc),"rec_name":recepi_name,"bit":0,"cn":cui_name[0]})
