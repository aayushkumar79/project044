from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import engine, Base, SessionLocal
from models import Student, Skill, Opportunity, Assessment, Application

app = FastAPI(title="SkillFill API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

Base.metadata.create_all(bind=engine)

class StudentRegister(BaseModel):
    name: str
    email: str
    password: str
    course: str
    college: str
    career_interest: str = ""

class StudentLogin(BaseModel):
    email: str
    password: str

class StudentProfile(BaseModel):
    name: str
    course: str
    college: str
    career_interest: str = ""

class SkillCreate(BaseModel):
    student_id: int
    skill_name: str
    skill_level: int

class OpportunityCreate(BaseModel):
    title: str
    company: str
    description: str
    location: str
    opportunity_type: str
    required_skills: str
    minimum_skill_level: int

class AssessmentCreate(BaseModel):
    student_id: int
    skill_name: str
    score: int

class ApplicationCreate(BaseModel):
    student_id: int
    opportunity_id: int

class ApplicationStatus(BaseModel):
    status: str

@app.get("/")
def home():
    return {"message": "SkillFill Backend is Running"}

@app.post("/register")
def register(student: StudentRegister):
    db = SessionLocal()
    existing_student = db.query(Student).filter(
        Student.email == student.email
    ).first()
    if existing_student:
        db.close()
        return {"message": "Email already registered"}
    new_student = Student(
        name=student.name,
        email=student.email,
        password=student.password,
        course=student.course,
        college=student.college,
        career_interest=student.career_interest
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    student_id = new_student.id
    db.close()
    return {
        "message": "Student registered successfully",
        "student_id": student_id
    }

@app.post("/login")
def login(student: StudentLogin):
    db = SessionLocal()
    existing_student = db.query(Student).filter(
        Student.email == student.email,
        Student.password == student.password
    ).first()
    if existing_student:
        result = {
            "message": "Login successful",
            "student_id": existing_student.id,
            "name": existing_student.name,
            "email": existing_student.email
        }
        db.close()
        return result
    db.close()
    return {"message": "Invalid email or password"}

@app.get("/student/{student_id}")
def get_student_profile(student_id: int):
    db = SessionLocal()
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()
    if not student:
        db.close()
        return {"message": "Student not found"}
    result = {
        "student_id": student.id,
        "name": student.name,
        "email": student.email,
        "course": student.course,
        "college": student.college,
        "career_interest": student.career_interest or ""
    }
    db.close()
    return result


@app.put("/student/{student_id}")
def update_student_profile(student_id: int, profile: StudentProfile):
    db = SessionLocal()
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()
    if not student:
        db.close()
        return {"message": "Student not found"}
    student.name = profile.name
    student.course = profile.course
    student.college = profile.college
    student.career_interest = profile.career_interest
    db.commit()
    db.close()
    return {"message": "Profile updated successfully"}

@app.post("/skills")
def add_skill(skill: SkillCreate):
    db = SessionLocal()
    student = db.query(Student).filter(
        Student.id == skill.student_id
    ).first()
    if not student:
        db.close()
        return {"message": "Student not found"}
    if skill.skill_level < 1 or skill.skill_level > 5:
        db.close()
        return {"message": "Skill level must be between 1 and 5"}

    existing_skill = db.query(Skill).filter(
        Skill.student_id == skill.student_id,
        Skill.skill_name == skill.skill_name
    ).first()
    if existing_skill:
        existing_skill.skill_level = skill.skill_level
        db.commit()
        skill_id = existing_skill.id
        db.close()
        return {
            "message": "Skill updated successfully",
            "skill_id": skill_id
        }
    new_skill = Skill(
        student_id=skill.student_id,
        skill_name=skill.skill_name,
        skill_level=skill.skill_level
    )
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    skill_id = new_skill.id
    db.close()
    return {
        "message": "Skill added successfully",
        "skill_id": skill_id
    }

@app.get("/skills/{student_id}")
def get_student_skills(student_id: int):
    db = SessionLocal()
    skills = db.query(Skill).filter(
        Skill.student_id == student_id
    ).all()
    result = []
    for skill in skills:
        result.append({
            "skill_id": skill.id,
            "skill_name": skill.skill_name,
            "skill_level": skill.skill_level
        })
    db.close()
    return {
        "student_id": student_id,
        "skills": result
    }

@app.post("/assessment")
def submit_assessment(assessment: AssessmentCreate):
    db = SessionLocal()
    student = db.query(Student).filter(
        Student.id == assessment.student_id
    ).first()
    if not student:
        db.close()
        return {"message": "Student not found"}
    if assessment.score < 0 or assessment.score > 100:
        db.close()
        return {"message": "Score must be between 0 and 100"}
    new_assessment = Assessment(
        student_id=assessment.student_id,
        skill_name=assessment.skill_name,
        score=assessment.score
    )
    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)

    assessment_id = new_assessment.id
    db.close()
    return {
        "message": "Assessment submitted successfully",
        "assessment_id": assessment_id
    }

@app.get("/assessment/{student_id}")
def get_assessment(student_id: int):
    db = SessionLocal()
    assessments = db.query(Assessment).filter(
        Assessment.student_id == student_id
    ).all()
    result = []
    for assessment in assessments:
        result.append({
            "assessment_id": assessment.id,
            "skill_name": assessment.skill_name,
            "score": assessment.score
        })
    db.close()

    return {
        "student_id": student_id,
        "assessments": result
    }

@app.post("/opportunities")
def create_opportunity(opportunity: OpportunityCreate):
    db = SessionLocal()
    new_opportunity = Opportunity(
        title=opportunity.title,
        company=opportunity.company,
        description=opportunity.description,
        location=opportunity.location,
        opportunity_type=opportunity.opportunity_type,
        required_skills=opportunity.required_skills,
        minimum_skill_level=opportunity.minimum_skill_level
    )
    db.add(new_opportunity)
    db.commit()
    db.refresh(new_opportunity)
    opportunity_id = new_opportunity.id
    db.close()

    return {
        "message": "Opportunity created successfully",
        "opportunity_id": opportunity_id
    }

@app.get("/opportunities")
def get_opportunities():
    db = SessionLocal()
    opportunities = db.query(Opportunity).all()
    result = []

    for opportunity in opportunities:
        result.append({
            "opportunity_id": opportunity.id,
            "title": opportunity.title,
            "company": opportunity.company,
            "description": opportunity.description,
            "location": opportunity.location,
            "opportunity_type": opportunity.opportunity_type,
            "required_skills": opportunity.required_skills,
            "minimum_skill_level": opportunity.minimum_skill_level
        })
    db.close()
    return result


@app.get("/opportunities/{opportunity_id}")
def get_opportunity(opportunity_id: int):
    db = SessionLocal()
    opportunity = db.query(Opportunity).filter(
        Opportunity.id == opportunity_id
    ).first()
    if not opportunity:
        db.close()
        return {"message": "Opportunity not found"}
    result = {
        "opportunity_id": opportunity.id,
        "title": opportunity.title,
        "company": opportunity.company,
        "description": opportunity.description,
        "location": opportunity.location,
        "opportunity_type": opportunity.opportunity_type,
        "required_skills": opportunity.required_skills,
        "minimum_skill_level": opportunity.minimum_skill_level
    }

    db.close()
    return result

@app.get("/skill-gaps/{student_id}")
def get_skill_gaps(student_id: int):
    db = SessionLocal()
    student_skills = db.query(Skill).filter(
        Skill.student_id == student_id
    ).all()

    opportunities = db.query(Opportunity).all()
    gaps = {}
    for opportunity in opportunities:
        required_skills = opportunity.required_skills.split(",")
        for required_skill in required_skills:
            required_skill = required_skill.strip()
            found = False
            for student_skill in student_skills:
                if student_skill.skill_name.lower() == required_skill.lower():
                    found = True
                    if student_skill.skill_level < opportunity.minimum_skill_level:
                        gaps[required_skill] = {
                            "skill": required_skill,
                            "current_level": student_skill.skill_level,
                            "required_level": opportunity.minimum_skill_level
                        }
                    break
            if not found:
                gaps[required_skill] = {
                    "skill": required_skill,
                    "current_level": 0,
                    "required_level": opportunity.minimum_skill_level
                }

    db.close()
    return {
        "student_id": student_id,
        "skill_gaps": list(gaps.values())
    }

@app.get("/recommendations/{student_id}")
def get_recommendations(student_id: int):
    db = SessionLocal()
    student_skills = db.query(Skill).filter(
        Skill.student_id == student_id
    ).all()
    opportunities = db.query(Opportunity).all()
    recommendations = []
    for opportunity in opportunities:
        required_skills = [
            skill.strip()
            for skill in opportunity.required_skills.split(",")
            if skill.strip()
        ]
        matched_skills = []
        for required_skill in required_skills:
            for student_skill in student_skills:
                if student_skill.skill_name.lower() == required_skill.lower():
                    if student_skill.skill_level >= opportunity.minimum_skill_level:
                        matched_skills.append(student_skill.skill_name)
                    break
        if required_skills:
            match_score = (
                len(matched_skills) / len(required_skills)
            ) * 100
        else:
            match_score = 0
        recommendations.append({
            "opportunity_id": opportunity.id,
            "title": opportunity.title,
            "company": opportunity.company,
            "location": opportunity.location,
            "opportunity_type": opportunity.opportunity_type,
            "match_score": round(match_score, 2),
            "matched_skills": matched_skills
        })
    recommendations.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )
    db.close()
    return {
        "student_id": student_id,
        "recommendations": recommendations
    }

