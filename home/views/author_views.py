from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from ..models import Author

#@csrf_exempt: You're using it because you're sending JSON via fetch
@csrf_exempt
def update_author_profile(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print('Incoming data:', data)
            user = request.user  # Assumes user is authenticated
            #author = Author.objects.get(author_user=user)
            author_id = data.get("author_id")
            author = Author.objects.get(author_id=author_id)
            # Correctly assign each field
            author.author_name = data.get("author_name", author.author_name)
            author.author_subject_a = data.get("author_subject_a", author.author_subject_a)
            author.author_subject_b = data.get("author_subject_b", author.author_subject_b)
            author.author_subject_c = data.get("author_subject_c", author.author_subject_c)  # Fixed
            author.author_subject_d = data.get("author_subject_d", author.author_subject_d)  # Fixed
            author.save()

            return JsonResponse({"status": "success"})
        except Author.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Author not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request"})


def author_subjects_api(request):
    author_id = request.GET.get('author_id')
    author = Author.objects.filter(author_id=author_id).first()
    print(author.author_subject_a)
    subjects = []
    if author:
        for field in ['author_subject_a', 'author_subject_b', 'author_subject_c', 'author_subject_d']:
            value = getattr(author, field)
            if value:  # Only include non-empty
                subjects.append(value)
    print(subjects,author_id)
    return JsonResponse({'subjects': subjects})