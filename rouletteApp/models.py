from django.db import models
import datetime
from django.db import models
from django.utils import timezone
from django.utils.timezone import make_aware



class Reciept(models.Model):
    uidString = models.CharField(max_length=255, unique=True)
    retailer = models.CharField(max_length=255)
    purchaseDate = models.DateField()
    purchaseTime = models.TimeField()
    total = models.FloatField()
    total_points = models.FloatField(null=True, blank=True)

    def calculate_points(self):
        try:
            self.total_points = (
                self.calculate_item_description_points() +
                self.calculate_items_points() +
                self.calculate_multiple_of_25_points() +
                self.calculate_round_dollar_points() +
                self.calculate_alphanumeric_points() +
                self.odd_day() 
            )
        except Exception as e:
            raise e#ValueError("Receipt Incomplete")
    
    def calculate_round_dollar_points(self):
        if self.total % 1 == 0:
            return 50.0
        return 0.0
    
    def calculate_multiple_of_25_points(self):
        if self.total % 0.25 == 0:
            return 25.0
        return 0.0
    
    def calculate_items_points(self):
        return float(self.items.count() / 2 * 5)
    
    def calculate_item_description_points(self):
        print(self.items.all())
        points = 0.0
        for item in self.items.all():
            description = item.shortDescription.strip()
            if len(description) % 3 == 0:
                points += round(item.price * 0.2)
        return points
    
    def calculate_alphanumeric_points(self):
        points = 0.0
        for c in self.retailer:
            if c.isalnum():
                points += 1
        return points
    
    def odd_day(self):
        if isinstance(self.purchaseDate, str):
            self.purchaseDate = datetime.datetime.strptime(self.purchaseDate, '%Y-%m-%d').date()
        return 6.0 if self.purchaseDate.day % 2 != 0 else 0.0
    
    
    def __str__(self):
        return f"Reciept(uid_string={self.uid_string}, retailer={self.retailer}, purchaseDate={self.purchaseDate}, purchaseTime={self.purchaseTime}, total={self.total})"



class Item(models.Model):
    receipt = models.ForeignKey(Reciept, related_name='items', on_delete=models.CASCADE)
    shortDescription = models.CharField(max_length=255)
    price = models.FloatField()
    
    def __str__(self):
        return f"{self.shortDescription} price: {self.price}"

