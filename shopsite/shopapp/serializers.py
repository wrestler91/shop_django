from rest_framework import serializers
from .models import Item, RequestedItem, Category

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", 
                  "title", 
                  "description", 
                  "size", 
                  "price", 
                  "count", 
                  "discount", 
                  "brand", 
                  "time_update", 
                  "categ", 
                  )



class RequestedItemSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    categ = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
      model = RequestedItem
      fields = ("id",
                "title", 
                "comments", 
                "size", 
                "count", 
                "url",
                "categ",
                "user",
                )