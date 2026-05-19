from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
import google.generativeai as genai
from PIL import Image

# Create your views here.
from myapp.models import *
from django.contrib.auth.models import User, Group


def login_get(request):
    return render(request,'login.html')

def login_post(request):
    username=request.POST["username"]
    password=request.POST["password"]
    user=authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user)
        if user.groups.filter(name="Admin").exists():
            return redirect('/myapp/adm_index_get/')
        elif user.groups.filter(name="Pickup").exists():
            return redirect('/myapp/pickupindex_get/')
        else:
            return redirect('/myapp/login_get/')
    else:
        return redirect('/myapp/login_get/')


# u=User.objects.get(username='sona@gmail.com')
# u.set_password('123456')
# u.save()

def adm_index_get(request):
    return render(request,'adminpages/index.html')


def adm_verify_pickup_get(request):
    data=Pickup.objects.filter(Status='pending')
    return render(request,'adminpages/verify pickup.html',{'data':data})

def adm_verified_pickup_get(request):
    data=Pickup.objects.filter(Status='Approved')
    return render(request,'adminpages/verified pickup.html',{'data':data})

def adm_rejected_pickup_get(request):
    data=Pickup.objects.filter(Status='Rejected')
    return render(request,'adminpages/rejected pickup.html',{'data':data})

def approve_pickup(request,id):
    Pickup.objects.filter(id=id).update(Status="Approved")
    return redirect('/myapp/adm_verify_pickup_get/')

def reject_pickup(request,id):
    Pickup.objects.filter(id=id).update(Status="Rejected")
    return redirect('/myapp/adm_verify_pickup_get/')

def adm_view_worker_get(request):
    data=Staff.objects.all()
    return render(request,'adminpages/view worker.html',{'data':data})

def adm_view_user_category_get(request):
    data=Users.objects.all()
    return render(request,'adminpages/viewuser.html',{'data':data})

def adm_view_compliant_get(request):
    data=Complaint.objects.all()
    return render(request,'adminpages/view compliant.html',{'data':data})

def adm_add_waste_category_get(request):
    return render(request,'adminpages/Manage Waste Category.html')

def adm_add_waste_category_post(request):
    category=request.POST['category']
    type=request.POST['type']
    price=request.POST['price']

    obj=Category()
    obj.Category=category
    obj.Type=type
    obj.Price=price
    obj.save()

    return redirect('/myapp/adm_view_waste_category_get/')

def adm_view_waste_category_get(request):
    data=Category.objects.all()
    return render(request,'adminpages/View Waste Category.html',{"data":data})

def adm_edit_waste_category_get(request,id):
    data=Category.objects.get(id=id)
    return render(request,'adminpages/Edit Waste.html',{'data':data})

def adm_edit_waste_category_post(request):
    category = request.POST['category']
    type = request.POST['type']
    price = request.POST['Price']
    id = request.POST['id']

    obj = Category.objects.get(id=id)
    obj.Category = category
    obj.Type = type
    obj.Price = price
    obj.save()

    return redirect('/myapp/adm_view_waste_category_get/')

def delete_waste_category(request,id):
    Category.objects.get(id=id).delete()
    return redirect('/myapp/adm_view_waste_category_get/')


def adm_view_feedback_get(request):
    data=Feedback.objects.all()
    return render(request,'adminpages/viewfeedback.html',{'data':data})

def adm_change_password_get(request):
    return render(request,'adminpages/changepassword.html')

def adm_change_password_post(request):
    currentpass=request.POST['currentpass']
    newpass=request.POST['newpass']
    confirmpass=request.POST['confirmpass']
    user=request.user
    if user.check_password(currentpass):
        if newpass==confirmpass:
            user.set_password(newpass)
            user.save()
            return redirect('/myapp/login_get/')
        else:
            return redirect('/myapp/adm_change_password_get/')
    else:
        return redirect('/myapp/adm_change_password_get/')


