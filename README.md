# Food Delivery Application

A Django-based food delivery application that allows users to order food online.

## Features

- User Authentication (Login/Register)
- Password Reset Functionality
- Custom Admin Interface
- Order Management System

## Project Structure

```
food_delivery/
├── food_delivery/        # Project settings
├── frontend/            # Frontend templates and static files
│   ├── static/         # CSS and other static assets
│   └── templates/      # HTML templates
└── orders/             # Main application
    ├── models.py       # Database models
    ├── views.py        # View logic
    ├── forms.py        # Form definitions
    └── admin.py        # Admin interface customization
```

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run migrations:
   ```
   python manage.py migrate
   ```
6. Start the development server:
   ```
   python manage.py runserver
   ```

## Running the Project Without a Virtual Environment

To run this project without a virtual environment, follow these steps:

1. Install Django globally:
   ```bash
   pip install django
   ```

2. Install other dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Navigate to the project directory:
   ```bash
   cd path/to/food_delivery
   ```

4. Run the server:
   ```bash
   python manage.py runserver
   ```

5. Access the application at `http://127.0.0.1:8000/`.

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