@app.post("/applications")
def apply_for_opportunity(application: ApplicationCreate):
    db = SessionLocal()
    student = db.query(Student).filter(
        Student.id == application.student_id
    ).first()
    if not student:
        db.close()
        return {"message": "Student not found"}
    opportunity = db.query(Opportunity).filter(
        Opportunity.id == application.opportunity_id
    ).first()
    if not opportunity:
        db.close()
        return {"message": "Opportunity not found"}

    existing_application = db.query(Application).filter(
        Application.student_id == application.student_id,
        Application.opportunity_id == application.opportunity_id
    ).first()
    if existing_application:
        db.close()
        return {"message": "Already applied"}

    new_application = Application(
        student_id=application.student_id,
        opportunity_id=application.opportunity_id,
        status="Applied"
    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    application_id = new_application.id
    db.close()
    return {
        "message": "Application submitted successfully",
        "application_id": application_id
    }

@app.get("/applications/{student_id}")
def get_student_applications(student_id: int):
    db = SessionLocal()
    applications = db.query(Application).filter(
        Application.student_id == student_id
    ).all()

    result = []
    for application in applications:
        opportunity = db.query(Opportunity).filter(
            Opportunity.id == application.opportunity_id
        ).first()

        if opportunity:
            result.append({
                "application_id": application.id,
                "opportunity_id": opportunity.id,
                "title": opportunity.title,
                "company": opportunity.company,
                "status": application.status
            })
    db.close()
    return {
        "student_id": student_id,
        "applications": result
    }

@app.put("/applications/{application_id}")
def update_application_status(application_id: int,status: ApplicationStatus):
    db = SessionLocal()
    application = db.query(Application).filter(
        Application.id == application_id
    ).first()
    if not application:
        db.close()
        return {"message": "Application not found"}
    application.status = status.status
    db.commit()
    db.close()

    return {
        "message": "Application status updated successfully"
    }
