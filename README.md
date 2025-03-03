# E-Shop: Custom Admin Dashboard

A comprehensive e-commerce platform with a custom admin dashboard built with Django, offering powerful product management, order processing, user management, and analytics features.

## 🌟 Features

### Custom Admin Dashboard
- **Intuitive Interface**: Modern, responsive design built with Bootstrap 5
- **Comprehensive Analytics**: Real-time sales data, product performance, and inventory tracking
- **Role-based Access Control**: Secure access management for different staff roles

### Product Management
- Complete CRUD operations for products and categories
- Bulk operations for efficient inventory management
- Image upload and management
- Stock level tracking and alerts

### Order Processing
- Order status tracking and management
- Detailed order history and customer information
- Order filtering by date, status, and customer
- Order timeline visualization

### User Management
- Customer account management
- Staff access control
- User activity tracking

### Analytics & Reporting
- Sales performance charts and metrics
- Product popularity analysis
- Inventory level monitoring
- Time-period comparison (daily/weekly/monthly)

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Danh-coder/eshop.git
   cd ecommerce_project
   ```

2. **Set up a virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate it
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Create a `.env` file in the root directory
   - Add necessary environment variables (see `.env.example`)

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the admin dashboard**
   - Navigate to `http://127.0.0.1:8000/custom-admin/`
   - Log in with your superuser credentials

10. **Access the Eshop interface**
   - Navigate to `http://127.0.0.1:8000/`

## 📁 Project Structure

```
eshop/
├── custom_admin/            # Custom admin dashboard app
│   ├── static/              # Static files for admin
│   ├── templates/           # Admin templates
│   ├── views/               # Admin view functions
│   └── ...
├── store/                   # Main store app
│   ├── models.py            # Database models
│   ├── views.py             # Store views
│   └── ...
├── templates/               # Global templates
├── static/                  # Global static files
├── media/                   # User-uploaded files
└── manage.py                # Django management script
README.md                # This file
```

## 🛠️ Technology Stack

- **Backend**: Django 4.2+
- **Frontend**: HTML, CSS, JavaScript
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome
- **Charts**: Chart.js
- **Database**: SQLite (development), PostgreSQL (production recommended)

## 🔧 Configuration

### Custom Settings
The project includes several customizable settings in `settings.py`:

- `CUSTOM_ADMIN_SITE_HEADER`: Change the admin site header
- `CUSTOM_ADMIN_SITE_TITLE`: Change the admin site title
- `PRODUCTS_PER_PAGE`: Number of products to display per page
- `ORDERS_PER_PAGE`: Number of orders to display per page

### Environment Variables
Create a `.env` file with the following variables:

```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
EMAIL_HOST=your-email-host
EMAIL_PORT=your-email-port
EMAIL_HOST_USER=your-email-user
EMAIL_HOST_PASSWORD=your-email-password
```

## 📊 Dashboard Sections

### Main Dashboard
- Overview of key metrics
- Recent orders and activities
- Quick access to common tasks

### Products
- List, add, edit, and delete products
- Filter and search functionality
- Category management

### Orders
- Order listing with advanced filtering
- Detailed order view
- Order status management
- Customer communication

### Users
- Customer account management
- Staff user management
- Activity tracking

### Analytics
- Sales charts and trends
- Product performance
- Category distribution
- Inventory levels

## 🔄 API Endpoints

The custom admin includes several API endpoints for chart data:

- `/custom-admin/analytics/api/chart-data/?type=sales&period=daily`: Daily sales data
- `/custom-admin/analytics/api/chart-data/?type=sales&period=weekly`: Weekly sales data
- `/custom-admin/analytics/api/chart-data/?type=sales&period=monthly`: Monthly sales data
- `/custom-admin/analytics/api/chart-data/?type=categories`: Category distribution
- `/custom-admin/analytics/api/chart-data/?type=popular_products`: Popular products
- `/custom-admin/analytics/api/chart-data/?type=stock_levels`: Stock levels

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

## 🚀 Deployment

### Production Settings
For production deployment:

1. Set `DEBUG=False` in your environment
2. Configure a production database (PostgreSQL recommended)
3. Set up proper email settings
4. Configure static files serving with a CDN or web server
5. Set up HTTPS with a valid SSL certificate

### Deployment Platforms
The project can be deployed on:
- Heroku
- AWS Elastic Beanstalk
- DigitalOcean
- PythonAnywhere
- Any platform supporting Django applications

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

Your Name - your.email@example.com

Project Link: [https://github.com/Danh-coder/eshop.git](https://github.com/Danh-coder/eshop.git)

## 🙏 Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Chart.js](https://www.chartjs.org/)
- [Font Awesome](https://fontawesome.com/)

---

*Made with ❤️ by Danh Phan*