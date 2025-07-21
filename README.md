***Ecommerce Backend API***
-> This is a backend API built using FastAPI and MongoDB for managing products and orders.

***Tech Stack***
1. Python 3.10+
2. FastAPI
3. MongoDB
4. Motor (Async MongoDB driver)
5. Pydantic
6. Poetry (Dependency management)
7. Uvicorn (ASGI server)

***Setup Instructions***
1. Clone the repository
   git clone https://github.com/your-username/ecom-backend.git
   cd ecom-backend
2. Configure environment variables
   -> Create a .env file in the root directory with the following:
        MONGO_URI=your_mongo_connection_string
        DATABASE_NAME=your_database_name
3. Install dependencies
    poetry install
4. Run the server
    uvicorn app.main:app --reload

***API Endpoints***
1. Create Product
    POST /products

2. Get All Products
    GET /products

        Supports query parameters:
        search — keyword filter
        limit — limit number of products
        skip — skip N products

3. Get Single Product
    GET /products/{product_id}

4. Create Order
    POST /orders

5. Get All Orders
    GET /orders