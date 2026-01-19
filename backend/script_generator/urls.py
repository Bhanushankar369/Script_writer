from django.urls import path

from .views import ScriptView

urlpatterns = [
    path('llm/', ScriptView.as_view())
]
