from django import forms
from django.forms import formset_factory, modelformset_factory
from .models import VertexChatExampleIOPair

class VertexChatExampleIOPairForm(forms.ModelForm):
    class Meta:
        model = VertexChatExampleIOPair
        fields = ['input_text', 'output_text']

ExampleFormSet = modelformset_factory(VertexChatExampleIOPair, form=VertexChatExampleIOPairForm, extra=1)
#ExampleFormSet = formset_factory(VertexChatExampleIOPairForm, extra=1)