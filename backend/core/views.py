from pathlib import Path

from django.conf import settings
from django.http import FileResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from catalogue.loader import load_catalogue


@api_view(["GET"])
@permission_classes([AllowAny])
def health(request) -> Response:
    catalogue = load_catalogue(settings.CARD_CATALOGUE_DIR)
    return Response(
        {
            "status": "ok",
            "service": "spenddeck-api",
            "catalogue": {"cards": len(catalogue.cards)},
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def card_list(request) -> Response:
    catalogue = load_catalogue(settings.CARD_CATALOGUE_DIR)
    return Response(
        {
            "cards": [
                {
                    "id": loaded.card.id,
                    "issuer": loaded.card.issuer,
                    "name": loaded.card.name,
                    "networks": loaded.card.networks,
                    "rule_versions": [rule.version for rule in loaded.rules],
                }
                for loaded in catalogue.cards
            ]
        }
    )


def frontend_index(request):
    index_path = Path(settings.FRONTEND_DIST_DIR) / "index.html"
    if index_path.exists():
        return FileResponse(index_path.open("rb"), content_type="text/html")

    return JsonResponse(
        {
            "detail": "SpendDeck API is running. Start the frontend development server on port 5173."
        }
    )
