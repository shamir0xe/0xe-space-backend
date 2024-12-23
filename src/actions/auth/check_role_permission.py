from src.models.user import User
from src.types.user_roles import UserRoles


class CheckRolePermission:
    @staticmethod
    def check(user: User, role: UserRoles) -> bool:
        if role is UserRoles.ADMIN:
            return user.is_admin
        return True
