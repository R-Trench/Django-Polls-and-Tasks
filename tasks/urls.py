from django.contrib import admin
from django.urls import path
from tasks import views

app_name = 'tasks'
urlpatterns = [
    path('admin/', admin.site.urls),

    #authentication urls
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),

    path('', views.homepage, name='homepage'),

    path('create/', views.createtodo, name='createtodo'),
    path('completed/', views.completedtodos, name='completedtodos'),
    path('current/', views.currenttodos, name='currenttodos'),
    path('view/<int:todo_pk>', views.viewtodos, name='viewtodos'),
    path('view/<int:todo_pk>/complete', views.completetodos, name='completetodos'),
    path('view/<int:todo_pk>/delete', views.deletetodos, name='deletetodos'),
]
