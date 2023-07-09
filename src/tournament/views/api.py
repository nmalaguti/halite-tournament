from django.db import transaction
from rest_framework import authentication, exceptions, parsers, permissions, views
from rest_framework.response import Response

from tournament.models import Match


class MatchResultView(views.APIView):
    parser_classes = [parsers.MultiPartParser]
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    @transaction.atomic
    def post(self, request):
        if "result" not in request.data:
            raise exceptions.ParseError(
                detail="Request missing 'result' file.", code="result_missing"
            )

        file = request.data["result"]
        if not file.name.endswith(".tar.xz"):
            raise exceptions.ParseError(
                detail="File has a bad extension.", code="bad_extension"
            )

        try:
            Match.create_from_tar(file)
        except Exception as e:
            print(f"Failed to process upload: {e}")
            raise exceptions.ParseError(
                detail="Failed to process the file.", code="file_malformed"
            )

        return Response(status=204)
