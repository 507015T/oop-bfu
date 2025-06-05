from schemas.users import User
from repositories.users import UserRepository
from services.auth import AuthService

if __name__ == "__main__":
    USER_DATA = {
        "id": 1,
        "name": "Фрейзер",
        "login": "tralalelotralala",
        "password": "piter_de_Oras6847",
        "email": "mozgoduitoshnilov@gmail.com",
    }

    user_repo = UserRepository("users.json", User)
    auth_service = AuthService("session.json", user_repo)

    new_user = User(**USER_DATA)
    if not user_repo.get_by_id(USER_DATA["id"]):
        user_repo.add(new_user)
        print(f"Пользователь {new_user.name} успешно добавлен.")

    user = user_repo.get_by_id(USER_DATA["id"])
    if user:
        old_name = user.name
        user.name = "Фатих"
        user_repo.update(user)
        print(f"Данные пользователя обновлены[name]: {old_name} -> {user.name}")

    login_user = user_repo.get_by_login(USER_DATA["login"])
    if login_user and login_user.password == USER_DATA["password"]:
        auth_service.sign_in(login_user)
        print(f"Успешная авторизация: {auth_service.current_user.name}")

    # auth_service.sign_out()
    # print("Пользователь вышел из системы.")

    # Проверка автологина
    if auth_service.is_authorized:
        print(f"Сессия восстановлена: {auth_service.current_user.name}")
    else:
        print("Нет активной сессии.")

    user_to_delete = user_repo.get_by_id(USER_DATA["id"])
    if user_to_delete:
        user_repo.delete(user_to_delete)
        print(f"Пользователь {user_to_delete.name} удалён.")
