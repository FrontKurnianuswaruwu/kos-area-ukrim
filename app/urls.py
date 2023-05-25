from django.urls import path
from.views import index,tampilan,tambah_admin,post_masuk,tampilan_awal,update_user,postupdate_user,delete_user,tampilankost,tambah_kost,post_masukkost,update_kost,postupdate_kost,delete_kost
from.views import tampilan_penghuni,tambah_penghuni,post_masukpenghuni,update_penghuni,postupdate_penghuni,delete_penghuni,index2,login,login_post,dashboard_awal,tampilan_admin,detail_kamar,logout,dashboard
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('tampilan_admin',tampilan_admin,name='tampilanadmin'), 
    path('dashboard_awal',index,name='index'),
    path('tampilan',tampilan,name='tampilan.tamp'),
    path('tambah_admin',tambah_admin,name='tambahadmin'),
    path('post_masuk',post_masuk,name='postmasuk'),
    path('tampilan_awal',tampilan_awal,name='tampilanawal'),
    path('update_user/<str:idNama>',update_user,name='update'),
    path('postupdate_user',postupdate_user,name='postupdateuser'),
    path('selete_user/<str:idNama>',delete_user,name='deleteuser'),
    
#kamar kost  
    path('index2/<str:idKamar>',index2,name='index2'),
    path('tampilankost',tampilankost,name='tampilan.tampkost'),
    path('tambah_kost',tambah_kost,name='tambahkost'),
    path('post_masukkost',post_masukkost,name='postmasukkost'),
    path('update_kost/<str:idKamar>',update_kost,name='updatekost'),
    path('postupdate_kost',postupdate_kost,name='postupdatekost'),
    path('delete_kost/<str:idKamar>',delete_kost,name='deletekost'),
    
#penghuni     
    path('tampilan_penghuni',tampilan_penghuni,name='tampilanpenghunit'),
    path('tambah_penghuni',tambah_penghuni,name='tambahpenghuni'),
    path('post_masukpenghuni',post_masukpenghuni,name='postmasukpenghuni'),
    path('update_penghuni/<str:IdKamar>',update_penghuni,name='updatepenghuni'),
    path('postupdate_penghuni',postupdate_penghuni,name='postupdatepenghuni'),
    path('delete_penghuni/<str:IdKamar>',delete_penghuni,name='deletepenghuni'),
    
#login
    path('login_post',login_post,name='loginpost'),
    path('login',login,name='login'),
    
#logout
    path('logout',logout,name='logout'),
    
#user  
   path('',dashboard_awal,name='dashboardawal'),
   path('detail_kamar/<str:idKamar>',detail_kamar,name='detailkamar'),
   
#Dashboard
    path('dashboard',dashboard,name='dashboard'),
   
    
]  +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    
    

    
    

