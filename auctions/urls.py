from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<int:listing_id>", views.listing_details, name="details"),
    path("listing/<int:listing_id>/take-bid", views.take_bid, name="takebid"),
    path("listing/<int:listing_id>/Add-comment", views.Add_comment, name="comment"),
    path("listing/<int:listing_id>/closelisting", views.close_listing, name="close"),
    path("watchlist", views.watchlist_index, name="watchistlindex"),
    path("watchlist/<int:listing_id>/add", views.add_watchlist, name="add_watchlist"),
    path("watchlist/<int:listing_id>/remove'", views.remove_watchlist, name="remove"),
    path("category/<int:category_id>", views.category_listing, name="category_listing"),
    path("category", views.category_view, name="category"),
    path("listing", views.new_listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
