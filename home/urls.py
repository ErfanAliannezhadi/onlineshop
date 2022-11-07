from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('',views.HomeView.as_view(),name='homepage'),
    path('bucket/', views.BucketView.as_view(),name='bucket'),
    path('bucket/delete/<key>/',views.BucketObjectDeleteView.as_view(), name='bucket_delete'),
    path('bucket/dowmload/<key>/', views.BucketObjectDownloadView.as_view(), name='bucket_download'),
    path('category/<slug:category_slug>/',views.CategoryView.as_view(), name='category_detail'),
    path('products/<slug:product_slug>/', views.ProductView.as_view(), name='product_detail')

]