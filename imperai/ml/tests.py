import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import CustomUser
from .models import VertexChatConfig, VertexChatExampleIOPair, VertexChatContext, VertexChatContextInstruct, VertexChatContextRule, VertexChatContextDetail, VertexChatRequest, InputOutputTextPair
import os

test_user_email = os.environ.get('TEST_EMAIL')
test_user_password = os.environ.get('TEST_PASSWORD')

class VertexChatConfigTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email=test_user_email,
            password=test_user_password,
        )
        self.config = VertexChatConfig.objects.create(
            user=self.user,
            is_advanced=True,
            is_active=True,
            is_copy=False,
            copy_id=0,
            managed_status=1,
            chat_model='chat-bison',
            location='us-east1',
            project='imperai',
            temperature=0.5,
            max_tokens=1000,
            top_k=5,
            top_p=0.5,
        )

    def test_vertex_chat_config_creation(self):
        config = VertexChatConfig.objects.get(id=self.config.id)
        self.assertEqual(config.user, self.user)
        self.assertTrue(config.is_advanced)
        self.assertTrue(config.is_active)
        self.assertFalse(config.is_copy)
        self.assertEqual(config.copy_id, 0)
        self.assertEqual(config.managed_status, 1)
        self.assertEqual(config.chat_model, 'chat-bison')
        self.assertEqual(config.location, 'us-east1')
        self.assertEqual(config.project, 'imperai')
        self.assertEqual(config.temperature, 0.5)
        self.assertEqual(config.max_tokens, 1000)
        self.assertEqual(config.top_k, 5)
        self.assertEqual(config.top_p, 0.5)

    def test_vertex_chat_config_str(self):
        config = VertexChatConfig.objects.get(id=self.config.id)
        self.assertEqual(str(config), str(self.config.id))
    
    def test_vertex_chat_config_id(self):
        config = VertexChatConfig.objects.get(id=self.config.id)
        self.assertIsInstance(config.id, uuid.UUID)

    def test_vertex_chat_config_user(self):
        config = VertexChatConfig.objects.get(id=self.config.id)
        self.assertIsInstance(config.user, CustomUser)

    def test_vertext_chat_config_managed_status(self):
        config = VertexChatConfig.objects.get(id=self.config.id)
        self.assertEqual(config.managed_status, 1)

class VertexChatExampleInputOutputPairTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email=test_user_email,
            password=test_user_password,
        )
        self.io_pair = VertexChatExampleIOPair.objects.create(
            user=self.user,
            name='test IO pair',
            input_text='What is the purpose of this chatbot?',
            output_text='To answer questions about this e-commerce store',
            description='Q and A Example 1',
            managed_status=1,
        )

    def test_vertex_chat_example_io_pair_creation(self):
        io_pair = VertexChatExampleIOPair.objects.get(id=self.io_pair.id)
        self.assertEqual(io_pair.user, self.user)
        self.assertEqual(io_pair.name, 'test IO pair')
        self.assertEqual(io_pair.input_text, 'What is the purpose of this chatbot?')
        self.assertEqual(io_pair.output_text, 'To answer questions about this e-commerce store')
        self.assertEqual(io_pair.description, 'Q and A Example 1')
        self.assertEqual(io_pair.managed_status, 1)

    def test_vertex_chat_example_io_pair_str(self):
        io_pair = VertexChatExampleIOPair.objects.get(id=self.io_pair.id)
        self.assertEqual(str(io_pair), str(self.io_pair.id))

    def test_vertex_chat_example_io_pair_id(self):
        io_pair = VertexChatExampleIOPair.objects.get(id=self.io_pair.id)
        self.assertIsInstance(io_pair.id, uuid.UUID)

    def test_vertex_chat_example_io_pair_user(self):
        io_pair = VertexChatExampleIOPair.objects.get(id=self.io_pair.id)
        self.assertIsInstance(io_pair.user, CustomUser)

    def test_vertex_chat_example_io_pair_to_io_pair(self):
        io_pair = VertexChatExampleIOPair.objects.get(id=self.io_pair.id)
        input_output_pair = io_pair.to_input_output_pair()
        self.assertEqual(input_output_pair.input_text, 'What is the purpose of this chatbot?')
        self.assertEqual(input_output_pair.output_text, 'To answer questions about this e-commerce store')

    def test_from_input_output_text_pair(self):
        io_pair = InputOutputTextPair(input_text='What is the purpose of this chatbot?', output_text='To answer questions about this e-commerce store')
        example = VertexChatExampleIOPair.from_input_output_text_pair(io_pair)
        self.assertEqual(example.input_text, 'What is the purpose of this chatbot?')
        self.assertEqual(example.output_text, 'To answer questions about this e-commerce store')

    def test_to_input_output_pair(self):
        example = VertexChatExampleIOPair(input_text='What is the purpose of this chatbot?', output_text='To answer questions about this e-commerce store')
        io_pair = example.to_input_output_pair()
        self.assertEqual(io_pair.input_text, 'What is the purpose of this chatbot?')
        self.assertEqual(io_pair.output_text, 'To answer questions about this e-commerce store')

class VertexChatContextTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email=test_user_email,
            password=test_user_password,
        )
        self.instruct = VertexChatContextInstruct.objects.create(
            user=self.user,
            name='test instruction',
            instruct = 'Your job is to serve as an e-commerce shopping assistant for this website.',
            managed_status=1,
        )
        self.rule = VertexChatContextRule.objects.create(
            user=self.user,
            name='test rule',
            rule='If the user asks about the price of a product, then answer with the price of the product.',
            managed_status=1,
        )
        self.detail = VertexChatContextDetail.objects.create(
            user=self.user,
            name='test detail',
            detail='The name of the company this chat bot works for is Shoes and More, headquartered in Boston.',
            managed_status=1,
        )
        self.context = VertexChatContext.objects.create(
            user=self.user,
            name='test context',
            instruct=self.instruct,
            rule=self.rule,
            detail=self.detail,
            managed_status=1,
            context='Can you help me find a pair of shoes?',
        )

    def test_vertex_chat_context_creation(self):
        context = VertexChatContext.objects.get(id=self.context.id)
        self.assertEqual(context.user, self.user)
        self.assertEqual(context.name, 'test context')
        self.assertEqual(context.instruct, self.instruct)
        self.assertEqual(context.rule, self.rule)
        self.assertEqual(context.detail, self.detail)
        self.assertEqual(context.managed_status, 1)
        self.assertEqual(context.context, 'Can you help me find a pair of shoes?')

    def test_vertex_chat_context_str(self):
        context = VertexChatContext.objects.get(id=self.context.id)
        self.assertEqual(str(context), str(self.context.id))

    def test_vertex_chat_context_id(self):
        context = VertexChatContext.objects.get(id=self.context.id)
        self.assertIsInstance(context.id, uuid.UUID)

    def test_vertex_chat_context_user(self):
        context = VertexChatContext.objects.get(id=self.context.id)
        self.assertIsInstance(context.user, CustomUser)

    def test_vertex_chat_context_instruct(self):
        context = VertexChatContext.objects.get(id=self.context.id)
        self.assertIsInstance(context.instruct, VertexChatContextInstruct)

    def test_vertext_chat_context_rule(self):
        context = VertexChatContext.objects.get(id=self.context.id)
        self.assertIsInstance(context.rule, VertexChatContextRule)

    def test_vertext_chat_context_detail(self):
        context = VertexChatContext.objects.get(id=self.context.id)
        self.assertIsInstance(context.detail, VertexChatContextDetail)

    def test_vertext_chat_context_managed_status(self):
        context = VertexChatContext.objects.get(id=self.context.id)
        self.assertEqual(context.managed_status, 1)

    def test_vertex_chat_context(self):
        context = VertexChatContext.objects.get(id=self.context.id)
        self.assertEqual(context.context, 'Can you help me find a pair of shoes?')

class VertexChatContextInstructTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email=test_user_email,
            password=test_user_password,
        )
        self.instruct = VertexChatContextInstruct.objects.create(
            user=self.user,
            name='test instruction',
            instruct = 'Your job is to serve as an e-commerce shopping assistant for this website.',
            managed_status=1,
        )

    def test_vertex_chat_context_instruct_creation(self):
        instruct = VertexChatContextInstruct.objects.get(id=self.instruct.id)
        self.assertEqual(instruct.user, self.user)
        self.assertEqual(instruct.name, 'test instruction')
        self.assertEqual(instruct.instruct, 'Your job is to serve as an e-commerce shopping assistant for this website.')
        self.assertEqual(instruct.managed_status, 1)

    def test_vertex_chat_context_instruct_str(self):
        instruct = VertexChatContextInstruct.objects.get(id=self.instruct.id)
        self.assertEqual(str(instruct), str(self.instruct.id))

    def test_vertex_chat_context_instruct_id(self):
        instruct = VertexChatContextInstruct.objects.get(id=self.instruct.id)
        self.assertIsInstance(instruct.id, uuid.UUID)

    def test_vertex_chat_context_instruct_user(self):
        instruct = VertexChatContextInstruct.objects.get(id=self.instruct.id)
        self.assertIsInstance(instruct.user, CustomUser)

class VertexChatContextRuleTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email=test_user_email,
            password=test_user_password,
        )
        self.rule = VertexChatContextRule.objects.create(
            user=self.user,
            name='test rule',
            rule='If the user asks about the price of a product, then answer with the price of the product.',
            managed_status=1,
        )

    def test_vertex_chat_context_rule_creation(self):
        rule = VertexChatContextRule.objects.get(id=self.rule.id)
        self.assertEqual(rule.user, self.user)
        self.assertEqual(rule.name, 'test rule')
        self.assertEqual(rule.rule, 'If the user asks about the price of a product, then answer with the price of the product.')
        self.assertEqual(rule.managed_status, 1)

    def test_vertex_chat_context_rule_str(self):
        rule = VertexChatContextRule.objects.get(id=self.rule.id)
        self.assertEqual(str(rule), str(self.rule.id))

    def test_vertex_chat_context_rule_id(self):
        rule = VertexChatContextRule.objects.get(id=self.rule.id)
        self.assertIsInstance(rule.id, uuid.UUID)

    def test_vertex_chat_context_rule_user(self):
        rule = VertexChatContextRule.objects.get(id=self.rule.id)
        self.assertIsInstance(rule.user, CustomUser)

class VertexChatContextDetailTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email=test_user_email,
            password=test_user_password,
        )
        self.detail = VertexChatContextDetail.objects.create(
            user=self.user,
            name='test detail',
            detail='This is the detail of the context.',
            managed_status=1,
        )

    def test_vertex_chat_context_detail_creation(self):
        detail = VertexChatContextDetail.objects.get(id=self.detail.id)
        self.assertEqual(detail.user, self.user)
        self.assertEqual(detail.name, 'test detail')
        self.assertEqual(detail.detail, 'This is the detail of the context.')
        self.assertEqual(detail.managed_status, 1)

    def test_vertex_chat_context_detail_str(self):
        detail = VertexChatContextDetail.objects.get(id=self.detail.id)
        self.assertEqual(str(detail), str(self.detail.id))

    def test_vertex_chat_context_detail_id(self):
        detail = VertexChatContextDetail.objects.get(id=self.detail.id)
        self.assertIsInstance(detail.id, uuid.UUID)

    def test_vertex_chat_context_detail_user(self):
        detail = VertexChatContextDetail.objects.get(id=self.detail.id)
        self.assertIsInstance(detail.user, CustomUser)

class VertexChatRequestTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email=test_user_email,
            password=test_user_password,
        )
        self.chat_config = VertexChatConfig.objects.create(
            user=self.user,
            is_advanced=False,
            is_active=True,
            is_copy=False,
            copy_id=0,
            managed_status=1,
            chat_model='test model',
            location='us-east1',
            project='imperai',
            temperature=0.5,
            max_tokens=1000,
            top_k=5,
            top_p=0.5
        )
        self.instruct = VertexChatContextInstruct.objects.create(
            user=self.user,
            name='test instruction',
            instruct = 'Your job is to serve as an e-commerce shopping assistant for this website.',
            managed_status=1,
        )
        self.rule = VertexChatContextRule.objects.create(
            user=self.user,
            name='test rule',
            rule='If the user asks about the price of a product, then answer with the price of the product.',
            managed_status=1,
        )
        self.detail = VertexChatContextDetail.objects.create(
            user=self.user,
            name='test detail',
            detail='The name of the company this chat bot works for is Shoes and More, headquartered in Boston.',
            managed_status=1,
        )
        self.context = VertexChatContext.objects.create(
            user=self.user,
            name='test context',
            instruct=self.instruct,
            rule=self.rule,
            detail=self.detail,
            managed_status=1,
            context='Can you help me find a pair of shoes?',
        )
        self.example = VertexChatExampleIOPair.objects.create(
            user=self.user,
            name='test IO pair',
            input_text='What is the purpose of this chatbot?',
            output_text='To answer questions about this e-commerce store',
            description='Q and A Example 1',
            managed_status=1,
        )
        self.request = VertexChatRequest.objects.create(
            user=self.user,
            chat_config=self.chat_config,
            context=self.context,
            managed_status=1,
        )
        self.request.example.set([self.example])

    def test_vertex_chat_request_str(self):
        self.assertEqual(str(self.request), str(self.request.id))

    def test_vertex_chat_request_id(self):
        request = VertexChatRequest.objects.get(id=self.request.id)
        self.assertIsInstance(request.id, uuid.UUID)

    def test_vertex_chat_request_user(self):
        self.assertEqual(self.request.user, self.user)

    def test_vertex_chat_request_config(self):
        request = VertexChatRequest.objects.get(id=self.request.id)
        self.assertIsInstance(request.chat_config, VertexChatConfig)

    def test_vertex_chat_request_context(self):
        request = VertexChatRequest.objects.get(id=self.request.id)
        self.assertIsInstance(request.context, VertexChatContext)
    
    def test_vertex_chat_request_example(self):
        request = VertexChatRequest.objects.get(id=self.request.id)
        self.assertEqual(request.example.count(), 1)
        self.assertIsInstance(request.example.first(), type(self.example))

    def test_vertex_chat_request_managed_status(self):
        request = VertexChatRequest.objects.get(id=self.request.id)
        self.assertEqual(request.managed_status, 1)

    def test_vertex_chat_request_creation(self):
        request = VertexChatRequest.objects.get(id=self.request.id)
        self.assertEqual(request.user, self.user)
        self.assertEqual(request.chat_config, self.chat_config)
        self.assertEqual(request.context, self.context)
        self.assertEqual(request.example.count(), 1)
        self.assertEqual(request.managed_status, 1)
        self.assertEqual(request.example.first(), self.example)
