import logging
import uuid
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import uuid
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .services import save_receipt, get_points as get_receipt_points
import json

logger = logging.getLogger(__name__)


@csrf_exempt
def process_receipt(request):
    if request.method == 'POST':
        try:
            # Parse JSON input
            receipt_data = json.loads(request.body)
            print(receipt_data)
            receipt_data['uidString'] = uuid.uuid4().hex
            
            logger.debug(receipt_data)
            
            uid = save_receipt(receipt_data)
            
            if uid == "Invalid Receipt without Items" or uid == "Receipt Already exists":
                return JsonResponse({'message': uid}, status=400)
            print("returning id:",uid)
            response = {'uid': uid}
            return JsonResponse(response, status=200)
        
        except Exception as e:
            logger.error(f"Error processing receipt: {str(e)}")
            return HttpResponseBadRequest()
    
    else:
        return HttpResponseBadRequest()

def get_points(request, id):
    if request.method == 'GET':
        try:
            points = get_receipt_points(id)
            print(points)
            if points == -1.0:
                return JsonResponse({'message': 'Invalid Receipt Id'}, status=400)
            
            response = {'points': points}
            return JsonResponse(response, status=200)
        
        except Exception as e:
            logger.error(f"Receipt with id {id} does not exist: {str(e)}")
            return JsonResponse({'message': 'Receipt not found'}, status=404)

    
    else:
        return HttpResponseBadRequest()