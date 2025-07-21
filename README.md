# 🛍️ Ecommerce Backend API 

This is a sample ecommerce backend built using **FastAPI**, **MongoDB**, and **Motor**. The app provides APIs to manage products and customer orders, with filtering and pagination features.

---

## 📦 Tech Stack

- **Python 3.10+**
- **FastAPI** (Backend Framework)
- **Motor** (Async MongoDB driver)
- **MongoDB Atlas (M0 Free Tier)**
- **Poetry** (Dependency Management)
- **Render** (Deployment Platform)

---

## 🚀 API Endpoints

### 📌 Create Product

- **Endpoint:** `POST /products`
- **Request Body:**
```json
{
  "name": "Sample Product",
  "price": 199.99,
  "sizes": [
    { "size": "M", "quantity": 10 },
    { "size": "L", "quantity": 5 }
  ]
}
