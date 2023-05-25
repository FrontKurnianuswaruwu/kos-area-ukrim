from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Admin,KamarKost,penghuni,User
from django.contrib import messages
import json
from django.db.models import Q
from django.contrib.auth import authenticate, login
from .decorators import login_required

@login_required()
def dashboard(request):
    return HttpResponse('dashboardawal')
 
# Create your views here.
@login_required()
def index(request):
    if request.method == 'GET':
        namakost = request.GET.get('namakost')
        harga_min = request.GET.get('harga_min')
        harga_max = request.GET.get('harga_max')
        ac_checked = request.GET.get('ac')
        lemari_checked = request.GET.get('lemari')
        putra_checked = request.GET.get('Putra')
        putri_checked = request.GET.get('Putri')
        if namakost:
            kost = KamarKost.objects.filter(namakost__icontains=namakost,kodeadmin=request.session.get('idNama'))
        else:
            kost = KamarKost.objects.filter(kodeadmin=request.session.get('idNama'))
        if harga_min:
            kost = KamarKost.objects.filter(Harga__gte=harga_min,kodeadmin=request.session.get('idNama'))

        if harga_max:
            kost = KamarKost.objects.filter(Harga__lte=harga_max,kodeadmin=request.session.get('idNama'))
        if ac_checked:
            kost = KamarKost.objects.filter(FasilitasKOst__contains='ac',kodeadmin=request.session.get('idNama'))
        if lemari_checked:
            kost = KamarKost.objects.filter(FasilitasKOst__contains='lemari',kodeadmin=request.session.get('idNama'))
        if putra_checked:
            kost = KamarKost.objects.filter(status_kamar__contains='Putra',kodeadmin=request.session.get('idNama'))
        if putri_checked:
            kost = KamarKost.objects.filter(status_kamar__contains='Putri',kodeadmin=request.session.get('idNama'))
    return render(request, 'index.html', {'kost': kost})


@login_required()
def index2(request,idKamar):
    data_user = Admin.objects.filter(idNama=request.session.get('idNama'))
    kost = KamarKost.objects.get(idKamar=idKamar)
    context ={
        'kost' : kost,
        'data_user' : data_user
    }
    return render(request, 'index2.html',context)

def login(request):
    return render(request, 'login.html')

@login_required()
def tampilan_admin(request):
    return render(request, 'tampilan-admin.html') 
  
 
def login_post(request):
    idNama = request.POST['idNama'].upper()
    password = request.POST['password'].upper()
    if Admin.objects.filter(idNama=idNama).exists():
        admin = Admin.objects.get(idNama=idNama)
        if password == admin.password: 
            # simpan data session
            request.session['idNama'] = admin.idNama
            request.session['user_name'] = admin.user_name
            request.session.save()
            messages.success(request, 'BERHASIL LOGIN ')
            return redirect('tampilanadmin')
        else:
            messages.error(request, 'PASSWORD SALAH')
    else:
        messages.error(request, 'USER TIDAK DITEMUKAN')
    return redirect('login')

@login_required()
def tampilan(request):
    tamp = Admin.objects.all()
    context ={
        'temp' : tamp
    }
    return render (request, 'tampilan.html',context)


@login_required()
def tambah_admin(request):
    return render(request, 'tambah-admin.html')


def post_masuk(request):
    if request.method == 'POST':
        idNama = request.POST['idNama']
        user_name = request.POST['user_name']
        NoTelp = request.POST['NoTelp']
        email = request.POST['email']
        password = request.POST['password']
   
        # create admin object
        admin = Admin(password=password,user_name=user_name, NoTelp=NoTelp,email=email, idNama=idNama)
        admin.save()
        
        # redirect to login page
        return redirect('login')
   
@login_required()
def tampilan_awal(request):
    data_user = Admin.objects.filter(idNama=request.session.get('idNama'))
    context ={
        'data_user' :data_user
        
    }
    return render(request, 'tampilan-awal.html', context)

@login_required()
def update_user(request, idNama):
    data_user = Admin.objects.get(idNama=idNama)
    context = {
        'data_user' : data_user
    }
    return render(request,'update-user.html',context)

@login_required()
#ambil data post
def postupdate_user(request):
    idNama = request.POST['idNama']
    user_name = request.POST['user_name']
    NoTelp= request.POST['NoTelp']
    email = request.POST['email']
    #proses update
    admin = Admin.objects.get(idNama=idNama)
    if NoTelp == NoTelp :
        admin.user_name = user_name
        admin.NoTelp = NoTelp
        admin.email =email
        admin.save()
        messages.success(request,'BERHASIL UPDATE ADMIN')
    else:
        messages.success(request,'ID KAMR TIDAK COCOOK')
    return redirect(request.META.get('HTTP_REFERER','/'))

