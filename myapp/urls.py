"""
URL configuration for wastemanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('login_get/',views.login_get),
    path('login_post/',views.login_post),
    path('adm_index_get/',views.adm_index_get),
    path('adm_add_waste_category_get/',views.adm_add_waste_category_get),
    path('adm_add_waste_category_post/',views.adm_add_waste_category_post),
    path('adm_verify_pickup_get/',views.adm_verify_pickup_get),
    path('approve_pickup/<id>',views.approve_pickup),
    path('reject_pickup/<id>',views.reject_pickup),
    path('adm_view_worker_get/',views.adm_view_worker_get),
    path('adm_view_user_category_get/',views.adm_view_user_category_get),
    path('adm_view_compliant_get/',views.adm_view_compliant_get),
    path('adm_add_waste_category_get/',views.adm_add_waste_category_get),
    path('adm_add_waste_category_post/',views.adm_add_waste_category_post),
    path('adm_view_waste_category_get/',views.adm_view_waste_category_get),
    path('adm_edit_waste_category_get/<id>',views.adm_edit_waste_category_get),
    path('delete_waste_category/<id>',views.delete_waste_category),
    path('adm_edit_waste_category_post/',views.adm_edit_waste_category_post),
    path('adm_view_feedback_get/',views.adm_view_feedback_get),
    path('adm_change_password_get/',views.adm_change_password_get),
    path('adm_change_password_post/',views.adm_change_password_post),
    path('adm_send_reply_get/<id>',views.adm_send_reply_get),
    path('adm_send_reply_post/',views.adm_send_reply_post),
    path('adm_verified_pickup_get/',views.adm_verified_pickup_get),
    path('adm_rejected_pickup_get/', views.adm_rejected_pickup_get),
#pickup
    path('pickupindex_get/', views.pickupindex_get),
    path('pickup_register/', views.pickup_register),
    path('pickup_register_post/', views.pickup_register_post),
    path('pickup_viewprofile/', views.pickup_viewprofile),
    path('pickup_editprofile/', views.pickup_editprofile),
    path('pickup_editprofile_post/', views.pickup_editprofile_post),
    # path('pickup_deleteprofile/<id>',views.delete_staff),
    path('pickup_managestaff/', views.pickup_managestaff),
    path('pickup_managestaff_post/', views.pickup_managestaff_post),
    path('delete_staff/<id>', views.delete_staff),
    path('pickup_viewstaff/', views.pickup_viewstaff),
    path('pickup_editstaff/<id>', views.pickup_editstaff),
    path('pickup_editstaff_post/', views.pickup_editstaff_post),
    path('pickup_managesubarea/', views.pickup_managesubarea),
    path('pickup_managesubarea_post/', views.pickup_managesubarea_post),
    path('pickup_viewsubarea/', views.pickup_viewsubarea),
    path('pickup_editsubarea/<id>',views.pickup_editsubarea),
    path('pickup_editsubarea_post/',views.pickup_editsubarea_post),
    path('pickup_deletesubarea/<id>', views.pickup_deletesubarea),
    path('pickup_viewstafffeedback/', views.pickup_viewstafffeedback),
    path('pickup_viewwasterequest/', views.pickup_viewwasterequest),
    path('pickup_assignstaff/<id>', views.pickup_assignstaff),
    path('pickup_viewassignedstaff/<id>', views.pickup_viewassignedstaff),
    path('pickup_assignstaff_post/', views.pickup_assignstaff_post),
    path('pickup_editassignedstaff/<id>', views.pickup_editassignedstaff),
    path('pickup_edit_assignedstaff_post/',views. pickup_edit_assignedstaff_post),
    path('pickup_deleteassignedstaff/<id>',views. pickup_deleteassignedstaff),
    path('pickup_viewstatus/', views.pickup_viewstatus),
    path('pickup_managebill/<id>', views.pickup_managebill),
    path('pickup_managebill_post/', views.pickup_managebill_post),
    path('pickup_viewbill/<id>', views.pickup_viewbill),
    path('pickup_changepassword/', views.pickup_changepassword),
    path('pickup_changepassword_post/', views.pickup_changepassword_post),
    path('pickup_chatwithuser/', views.pickup_chatwithuser),
    path('pickup_chatwithuser_post/', views.pickup_chatwithuser_post),
    path('pickup_viewapproved_waste_req/', views.pickup_viewapproved_waste_req),

    #Staff


    path('flutter_login/', views.flutter_login),
    path('staff_view_profile/', views.staff_view_profile),
    path('flutter_change_password/', views.flutter_change_password),
    path('staff_viewassignedwork/', views.staff_viewassignedwork),
    path('staff_viewuserfeedback/', views.staff_viewuserfeedback),
    path('staff_update_status/', views.staff_update_status),
    path('staff_viewpayment/', views.staff_viewpayment),
    path('user_view_payment_status/', views.user_view_payment_status),


    #Users
    path('user_viewarea/', views.user_viewarea),
    path('user_signup/', views.user_signup),
    path('user_view_profile/', views.user_view_profile),
    path('user_editprofile/', views.user_editprofile),
    path('user_send_complaint/', views.user_send_complaint),
    path('user_view_complaint_reply/', views.user_view_complaint_reply),
    path('user_send_feedback/', views.user_send_feedback),
    path('user_view_assigned_staff/', views.user_view_assigned_staff),
    path('user_view_pickup/', views.user_view_pickup),
    path('user_send_wasterequest/', views.user_send_wasterequest),
    path('user_view_category/', views.user_view_category),
    path('user_view_request_status/', views.user_view_request_status),
    path('chat1/<id>', views.chat1),
    path('chat_view/', views.chat_view),
    path('chat_send/<msg>', views.chat_send),
    path('User_sendchat/', views.User_sendchat),
    path('User_viewchat/', views.User_viewchat),
    path('approve_wasterequest/<id>', views.approve_wasterequest),
    path('reject_wasterequest/<id>', views.reject_wasterequest),
    path('userupload/', views.userupload),








]
