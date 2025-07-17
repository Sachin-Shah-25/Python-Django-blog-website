from django.urls import path
from . import views
urlpatterns=[
    path("",views.home,name="index"),
    path("signup/",views.signup,name="signup"),
    path("signin/",views.signin,name="signin"),
    path("profile/",views.profile,name="profile"),
    path("create/",views.create,name="create"),
    path("blog/",views.blogs,name="blog"),
    path("delete/<int:id>",views.blogdelete,name="delete"),
    path("update/<int:id>",views.blogupdate,name="blogupdate"),
    path("view/<int:id>",views.blogview,name="view"),
    path("view/likes/<int:id>",views.increaselike,name="likes"),
    path("view/comment/<int:id>",views.comment,name="comment"),
    path("view/comment/delete/<int:id>",views.commentdel,name="commentdel"),
    path("contact/",views.contact,name="contact"),
    path("logout/",views.log_out,name="logout")
]