def adm_send_reply_get(request,id):
    return render(request,'adminpages/Send reply.html',{'id':id})

def adm_send_reply_post(request):
    id = request.POST['id']
    reply= request.POST['reply']
    Complaint.objects.filter(id=id).update(Status="Replied",Reply=reply)
    return redirect("/myapp/adm_view_compliant_get/")



##-------------------------------------- P I C K U P ---------------------------------------------
def pickupindex_get(request):
    return render(request,'pickuppages/pickupindex.html')

def pickup_register(request):
    area = Area.objects.all()
    return render(request,'pickuppages/register.html',{"area":area})

def pickup_register_post(request):
    name = request.POST['name']
    logo = request.FILES['logo']
    email = request.POST['email']
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']
    phone = request.POST['phone']
    area = request.POST['area']
    tagline = request.POST['tagline']

    fs=FileSystemStorage()
    date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
    fs.save(date,logo)
    path=fs.url(date)

    user=User.objects.create(username=email,password=make_password(phone))
    user.groups.add(Group.objects.get(name='Pickup'))
    user.save()

    data = Pickup()
    data.Name = name
    data.Logo = path
    data.Email = email
    data.Phone = phone
    data.Tagline = tagline
    data.Latitude = latitude
    data.Longitude = longitude
    data.Status = 'pending'
    data.AREA_id= area
    data.AUTHUSER = user
    data.save()
    return redirect("/myapp/login_get/")


def pickup_viewprofile(request):
    pickup = Pickup.objects.get(AUTHUSER=request.user)
    return render(request,'pickuppages/view profile.html',{'pickup': pickup})

def pickup_editprofile(request):
    a=Pickup.objects.get(id=request.user)
    return render(request,'pickuppages/edit profile.html', {'pickup': a})

