from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import Optional


# data validator
class Course(BaseModel):
    id: Optional[int] = None
    title: str   = Field(min_length  = 2,max_length  = 100,description = "Course ka title")
    instructor: str   = Field(min_length  = 2,max_length  = 50,description = "Instructor ka naam")
    
    category: str = Field(min_length  = 2,max_length  = 30,description = "Course ki category — jaise Python, Web Dev") 
    price           : float = Field(gt=0, le=1_00_000, description="Course ki price")   # FIX 3: le=1_00_000 add kiya
    
    duration_hours  : float = Field(gt= 0, le= 500, description = "Course ki duration ghanton mein")
    
    discount_percent: float = Field(ge=0, le=100, default=0.0)    
    is_published: bool  = Field(default     = False,description = "Course published hai ya nahi")





# field validators
@field_validator('title')
@classmethod
def clean_title(cls, value: str) -> str:
    return value.title()

@field_validator('instructor')
@classmethod
def clean_instructor(cls, value: str) -> str:
        
    return value.title()    #First letter captile(camel Case)
 
@field_validator('category')
@classmethod
def clean_category(cls, value: str) -> str:
       
    return value.lower()      # "WEB DEV" → "web dev"





# ── Model Validator ──────────────────────────────────────
# Saare fields validate hone KE BAAD chalta hai
 
@model_validator(mode='after')
def check_published_and_price(self):
    # Agar course published hai toh discount 100% nahi ho sakta
    if self.is_published and self.discount_percent == 100:
        raise ValueError('Published course ka discount 100% nahi ho sakta — free nahi de sakte')
    return self
 
 
# ── Computed Fields ──────────────────────────────────────
# Ye fields user nahi bhejta — automatically calculate hoti hain
 
@computed_field
@property
def discounted_price(self) -> float:
    # Discount lagane ke baad actual price
    return round(self.price - (self.price * self.discount_percent / 100), 2)
 
@computed_field
@property
def price_category(self) -> str:
    if self.price < 500:
        return 'Free / Budget'      # 0 - 499
    elif self.price < 5000:
        return 'Mid-Range'          # 500 - 4999
    else:
        return 'Premium'            # 5000+