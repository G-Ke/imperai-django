from django.shortcuts import render
import vertexai
from django.views.generic import TemplateView, UpdateView
from vertexai.preview.language_models import ChatModel, InputOutputTextPair
from django.contrib.auth.mixins import LoginRequiredMixin


def send_vertex_chat(self):
    vertexai.init(project=self.project, location=self.location)
    chat_model = ChatModel.from_pretrained(self.chat_model)
    parameters = {
        "temperature": self.temperature,
        "max_output_tokens": self.max_tokens,
        "top_p": self.top_p,
        "top_k": self.top_k
    }
    chat = chat_model.start_chat(
        context=self.context,
        examples=[
            InputOutputTextPair(
                input_text="""User EX""",
                output_text="""AI EX"""
            )
        ]
    )

class VertexChatWelcomeView(LoginRequiredMixin, TemplateView):
    template_name = 'vertex_chat_welcome.html'
    login_url = 'accounts/login'