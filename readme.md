# FastAPI Project

This is a FastAPI project that includes the following features:

## Features

- **CRUD for Posts**: Create, read, update, and delete posts.
- **Comments on Posts**: Users can comment on posts.
- **User Authentication**: Secure user authentication system.
- **User Authorization**: Role-based access control for users.
- **PostgreSQL**: Database management using PostgreSQL.
- **Alembic**: Database migrations using Alembic.

## Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/sanusiabubkr343/fast-api-project
  cd fastapi_project
  ```

2. Create and activate a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
  ```

3. Install the dependencies:
  ```bash
  pip install -r requirements.txt
  ```

4. Set up the database:
  ```bash
  alembic upgrade head
  ```

## Usage

1. Run the FastAPI application:
  ```bash
  uvicorn main:app --reload
  ```

2. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the API documentation.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
