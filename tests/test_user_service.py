import pytest

from user_service import UserService, IllegalArgumentException, IndexOutOfBoundsException


def test_add_user_adds_valid_user_and_increments_count():
    service = UserService()

    assert service.get_user_count() == 0
    service.add_user("alice")
    assert service.get_user_count() == 1
    assert service.get_all_users() == ["alice"]


def test_add_user_allows_whitespace_string_because_only_empty_is_rejected():
    service = UserService()

    service.add_user(" ")
    assert service.get_user_count() == 1
    assert service.get_user_by_index(0) == " "


def test_add_user_allows_duplicates():
    service = UserService()

    service.add_user("alice")
    service.add_user("alice")

    assert service.get_user_count() == 2
    assert service.get_all_users() == ["alice", "alice"]


def test_add_user_throws_for_null():
    service = UserService()

    with pytest.raises(IllegalArgumentException) as ex:
        service.add_user(None)
    assert str(ex.value) == "Username cannot be null or empty"
    assert service.get_user_count() == 0


def test_add_user_throws_for_empty_string():
    service = UserService()

    with pytest.raises(IllegalArgumentException) as ex:
        service.add_user("")
    assert str(ex.value) == "Username cannot be null or empty"
    assert service.get_user_count() == 0


def test_delete_user_returns_true_and_removes_when_user_exists():
    service = UserService()
    service.add_user("alice")
    service.add_user("bob")

    assert service.delete_user("alice") is True
    assert service.get_user_count() == 1
    assert service.get_all_users() == ["bob"]


def test_delete_user_returns_false_when_user_does_not_exist():
    service = UserService()
    service.add_user("alice")

    assert service.delete_user("missing") is False
    assert service.get_user_count() == 1
    assert service.get_all_users() == ["alice"]


def test_delete_user_returns_false_for_null_because_null_cannot_be_added():
    service = UserService()
    service.add_user("alice")

    assert service.delete_user(None) is False
    assert service.get_user_count() == 1
    assert service.get_all_users() == ["alice"]


def test_get_all_users_returns_copy_modifying_returned_list_does_not_affect_internal_state():
    service = UserService()
    service.add_user("alice")
    service.add_user("bob")

    snapshot = service.get_all_users()
    snapshot.append("mallory")
    snapshot.remove("alice")

    assert service.get_user_count() == 2
    assert service.get_all_users() == ["alice", "bob"]


def test_get_user_by_index_returns_correct_user_for_valid_indices():
    service = UserService()
    service.add_user("alice")
    service.add_user("bob")

    assert service.get_user_by_index(0) == "alice"
    assert service.get_user_by_index(1) == "bob"


def test_get_user_by_index_throws_for_negative_index():
    service = UserService()
    service.add_user("alice")

    with pytest.raises(IndexOutOfBoundsException) as ex:
        service.get_user_by_index(-1)
    assert str(ex.value) == "Invalid user index: -1"


def test_get_user_by_index_throws_for_index_equal_to_size():
    service = UserService()
    service.add_user("alice")

    with pytest.raises(IndexOutOfBoundsException) as ex:
        service.get_user_by_index(1)
    assert str(ex.value) == "Invalid user index: 1"


def test_get_user_by_index_throws_when_list_empty_and_index_zero():
    service = UserService()

    with pytest.raises(IndexOutOfBoundsException) as ex:
        service.get_user_by_index(0)
    assert str(ex.value) == "Invalid user index: 0"


def test_get_user_count_tracks_adds_deletes_and_clear():
    service = UserService()

    assert service.get_user_count() == 0

    service.add_user("alice")
    service.add_user("bob")
    assert service.get_user_count() == 2

    assert service.delete_user("alice") is True
    assert service.get_user_count() == 1

    service.clear_all_users()
    assert service.get_user_count() == 0
    assert service.get_all_users() == []


def test_clear_all_users_is_idempotent():
    service = UserService()

    service.clear_all_users()
    service.clear_all_users()

    assert service.get_user_count() == 0
    assert service.get_all_users() == []
