from typing import List
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import vertexai
import uuid
from django.views.generic import TemplateView, UpdateView, CreateView
from vertexai.preview.language_models import ChatModel, InputOutputTextPair
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import formset_factory
from django.forms import modelformset_factory
from .forms import VertexChatExampleIOPairForm
from django.contrib import messages
from .models import (
    VertexChatContextDetail, 
    VertexChatContextInstruct, 
    VertexChatContextRule,
    VertexChatExampleIOPair
)



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

# View related to the basic/custom Vertex Chat Configurator

class VertexChatConfigStartView(LoginRequiredMixin, TemplateView):
    template_name = 'vertex_chat_config_start.html'
    login_url = 'accounts/login'

class VertexChatConfigStartDetailCreateView(LoginRequiredMixin, CreateView):
    template_name = 'vertex_chat_config_start_detail_create.html'
    login_url = 'accounts/login'
    model = VertexChatContextDetail
    success_url = '/ml/vertex/configurator/instruct/create'
    fields = ['name', 'detail']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.managed_status = 2
        return super().form_valid(form)

class VertexChatConfigStartInstructCreateView(LoginRequiredMixin, CreateView):
    template_name = 'vertex_chat_config_start_instruct_create.html'
    login_url = 'accounts/login'
    model = VertexChatContextInstruct
    success_url = '/ml/vertex/configurator/rule/create'
    fields = ['name', 'instruct']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.managed_status = 2
        return super().form_valid(form)

class VertexChatConfigStartRuleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'vertex_chat_config_start_rule_create.html'
    login_url = 'accounts/login'
    model = VertexChatContextRule
    success_url = '/ml/vertex/configurator/example/create'
    fields = ['name', 'rule']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.managed_status = 2
        return super().form_valid(form)

class VertexChatConfigStartExampleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'vertex_chat_config_start_example_create.html'
    login_url = 'accounts/login'
    model = VertexChatExampleIOPair
    success_url = '/ml/vertex/configurator/review-context'
    form_class = VertexChatExampleIOPairForm

    """def get(self, request, **kwargs)
        is_htmx = request.headers.get('HX-Request', False) == True
        if is_htmx:
            return render(request, 'partials/example-list.html')
        else:
            return render(request, self.template_name)"""
    
    def get_template_names(self):
        is_htmx = self.request.headers.get('HX-Request')
        if is_htmx == 'true':
            return 'partials/example-list.html'
        else:
            return self.template_name

    def get_context_data(self, **kwargs):
        context = super(VertexChatConfigStartExampleCreateView, self).get_context_data(**kwargs)
        context['example_count'] = VertexChatExampleIOPair.objects.filter(user=self.request.user).count()
        context['examples'] = VertexChatExampleIOPair.objects.filter(user=self.request.user).order_by('-created_at')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.managed_status = 2
        self.object.name = 'Quickstart Example'
        self.object.description = 'Quickstart Example'
        self.object.save()
        example_count = VertexChatExampleIOPair.objects.filter(user=self.request.user).count()
        if example_count < 10:
            # messages.info(self.request, message='Example added successfully, let us add some more')
            return redirect('vertex_chat_config_start_example_create')
        else:
            # messages.success(self.request, message='All examples added successfully')
            return redirect(self.success_url)
        
def check_examples(request):
    example_count = VertexChatExampleIOPair.objects.filter(user=request.user).count()
    if example_count < 4:
        # messages.add_message(request, messages.INFO, 'Example added successfully, let us add some more')
        return redirect('vertex_chat_config_start_example_create')
    else:
        # messages.add_message(request, messages.SUCCESS, 'All examples added successfully')
        return redirect('vertex_chat_config_review_context')

class VertexChatConfigStartReviewContextView(LoginRequiredMixin, TemplateView):
    template_name = 'vertex_chat_config_start_review_context.html'
    login_url = 'accounts/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['example_count'] = VertexChatExampleIOPair.objects.filter(user=self.request.user).count()
        context['details_count'] = VertexChatContextDetail.objects.filter(user=self.request.user).count()
        context['instructs_count'] = VertexChatContextInstruct.objects.filter(user=self.request.user).count()
        context['rules_count'] = VertexChatContextRule.objects.filter(user=self.request.user).count()
        return context

class VertexChatConfigStartContextCreateView(LoginRequiredMixin, CreateView):
    template_name = 'vertex_chat_config_start_context_create.html'
    login_url = 'accounts/login'
    model = VertexChatContextDetail
    success_url = '/ml/vertex/configurator/complete'
    fields = ['name', 'detail']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.managed_status = 2
        return super().form_valid(form)

class VertexChatConfigStartConnectView(LoginRequiredMixin, TemplateView):
    template_name = 'vertex_chat_config_start_connect.html'
    login_url = 'accounts/login'