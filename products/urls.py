from django.urls import path 
from .import views


urlpatterns = [
    path("bookmarks/",views.bookmarksUserAPIView.as_view()),
    path("suggested/<int:product_id>/",views.SuggestedProductAPIView.as_view()),
    path("bookmark/add/<int:product_id>/",views.BookmarkProductAPIView.as_view()),
    path("categorys/",views.CategoryAPIView.as_view()),
    path("",views.ProductAPIView.as_view()),
    path("<slug:slug_product>/",views.RetrieveProductAPIView.as_view()),
    
]
