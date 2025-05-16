# 🛍️ Market Website  
* A modern e-commerce platform with product browsing, cart functionality, user authentication, and  admin panel 
* It's not production ready
* [Market Website Preview]

<video width="100%" controls>
  <source src="./Preview/video/Video.mp4" type="video/mp4">
</video>

## ✨ Features  
- **User System**  
  - Registration & login functionality  
  - Profile management  
- **Product Catalog**  
  - Browse products by categories  
  - Product Recommendation
  - Search functionality  
- **Shopping Cart**  
  - Add/remove items  
  - Quantity adjustment  
- **Order System**  
  - Checkout process  
  - Track order status
  - Order history  
- **Admin Panel**  
  - Product management (add/edit/delete)
  - Product price prediction
  - Analytics for sales  
  - User management  

<!-- ## 🚀 Live Demo  
*(If deployed, add link here - e.g.: [View Live Demo](https://yourdeploymentlink.com))*   -->

## 🛠️ Tech Stack  
### Frontend  
- HTML5, CSS3, JavaScript    
- Font Awesome (icons)  

### Backend  
- Django 
- Django Rest Framework  
- Sqlite  

### AI Models
- Price Predictor
- Product Recommendation


## 📥 Installation Guide (Django)  
## 1. Prerequisites  
### Ensure you have:
- Python 3.10+
- pip installed
- Virtualenv (recommended)

# Clone repository
git clone https://github.com/Hazem-Ahmed-Salem/Market-Website.git
cd Market-Website

# Create virtual environment (recommended)
python -m venv venv
### On Linux: source venv/bin/activate  
### On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt  

# Database setup
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Collect static files (Django)
python manage.py collectstatic

# For Running Development server
python manage.py runserver
### Access at http://127.0.0.1:8000
### Admin at http://127.0.0.1:8000/admin


## 👥 Development Team

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Hazem-Ahmed-Salem">
        <img src="https://avatars.githubusercontent.com/Hazem-Ahmed-Salem" width="100px;" style="border-radius: 50%;" alt="Hazem Ahmed Salem"/>
        <br />
        <sub><b>Hazem Ahmed Salem</b></sub>
      </a>
      <br />
      <br />
      <span>Frontend and backend dev</span>
    </td>
    <td align="center">
      <a href="https://github.com/Ahmed482-21albadawy">
        <img src="https://avatars.githubusercontent.com/Ahmed482-21albadawy" width="100px;" style="border-radius: 50%;" alt="Ahmed482-21albadawy"/>
        <br />
        <sub><b>Ahmed Albadawy</b></sub>
      </a>
      <br />
      <br />
      <span>Machine Learning dev</span>
    </td>
  </tr>
</table>