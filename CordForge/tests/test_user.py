import pytest
from unittest.mock import Mock
from CordForge.user import User
from discord import Member


@pytest.fixture
def mock_member():
    m = Mock(spec=Member)
    m.id = 123
    m.name = "TestUser"
    m.nick = "TestNick"
    return m


@pytest.fixture
def test_user(mock_member):
    return User(mock_member)


@pytest.fixture
def test_user_no_member():
    return User(None)


def test_unsupplied_member(test_user_no_member):
    assert test_user_no_member


def test_initialization(test_user, mock_member):
    assert test_user.account == mock_member
    assert test_user.id == mock_member.id
    assert test_user.name == mock_member.name
    assert test_user.nickname == mock_member.nick


def test_immutable_attributes(test_user):
    with pytest.raises(AttributeError):
        test_user.account = "new_account"

    with pytest.raises(AttributeError):
        test_user.id = 999

    with pytest.raises(AttributeError):
        test_user.name = "Hacker"


def test_dynamic_trait_addition():
    assert not hasattr(User, "test_trait")
    User.add_trait("test_trait", 10)
    assert hasattr(User, "test_trait")
    assert User.test_trait == 10


def test_setting_non_immutable_updates_data(test_user):
    # Setting a non-immutable attribute should update data dict
    test_user.nickname = "NewNick"
    assert test_user.data.get("nickname") == "NewNick"