def pickup_editprofile_post(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    logo = request.POST['logo']
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']
    area = request.POST['area']
    tagline = request.POST['tagline']

    pickup = Pickup.objects.get(AUTHUSER=request.user)

    pickup.Name = name
    pickup.Latitude =latitude
    pickup.Longitude = longitude
    pickup.Email = email
    pickup.Phone = phone
    pickup.Tagline = tagline
    pickup.AREA_id = area
    pickup.Logo = logo
    pickup.save()

    return redirect('/myapp/pickup_viewprofile/')



def pickup_managestaff(request):
    a=Subarea.objects.filter(PICKUP__AUTHUSER=request.user)
    return render(request,'pickuppages/manage staff.html',{'data':a})

def pickup_managestaff_post(request):
    name = request.POST['name']
    photo = request.FILES['photo']
    license = request.FILES['license']
    dob = request.POST['dob']
    gender = request.POST['gender']
    email = request.POST['email']

    phone = request.POST['phone']
    subarea = request.POST['subarea']

    a=User.objects.create_user(username=email,password=phone)
    a.groups.add(Group.objects.get(name='Staff'))

    fs=FileSystemStorage()
    date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
    fs.save(date,photo)
    path=fs.url(date)

    fs1 = FileSystemStorage()
    date1 = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
    fs1.save(date1, license)
    path1 = fs1.url(date1)

    obj=Staff()
    obj.Name = name
    obj.Photo = path
    obj.License = path1
    obj.Email = email
    obj.Number = phone
    obj.DOB = dob

    obj.Gender = gender
    obj.SUBAREA = Subarea.objects.get(id=subarea)
    obj.AUTHUSER=a
    obj.save()

    return redirect('/myapp/pickup_viewstaff/')


def pickup_editstaff(request,id):
    a=Staff.objects.get(id=id)
    b=Subarea.objects.all()
    return render(request,'pickuppages/edit staff.html',{'data':a,'data1':b})

def pickup_editstaff_post(request):
    name = request.POST['name']

    dob = request.POST['dob']
    gender = request.POST['gender']
    email = request.POST['email']
    phone = request.POST['phone']
    subarea = request.POST['subarea']
    id = request.POST['id']
    obj=Staff.objects.get(id=id)


    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs=FileSystemStorage()
        date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
        fs.save(date,photo)
        path=fs.url(date)
        obj.Photo = path
        obj.save()

    if 'license' in request.FILES:
        license = request.FILES['license']
        fs1 = FileSystemStorage()
        date1 = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        fs1.save(date1, license)
        path1 = fs1.url(date1)
        obj.License = path1
        obj.save()

    obj.Name = name
    obj.Email = email
    obj.Number = phone
    obj.DOB = dob
    obj.Gender = gender
    obj.SUBAREA_id =  subarea
    obj.save()

    return redirect('/myapp/pickup_viewstaff/')

def delete_staff(request,id):
    Staff.objects.get(AUTHUSER_id=id).delete()
    User.objects.get(id=id).delete()
    return redirect('/myapp/pickup_viewstaff/')




def pickup_managesubarea(request):
    area = Area.objects.all()
    return render(request,'pickuppages/manage subarea.html',{"area":area})


def pickup_managesubarea_post(request):
    area = request.POST['area']
    subarea = request.POST['subarea']

    data = Subarea()
    data.Subarea = subarea
    data.AREA_id = area
    data.PICKUP = Pickup.objects.get(AUTHUSER=request.user)
    data.save()
    return redirect('/myapp/pickup_viewsubarea/')

def pickup_viewstafffeedback(request):
    a=Feedback.objects.all()
    return render(request,'pickuppages/view staff feedback.html',{"data":a})

def pickup_viewsubarea(request):
    data=Subarea.objects.filter(PICKUP__AUTHUSER=request.user)
    return render(request,'pickuppages/view sub area.html',{"data":data})

def pickup_editsubarea(request,id):
    area = Area.objects.all()
    data = Subarea.objects.get(id=id)
    return render(request,'pickuppages/edit subarea.html',{"area":area,"data":data})

def pickup_editsubarea_post(request):
    id = request.POST['id']
    area = request.POST['area']
    subarea = request.POST['subarea']

    data = Subarea.objects.get(id=id)
    data.Subarea = subarea
    data.AREA_id = area
    data.save()
    return redirect('/myapp/pickup_viewsubarea/')

def pickup_deletesubarea(request,id):
    Subarea.objects.get(id=id).delete()
    return redirect('/myapp/pickup_viewsubarea/')

def pickup_viewwasterequest(request):
    a = WasteRequest.objects.filter(PICKUP__AUTHUSER=request.user)
    return render(request,'pickuppages/view waste req.html',{'data':a})


def pickup_viewapproved_waste_req(request):
    a = WasteRequest.objects.filter(PICKUP__AUTHUSER=request.user,Status='approved')
    return render(request,'pickuppages/view approved waste request.html',{'data':a})


def pickup_viewassignedstaff(request,id):
    request.session['pid']=id
    data = AssignStaff.objects.filter(WASTEREQ_id=id)
    return render(request,'pickuppages/view assigned work.html',{"data":data})

def pickup_assignstaff(request,id):
    request.session['pid'] = id
    a=WasteRequest.objects.get(id=id)
    b=Staff.objects.all()
    return render(request,'pickuppages/assign staff.html',{'data':a,'data1':b})

def pickup_assignstaff_post(request):
    staff =request.POST['staff']
    id =request.POST['id']


    a=AssignStaff()
    a.STAFF_id=staff
    a.Date=datetime.now().date()
    a.Status="pending"
    a.WASTEREQ_id=id
    a.save()

    return redirect(f"/myapp/pickup_viewassignedstaff/{request.session['pid']}")




def pickup_editassignedstaff(request,id):
    a=Staff.objects.all()
    b=AssignStaff.objects.get(id=id)
    return render(request,'pickuppages/edit assigned staff.html',{"data":a,"data1":b})

def pickup_edit_assignedstaff_post(request):
    staff =request.POST['staff']
    Date =request.POST['date']
    id =request.POST['id']


    a=AssignStaff.objects.get(id=id)
    a.STAFF_id=staff
    a.Date=Date
    a.Status="pending"
    a.save()

    return redirect('/myapp/pickup_viewassignedstaff/')


def pickup_deleteassignedstaff(request,id):
    AssignStaff.objects.get(id=id).delete()
    return redirect('/myapp/pickup_viewassignedstaff/')


def pickup_viewstaff(request):
    data = Staff.objects.filter(SUBAREA__PICKUP__AUTHUSER=request.user)
    return render(request,'pickuppages/view staff.html',{"data":data})

def pickup_viewstatus(request):
    return render(request,'pickuppages/view status.html')

def pickup_viewbill(request,id):
    request.session['rid']=id
    a=Bill.objects.filter(WASTEREQ_id=id)
    return render(request,'pickuppages/view bill.html',{'data':a})

def approve_wasterequest(request,id):

    WasteRequest.objects.filter(id=id).update(Status='approved')
    return redirect('/myapp/pickup_viewwasterequest/')


def reject_wasterequest(request, id):
    WasteRequest.objects.filter(id=id).update(Status='rejected')
    return redirect('/myapp/pickup_viewwasterequest/')


def pickup_managebill(request,id):
    return render(request,'pickuppages/manage bill.html',{'id':id})

def pickup_managebill_post(request):
    bill = request.FILES['Bill']
    id = request.POST['id']

    fs = FileSystemStorage()
    date = datetime.now().strftime('%Y%m%d%H%M%S') + '.pdf'
    fs.save(date, bill)
    path = fs.url(date)

    a=Bill()
    a.Bill=path
    a.WASTEREQ=WasteRequest.objects.get(id=id)
    a.save()
    return redirect(f"/myapp/pickup_viewbill/{request.session['rid']}")


def pickup_changepassword(request):
    return render(request,'pickuppages/change password.html')

def pickup_changepassword_post(request):
    currentpass = request.POST['currentpass']
    newpass = request.POST['newpass']
    confirmpass = request.POST['confirmpass']
    user = request.user
    if user.check_password(currentpass):
        if newpass == confirmpass:
            user.set_password(newpass)
            user.save()
            return redirect('/myapp/login_get/')
        else:
            return redirect('/myapp/pickup_changepassword/')
    else:
        return redirect('/myapp/pickup_changepassword/')


def pickup_chatwithuser(request):
    return render(request,'pickuppages/chat with user.html')

def pickup_chatwithuser_post(request):

    return



###-------------------------------------- Staff ---------------------------------------------

def flutter_login(request):
    username=request.POST["Username"]
    password=request.POST["Password"]
    print(username,password)
    user=authenticate(username=username,password=password)
    print("uuuuuuuuuuu",user)
    if user is not None:
        login(request,user)
        print("jjjjjjjjjjjjjjjj")
        if user.groups.filter(name="Staff").exists():
            print("kkkkkkkkkkkkkkkkk")
            return JsonResponse({'status':'ok','lid':str(user.id),'type':'Staff'})
        elif user.groups.filter(name="User").exists():
            print("ooooooooooooo")
            return JsonResponse({'status':'ok','lid':str(user.id),'type':'user'})

        else:
            return JsonResponse({'status':'no'})
    else:
        return JsonResponse({'status': 'no'})


def staff_view_profile(request):
    lid=request.POST["lid"]
    s=Staff.objects.get(AUTHUSER_id=lid)
    return JsonResponse({'status':'ok','id':s.id,
                         'name':s.Name,
                         'photo':s.Photo,
                         'license':s.License,
                         'email':s.Email,
                         'number':s.Number,
                         'dob':s.DOB,
                         'gender':s.Gender,
                         'subarea':s.SUBAREA.Subarea
                          })


def flutter_change_password(request):
    currentpass=request.POST['currentpass']
    newpass=request.POST['newpass']
    confirmpass=request.POST['confirmpass']
    lid=request.POST['lid']
    user=User.objects.get(id=lid)
    if user.check_password(currentpass):
        if newpass==confirmpass:
            user.set_password(newpass)
            user.save()
            return JsonResponse({'status': 'ok'})

        else:
            return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status': 'no'})


def staff_update_status(request):

    work_id=request.POST['work_id']
    wrid=request.POST['wrid']
    amt=request.POST['amount']
    AssignStaff.objects.filter(id=work_id).update(Status='completed')
    p=Payment()
    p.Date=datetime.now().date()
    p.amount=amt
    p.Status='Done'
    p.WASTEREQ_id=wrid
    p.save()

    return JsonResponse({'status': 'ok'})



def staff_viewassignedwork(request):
    lid=request.POST["lid"]
    s=AssignStaff.objects.filter(STAFF__AUTHUSER_id=lid,Status="pending")

    l=[]
    for i in s:
        l.append({'id':i.id,'username':i.WASTEREQ.USERS.Name,
                  'useremail':i.WASTEREQ.USERS.Email,
                  'date':i.Date,
                  'userphone':i.WASTEREQ.USERS.Number,

                 'category': i.WASTEREQ.CATEGORY.Category,
                 'cat_type': i.WASTEREQ.CATEGORY.Type,
                 'cat_price': i.WASTEREQ.CATEGORY.Price,
                 'wrid': i.WASTEREQ.id,
                 'Latitude': i.WASTEREQ.Latitude,
                 'Longitude': i.WASTEREQ.Longitude,
                 'pickupname': i.WASTEREQ.PICKUP.Name,
                  'pickupemail': i.WASTEREQ.PICKUP.Email,
                  'pickupphone': i.WASTEREQ.PICKUP.Phone,
                  'pickuparea': i.WASTEREQ.PICKUP.AREA.Area,
                  'status': i.Status,
                  })
    return JsonResponse({'status':'ok','data':l,})


def staff_viewuserfeedback(request):
    lid=request.POST["lid"]
    print(lid)
    s=Feedback.objects.filter(STAFF__AUTHUSER_id=lid)
    l=[]
    for i in s:
        l.append({'id':i.id,
                  'username':i.USERS.Name,
                  'useremail':i.USERS.Email,
                  'date': i.Date,
                  'feedback': i.Feedback,
                  'rating': i.Rating})



    print(l)
    return JsonResponse({'status':'ok','data':l,})


def staff_viewpayment(request):
    lid=request.POST["lid"]
    h=AssignStaff.objects.filter(STAFF__AUTHUSER=lid).values_list("WASTEREQ",flat=True)
    print(h)
    s=Payment.objects.filter(WASTEREQ__in=h)
    l=[]
    for i in s:
        l.append({'id':i.id,'username':i.WASTEREQ.USERS.Name,
                  'useremail':i.WASTEREQ.USERS.Email,
                  'date': i.Date,
                  'amount': i.amount,
                  'status': i.Status})


    return JsonResponse({'status':'ok','data':l,})


#Users

def user_viewarea(request):
    s=Area.objects.all()
    l=[]
    for i in s:
        l.append({'id':i.id,'area':i.Area,   })
    return JsonResponse({'status':'ok','data':l,})


def user_signup(request):
    name = request.POST['uname']
    photo = request.FILES['photo']
    dob = request.POST['udob']
    gender = request.POST['ugender']
    email = request.POST['uemail']
    phone = request.POST['uphoneno']
    area = request.POST['area']
    password = request.POST['password']
    confirmpassword = request.POST['confirmpassword']

    if password!=confirmpassword:
        return JsonResponse({'Password does not match'})


    a=User.objects.create_user(username=email,password=password)
    a.groups.add(Group.objects.get(name='User'))
    a.save()

    fs=FileSystemStorage()
    date=datetime.now().strftime('%Y%m%d%H%M%S')+'.jpg'
    fs.save(date,photo)
    path=fs.url(date)

    obj=Users()
    obj.Name = name
    obj.Photo = path
    obj.Email = email
    obj.Number = phone
    obj.DOB = dob
    obj.Gender = gender
    obj.AREA = Area.objects.get(id=area)
    obj.AUTHUSER=a
    obj.save()

    return JsonResponse({"status":'ok'})



def user_editprofile(request):
    name = request.POST['uname']
    dob = request.POST['udob']
    gender = request.POST['ugender']
    email = request.POST['uemail']
    phone = request.POST['uphoneno']
    area = request.POST['area']
    id = request.POST['lid']
    obj=Users.objects.get(AUTHUSER_id=id)

    a=User.objects.get(id=id)
    a.username=email
    a.save()

    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        fs.save(date, photo)
        path = fs.url(date)
        obj.Photo = path
        obj.save()

    obj.Name = name
    obj.Email = email
    obj.Number = phone
    obj.DOB = dob
    obj.Gender = gender
    obj.AREA = Area.objects.get(id=area)
    obj.save()

    return JsonResponse({"status":'ok'})

def user_view_profile(request):
    lid=request.POST["lid"]
    s=Users.objects.get(AUTHUSER_id=lid)
    return JsonResponse({'status':'ok','id':s.id,
                         'name':s.Name,
                         'photo':s.Photo,
                         'email':s.Email,
                         'number':s.Number,
                         'dob':s.DOB,
                         'gender':s.Gender,
                         'area':s.AREA.Area
                          })


def user_send_complaint(request):
    complaint = request.POST['complaint']
    lid = request.POST['lid']

    obj=Complaint()
    obj.Date = datetime.now().date()
    obj.Complaint = complaint
    obj.Reply = 'pending'
    obj.Status = 'pending'
    obj.USERS = Users.objects.get(AUTHUSER=lid)

    obj.save()

    return JsonResponse({"status":'ok'})

def user_view_complaint_reply(request):
    lid=request.POST['lid']
    a=Complaint.objects.filter(USERS__AUTHUSER_id=lid)
    l=[]
    for i in a:
        l.append({'id':i.id,
                  'Date':i.Date,
                  'Complaint':i.Complaint,
                  'Reply':i.Reply,
                  'Status':i.Status
                  })
        print(l)
        return JsonResponse({'status':'ok','data':l})


def user_send_feedback(request):
    lid=request.POST['lid']
    sid=request.POST['sid']
    feedback=request.POST['feedback']
    rating=request.POST['rating']

    obj=Feedback()
    obj.Feedback=feedback
    obj.Rating=rating
    obj.Date=datetime.now().date()
    obj.USERS=Users.objects.get(AUTHUSER_id=lid)
    obj.STAFF=Staff.objects.get(id=sid)
    obj.save()
    return JsonResponse({'status':'ok'})


def user_view_assigned_staff(request):
    lid=request.POST['lid']
    a=AssignStaff.objects.filter(WASTEREQ__USERS__AUTHUSER=lid)
    l=[]
    for i in a:
        l.append({'id':i.id,
                  'Name':i.STAFF.Name,
                  'Sid':i.STAFF.id,
                  'Photo':i.STAFF.Photo,
                  'License':i.STAFF.License,
                  'Email':i.STAFF.Email,
                  'Number':i.STAFF.Number,
                  'DOB':i.STAFF.DOB,
                  'Gender':i.STAFF.Gender,
                  'SUBAREA':i.STAFF.SUBAREA.Subarea,
                  'CATEGORY':i.WASTEREQ.CATEGORY.Category,
                  'LATITUDE':i.WASTEREQ.Latitude,
                  'LONGITUDE':i.WASTEREQ.Longitude,
                  'Type':i.WASTEREQ.CATEGORY.Type,
                  'Price':i.WASTEREQ.CATEGORY.Price
                  })
    print(l)
    return JsonResponse({'status':'ok','data':l})


def user_view_pickup(request):
    a=Pickup.objects.all()
    l=[]
    for i in a:
        l.append({'id':i.id,
                  'Name': i.Name,
                  'Logo': i.Logo,
                  'Email': i.Email,
                  'Phone': i.Phone,
                  'Tagline': i.Tagline,
                  'Status': i.Status,
                  'AREA': i.AREA.Area
                  })
    print(l)
    return JsonResponse({'status':'ok','data':l})


import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in KM
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c



# def user_send_wasterequest(request):
#     lid=request.POST['lid']
#     cat=request.POST['cat']
#     latitude=request.POST['latitude']
#     longitude=request.POST['longitude']
#
#     obj=WasteRequest()
#     obj.latitude=latitude
#     obj.longitude=longitude
#     obj.USERS=Users.objects.get(AUTHUSER=lid)
#     obj.CATEGORY_id=cat
#     obj.save()
#     return JsonResponse({"status":'ok'})


def user_send_wasterequest(request):
    lid = request.POST['lid']
    cat = request.POST['cat']
    latitude = float(request.POST['latitude'])
    longitude = float(request.POST['longitude'])

    user = Users.objects.get(AUTHUSER=lid)

    pickups = Pickup.objects.all()

    nearest_pickup = None
    min_distance = float('inf')

    for p in pickups:
        if p.Latitude and p.Longitude:
            dist = haversine(
                latitude,
                longitude,
                float(p.Latitude),
                float(p.Longitude)
            )
            if dist < min_distance:
                min_distance = dist
                nearest_pickup = p

    if not nearest_pickup:
        return JsonResponse({"status": "failed", "msg": "No pickup available"})

    obj = WasteRequest()
    obj.Date = datetime.now().today()
    obj.Status = "Pending"
    obj.Latitude = latitude
    obj.Longitude = longitude
    obj.USERS = user
    obj.CATEGORY_id = cat
    obj.PICKUP = nearest_pickup
    obj.save()

    return JsonResponse({
        "status": "ok",
        "pickup_id": nearest_pickup.id,
        "distance_km": round(min_distance, 2)
    })



def user_change_password(request):
    currentpass=request.POST['currentpass']
    newpass=request.POST['newpass']
    confirmpass=request.POST['confirmpass']
    lid=request.POST['lid']
    user=User.objects.get(id=lid)
    if user.check_password(currentpass):
        if newpass==confirmpass:
            user.set_password(newpass)
            user.save()
            return JsonResponse({'status': 'ok'})

        else:
            return JsonResponse({'status': 'no'})
    else:
        return JsonResponse({'status': 'no'})

def user_view_category(request):
    a=Category.objects.all()
    l=[]
    for i in a:
        l.append({'id':i.id,
                  'Category': i.Category,
                  'Type': i.Type,
                  'Price': i.Price,

                  })
    print(l)
    return JsonResponse({'status':'ok','data':l})


def user_view_request_status(request):
    lid=request.POST['lid']
    a=WasteRequest.objects.filter(USERS__AUTHUSER_id=lid)
    l=[]
    for i in a:
        l.append({'id':i.id,
                  'Date': i.Date,
                  'Status': i.Status,
                  'Latitude': i.Latitude,
                  'Longitude': i.Longitude,
                  'Category': i.CATEGORY.Category,
                  'pickid': i.PICKUP.AUTHUSER.id,
                  'Pickup': i.PICKUP.Name,
                  'Price': i.CATEGORY.Price,
                  })
    print(l)
    return JsonResponse({'status':'ok','data':l})

def user_view_payment_status(request):
    lid=request.POST['lid']
    a=Payment.objects.filter(WASTEREQ__USERS__AUTHUSER_id=lid)
    l=[]
    for i in a:
        l.append({'id':i.id,
                  'Date': i.Date,
                  'Amount': i.amount,
                  'Type': i.WASTEREQ.CATEGORY.Type,
                  'Status': i.Status,
                  'Category': i.WASTEREQ.CATEGORY.Category,
                  })
    print(l)
    return JsonResponse({'status':'ok','data':l})


def chat1(request,id):
    request.session["userid"] = id
    cid = str(request.session["userid"])
    # request.session["new"] = cid
    qry = Users.objects.get(AUTHUSER=cid)

    return render(request, "pickuppages/Chat.html", { 'name': qry.Name, 'toid': cid})

def chat_view(request):
    fromid = request.user
    toid = request.session["userid"]
    qry = Users.objects.get(AUTHUSER=request.session["userid"])
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROMUSER_id=fromid.id, TOUSER_id=toid) | Q(FROMUSER_id=toid, TOUSER_id=fromid.id)).order_by('id')
    l = []

    for i in res:
        l.append({"id": i.id, "message": i.Message, "to": i.TOUSER_id, "Date": i.Date, "from": i.FROMUSER_id})

    return JsonResponse({'photo': qry.Photo, "data": l, 'name': qry.Name, 'toid': request.session["userid"]})

