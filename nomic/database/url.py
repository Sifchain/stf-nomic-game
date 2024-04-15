import os


def get_url():
    return f'postgresql://{os.getenv("DB_USER", "user")}:{os.getenv("DB_PASSWORD", "password")}@{os.getenv("DB_HOST", "localhost")}:{os.getenv("DB_PORT", "5432")}/{os.getenv("DB_NAME", "postgres")}'
