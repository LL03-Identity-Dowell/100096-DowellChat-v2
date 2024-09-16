import random
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
from .serializers import MasterLinkSerializer
from .models import MasterLink
from websocket.models import Workspace
from .kafka.kafka_producer import ProducerAllEvents
from django.shortcuts import get_object_or_404
from django.db.models import Q

from api.utils.datacube_utils import (
    check_collection,
)

data_cube = DataCubeConnection()
import jwt


@method_decorator(csrf_exempt, name="dispatch")
class serverStatus(APIView):
    @swagger_auto_schema(
        operation_description="Server Health Check",
    )
    def get(self, request):
        return Response({"info": "Server is working fine!!"}, status=status.HTTP_200_OK)


"""PUBLIC RELEASE"""
public_namespace = "/public"


@api_view(["GET"])
@csrf_exempt
def public(request):
    return HttpResponse("Successfully Connected to Public Dowell Chat Backend")


def redirect_to_product_link(request):
    try:
        link_id = request.GET["link_id"]
        find_link = MasterLink.objects.filter(
            link_id=link_id,
            is_active=True,
            available_links__gt=0
        ).first()
        if find_link:
            return redirect(find_link.link)

        return render(request, "api/error.html")
    except KeyError as e:
        context = {"error": e}

        return render(request, "api/error.html", context)


class MasterlinkAPI(APIView):  
    @swagger_auto_schema(
        operation_id="get_masterlink",
        operation_description="API endpoint for returning master links",
        manual_parameters=get_master_link_docs["masterlink_get_params"],
        responses=get_master_link_docs["masterlink_get_responses"],
    )
    def get(self, request):
        workspace_id = request.query_params.get("workspace_id")

        if not workspace_id:
            return Response(
                {"message": "workspace_id is required.", "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        try:
            workspace = get_object_or_404(Workspace, org_id=workspace_id)
            masterlink = MasterLink.objects.filter(workspace=workspace)
            serializer = MasterLinkSerializer(masterlink, many=True)
            return Response(
                {
                    "success": True,
                    "message": "All master links",
                    "response": serializer.data
                }
            )

        except Exception as e:
            return Response(
                {"message": str(e), "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request):
        producerAllEvents = ProducerAllEvents()
        try:
            secret_key = "master_link"
            serializer = MasterLinkSerializer(data=request.data)

            if serializer.is_valid():
                workspace_id = serializer.validated_data["workspace_id"]
                api_key = serializer.validated_data["api_key"]
                url = "https://www.dowellchat.uxlivinglab.online/"
                link_id = "".join([str(random.randint(0, 9)) for _ in range(20)])
                master_link = f"https://www.dowellchat.uxlivinglab.online/api/share/?link_id={link_id}"

                payload = {
                    "link_id": link_id,
                    "number_of_links": serializer.validated_data["number_of_links"],
                    "available_links": serializer.validated_data["number_of_links"],
                    "product_distribution": serializer.validated_data[
                        "product_distribution"
                    ],
                    "usernames": serializer.validated_data["usernames"],
                    "is_active": True,
                    "master_link": master_link,
                    "workspace_id": workspace_id,
                    "api_key": api_key,
                }
                token = jwt.encode(payload, secret_key, algorithm="HS256")
                link = f"{url}?token={token}"

                payload["link"] = link
                
                workspace, _ = Workspace.objects.get_or_create(
                    org_id=workspace_id,
                    api_key=api_key
                )
                # Create MasterLink object
                MasterLink.objects.create(
                    link_id=link_id,
                    number_of_links=serializer.validated_data["number_of_links"],
                    available_links=serializer.validated_data["number_of_links"],
                    product_distribution=serializer.validated_data["product_distribution"],
                    usernames=serializer.validated_data["usernames"],
                    is_active=True,
                    master_link=master_link,
                    workspace=workspace, 
                    link=link,
                )

                producerAllEvents.publish(payload, event_type="create_masterlink")
                return Response(
                    {
                        "success": True,
                        "message": "Masterlink generated successfully",
                        "data": master_link,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"success": False, "message": serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"message": str(e), "success": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
