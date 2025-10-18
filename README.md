# E-commerce_ALx

# 🛍️ E-Commerce API (Django REST Framework)

A full-stack-ready **E-Commerce Backend API** built with **Django + Django REST Framework**, featuring user authentication, product management, cart & orders, payments (Stripe/Paystack), reviews, and optional AI product recommendations.

---

## 🚀 Overview

This project provides a complete RESTful backend for an e-commerce web or mobile app.  
It includes **authentication**, **product CRUD**, **cart and order flow**, **payments**, **reviews**, and optional **AI-based product recommendations**.

The backend is built using:
- **Django 5+**
- **Django REST Framework (DRF)**
- **JWT Authentication (SimpleJWT)**
- **Stripe or Paystack** for payments
- **Celery + Redis** for background tasks
- **Gunicorn + Whitenoise** for production deployment

---

## 🧩 Features

| Feature | Description |
|----------|-------------|
| 👤 **User Authentication** | Register, Login, JWT Token Auth (SimpleJWT). |
| 🛒 **Product Management** | CRUD endpoints for products and categories (admin protected). |
| 🧺 **Cart & Checkout** | Add/remove products, calculate totals, and checkout to create orders. |
| 💳 **Payments** | Integrate with **Stripe** or **Paystack** for real transactions. |
| 📝 **Reviews & Ratings** | Users can rate and review products. |
| 🔍 **Search & Filters** | Search products by name or filter by category. |
| 🤖 **AI Recommendations (Optional)** | Collaborative/content-based product recommendations. |
| 📧 **Celery Tasks** | Background jobs for email notifications and stock updates. |
| ☁️ **Deployment Ready** | Configured for Render or Heroku using Gunicorn & Whitenoise. |

---

## 🗄️ Entity-Relationship Diagram (ERD)

