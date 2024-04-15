import subprocess


def run_alembic_upgrade():
    try:
        # Run the Alembic upgrade command
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("Alembic upgrade completed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Alembic: {e}")


if __name__ == "__main__":
    run_alembic_upgrade()
