from config.auth import ROLES
from infra.logging.security_logger import security_logger
from infra.metrics import metrics


USERS = {
    "admin": {"password": "admin123", "role": "ADMIN"},
    "manager": {"password": "manager123", "role": "MANAGER"},
    "user": {"password": "user123", "role": "USER"},
}


def authenticate(username: str, password: str) -> dict | None:
    user = USERS.get(username)

    if not user or user["password"] != password:
        return None

    role = user["role"]
    metrics.increment("logins")

    return {
        "username": username,
        "role": role,
        "permissions": ROLES.get(role, []),  # <-- FIXED HERE
    }

    


def has_permission(user: dict, permission: str) -> bool:
    return permission in user.get("permissions", [])


def require_permission(user: dict, permission: str) -> None:
    if not user:
        security_logger.warning("Permission denied: unauthenticated access attempt")
        raise PermissionError("User not authenticated")

    if permission not in user.get("permissions", []):
        metrics.increment("permission_denials")
        security_logger.warning(
            f"Permission denied | user={user.get('username')} | permission={permission}"
        )
        raise PermissionError("You do not have permission to perform this action")
