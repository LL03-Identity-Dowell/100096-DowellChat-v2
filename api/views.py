from django.conf import settings
from django.http import HttpResponse
from api.connector.database_connector import DataCubeConnection
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from django.shortcuts import redirect, render
data_cube = DataCubeConnection()

@method_decorator(csrf_exempt, name='dispatch')
class serverStatus(APIView):

    def get(self, request):
        return Response({"info": "Server is working fine!!"},status=status.HTTP_200_OK)



"""PUBLIC RELEASE"""
public_namespace = '/public'
@api_view(['GET'])
@csrf_exempt
def public(request):
    return HttpResponse("Connected to Public Dowell Chat Backend")




def redirect_to_product_link(request):
    try:
        link_id = request.GET['link_id']
        workspace_id = request.GET['workspace_id']
        api_key = request.GET['link_key']

        db_name = f"{workspace_id}_cs_ticketing_system_db0"
        coll_name = f"{workspace_id}_master_link"
        filters = {"link_id": link_id, "is_active": True, "available_links": { "$ne": 0 }}

        find_link = data_cube.fetch_data(api_key=api_key,db_name=db_name, coll_name=coll_name, filters=filters,limit=1, offset=0)
        
        if find_link['success']:
            if find_link['data']:
                redirect_url = find_link['data'][0]['link']
                return redirect(redirect_url)
            
        
        return render(request, 'api/error.html')
    except KeyError as e:
        context = {
            "error": e
        }
        
        return render(request, 'api/error.html', context)
        # return HttpResponse(f"Missing parameter: {e}")
    
