import logging

import pytest
from django.urls import reverse
from django.test import Client
from django.test.utils import override_settings
from django.core.management import call_command

from apps.core.models import CustomUser
from .fixtures import *

logger = logging.getLogger(__name__)


class TestViews:
    @pytest.fixture(autouse=True)
    def setup_atuff(self, db):
        self.c = Client()
        self.COOKIE_AGE = (604800 * 3)  # 3 weeks in seconds
        self.credentials = {
            'email': 'test@test.com',
            'password': '12345678',
        }
        self.u = CustomUser.objects.create_user(**self.credentials)
        call_command('creategroups')

    def test_home_view_return_200(self):
        self.c.force_login(self.u)
        url = reverse('home')
        res = self.c.get(url)
        assert res.status_code == 200

    def test_overview_view_return_200(self):
        self.c.force_login(self.u)
        url = reverse('overview')
        res = self.c.get(url)
        assert res.status_code == 200

    def test_dashboard_view_return_200(self):
        self.c.force_login(self.u)
        url = reverse('dashboard')
        res = self.c.get(url)
        assert res.status_code == 200

    def test_redirect_user_function(self):
        url = reverse('home')
        res = self.c.get(url)
        assert res.status_code == 302

    def test_logout_view_status_code_302(self):
        self.c.force_login(self.u)
        url = reverse('logout')
        res = self.c.get(url)
        assert res.status_code == 302

    def test_overview_anonymoususer_redirect_to_login_page(self):
        url = reverse('overview')
        res = self.c.get(url)
        assert res.status_code == 302
        assert res.url == 'accounts/login/?next=/overview/'

    def test_dashboard_anonymoususer_redirect_to_login_page(self):
        url = reverse('dashboard')
        res = self.c.get(url)
        assert res.status_code == 302
        assert res.url == 'accounts/login/?next=/dashboard/'

    def test_login_remember(self):
        logger.debug("Testing login with 'remember me' checked")
        res = self.c.post(reverse('login'), {
            'email': 'test@test.com',
            'password': '12345678',
            'remember': 'true',
        })
        session = self.c.session
        logger.debug(f"Session expiry age: {session.get_expiry_age()}")
        assert session.get_expiry_age() == self.COOKIE_AGE

    @override_settings(SESSION_COOKIE_AGE=0)
    def test_login_without_remember(self, db):
        logger.debug("Testing login without 'remember me' checked")
        with override_settings(SESSION_EXPIRE_AT_BROWSER_CLOSE=True):
            res = self.c.post(reverse('login'), {
                'email': 'test@test.com',
                'password': '12345678',
            })
            session = self.c.session
            assert session.get_expire_at_browser_close() == True
            assert session.get_expiry_age() == 0

    def test_login_send_message_for_empty_field(self):
        res = self.c.post(reverse('login'), {
            'email': '',
            'password': '12345678',
            })
        messages = list(res.context['messages'])
        assert str(messages[0]) == 'Você precisa preencher Email e Senha válidos para entrar.'

    def test_login_template_render(self):
        res = self.c.get(reverse('login'))
        assert res.status_code == 200

    def test_user_login_success(self):
        res = self.c.post(
            reverse('login'), 
            self.credentials,
            follow=True
        )
        assert res.context['user'].is_authenticated == True

    def test_login_send_message_for_unregistered_user(self):
        res = self.c.post(
            reverse('login'), 
            {
                'email': 'testnotuser@email.com',
                'password': 'testnotuser',
            }
        )
        messages = list(res.context['messages'])
        assert str(messages[0]) == 'Email ou Senha icorreto!\
                     Não foi possível encontrar o usuário.\
                     Tente novamente.'

    def test_create_waiter_status_200(self):
        self.c.force_login(self.u)
        res = self.c.get(reverse('waiters-new'))
        assert res.status_code == 200

    def test_create_waiter_success(self):
        self.c.force_login(self.u)
        res = self.c.post(
            reverse('waiters-new'),
            {
                'email': 'example@example.com', 
                'full_name': 'example full name', 
                'password': '12345678'
            }
        )
        messages = list(res.context['messages'])
        assert res.status_code == 200
        assert str(messages[0]) == 'Garçon criado com sucesso!'

    def test_create_waiter_without_data_field_couse_error(self):
        self.c.force_login(self.u)
        res = self.c.post(
            reverse('waiters-new'),
            {
                'email': 'example@example.com', 
                'full_name': '', 
                'password': '12345678'
            }
        )
        messages = list(res.context['messages'])
        assert res.status_code == 200
        assert str(messages[0]) == 'Algo deu errado ao criar Garçon!'