def chat_send(request, msg):
    lid = request.user
    toid = request.session["userid"]
    message = msg

    import datetime
    d = datetime.datetime.now().date()
    chatobt = Chat()
    chatobt.Message = message
    chatobt.TOUSER_id = toid
    chatobt.FROMUSER_id = lid.id
    chatobt.Date = d
    chatobt.save()

    return JsonResponse({"status": "ok"})




def User_sendchat(request):
    FROM_id=request.POST['from_id']
    TOID_id=request.POST['to_id']
    print(FROM_id)
    print(TOID_id)
    msg=request.POST['message']

    from  datetime import datetime
    c=Chat()
    c.FROMUSER_id=FROM_id
    c.TOUSER_id=TOID_id
    c.Message=msg
    c.Date=datetime.now()
    c.save()
    return JsonResponse({'status':"ok"})


def User_viewchat(request):
    fromid = request.POST["from_id"]
    print(fromid)
    toid = request.POST["to_id"]
    print(toid)
    # lmid = request.POST["lastmsgid"]
    from django.db.models import Q

    res = Chat.objects.filter(Q(FROMUSER_id=fromid, TOUSER_id=toid) | Q(FROMUSER_id=toid, TOUSER_id=fromid)).order_by('id')
    l = []

    for i in res:
        l.append({"id": i.id, "msg": i.Message, "from": i.FROMUSER_id, "Date": i.Date, "to": i.TOUSER_id})

    return JsonResponse({"status":"ok",'data':l})

