import pytest


class IllegalArgumentException(Exception):
    pass


class IndexOutOfBoundsException(Exception):
    pass


class UserService:
    def __init__(self):
        self.users = []

    def addUser(self, username):
        if username is None or username == "":
            raise IllegalArgumentException("Username cannot be null or empty")
        self.users.append(username)

    def deleteUser(self, username):
        if username in self.users:
            self.users.remove(username)
            return True
        return False

    def getAllUsers(self):
        return list(self.users)

    def getUserByIndex(self, index):
        if index < 0 or index >= len(self.users):
            raise IndexOutOfBoundsException(f"Invalid user index: {index}")
        return self.users[index]

    def getUserCount(self):
        return len(self.users)

    def clearAllUsers(self):
        self.users.clear()


@pytest.fixture
def service():
    return UserService()


def test_add_user_increases_count_and_stores_username(service):
    service.addUser("alice")

    assert service.getUserCount() == 1
    assert service.getAllUsers() == ["alice"]


def test_add_multiple_users_preserves_insertion_order(service):
    service.addUser("alice")
    service.addUser("bob")
    service.addUser("charlie")

    assert service.getUserCount() == 3
    assert service.getAllUsers() == ["alice", "bob", "charlie"]
    assert service.getUserByIndex(0) == "alice"
    assert service.getUserByIndex(2) == "charlie"


def test_add_user_with_none_raises_exception(service):
    with pytest.raises(IllegalArgumentException) as exc_info:
        service.addUser(None)

    assert str(exc_info.value) == "Username cannot be null or empty"
    assert service.getUserCount() == 0


def test_add_user_with_empty_string_raises_exception(service):
    with pytest.raises(IllegalArgumentException) as exc_info:
        service.addUser("")

    assert str(exc_info.value) == "Username cannot be null or empty"
    assert service.getUserCount() == 0


def test_delete_existing_user_returns_true_and_removes_user(service):
    service.addUser("alice")
    service.addUser("bob")

    result = service.deleteUser("alice")

    assert result is True
    assert service.getUserCount() == 1
    assert service.getAllUsers() == ["bob"]


def test_delete_nonexistent_user_returns_false_and_keeps_state(service):
    service.addUser("alice")

    result = service.deleteUser("bob")

    assert result is False
    assert service.getUserCount() == 1
    assert service.getAllUsers() == ["alice"]


def test_get_all_users_returns_defensive_copy(service):
    service.addUser("alice")
    service.addUser("bob")

    users_copy = service.getAllUsers()
    users_copy.append("charlie")
    users_copy.remove("alice")

    assert users_copy == ["bob", "charlie"]
    assert service.getAllUsers() == ["alice", "bob"]
    assert service.getUserCount() == 2


def test_get_user_by_index_returns_correct_user(service):
    service.addUser("alice")
    service.addUser("bob")

    assert service.getUserByIndex(0) == "alice"
    assert service.getUserByIndex(1) == "bob"


def test_get_user_by_index_negative_raises_exception(service):
    service.addUser("alice")

    with pytest.raises(IndexOutOfBoundsException) as exc_info:
        service.getUserByIndex(-1)

    assert str(exc_info.value) == "Invalid user index: -1"


def test_get_user_by_index_equal_to_size_raises_exception(service):
    service.addUser("alice")

    with pytest.raises(IndexOutOfBoundsException) as exc_info:
        service.getUserByIndex(1)

    assert str(exc_info.value) == "Invalid user index: 1"


def test_get_user_by_index_from_empty_service_raises_exception(service):
    with pytest.raises(IndexOutOfBoundsException) as exc_info:
        service.getUserByIndex(0)

    assert str(exc_info.value) == "Invalid user index: 0"


def test_get_user_count_reflects_current_number_of_users(service):
    assert service.getUserCount() == 0

    service.addUser("alice")
    assert service.getUserCount() == 1

    service.addUser("bob")
    assert service.getUserCount() == 2

    service.deleteUser("alice")
    assert service.getUserCount() == 1


def test_clear_all_users_removes_every_user(service):
    service.addUser("alice")
    service.addUser("bob")

    service.clearAllUsers()

    assert service.getUserCount() == 0
    assert service.getAllUsers() == []


def test_clear_all_users_on_empty_service_keeps_it_empty(service):
    service.clearAllUsers()

    assert service.getUserCount() == 0
    assert service.getAllUsers() == []
