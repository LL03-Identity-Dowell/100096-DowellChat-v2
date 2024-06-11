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
from django.shortcuts import redirect, render
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from api.utils.swagger_docs import get_master_link_docs

data_cube = DataCubeConnection()


@method_decorator(csrf_exempt, name='dispatch')
class serverStatus(APIView):
    @swagger_auto_schema(
        operation_description="Server Health Check",
    )
    def get(self, request):
        return Response({"info": "Server is working fine!!"}, status=status.HTTP_200_OK)


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
        filters = {"link_id": link_id, "is_active": True,
                   "available_links": {"$ne": 0}}

        find_link = data_cube.fetch_data(
            api_key=api_key, db_name=db_name, coll_name=coll_name, filters=filters, limit=1, offset=0)

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


class Masterlink(APIView):
    
    @swagger_auto_schema(
        operation_id='get_masterlink',
        operation_description="API endpoint for returning master links",
        manual_parameters=get_master_link_docs["masterlink_get_params"],
        responses=get_master_link_docs["masterlink_get_responses"] 
    )
    
    def get(self, request):
        workspace_id = request.query_params.get('workspace_id')
        api_key = request.query_params.get('api_key')

        if not workspace_id or not api_key:
            return Response(
                {"message": "workspace_id and api_key are required.", "success": False},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            limit = int(request.query_params.get('limit', 10))
            offset = int(request.query_params.get('offset', 0))
        except ValueError:
            return Response(
                {"message": "limit and offset must be integers.", "success": False},
                status=status.HTTP_400_BAD_REQUEST
            )

        db_name = f"{workspace_id}_cs_ticketing_system_db0"
        coll_name = f"{workspace_id}_master_link"

        try:
            response = data_cube.fetch_data(api_key=api_key, db_name=db_name, coll_name=coll_name, filters={},
                                            limit=limit,
                                            offset=offset
                                            )
            return Response({
                "success": True, "message": "All master links", "response": response.get('data', []),
            })

        except Exception as e:
            return Response(
                {"message": str(e), "success": False}, status=status.HTTP_400_BAD_REQUEST
            )
