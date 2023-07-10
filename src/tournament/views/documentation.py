from django.http import Http404
from django.shortcuts import render
from django.template import TemplateDoesNotExist


def documentation(request, page_name: str):
    try:
        return render(
            request,
            f"tournament/documentation/{page_name}.html",
            context={"page_name": page_name},
        )
    except TemplateDoesNotExist:
        try:
            return render(
                request,
                f"tournament/documentation/{page_name}.md",
                context={"page_name": page_name},
            )
        except TemplateDoesNotExist:
            raise Http404("Page does not exist.")