@login_required()
def delete_user(request, idNama):
    admin = Admin.objects.get(idNama=idNama).delete()
    messages.success(request,'BERHASIL HAPUS ADMIN')
    return redirect(request.META.get('HTTP_REFERER','/'))

@login_required()
def tampilankost(request):
    kamarkost = KamarKost.objects.filter(kodeadmin=request.session.get('idNama'))
    context = {
        'kamarkost' :kamarkost
    }
    return render(request, 'tampilankost.html', context)

@login_required()
def tambah_kost(request):
    return render(request, 'tambah-kost.html')


@login_required()
def post_masukkost(request):
    idKamar = request.POST['idKamar']
    TipeKamar = request.POST['TipeKamar']
    Harga = request.POST['Harga']
    FasilitasKOst = request.POST.getlist('FasilitasKOst[]')
    fasilitas_kost = ''
    for i in range(len(FasilitasKOst)):
        fasilitas_kost = fasilitas_kost + FasilitasKOst[i]
        if i != len(FasilitasKOst)-1:
            fasilitas_kost = fasilitas_kost + ','
    masaTenggang = request.POST['masaTenggang']
    gambar =  request.FILES['gambar']
    namakost = request.POST['namakost']
    status = request.POST['status']
    status_kamar = request.POST['status_kamar']
    alamat = request.POST['alamat']
    
    if KamarKost.objects.filter(idKamar=idKamar).exists():
        messages.error(request,'ID KAMAR SUDAH DIGGUNAKAN')
        return redirect(request.META.get('HTTP_REFERER', '/'))

    else :
        if idKamar==idKamar:
            admin = Admin.objects.get(idNama=request.session.get('idNama'))
            tambah_user = KamarKost(
                idKamar=idKamar,
                TipeKamar=TipeKamar,
                Harga=Harga,
                FasilitasKOst=fasilitas_kost,
                masaTenggang=masaTenggang,
                gambar=gambar,
                namakost=namakost,
                status=status,
                status_kamar=status_kamar,
                alamat=alamat,
                kodeadmin=admin
            )
            tambah_user.save()
            messages.success(request,'BERHASI TAMBAH KOST')
        else :
            messages.error(request,'ID KAMAR SUDAH DI GUNAKAN')
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def update_kost(request, idKamar):
    kost = KamarKost.objects.get(idKamar=idKamar)
    context = {
        'kost' : kost
    }
    return render(request,'update-kost.html',context)


@login_required()
def postupdate_kost(request):
    idKamar = request.POST['idKamar']
    TipeKamar = request.POST['TipeKamar']
    Harga = request.POST['Harga']
    FasilitasKOst = request.POST.getlist('FasilitasKOst[]')
    fasilitas_kost = ''
    for i in range(len(FasilitasKOst)):
        fasilitas_kost = fasilitas_kost + FasilitasKOst[i]
        if i != len(FasilitasKOst)-1:
            fasilitas_kost = fasilitas_kost + ','
    masaTenggang = request.POST['masaTenggang']
    namakost = request.POST['namakost']
    status = request.POST['status']
    status_kamar=request.POST['status_kamar']
    alamat = request.POST['alamat']
    #proses update
    admin = Admin.objects.get(idNama=request.session.get('idNama'))
    kamarkost = KamarKost.objects.get(idKamar=idKamar)
    if idKamar == idKamar:
        kamarkost.idKamar = idKamar
        kamarkost.TipeKamar = TipeKamar
        kamarkost.Harga = Harga
        kamarkost.FasilitasKOst = fasilitas_kost
        kamarkost.masaTenggang = masaTenggang
        kamarkost.namakost = namakost
        kamarkost.status = status
        kamarkost.status_kamar = status_kamar
        kamarkost.alamat = alamat
        kamarkost.kodeadmin = admin
        kamarkost.save()
        messages.success(request,'BERHASIL UPDATE KOST')
    else:
        messages.success(request,'ID KAMAR SUDAH DI GUNAKAN')
    return redirect(request.META.get('HTTP_REFERER','/'))

