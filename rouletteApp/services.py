# services.py
from .models import Reciept, Item

from django.shortcuts import get_object_or_404



def save_receipt(receipt_data):
    try:
        existing_receipt = Reciept.objects.filter(uidString=receipt_data['uidString']).first()
        print(existing_receipt)
        if not receipt_data['items']:
            return "Invalid Receipt without Items"

        if existing_receipt:
            return "Receipt Already exists"

        # Pop the items data
        items_data = receipt_data.pop('items')
        new_receipt = Reciept.objects.create(
            uidString=receipt_data['uidString'],
            retailer=receipt_data['retailer'],
            purchaseDate=receipt_data['purchaseDate'],
            purchaseTime=receipt_data['purchaseTime'],
            total=float(receipt_data['total'])
        )
       
        # Add items to the receipt
        for item_data in items_data:
            Item.objects.create(
                receipt=new_receipt,
                shortDescription=item_data['shortDescription'],
                price=float(item_data['price'])
            )
        new_receipt.calculate_points()
        new_receipt.save()
        print("Points - ",new_receipt.total_points)
        return new_receipt.uidString
    except Exception as e:
        raise e
    
def get_points(uidString):
    try:
        existing_receipt = Reciept.objects.filter(uidString=uidString).first()
        
        if existing_receipt is None:
            raise ValueError(f"No receipt found with uidString: {uidString}")

        return existing_receipt.total_points

    except ValueError as ve:
          raise ve

    except Exception as e:
        raise ValueError("Error fetching receipt")
