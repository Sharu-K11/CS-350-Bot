from django.shortcuts import render
from django.http import HttpResponse
from chatApp.chatRag.services.rag_chain import build_pipeline
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


rag_chain = build_pipeline()

def home(request):
    return render(request,'index.html' ,{})




def chat(request):
    return render (request,'chat.html',{})




# Build ONCE (on app startup)
rag_chain = build_pipeline()


def ask(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    try:
        data = json.loads(request.body or "{}")
        question = (data.get("question") or "").strip()

        if not question:
            return JsonResponse({"error": "Question is required"}, status=400)

        question = f"{question} At the same time pick related prective problem from the book."
        answer = rag_chain.invoke(question)

        return JsonResponse({
            "question": question,
            "answer": str(answer),   
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
