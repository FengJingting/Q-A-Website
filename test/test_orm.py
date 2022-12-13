from models import UserModel
import pytest

@pytest.fixture(scope='module')
def new_user():
    user =  UserModel(email='patkennedy79@gmail.com', username='test', password='111111')
    return user

def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    assert new_user.email == 'patkennedy79@gmail.com'
    assert new_user.password == '111111'
    assert new_user.username == 'test'