# j=User.objects.get(username="farhank89434@gmail.com")
# j.set_password("12345")
# j.save()


def userupload(request):

    file= request.FILES["photo"]
    from  datetime import  datetime

    fname= datetime.now().strftime("%Y%m%d%H%M%S")+".jpg"

    fs=FileSystemStorage()
    fs.save(fname,file)


    mpath="C:\\Users\\Saiph\\PycharmProjects\\wastemanagement\\media\\"+fname

    key="AIzaSyDnXMN9qIcZIoQml8lAkm2-WhvE9JMD2Bo"

    import google.generativeai as genai
    from PIL import Image

    genai.configure(api_key="AIzaSyCAAHs3rtoRSaPDg8vkr_ywenxWYdx0U0I")  # Replace with your actual key

    f = r"C:\Riss\/opra\web\opra\media\20260102000746.jpg"
    #######################################

    import google.generativeai as genai
    import json

    image = Image.open(mpath)

    model = genai.GenerativeModel("gemini-flash-latest")

    prompt = """
           Analyze this food image and respond ONLY in valid JSON.
           Required JSON format:
           {
               "type of waste": "",

           }
           Do NOT add explanation.
           """

    response = model.generate_content(
        [prompt, image],
        stream=False
    )

    # Clean response (important if model adds formatting)
    cleaned_text = response.text.strip()

    # Convert to Python dictionary
    data = json.loads(cleaned_text)


    print(data)


    return  JsonResponse(
        {
            'status':'ok',
            'data':data['type of waste']
        }
    )


