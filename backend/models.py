from sqlalchemy import Column, Integer, String, Text
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(100))
    course = Column(String(100))
    college = Column(String(150))
    career_interest = Column(String(150))

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer)
    skill_name = Column(String(100))
    skill_level = Column(Integer)

class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150))
    company = Column(String(150))
    description = Column(Text)
    location = Column(String(100))
    opportunity_type = Column(String(50))
    required_skills = Column(Text)
    minimum_skill_level = Column(Integer)

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer)
    skill_name = Column(String(100))
    score = Column(Integer)

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer)
    opportunity_id = Column(Integer)
    status = Column(String(50))
