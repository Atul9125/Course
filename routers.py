from email.mime import text
from unittest import result
from database import engine, get_db
from models import Course
from utils import read_data, save_data, get_next_id
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session


routers= APIRouter()


# ==============================
# Pydantic Model
# ==============================
class Product(BaseModel):
    id: Optional[int] = None
    title: str
    instructor: str
    category: str
    price: float
    duration_hours: int
    is_published: bool
    discount_percent: float
    


# ==============================
# Basic Route
# ==============================
@routers.get('/data',tags=["Data"])
def get_all_data(db:Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM courses"))
    return result.mappings().all()
    

# ==============================
# GET All Courses
# ==============================
@routers.get('/courses')
def show_courses():
    return read_data()

            
# ==============================  # GET Course by ID=========
@routers.get('/courses/{id}', tags=["Data"])
def get_course_by_id(id: int, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT * FROM courses WHERE id = :id"),
        {"id": id}
    )

    course = result.mappings().first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    return course  #Where will get record of specified id, if id not found then it will return None


# ==============================
# POST - Add Course
# ==============================



@routers.post("/courses")
def add_course(course: Course, db: Session = Depends(get_db)):
    data=course.dict(exclude={'id','price_category'})

    #Qurery  for creating new record in database
    result = db.execute(text("""
        INSERT INTO courses (title, instructor, category, price, duration_hours, is_published, discount_percent)
        VALUES (:title, :instructor, :category, :price, :duration_hours, :is_published, :discount_percent)
    """),data)
    db.commit()
    return {"message": "Course added successfully"}


# ==============================
# PUT - Update Course
# ==============================
@routers.put('/update/{item_id}', tags=['update'])
def update_data(item_id: int, course: Course, db: Session = Depends(get_db)):
    
    # 1. Check if course exists
    existing_course = db.execute(
        text("SELECT * FROM courses WHERE id = :id"),
        {"id": item_id}
    ).first()

    if not existing_course:
        raise HTTPException(status_code=404, detail="Course not found")

    # 2. Prepare data
    data = course.dict()
    data['id'] = item_id   # required for WHERE clause

    # 3. Update query
    db.execute(text("""
        UPDATE courses
        SET 
            title = :title,
            instructor = :instructor, 
            category = :category, 
            price = :price, 
            duration_hours = :duration_hours, 
            is_published = :is_published, 
            discount_percent = :discount_percent
        WHERE id = :id
    """), data)

    db.commit()

    return {"message": "Course updated successfully"}


# ==============================
# DELETE - Remove Course
# ==============================
@routers.delete('/remove_courses/{item_id}', tags=['Delete'])
def remove_courses(item_id: int, db: Session = Depends(get_db)):

    # 1. Check if course exists
    existing_course = db.execute(
        text("SELECT * FROM courses WHERE id = :id"),
        {"id": item_id}
    ).first()

    if not existing_course:
        raise HTTPException(status_code=404, detail="Course not found")

    # 2. Delete query
    db.execute(
        text("DELETE FROM courses WHERE id = :id"),
        {"id": item_id}
    )
    db.commit()

    return {"message": "Course removed successfully"}


# ==============================
# FILTER Courses
# ==============================
@routers.get('/courses/filter/search')
def filter_courses(
    category: Optional[str] =Query (None,description="Filter by Category"),
    instructor: Optional[str] =Query (None,description="Filter by instructor"),
    is_published: Optional[str] =Query (None,description="Filter by Published status"),
    min_price: Optional[float] =Query (None,description="Minimum Price"),
    max_price: Optional[float] =Query (None,description="Maximum Price"),
    min_duration: Optional[float] =Query (None,description="Minimum Duration in hours"),
    max_duration: Optional[float] =Query (None,description="Maximum Duration in hours"),
    db: Session = Depends(get_db)
):
    query="SELECT * FROM courses WHERE 1=1" #No-op condition to simplify appending filters
    if category:
        query += " AND category = :category"
        params={"category": category}
    if instructor:
        query += " AND instructor = :instructor"
        params={"instructor": instructor}
    if is_published is not None:
        query += " AND is_published = :is_published"
        params={"is_published": is_published.lower() == 'true'}
    if min_price is not None:
        query += " AND price >= :min_price"
        params={"min_price": min_price}
    if max_price is not None:
        query += " AND price <= :max_price"
        params={"max_price": max_price}
    if min_duration is not None:
        query += " AND duration_hours >= :min_duration"
        params={"min_duration": min_duration}
    if max_duration is not None:
        query += " AND duration_hours <= :max_duration"
        params={"max_duration": max_duration}
    return db.execute(text(query), params).mappings().all()

# ==============================
# PAGINATION
# ==============================


@routers.get("/courses_paginated")
def get_paginated_courses(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit

    # Get paginated data
    data = db.execute(
        text("SELECT * FROM courses LIMIT :limit OFFSET :offset"),
        {"limit": limit, "offset": offset}
    ).mappings().all()

    # Get total count
    # data = db.execute(text("SELECT * FROM courses LIMIT :limit OFFSET :offset" ), {'limit': limit, 'offset': offset}).mappings().all()

    return {
        "total": len(data),
        "page": page,
        "limit": limit,
        "offset": offset,
        "data": data
    }





# from utils import read_data, save_data
# from fastapi import APIRouter, HTTPException, Query
# from typing import Optional
# from pydantic import BaseModel

# routers = APIRouter()


# # ==============================
# # Pydantic Model
# # ==============================
# class Product(BaseModel):
#     id: Optional[int] = None
#     title: str
#     instructor: str
#     price: float
#     duration_hours: int
#     is_published: bool
#     discount_percent: float


# # ==============================
# # Basic Route
# # ==============================
# @routers.get('/basic-routes')
# def show():
#     return {'message': "Welcome to FastAPI"}


# # ==============================
# # GET All Courses
# # ==============================
# @routers.get('/courses')
# def show_courses():
#     return read_data()


# # ==============================
# # GET Course by ID
# # ==============================
# @routers.get('/courses/{courses_id}')
# def show_course_by_id(courses_id: int):

#     data = read_data()

#     for course in data:
#         if int(course['id']) == courses_id:
#             return course

#     raise HTTPException(
#         status_code=404,
#         detail=f"Course with ID {courses_id} not found"
#     )


# # ==============================
# # POST - Add Course
# # ==============================
# @routers.post('/courses', status_code=201)
# def add_data(course: Product):

#     data = read_data()

#     # Auto ID generation
#     if data:
#         new_id = max(item['id'] for item in data) + 1
#     else:
#         new_id = 1

#     course_dict = course.dict()
#     course_dict['id'] = new_id

#     data.append(course_dict)

#     save_data(data)

#     return {
#         'message': "Course added successfully",
#         'course_id': new_id
#     }


# # ==============================
# # PUT - Update Course
# # ==============================
# @routers.put('/courses/{courses_id}')
# def update_data(courses_id: int, update_course: Product):

#     data = read_data()

#     for index, course in enumerate(data):
#         if course['id'] == courses_id:

#             updated_dict = update_course.dict()
#             updated_dict['id'] = courses_id

#             data[index] = updated_dict

#             save_data(data)

#             return {
#                 'message': 'Course updated successfully'
#             }

#     raise HTTPException(
#         status_code=404,
#         detail="Course not found"
#     )


# # ==============================
# # DELETE - Remove Course
# # ==============================
# @routers.delete('/courses/{courses_id}')
# def remove_courses(courses_id: int):

#     data = read_data()

#     for index, course in enumerate(data):
#         if course.get('id') == courses_id:

#             data.pop(index)

#             save_data(data)

#             return {
#                 'message': "Course removed successfully"
#             }

#     raise HTTPException(
#         status_code=404,
#         detail="Course not found"
#     )


# # ==============================
# # FILTER Courses
# # ==============================
# @routers.get('/courses/filter/search')
# def filter_courses(
#     max_price: Optional[float] = Query(None, description='Maximum Price'),
#     is_published: bool = Query(False, description='Show only published courses')
# ):

#     data = read_data()

#     if max_price is not None:
#         data = [
#             course for course in data
#             if course['price'] <= max_price
#         ]

#     if is_published:
#         data = [
#             course for course in data
#             if course.get('is_published')
#         ]

#     return {
#         'total': len(data),
#         'courses': data
#     }


# # ==============================
# # PAGINATION
# # ==============================
# @routers.get('/courses/paginated')
# def get_paginated_courses(
#     page: int = Query(1, ge=1, description="Page number — starts from 1"),
#     page_size: int = Query(5, ge=1, le=50, description="Courses per page")
# ):

#     data = read_data()

#     total_courses = len(data)

#     # Calculate start and end index
#     start = (page - 1) * page_size
#     end = start + page_size

#     paginated_data = data[start:end]

#     # Calculate total pages (ceiling division)
#     total_pages = -(-total_courses // page_size)

#     # If page does not exist
#     if page > total_pages and total_courses > 0:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Page {page} does not exist. Total pages: {total_pages}"
#         )

#     return {
#         'page': page,
#         'page_size': page_size,
#         'total_pages': total_pages,
#         'total_courses': total_courses,
#         'has_next': page < total_pages,
#         'has_previous': page > 1,
#         'courses': paginated_data
#     }
