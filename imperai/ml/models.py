from django.db import models
import uuid
from django.conf import settings
from vertexai.preview.language_models import InputOutputTextPair

# Create your models here.

# Models to support sending requests to Google's Vertex AI API endpoints for text predictions.
# 
"""
- Parameters are contained within the *VertexChatConfig* model.
- Context is contained within the *VertexChatContext* model.
- Examples are contained within the *VertexChatExampleIOPair* model.
- VertexChatConfig + VertexChatContext + VertexChatExampleIOPair + Instruct + Rule + Detail = VertexChatRequest
- VertexChatRequest + a message = the request below

Example of a request to the Vertex AI API endpoint for text predictions:
    import vertexai
    from vertexai.preview.language_models import ChatModel, InputOutputTextPair

    vertexai.init(project="centered-kiln-390619", location="us-central1")
    chat_model = ChatModel.from_pretrained("chat-bison@001")
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40
    }
    chat = chat_model.start_chat(
        context="CONTEXT",
        examples=[
            InputOutputTextPair(
                input_text="UEXAMPLE",
                output_text="AIEXAMPLE"
            )
        ]
    )
    response = chat.send_message("a message", **parameters)
    print(f"Response from Model: {response.text}")
""" 

class ManagedStatus(models.IntegerChoices):
    Managed = 1, "imperai Managed"
    Unmanaged = 2, "Unmanaged"
    PartnerManaged = 3, "Partner Managed"
    Hybrid = 4, "Hybrid Managed"

class VertexChatConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_advanced = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_copy = models.BooleanField(default=False)
    copy_id = models.IntegerField()
    managed_status = models.PositiveSmallIntegerField(choices=ManagedStatus.choices)

    chat_model = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    project = models.CharField(max_length=256)
    
    temperature = models.FloatField()
    max_tokens = models.IntegerField()
    top_k = models.IntegerField()
    top_p = models.FloatField()
    # context = models.ForeignKey('VertexChatContext', on_delete=models.CASCADE, blank=False)
    # example = models.ManyToManyField('VertexChatExampleInputOutputPair', on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return str(self.id)

class VertexChatExampleIOPair(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    input_text = models.CharField(max_length=256)
    output_text = models.CharField(max_length=256)
    description = models.TextField()
    managed_status = models.PositiveSmallIntegerField(choices=ManagedStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)

    @classmethod
    def from_input_output_text_pair(cls, pair: InputOutputTextPair):
        return cls(input_text=pair.input_text, output_text=pair.output_text)
    
    def to_input_output_pair(self) -> InputOutputTextPair:
        return InputOutputTextPair(input_text=self.input_text, output_text=self.output_text)

class VertexChatContext(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    instruct = models.ForeignKey('VertexChatContextInstruct', on_delete=models.CASCADE, blank=False)
    rule = models.ForeignKey('VertexChatContextRule', on_delete=models.CASCADE, blank=False)
    detail = models.ForeignKey('VertexChatContextDetail', on_delete=models.CASCADE, blank=False)
    managed_status = models.PositiveSmallIntegerField(choices=ManagedStatus.choices)
    context = models.TextField()

    def __str__(self):
        return str(self.id)

class VertexChatContextInstruct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    instruct = models.TextField()
    managed_status = models.PositiveSmallIntegerField(choices=ManagedStatus.choices)

    def __str__(self):
        return str(self.id)


class VertexChatContextRule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    rule = models.TextField()
    managed_status = models.PositiveSmallIntegerField(choices=ManagedStatus.choices)

    def __str__(self):
        return str(self.id)

class VertexChatContextDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    detail = models.TextField()
    managed_status = models.PositiveSmallIntegerField(choices=ManagedStatus.choices)

    def __str__(self):
        return str(self.id)

class VertexChatRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat_config = models.ForeignKey('VertexChatConfig', on_delete=models.CASCADE, blank=False)
    context = models.ForeignKey('VertexChatContext', on_delete=models.CASCADE, blank=False)
    example = models.ManyToManyField('VertexChatExampleIOPair', blank=False)
    managed_status = models.PositiveSmallIntegerField(choices=ManagedStatus.choices)

    def __str__(self):
        return str(self.id)