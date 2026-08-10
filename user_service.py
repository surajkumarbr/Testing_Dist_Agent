class UserService:
    def __init__(self):
        self._users = []

    def add_user(self, username: str) -> None:
        if username is None or username == "":
            raise ValueError("Username cannot be null or empty")
        self._users.append(username)

    def delete_user(self, username: str) -> bool:
        try:
            self._users.remove(username)
            return True
        except ValueError:
            return False

    def get_all_users(self) -> list[str]:
        return list(self._users)

    def get_user_by_index(self, index: int) -> str:
        if index < 0 or index >= len(self._users):
            raise IndexError(f"Invalid user index: {index}")
        return self._users[index]

    def get_user_count(self) -> int:
        return len(self._users)

    def clear_all_users(self) -> None:
        self._users.clear()
