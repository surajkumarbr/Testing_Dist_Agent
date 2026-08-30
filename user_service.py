class IllegalArgumentException(ValueError):
    pass


class IndexOutOfBoundsException(IndexError):
    pass


class UserService:
    def __init__(self):
        self._users = []

    def add_user(self, username):
        if username is None or username == "":
            raise IllegalArgumentException("Username cannot be null or empty")
        self._users.append(username)

    def delete_user(self, username):
        try:
            self._users.remove(username)
            return True
        except ValueError:
            return False

    def get_all_users(self):
        return list(self._users)

    def get_user_by_index(self, index):
        if index < 0 or index >= len(self._users):
            raise IndexOutOfBoundsException(f"Invalid user index: {index}")
        return self._users[index]

    def get_user_count(self):
        return len(self._users)

    def clear_all_users(self):
        self._users.clear()
