# Library Management System - API Design Document

## 1. Project Description

### Overview
The Library Management System (LMS) is a RESTful API built with Django REST Framework that manages core library operations including book cataloging, member management, and borrowing transactions.

### Core Functionalities
- **Catalog Management**: Manage books, authors, and categories with complete CRUD operations
- **Member Management**: Track library members and their profiles
- **Borrowing System**: Handle book checkouts, returns, and track borrowing history
- **Search & Filter**: Advanced filtering by title, ISBN, author, category, and status
- **Availability Tracking**: Real-time book availability monitoring

### Key Features
- UUID-based primary keys for enhanced security
- Pagination support (10 items per page, configurable up to 100)
- Advanced filtering using django-filter
- Query optimization with select_related and prefetch_related
- Nested routes for related resources (books → borrow records, members → borrow records)
- Status tracking for borrowed books (Active, Returned, Overdue)

---

## 2. Database Schema (Models Definition)

### 2.1 Author Model
Stores information about book authors.

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| id | UUIDField (PK) | Auto-generated unique identifier |
| name | CharField(200) | Full name of the author |
| bio | TextField (optional) | Author biography |
| created_at | DateTimeField | Timestamp when author was added (auto) |

**Relationships:**
- Author to Book: Many-to-Many (one author can write multiple books, one book can have multiple authors)

---

### 2.2 Category Model
Organizes books into categories/genres.

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| id | BigAutoField (PK) | Auto-increment ID |
| name | CharField(100) | Category name (Fiction, Science, History, etc.) |
| description | TextField (optional) | Category description |
| created_at | DateTimeField | Timestamp when category was created (auto) |

**Relationships:**
- Category to Book: One-to-Many (one category has many books)

---

### 2.3 Book Model
Main book catalog with inventory tracking.

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| id | UUIDField (PK) | Auto-generated unique identifier |
| title | CharField(200) | Book title |
| isbn | CharField(13, unique) | International Standard Book Number |
| author | ManyToManyField | Links to Author model |
| category | ForeignKey | Links to Category model (PROTECT on delete) |
| total_copies | PositiveIntegerField | Total physical copies owned |
| available_copies | PositiveIntegerField | Currently available copies |
| created_at | DateTimeField | When book was added to system (auto) |
| updated_at | DateTimeField | Last modification timestamp (auto) |

**Relationships:**
- Book to Author: Many-to-Many (via default through table)
- Book to Category: Many-to-One (PROTECT - cannot delete category if books exist)
- Book to BorrowRecord: One-to-Many

---

### 2.4 Member Model
Represents library members.

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| id | UUIDField (PK) | Auto-generated unique identifier |
| email | EmailField (unique) | Member's email address |
| created_at | DateTimeField | Account creation timestamp (auto) |

**Relationships:**
- Member to BorrowRecord: One-to-Many

**Note:** This is a simplified member model. Future enhancements could include name, phone, address, and authentication fields.

---

### 2.5 BorrowRecord Model
Tracks all book borrowing transactions.

| Field Name | Data Type | Description |
|------------|-----------|-------------|
| id | UUIDField (PK) | Auto-generated unique identifier |
| book | ForeignKey | Links to Book (PROTECT - cannot delete borrowed books) |
| member | ForeignKey | Links to Member (CASCADE - delete records if member deleted) |
| borrow_date | DateTimeField | When book was borrowed (auto-set on creation) |
| due_date | DateField | Expected return date |
| return_date | DateTimeField (nullable) | Actual return date (null if not returned) |
| status | CharField(20) | Current status: Active, Returned, or Overdue |

**Status Choices:**
- `Active`: Book is currently borrowed
- `Returned`: Book has been returned
- `Overdue`: Book is past due date

**Relationships:**
- BorrowRecord to Book: Many-to-One (PROTECT)
- BorrowRecord to Member: Many-to-One (CASCADE)

---

## 3. API Endpoints Definition

### Base URL Structure
All endpoints are prefixed with `/api/`

Example: `http://localhost:8000/api/books/`

---

### 3.1 Author Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/authors/` | List all authors (paginated) | Public |
| POST | `/api/authors/` | Create new author | Admin |
| GET | `/api/authors/{id}/` | Retrieve specific author | Public |
| PUT | `/api/authors/{id}/` | Full update author | Admin |
| PATCH | `/api/authors/{id}/` | Partial update author | Admin |
| DELETE | `/api/authors/{id}/` | Delete author | Admin |

**Query Parameters:**
- `?name={search_term}` - Search authors by name (case-insensitive)
- `?page={number}` - Pagination
- `?page_size={number}` - Items per page (max 100)

---

### 3.2 Category Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/categories/` | List all categories (paginated) | Public |
| POST | `/api/categories/` | Create new category | Admin |
| GET | `/api/categories/{id}/` | Retrieve specific category | Public |
| PUT | `/api/categories/{id}/` | Full update category | Admin |
| PATCH | `/api/categories/{id}/` | Partial update category | Admin |
| DELETE | `/api/categories/{id}/` | Delete category | Admin |

