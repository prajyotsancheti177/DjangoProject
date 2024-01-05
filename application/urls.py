from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('authors-sellers/', views.authors_sellers_page, name="author_sellers_page"),
    path('upload-image/', views.upload_image, name="upload_image"),
    path('uploaded-image/', views.uploaded_images, name="uploaded_images"),
    # path('authors-sellers/', views.authors_sellers_page.as_view(), name='authors_sellers_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)