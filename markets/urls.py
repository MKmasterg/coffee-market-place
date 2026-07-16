from django.urls import path
from .views import MarketMain,MarketModification,Orders,Stocks,Search


app_name = "markets"

urlpatterns = [
    path("<int:market_id>/",MarketMain.MarketMainPage.as_view(),name="market_main"),
    path("edit/<int:market_id>/",MarketModification.MarketEdit.as_view(),name="market_edit"),
    path("delelte/<int:market_id>/",MarketModification.MarketDeletion.as_view(),name="market_delete"),
    path("stock/registration/<int:market_id>/",Stocks.StockRegistration.as_view(),name="stock_registration"),
    path("stock/deletion/<int:stock_id>/",Stocks.StockDeletion.as_view(),name="stock_deletion"),
    path("stock/modification/<int:stock_id>/",Stocks.StockModification.as_view(),name="stock_modification"),
    path("order/placeOrder/",Orders.PlaceOrder.as_view(),name="place_order"),
    path("search/",Search.SearchMarkets.as_view(),name="search"),
]