**Query Parameters:**
- `?name={search_term}` - Search categories by name (case-insensitive)
- `?page={number}` - Pagination
- `?page_size={number}` - Items per page

---

### 3.3 Book Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/books/` | List all books (paginated) | Public |
| POST | `/api/books/` | Add new book | Admin |
| GET | `/api/books/{id}/` | Retrieve specific book | Public |
| PUT | `/api/books/{id}/` | Full update book | Admin |
| PATCH | `/api/books/{id}/` | Partial update book | Admin |
| DELETE | `/api/books/{id}/` | Remove book | Admin |

**Query Parameters:**
- `?title={search_term}` - Search books by title (case-insensitive)
- `?isbn={exact_isbn}` - Filter by exact ISBN
- `?category_id={uuid}` - Filter by category ID
- `?author_id={uuid}` - Filter by author ID
- `?page={number}` - Pagination
- `?page_size={number}` - Items per page

---

### 3.4 Member Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/members/` | List all members (paginated) | Admin |
| POST | `/api/members/` | Create new member | Admin |
| GET | `/api/members/{id}/` | Retrieve specific member | Admin/Owner |
| PUT | `/api/members/{id}/` | Full update member | Admin/Owner |
| PATCH | `/api/members/{id}/` | Partial update member | Admin/Owner |
| DELETE | `/api/members/{id}/` | Delete member account | Admin |

**Query Parameters:**
- `?email={search_term}` - Search members by email (case-insensitive)
- `?page={number}` - Pagination
- `?page_size={number}` - Items per page

---

### 3.5 BorrowRecord Endpoints (Nested Routes)

#### Main BorrowRecord Routes
These endpoints are not exposed in the current implementation but can be accessed via nested routes.

#### Nested Route: Books → Borrow Records

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/books/{book_id}/borrow-records/` | List all borrow records for a specific book | Admin |
| POST | `/api/books/{book_id}/borrow-records/` | Create borrow record for specific book | Admin |
| GET | `/api/books/{book_id}/borrow-records/{id}/` | Get specific borrow record | Admin |
| PUT | `/api/books/{book_id}/borrow-records/{id}/` | Update borrow record | Admin |
| PATCH | `/api/books/{book_id}/borrow-records/{id}/` | Partial update | Admin |
| DELETE | `/api/books/{book_id}/borrow-records/{id}/` | Delete record | Admin |

#### Nested Route: Members → Borrow Records

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/members/{member_id}/borrow-records/` | List all borrow records for a specific member | Admin/Owner |
| POST | `/api/members/{member_id}/borrow-records/` | Create borrow record for specific member | Admin |
| GET | `/api/members/{member_id}/borrow-records/{id}/` | Get specific borrow record | Admin/Owner |
| PUT | `/api/members/{member_id}/borrow-records/{id}/` | Update borrow record | Admin |
| PATCH | `/api/members/{member_id}/borrow-records/{id}/` | Partial update | Admin |
| DELETE | `/api/members/{member_id}/borrow-records/{id}/` | Delete record | Admin |

**Query Parameters (for all borrow record endpoints):**
- `?status={Active|Returned|Overdue}` - Filter by status
- `?member_id={uuid}` - Filter by member
- `?book_id={uuid}` - Filter by book
- `?due_date_min={date}` - Filter by minimum due date
- `?due_date_max={date}` - Filter by maximum due date
- `?page={number}` - Pagination
- `?page_size={number}` - Items per page

---

### Total Endpoint Count

- **Authors**: 6 endpoints (CRUD operations)
- **Categories**: 6 endpoints (CRUD operations)
- **Books**: 6 endpoints (CRUD operations)
- **Members**: 6 endpoints (CRUD operations)
- **Borrow Records (Books nested)**: 6 endpoints
- **Borrow Records (Members nested)**: 6 endpoints

**Total: 36 endpoints**

---

## 4. Request & Response Examples

### 4.1 Author Operations

#### POST `/api/authors/`
**Request:**
```json
{
  "name": "F. Scott Fitzgerald",
  "bio": "American novelist and short story writer, widely regarded as one of the greatest American writers of the 20th century."
}
```

**Response (201 Created):**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "F. Scott Fitzgerald",
  "bio": "American novelist and short story writer, widely regarded as one of the greatest American writers of the 20th century.",
  "created_at": "2025-01-19T15:30:00Z"
}
```

#### GET `/api/authors/?name=fitzgerald`
**Response (200 OK):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "name": "F. Scott Fitzgerald",
      "bio": "American novelist and short story writer...",
      "created_at": "2025-01-19T15:30:00Z"
    }
  ]
}
```

---

### 4.2 Category Operations

#### POST `/api/categories/`
**Request:**
```json
{
  "name": "Fiction",
  "description": "Literary fiction and novels"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Fiction",
  "description": "Literary fiction and novels",
  "created_at": "2025-01-19T15:35:00Z"
}
```

---

### 4.3 Book Operations

