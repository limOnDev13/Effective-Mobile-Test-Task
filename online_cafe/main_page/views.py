from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def main_page_view(request: HttpRequest) -> HttpResponse:
    """View main page."""
    return render(request, "main_page/main-page.html")
