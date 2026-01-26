from django.shortcuts import render
from django.http import HttpResponse
from chatApp.chatRag.services.rag_chain import build_pipeline
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


rag_chain = build_pipeline()

# Create your views here.
def home(request):
    return render(request,'index.html' ,{})




def chat(request):
    return render (request,'chat.html',{})




# Build ONCE (on app startup)
rag_chain = build_pipeline()


@csrf_exempt
def ask(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    try:
        data = json.loads(request.body or "{}")
        question = (data.get("question") or "").strip()

        if not question:
            return JsonResponse({"error": "Question is required"}, status=400)

        answer = rag_chain.invoke(question)

        return JsonResponse({
            "question": question,
            "answer": str(answer),   
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
