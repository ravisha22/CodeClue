def normalize_user(name: str) -> str:
    return name.strip().lower()


def build_greeting(name: str) -> str:
    cleaned = normalize_user(name)
    return f"hello {cleaned}"


class Greeter:
    def greet(self, name: str) -> str:
        return build_greeting(name)
