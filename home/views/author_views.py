from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ..models import Author


@csrf_exempt
def update_author_profile(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print('Incoming data:', data)
            user = request.user  # if using Django Auth
            author = Author.objects.get(author_user=user)

            author.author_name = data.get("author_name", author.author_name)
            author.author_subject_a = data.get("author_subject_a", author.author_subject_a)
            author.author_subject_b = data.get("author_subject_b", author.author_subject_b)
            author.author_subject_c = data.get("author_subject_b", author.author_subject_c)
            author.author_subject_d = data.get("author_subject_b", author.author_subject_d)
            author.save()

            return JsonResponse({"status": "success"})
        except Author.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Author not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request"})