@login_required()
def delete_kost(request, idKamar):
    admin = KamarKost.objects.get(idKamar=idKamar).delete()
    messages.success(request,'BERHASIL HAPUS KOST')
    return redirect(request.META.get('HTTP_REFERER','/'))


@login_required()
def tampilan_penghuni(request):
    pemilik = penghuni.objects.filter(kodeadminpenghuni=request.session.get('idNama'))
    context ={
        'pemilik' : pemilik
    }
    return render (request, 'tampilanpenghuni.html',context)

@login_required()
def tambah_penghuni(request):
    listkamar = KamarKost.objects.filter(kodeadmin=request.session.get('idNama'))
    context = {
        'listkamar':listkamar
    }
    return render(request, 'tambah-penghuni.html',context)

@login_required()
def post_masukpenghuni(request):
    IdKamar = request.POST['IdKamar']
    NoTelepon = request.POST['NoTelepon']
    ktp  = request.POST['ktp ']
    
    
    if penghuni.objects.filter(IdKamar=IdKamar).exists():
        messages.error(request,'KAMAR SUDAH TERISI ')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    else :
        if IdKamar==IdKamar:
            admin = Admin.objects.get(idNama=request.session.get('idNama'))
            pemilik = penghuni(
                IdKamar=IdKamar,
                NoTelepon=NoTelepon,
                ktp=ktp,
                kodeadminpenghuni=admin 
            )
            pemilik.save()
            messages.success(request,'BERHASI TAMBAH PENGHUNI')
        else :
            messages.error(request,'ID KAMAR SUDAH DI GUNAKAN')
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required()
def update_penghuni(request, IdKamar):
    pemilik = penghuni.objects.get(IdKamar=IdKamar)
    context = {
        'pemilik' : pemilik
    }
    return render(request,'update-penghuni.html',context)


@login_required()
def postupdate_penghuni(request):
    IdKamar = request.POST['IdKamar']
    NoTelepon = request.POST['NoTelepon']
    ktp  = request.POST['ktp ']
    #proses update
    admin = Admin.objects.get(idNama=request.session.get('idNama'))
    pemilik = penghuni.objects.get(IdKamar=IdKamar)
    if IdKamar == IdKamar:
        pemilik.NoTelepon = NoTelepon
        pemilik.ktp = ktp
        pemilik.kodeadminpenghuni=admin 
        pemilik.save()
        messages.success(request,'BERHASIL UPDATE PENGHUNI')
    else:
        messages.success(request,'ID KAMAR SUDAH DI GUNAKAN')
    return redirect(request.META.get('HTTP_REFERER','/'))


@login_required()
def delete_penghuni(request, IdKamar):
    admin = penghuni.objects.get(IdKamar=IdKamar).delete()
    messages.success(request,'BERHASIL HAPUS PENGHUNI')
    return redirect(request.META.get('HTTP_REFERER','/'))

#user

def dashboard_awal(request):
    if request.method == 'GET':
        namakost = request.GET.get('namakost')
        harga_min = request.GET.get('harga_min')
        harga_max = request.GET.get('harga_max')
        ac_checked = request.GET.get('ac')
        lemari_checked = request.GET.get('lemari')
        putra_checked = request.GET.get('Putra')
        putri_checked = request.GET.get('Putri')
        if namakost:
            kost = KamarKost.objects.filter(namakost__icontains=namakost)
        else:
            kost = KamarKost.objects.filter()
        if harga_min:
            kost = KamarKost.objects.filter(Harga__gte=harga_min)

        if harga_max:
            kost = KamarKost.objects.filter(Harga__lte=harga_max)
        if ac_checked:
            kost = KamarKost.objects.filter(FasilitasKOst__contains='ac')
        if lemari_checked:
            kost = KamarKost.objects.filter(FasilitasKOst__contains='lemari')
        if putra_checked:
            kost = KamarKost.objects.filter(status_kamar__contains='Putra')
        if putri_checked:
            kost = KamarKost.objects.filter(status_kamar__contains='Putri')
        
    return render(request, 'index-user.html', {'kost': kost})

@login_required()
def detail_kamar(request,idKamar):
    data_user = Admin.objects.filter(idNama=request.session.get('idNama'))
    kost = KamarKost.objects.get(idKamar=idKamar)
    context ={
        'kost' : kost,
        'data_user' : data_user
    }
    return render(request, 'detailkamar-user.html',context)

#logout
def logout(request):
    # hapus data session
    request.session.flush()
    messages.success(request, 'BERHASIL LOGOUT')
    return redirect('login')

    
    


    
        
        



    
