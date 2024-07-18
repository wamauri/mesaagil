from io import StringIO

import pytest
from django.core.management import call_command
from django.contrib.auth.models import Group, Permission


class TestCreateGroupCommand:

    @pytest.fixture(autouse=True)
    def setup_atuff(self, db):
        call_command('creategroups')

    def test_create_groups(self):
        out = StringIO()
        call_command('creategroups', stdout=out)
        assert Group.objects.filter(name='Restaurant').exists()
        assert Group.objects.filter(name='Waiter').exists()
        assert Group.objects.filter(name='Client').exists()

    def test_permission_does_not_exist(self, caplog):
        Permission.objects.filter(codename='add_products').delete()

        out = StringIO()
        call_command('creategroups', stdout=out)
        assert 'Permission "add_products" not found' in out.getvalue()

    def test_assign_permissions(self):
        out = StringIO()
        call_command('creategroups', stdout=out)

        # Verify permissions for Restaurant group
        restaurant_group = Group.objects.get(name='Restaurant')
        restaurant_perm = restaurant_group.permissions.values_list('codename', flat=True)
        expected_permissions = [
            'add_products', 
            'change_products', 
            'delete_products', 
            'view_products'
        ]
        for perm in expected_permissions:
            assert perm in restaurant_perm

        # Verify permissions for Waiter group
        waiter_group = Group.objects.get(name='Waiter')
        waiter_perm = waiter_group.permissions.values_list('codename', flat=True)
        expected_permissions = ['add_products', 'change_products']
        for perm in expected_permissions:
            assert perm in waiter_perm

        # Verify permissions for Client group
        client_group = Group.objects.get(name='Client')
        client_perm = client_group.permissions.values_list('codename', flat=True)
        expected_permissions = ['view_products']
        for perm in expected_permissions:
            assert perm in client_perm

    def test_group_already_exists(self):
        out = StringIO()
        call_command('creategroups', stdout=out)
        assert 'Group "Restaurant" already exists' in out.getvalue()
