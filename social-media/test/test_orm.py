from models import UserModel,QuestionModel,AnswerModel,FavoriteModel,UserFavoriteQuestionModel
import pytest

# this test aims to test if the orm model can work correctly
@pytest.fixture(scope='module')
def new_user():
    user = UserModel(email='patkennedy79@gmail.com', username='test', password='111111')
    return user

def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, password,username fields are defined correctly
    """
    assert new_user.email == 'patkennedy79@gmail.com'
    assert new_user.password == '111111'
    assert new_user.username == 'test'

def test_user_id(new_user):
    """
    GIVEN an existing User
    WHEN the ID of the user is defined to a value
    THEN check the user ID returns a string (and not an integer) as needed by Flask-WTF
    """
    new_user.id = 17
    assert isinstance(new_user.id, int)
    assert not isinstance(new_user.id, str)
    assert new_user.id == 17