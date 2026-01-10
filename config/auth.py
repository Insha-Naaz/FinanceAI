# config/auth.py

ROLES = {
    "ADMIN": ["query", "update", "delete"],
    "MANAGER": ["query", "update"],
    "USER": ["query"]  # << must include "query" for Top Category, Count, Total queries
}
