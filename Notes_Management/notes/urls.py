from django.urls import path
from .views import home, add_note, edit_note, delete_note,signup,CustomLogin,CustomLogout,list_note,note_detail,user_list
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', home.as_view(), name='home'),
    path('add_note/', add_note.as_view(), name='add_note'),
    path('login/', CustomLogin.as_view(), name='login'),
    path('signup/', signup.as_view(), name='signup'),
    path('logout/', CustomLogout.as_view(), name='logout'),
    path('list_note/', list_note.as_view(), name='list_note'),
    path('user_list/', user_list.as_view(), name='user_list'),
    path('note_detail/<slug:slug>/',note_detail.as_view(),name='note_detail'),
    path('delete_note/<slug:slug>/', delete_note.as_view(), name='note_delete'),

    path('edit_note/<slug:slug>/', edit_note.as_view(), name='note_edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
