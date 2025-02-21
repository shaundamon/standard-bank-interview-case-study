from drf_yasg import openapi

# Image Search schemas
image_search_request = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'query': openapi.Schema(type=openapi.TYPE_STRING, description='Text query to search for images'),
        'num_results': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of results to return')
    },
    required=['query']
)

image_search_response = openapi.Response(
    'Successful search results',
    schema=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'results': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'path': openapi.Schema(type=openapi.TYPE_STRING),
                        'similarity': openapi.Schema(type=openapi.TYPE_NUMBER)
                    }
                ),
                description='List of image matches with similarity scores'
            )
        }
    )
)