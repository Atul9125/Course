#We will all the columns of the table and we will also assign name of the table
from sqlalchemy import Column, Integer, String

class Course:
    __tablename__ = "courses" #Table name

    id               =Column(primary_key=True)
    title            =Column(nullable=False)
    instructor       =Column(nullable=False),
    category         =Column(nullable=False),
    price            =Column(nullable=False),
    duration_hours   =Column(nullable=False),
    is_published     =Column(nullable=False),
    discount_percent =Column(nullable=False)