import pytest

from apps.core.models import CustomUser


class TestCoreModels:
    def setup_method(self, method):
        self.pw = "12345678"
        self.email = "test@test.com"

    def test_customuser_model_str_method(self, django_user_model):
        user = django_user_model.objects.create(
            email=self.email,
            password=self.pw,
        )
        assert str(user) == self.email

    def test_customuser_create_user_without_email_raises_an_valueerror(self, django_user_model):
        with pytest.raises(ValueError):
            django_user_model.objects.create_user(
                email=None,
                password=self.pw,
        )

    def test_customuser_creates_instance(self, django_user_model):
        user = django_user_model.objects.create_user(
            email=self.email,
            password=self.pw,
        )
        assert isinstance(user, CustomUser)

    def test_customuser_create_super_user_setting_isstaff_to_false_raises_valueerror(self, django_user_model):
        with pytest.raises(ValueError):
            django_user_model.objects.create_superuser(
                email=self.email,
                password=self.pw,
                is_staff=False
            )

    def test_customuser_create_super_user_setting_issuperuser_to_false_raises_valueerror(self, django_user_model):
        with pytest.raises(ValueError):
            django_user_model.objects.create_superuser(
                email=self.email,
                password=self.pw,
                is_superuser=False
            )

    def test_customuser_create_superuser(self, django_user_model):
        user = django_user_model.objects.create_superuser(
            email=self.email,
            password=self.pw,
        )
        assert user.is_superuser == True
        assert user.is_staff == True
