import json

from apps.paasapp.serilizers import PaasSerializer
from common.logger import logger
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .modules.ldap import LDAPHandler
from .modules.utm import UTMHandler
from .tasks import create_tf_files


class ApiPaasView(APIView):

    def post(self, request):
        """_summary_

        Args:
            request (json): data form serializer

        Returns:
            response: status
        """

        serializer = PaasSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                if serializer.is_valid():
                    serializer_validated_data = json.loads(serializer.validated_data['content'])
                    resources = serializer_validated_data['request']['udf_fields']
                    ticket_number = serializer_validated_data['request']['id']
                    create_tf_files(resources, ticket_number)
                    return Response(
                        {"response": [
                            {"status": "ok"}]
                        },
                        status=status.HTTP_200_OK
                    )
            except Exception as error:
                logger.error(f' Error at ApiPaasView : {error} ')

            return Response(
                {"response": [
                    {"status": "not ok"}]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LDAPGroups(APIView):

    def get(self, request):
        try:
            search_field = None
            params = request.GET.get('input_data')
            if params:
                params = eval(params)
                search_field = params.get('list_info').get('search_fields').get('name')

            ldap_handler = LDAPHandler()
            ldap_handler.connect()
            groups = ldap_handler.get_groups(search_field)

            ldap_handler.disconnect()
            return JsonResponse(
                {
                    "response_status": [
                        {
                            "status_code": 2000,
                            "status": "success"
                        }
                    ],
                    "list_info": {
                        "has_more_rows": True,
                        "start_index": 1,
                        "row_count": 20
                    },
                    "groups": groups
                })
        except Exception as error:
            logger.error(f'LDAPGroups get error : {error} ')

            return JsonResponse(
                {"response_status":
                    {
                        "status_code": 4000,
                        "messages": [{"status_code": 4000, "type": "failed", "message": error}],
                        "status": "failed",
                    }
                }
            )


class UTMService(APIView):

    def get(self, request):
        try:
            search_field = None
            params = request.GET.get('input_data')
            if params:
                params = eval(params)
                search_field = params.get('list_info').get('search_fields').get('name')

            utm_handler = UTMHandler()
            services = utm_handler.get_services(search_field)
            return JsonResponse(
                {
                    "response_status": [
                        {
                            "status_code": 2000,
                            "status": "success"
                        }
                    ],
                    "list_info": {
                        "has_more_rows": True,
                        "start_index": 1,
                        "row_count": 20
                    },
                    "services": services
                })

        except Exception as error:
            logger.error(f'UTMService get error : {error} ')

            return JsonResponse(
                {"response_status":
                    {
                        "status_code": 4000,
                        "messages": [{"status_code": 4000, "type": "failed", "message": error}],
                        "status": "failed",
                    }
                }
            )


class UTMInterface(APIView):
    def get(self, request):
        try:
            search_field = None
            params = request.GET.get('input_data')
            if params:
                params = eval(params)
                search_field = params.get('list_info').get('search_fields').get('name')
            interfaces = UTMHandler().get_interfaces(search_field)
            return JsonResponse(
                {
                    "response_status": [
                        {
                            "status_code": 2000,
                            "status": "success"
                        }
                    ],
                    "list_info": {
                        "has_more_rows": True,
                        "start_index": 1,
                        "row_count": 20
                    },
                    "interfaces": interfaces
                })
        except Exception as error:
            logger.error(f'UTMInterface get error : {error} ')

            return JsonResponse(
                {"response_status":
                    {
                        "status_code": 4000,
                        "messages": [{"status_code": 4000, "type": "failed", "message": error}],
                        "status": "failed",
                    }
                }
            )