#### POST `/api/books/`
**Request:**
```json
{
  "title": "The Great Gatsby",
  "isbn": "9780743273565",
  "author": ["a1b2c3d4-e5f6-7890-abcd-ef1234567890"],
  "category": 1,
  "total_copies": 5,
  "available_copies": 5
}
```

**Response (201 Created):**
```json
{
  "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "title": "The Great Gatsby",
  "isbn": "9780743273565",
  "author": ["a1b2c3d4-e5f6-7890-abcd-ef1234567890"],
  "category": 1,
  "total_copies": 5,
  "available_copies": 5,
  "created_at": "2025-01-19T15:40:00Z",
  "updated_at": "2025-01-19T15:40:00Z"
}
```

#### GET `/api/books/?title=gatsby`
**Response (200 OK):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "title": "The Great Gatsby",
      "isbn": "9780743273565",
      "author": ["a1b2c3d4-e5f6-7890-abcd-ef1234567890"],
      "category": 1,
      "total_copies": 5,
      "available_copies": 5,
      "created_at": "2025-01-19T15:40:00Z",
      "updated_at": "2025-01-19T15:40:00Z"
    }
  ]
}
```

---

### 4.4 Member Operations

#### POST `/api/members/`
**Request:**
```json
{
  "email": "john.doe@example.com"
}
```

**Response (201 Created):**
```json
{
  "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "email": "john.doe@example.com",
  "created_at": "2025-01-19T15:45:00Z"
}
```

---

### 4.5 Borrow Record Operations

#### POST `/api/members/{member_id}/borrow-records/`
**Request:**
```json
{
  "book": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "member": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "due_date": "2025-02-02"
}
```

**Response (201 Created):**
```json
{
  "id": "d4e5f6a7-b8c9-0123-def1-234567890123",
  "book": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "member": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "borrow_date": "2025-01-19T15:50:00Z",
  "due_date": "2025-02-02",
  "return_date": null,
  "status": "Active"
}
```

#### GET `/api/books/{book_id}/borrow-records/`
**Response (200 OK):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "d4e5f6a7-b8c9-0123-def1-234567890123",
      "book": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "member": "c3d4e5f6-a7b8-9012-cdef-123456789012",
      "borrow_date": "2025-01-19T15:50:00Z",
      "due_date": "2025-02-02",
      "return_date": null,
      "status": "Active"
    },
    {
      "id": "e5f6a7b8-c9d0-1234-ef12-345678901234",
      "book": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "member": "f6a7b8c9-d0e1-2345-f123-456789012345",
      "borrow_date": "2025-01-10T10:00:00Z",
      "due_date": "2025-01-24",
      "return_date": "2025-01-18T14:30:00Z",
      "status": "Returned"
    }
  ]
}
```

#### PATCH `/api/members/{member_id}/borrow-records/{id}/`
**Request (Returning a book):**
```json
{
  "return_date": "2025-01-25T10:00:00Z",
  "status": "Returned"
}
```

**Response (200 OK):**
```json
{
  "id": "d4e5f6a7-b8c9-0123-def1-234567890123",
  "book": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "member": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "borrow_date": "2025-01-19T15:50:00Z",
  "due_date": "2025-02-02",
  "return_date": "2025-01-25T10:00:00Z",
  "status": "Returned"
}
```

---

## 5. Technical Implementation Details

### 5.1 Technology Stack
- **Framework**: Django 6.0.1
- **API Framework**: Django REST Framework
- **Database**: SQLite (development)
- **Filtering**: django-filter
- **Debugging**: Django Debug Toolbar (development only)

### 5.2 Key Features Implemented

**Pagination:**
- Default page size: 10 items
- Customizable via `?page_size=` parameter (max 100)
- Page number via `?page=` parameter

**Filtering:**
- Text search (case-insensitive) for names, titles, emails
- Exact matching for ISBN and IDs
- Date range filtering for due dates
- Status filtering for borrow records

**Query Optimization:**
- `select_related()` for ForeignKey relationships (category in books)
- `prefetch_related()` for ManyToMany relationships (authors in books)
- Reduces database queries significantly

**Data Integrity:**
- UUID primary keys for Author, Book, Member, BorrowRecord
- PROTECT on delete for Book → Category (cannot delete categories with books)
- PROTECT on delete for BorrowRecord → Book (cannot delete borrowed books)
- CASCADE on delete for BorrowRecord → Member (cleanup when member deleted)
- Unique constraints on email and ISBN

**Nested Routes:**
- Automatic filtering in nested routes via `get_queryset()` override
- `/api/books/{id}/borrow-records/` - Shows only records for that book
- `/api/members/{id}/borrow-records/` - Shows only records for that member

### 5.3 Business Logic

**Book Availability:**
- `available_copies` decrements when a book is borrowed
- `available_copies` increments when a book is returned
- Books with `available_copies = 0` cannot be borrowed

**Borrow Status Management:**
- New borrows start with status "Active"
- Status changes to "Returned" when `return_date` is set
- Status should change to "Overdue" when current date > `due_date` (future enhancement)

**Timestamp Automation:**
- `borrow_date` auto-set on creation
- `created_at` auto-set for all models
- `updated_at` auto-updates for Book model

---