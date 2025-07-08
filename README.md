# PetCare-Backend

A RESTful API backend for a pet care application built with AWS Chalice, PostgreSQL, and Python.

## 📁 Project Structure

```
petcare-backend/
├── 📄 app.py                          # Main application entry point
├── 📄 requirements.txt                 # Python dependencies
├── 📄 policy-dev.json                 # AWS IAM policy for development
├── 📄 test_roles_improved.py         # Role testing scripts
├── 📄 test_roles.py                   # Role testing scripts
├── 📄 .gitignore                      # Git ignore rules
├── 📄 .chalice/                       # Chalice configuration
│   └── config.json                    # Chalice deployment config
│
├── 📁 vendor/                         # Vendored dependencies
│   ├── 📁 packages/                   # Application packages
│   │   ├── 📁 core/                   # Core functionality
│   │   │   ├── 📁 database/           # Database connection layer
│   │   │   │   └── postgresql.py      # PostgreSQL database handler
│   │   │   └── 📁 health/             # Health check endpoints
│   │   │       └── routers.py         # Health check routes
│   │   │
│   │   └── 📁 v1/                     # API version 1
│   │       ├── 📁 auth/               # Authentication module
│   │       │   ├── repository.py      # Database operations
│   │       │   ├── routers.py         # API routes
│   │       │   ├── schemas.py         # Data validation schemas
│   │       │   └── service.py         # Business logic
│   │       │
│   │       ├── 📁 category/           # Category management
│   │       │   ├── repository.py      # Database operations
│   │       │   ├── routers.py         # API routes
│   │       │   ├── schemas.py         # Data validation schemas
│   │       │   └── service.py         # Business logic
│   │       │
│   │       ├── 📁 comment/            # Comment system
│   │       │   ├── repository.py      # Database operations
│   │       │   ├── routers.py         # API routes
│   │       │   ├── schemas.py         # Data validation schemas
│   │       │   └── service.py         # Business logic
│   │       │
│   │       ├── 📁 posts/              # Posts management
│   │       │   ├── repository.py      # Database operations
│   │       │   ├── routers.py         # API routes
│   │       │   ├── schemas.py         # Data validation schemas
│   │       │   └── service.py         # Business logic
│   │       │
│   │       ├── 📁 products/           # Product catalog
│   │       │   ├── repository.py      # Database operations
│   │       │   ├── routers.py         # API routes
│   │       │   ├── schemas.py         # Data validation schemas
│   │       │   └── service.py         # Business logic
│   │       │
│   │       ├── 📁 rating/             # Rating system
│   │       │   ├── repository.py      # Database operations
│   │       │   ├── routers.py         # API routes
│   │       │   ├── schemas.py         # Data validation schemas
│   │       │   └── service.py         # Business logic
│   │       │
│   │       ├── 📁 roles/              # User roles management
│   │       │   ├── repository.py      # Database operations
│   │       │   ├── routers.py         # API routes
│   │       │   ├── schemas.py         # Data validation schemas
│   │       │   └── service.py         # Business logic
│   │       │
│   │       ├── 📁 tag/                # Tagging system
│   │       │   ├── repository.py      # Database operations
│   │       │   ├── routers.py         # API routes
│   │       │   ├── schemas.py         # Data validation schemas
│   │       │   └── service.py         # Business logic
│   │       │
│   │       └── 📁 user/               # User management
│   │           ├── repository.py      # Database operations
│   │           ├── routers.py         # API routes
│   │           ├── schemas.py         # Data validation schemas
│   │           └── service.py         # Business logic
│   │
│   └── 📁 [dependencies]/             # Vendored Python packages
│       ├── pydantic/                  # Data validation
│       ├── asyncpg/                   # Async PostgreSQL driver
│       ├── psycopg2/                  # PostgreSQL adapter
│       ├── dotenv/                    # Environment variable management
│       └── [other dependencies]/
```

## 🚀 Features

- **RESTful API**: Complete REST API with proper HTTP methods
- **Authentication**: User authentication and authorization system
- **Database**: PostgreSQL with async support
- **Validation**: Pydantic schemas for data validation
- **CORS**: Cross-origin resource sharing enabled
- **Health Checks**: API health monitoring endpoints
- **Modular Architecture**: Clean separation of concerns
- **Partial Updates**: Support for partial field updates (e.g., comments)

## 🛠️ Technology Stack

- **Framework**: AWS Chalice (Serverless)
- **Database**: PostgreSQL
- **ORM**: Custom repository pattern with asyncpg
- **Validation**: Pydantic v2
- **Authentication**: bcrypt for password hashing
- **Deployment**: AWS Lambda + API Gateway

## 📋 Prerequisites

- Python 3.12+ (recommended for AWS Lambda compatibility)
- PostgreSQL database
- AWS CLI configured
- Chalice CLI installed

