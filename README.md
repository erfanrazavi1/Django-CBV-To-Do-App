# Django CBV To-Do App

A simple To-Do list application built with Django using Class-Based Views (CBV). This project is designed for practicing Django development and demonstrates how to implement CRUD (Create, Read, Update, Delete) operations for managing tasks using CBV.

## Features

- **CRUD Operations**: Create, view, edit, and delete tasks.
- **User Authentication**: (If implemented) Allows users to log in and manage their own tasks.
- **Class-Based Views (CBV)**: Utilizes Django's CBV for clean and maintainable code.
- **Responsive Design**: (If implemented) Ensures the app works well on various devices.
- **Code Quality**: (If implemented) Uses tools like Black and Flake8 for formatting and linting.

## Technologies Used

- **Django**: The web framework for perfectionists with deadlines.
- **Python**: Version 3.x (recommended).
- **Database**: SQLite (default) or PostgreSQL (configured).
- **Class-Based Views (CBV)**: For handling views in a structured way.
- **Frontend**: (If implemented) Bootstrap or a similar CSS framework for responsive design.

## Installation and Setup

### Prerequisites
- [Python 3.x](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [Docker](https://www.docker.com) , [Docker Comopose](https://docs.docker.com/compose/)
- 

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/erfanrazavi1/Django-CBV-To-Do-App.git
   cd Django-CBV-To-Do-App
   ```


2. **build Docker compose**
   ```bash
   docker compose -f docker-compose-stage.yml up --build -d
   ```

3. **Apply Database Migrations**
   ```bash
   docker compose -f docker-compose-stage.yml exec backend sh -c "python manage.py migrate"
   ```

4. **Create a Superuser** (For admin access)
   ```bash
   docker compose -f docker-compose-stage.yml exec backend sh -c "python manage.py createsuperuser"
   ```

5. **Access the Application**
   - Open your browser and go to `http://127.0.0.1`.
   - If user authentication is implemented, log in with the superuser credentials.

## How to Use

- **Django Admin Panel**: Access it at `http://127.0.0.1/admin` to manage tasks and users (if applicable).
- **Task Management**:
  - Create new tasks.
  - View all tasks.
  - Edit or delete existing tasks.
- **User Authentication** (If implemented):
  - Register new users.
  - Log in to access personal tasks.

## Contributing

Contributions are welcome! If you'd like to contribute:
- Fork the repository.
- Make your changes.
- Submit a pull request.

Please ensure your code follows Django's best practices and includes tests where applicable.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
