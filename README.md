# Lab Management System
LMS MSD is a web-based application that helps laboratories optimize machine scheduling and streamline overall management. It is built using Django, Next.js, and MySQL, and deployed using Docker and Nginx. The system is designed to work with PlanetScale, ensuring scalability and performance.

## Features
- Optimal scheduling of laboratory machines
- User authentication and access control
- Inventory tracking and management
- Equipment maintenance and calibration tracking
- Reporting and analytics
- Responsive user interface for desktop and mobile devices

## Requirements
- Docker
- Nginx
- Python 3.x
- Node.js (for Next.js)
- MySQL (or PlanetScale)

## Installation and Running Locally

1. clone the repository:
`git clone https://github.com/yourusername/lab-management-system.git`
`cd lab-management-system`

2. Build and start the Docker images:
`docker-compose up --build --force-recreate`

3. Access the application at: http://app.localhost:3001

## Testing

We use tox for automated testing, which incorporates mypy, flake8, and pytest. To run the tests, execute the following command:

`tox`

## Contributing
We welcome contributions to the Lab Management System! Please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bugfix.
3. Make your changes, ensuring that your code follows the project's style guidelines and passes all tests.
4. Submit a pull request to the main repository, and provide a detailed description of your changes.

## License
This project is licensed under the BSD 3-Clause License.
