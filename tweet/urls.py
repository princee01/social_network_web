from . import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post-list'),
    path('post_create/',views.post_create,name="post-create"),
    path('/edit/<int:post_id>/',views.post_edit,name="post-edit"),
    path('<int:post_id>/delete/',views.post_delete,name="post-delete"),
    path('<int:post_id>/react/',views.react_to_post,name="react-to-post"),
    path('register/',views.register,name="register"),
    path('update_profile/',views.updateProfile,name="update-profile"),
    
    
]