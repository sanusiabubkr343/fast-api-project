DATABASE_URL = "sqlite://db.sqlite3"

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["app.models.user", "app.models.post",],
            "default_connection": "default",
        },
    },
}