## 🔧 Installation & Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd petcare-backend
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the root directory:
```env
DATABASE_URL=postgresql://username:password@host:port/database
AWS_REGION=ap-southeast-2
```

### 4. Deploy to AWS
```bash
chalice deploy
```

## 📚 API Endpoints

### Health Check
- `GET /health` - API health status

### Authentication
- `POST /v1/auth/login` - User login
- `POST /v1/auth/register` - User registration

### Users
- `GET /v1/user` - Get all users (paginated)
- `POST /v1/user` - Create new user
- `GET /v1/user/{user_id}` - Get user by ID
- `PUT /v1/user/{user_id}` - Update user
- `DELETE /v1/user/{user_id}` - Delete user

### Roles
- `GET /v1/roles` - Get all roles
- `POST /v1/roles` - Create new role
- `GET /v1/roles/{role_id}` - Get role by ID
- `PUT /v1/roles/{role_id}` - Update role
- `DELETE /v1/roles/{role_id}` - Delete role

### Products
- `GET /v1/products` - Get all products (paginated)
- `POST /v1/products` - Create new product
- `GET /v1/products/{product_id}` - Get product by ID
- `PUT /v1/products/{product_id}` - Update product
- `DELETE /v1/products/{product_id}` - Delete product

### Posts
- `GET /v1/posts` - Get all posts (paginated)
- `POST /v1/posts` - Create new post
- `GET /v1/posts/{post_id}` - Get post by ID
- `PUT /v1/posts/{post_id}` - Update post
- `DELETE /v1/posts/{post_id}` - Delete post

### Comments
- `GET /v1/comment` - Get all comments (paginated)
- `POST /v1/comment` - Create new comment
- `GET /v1/comment/{entity_type}/{entity_id}` - Get comments by entity
- `PUT /v1/comment/update/{comment_id}` - Update comment (partial updates supported)
- `DELETE /v1/comment/{entity_type}/{entity_id}` - Delete comments by entity

### Categories
- `GET /v1/category` - Get all categories
- `POST /v1/category` - Create new category
- `GET /v1/category/{category_id}` - Get category by ID
- `PUT /v1/category/{category_id}` - Update category
- `DELETE /v1/category/{category_id}` - Delete category

### Tags
- `GET /v1/tag` - Get all tags
- `POST /v1/tag` - Create new tag
- `GET /v1/tag/{tag_id}` - Get tag by ID
- `PUT /v1/tag/{tag_id}` - Update tag
- `DELETE /v1/tag/{tag_id}` - Delete tag

### Ratings
- `GET /v1/rating` - Get all ratings
- `POST /v1/rating` - Create new rating
- `GET /v1/rating/{rating_id}` - Get rating by ID
- `PUT /v1/rating/{rating_id}` - Update rating
- `DELETE /v1/rating/{rating_id}` - Delete rating

## 🔄 Partial Updates

The API supports partial updates for certain endpoints. For example, when updating a comment:

```json
// Update only the comment text
PUT /v1/comment/update/123
{
  "comment": "Updated comment text"
}

// Update only the status
PUT /v1/comment/update/123
{
  "status_id": 2
}

// Update both fields
PUT /v1/comment/update/123
{
  "comment": "Updated comment text",
  "status_id": 2
}
```

## 🏗️ Architecture

### Layer Structure
1. **Routers Layer** (`routers.py`) - HTTP request handling and validation
2. **Service Layer** (`service.py`) - Business logic and orchestration
3. **Repository Layer** (`repository.py`) - Database operations
4. **Schema Layer** (`schemas.py`) - Data validation and serialization

### Database Pattern
- Uses Repository pattern for data access
- Async PostgreSQL connections with asyncpg
- Connection pooling for optimal performance
- Parameterized queries for security

## 🧪 Testing

Run the test scripts:
```bash
python test_roles.py
python test_roles_improved.py
```

## 🚀 Deployment

### Development
```bash
chalice local
```

### Production
```bash
chalice deploy
```

## 📊 API Response Format

### Success Response
```json
{
  "data": {...},
  "message": "Success message",
  "status": "success"
}
```

### Error Response
```json
{
  "error": "Error message",
  "details": [...],
  "status": "error"
}
```

### Paginated Response
```json
{
  "data": [...],
  "total": 100,
  "total_pages": 10,
  "has_next": true,
  "has_prev": false,
  "current_page": 1
}
```

## 🔐 Security

- Password hashing with bcrypt
- CORS configuration for cross-origin requests
- Input validation with Pydantic
- Parameterized queries to prevent SQL injection
- AWS IAM roles for access control

## 📝 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `AWS_REGION` | AWS region for deployment | Yes |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

[Add your license information here]

## 🆘 Support

For support and questions, please contact [your contact information].