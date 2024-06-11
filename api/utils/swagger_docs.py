from drf_yasg import openapi

get_master_link_docs = {
    "masterlink_get_params": [
        openapi.Parameter('workspace_id', openapi.IN_QUERY,
                          description="Workspace ID of the user", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('api_key', openapi.IN_QUERY, description="Datacube API Key",
                          type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('limit', openapi.IN_QUERY, description="Limit",
                          type=openapi.TYPE_INTEGER, default=10),
        openapi.Parameter('offset', openapi.IN_QUERY,
                          description="Offset", type=openapi.TYPE_INTEGER, default=0),
    ],
    "masterlink_get_responses": {
        200: openapi.Response(
            description="Success",
            examples={
                "application/json": {
                    "success": True,
                    "message": "All master links",
                    "response": [
                        {"id": "link1", "name": "Master Link 1"},
                        {"id": "link2", "name": "Master Link 2"}
                    ]
                }
            }
        ),
        400: openapi.Response(
            description="Bad Request",
            examples={
                "application/json": {
                    "message": "Error message",
                    "success": False
                }
            }
        )
    }
}
