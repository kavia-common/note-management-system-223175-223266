from typing import Any, Dict

from django.db.models import Q
from rest_framework import generics, pagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from .models import Note
from .serializers import NoteSerializer


class DefaultPageNumberPagination(pagination.PageNumberPagination):
    """Default pagination: page/page_size with sane defaults."""
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# PUBLIC_INTERFACE
@api_view(["GET"])
def health(request: Request):
    """
    Health check endpoint.
    Returns 200 with a simple message indicating the server is up.
    """
    return Response({"message": "Server is up!"})


class NoteListCreateView(generics.ListCreateAPIView):
    """
    List and create notes.

    Filtering:
    - ?q= substring search in title or content (case-insensitive)
    - ?archived=true|false to filter by archived flag
    - ?tag=<tag> to filter if the comma-separated tags include the tag (case-insensitive)
    Pagination:
    - page, page_size via standard DRF PageNumberPagination
    """
    serializer_class = NoteSerializer
    pagination_class = DefaultPageNumberPagination

    def get_queryset(self):
        qs = Note.objects.all()
        params: Dict[str, Any] = self.request.query_params

        q = params.get("q")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))

        archived = params.get("archived")
        if archived is not None:
            if archived.lower() in ("true", "1", "yes"):
                qs = qs.filter(archived=True)
            elif archived.lower() in ("false", "0", "no"):
                qs = qs.filter(archived=False)

        tag = params.get("tag")
        if tag:
            # Match within comma-separated tags; simple icontains is acceptable here.
            qs = qs.filter(tags__icontains=tag)

        return qs


class NoteRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update (PUT/PATCH), or delete a note by ID.
    """
    serializer_class = NoteSerializer
    queryset = Note.objects.all()
