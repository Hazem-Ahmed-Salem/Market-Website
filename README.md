# 🛍️ Market Website  
* A modern e-commerce platform with product browsing, cart functionality, user authentication, and  admin panel 
* It's not production ready

## 🌟 Image Gallery
<div align="center">
  <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 10px;">
    <img src="https://github.com/Hazem-Ahmed-Salem/Market-Website/blob/master/Preview/1.jpg" width="30%" alt="Home Page">
    <img src="https://github.com/Hazem-Ahmed-Salem/Market-Website/blob/master/Preview/2.jpg" width="30%" alt="Home Page">
    <img src="https://github.com/Hazem-Ahmed-Salem/Market-Website/blob/master/Preview/3.jpg" width="30%" alt="Home Page">
    <img src="https://github.com/Hazem-Ahmed-Salem/Market-Website/blob/master/Preview/4.jpg" width="30%" alt="Home Page">
    <img src="https://github.com/Hazem-Ahmed-Salem/Market-Website/blob/master/Preview/5.jpg" width="30%" alt="Home Page">
    <img src="https://github.com/Hazem-Ahmed-Salem/Market-Website/blob/master/Preview/6.jpg" width="30%" alt="Home Page">
    <img src="https://github.com/Hazem-Ahmed-Salem/Market-Website/blob/master/Preview/7.jpg" width="30%" alt="Home Page">
    <img src="https://github.com/Hazem-Ahmed-Salem/Market-Website/blob/master/Preview/8.jpg" width="30%" alt="Home Page">
    <img src="https://github.com/Hazem-Ahmed-Salem/Market-Website/blob/master/Preview/9.jpg" width="30%" alt="Home Page">
    
  </div>
  <em>Click images to enlarge</em>
</div>

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

## 💻 User Roles  
- **Manager**  
- **Inventory Manager**  
- **Employee (Website Clerk)**  
- **Delivery Driver**  
- **Customer**  

   
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
      <span>Worked on:</span>
      <br />
      <span>Frontend and backend development</span>
    </td>
    <td align="center">
      <a href="https://github.com/Ahmed482-21albadawy">
        <img src="https://avatars.githubusercontent.com/Ahmed482-21albadawy" width="100px;" style="border-radius: 50%;" alt="Ahmed482-21albadawy"/>
        <br />
        <sub><b>Ahmed Albadawy</b></sub>
      </a>
      <br />
      <span>Worked on:</span>
      <br />
      <span>Machine Learning development</span>
    </td>
  </tr>
</table>