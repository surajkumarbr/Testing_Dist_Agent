import unittest

from user_service import UserService, IllegalArgumentException, IndexOutOfBoundsException


class UserServiceTest(unittest.TestCase):
    def test_add_user_adds_valid_user_and_increments_count(self):
        service = UserService()

        self.assertEqual(0, service.get_user_count())
        service.add_user("alice")
        self.assertEqual(1, service.get_user_count())
        self.assertEqual(["alice"], service.get_all_users())

    def test_add_user_allows_whitespace_string_because_only_empty_is_rejected(self):
        service = UserService()

        service.add_user(" ")
        self.assertEqual(1, service.get_user_count())
        self.assertEqual(" ", service.get_user_by_index(0))

    def test_add_user_allows_duplicates(self):
        service = UserService()

        service.add_user("alice")
        service.add_user("alice")

        self.assertEqual(2, service.get_user_count())
        self.assertEqual(["alice", "alice"], service.get_all_users())

    def test_add_user_throws_for_null(self):
        service = UserService()

        with self.assertRaises(IllegalArgumentException) as context:
            service.add_user(None)
        self.assertEqual("Username cannot be null or empty", str(context.exception))
        self.assertEqual(0, service.get_user_count())

    def test_add_user_throws_for_empty_string(self):
        service = UserService()

        with self.assertRaises(IllegalArgumentException) as context:
            service.add_user("")
        self.assertEqual("Username cannot be null or empty", str(context.exception))
        self.assertEqual(0, service.get_user_count())

    def test_delete_user_returns_true_and_removes_when_user_exists(self):
        service = UserService()
        service.add_user("alice")
        service.add_user("bob")

        self.assertTrue(service.delete_user("alice"))
        self.assertEqual(1, service.get_user_count())
        self.assertEqual(["bob"], service.get_all_users())

    def test_delete_user_returns_false_when_user_does_not_exist(self):
        service = UserService()
        service.add_user("alice")

        self.assertFalse(service.delete_user("missing"))
        self.assertEqual(1, service.get_user_count())
        self.assertEqual(["alice"], service.get_all_users())

    def test_delete_user_returns_false_for_null_because_null_cannot_be_added(self):
        service = UserService()
        service.add_user("alice")

        self.assertFalse(service.delete_user(None))
        self.assertEqual(1, service.get_user_count())
        self.assertEqual(["alice"], service.get_all_users())

    def test_get_all_users_returns_copy_modifying_returned_list_does_not_affect_internal_state(self):
        service = UserService()
        service.add_user("alice")
        service.add_user("bob")

        snapshot = service.get_all_users()
        snapshot.append("mallory")
        snapshot.remove("alice")

        self.assertEqual(2, service.get_user_count())
        self.assertEqual(["alice", "bob"], service.get_all_users())

    def test_get_user_by_index_returns_correct_user_for_valid_indices(self):
        service = UserService()
        service.add_user("alice")
        service.add_user("bob")

        self.assertEqual("alice", service.get_user_by_index(0))
        self.assertEqual("bob", service.get_user_by_index(1))

    def test_get_user_by_index_throws_for_negative_index(self):
        service = UserService()
        service.add_user("alice")

        with self.assertRaises(IndexOutOfBoundsException) as context:
            service.get_user_by_index(-1)
        self.assertEqual("Invalid user index: -1", str(context.exception))

    def test_get_user_by_index_throws_for_index_equal_to_size(self):
        service = UserService()
        service.add_user("alice")

        with self.assertRaises(IndexOutOfBoundsException) as context:
            service.get_user_by_index(1)
        self.assertEqual("Invalid user index: 1", str(context.exception))

    def test_get_user_by_index_throws_when_list_empty_and_index_zero(self):
        service = UserService()

        with self.assertRaises(IndexOutOfBoundsException) as context:
            service.get_user_by_index(0)
        self.assertEqual("Invalid user index: 0", str(context.exception))

    def test_get_user_count_tracks_adds_deletes_and_clear(self):
        service = UserService()

        self.assertEqual(0, service.get_user_count())

        service.add_user("alice")
        service.add_user("bob")
        self.assertEqual(2, service.get_user_count())

        self.assertTrue(service.delete_user("alice"))
        self.assertEqual(1, service.get_user_count())

        service.clear_all_users()
        self.assertEqual(0, service.get_user_count())
        self.assertEqual([], service.get_all_users())

    def test_clear_all_users_is_idempotent(self):
        service = UserService()

        service.clear_all_users()
        service.clear_all_users()

        self.assertEqual(0, service.get_user_count())
        self.assertEqual([], service.get_all_users())


if __name__ == "__main__":
    unittest.main()
