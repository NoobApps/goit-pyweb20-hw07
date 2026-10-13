# db_builder_sqla.py
import psycopg2
from typing import List
from faker import Faker
from random import randint

# SQLAlchemy imports
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, select, func, desc
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

# --- Configuration and Setup ---
fake = Faker()


SUBJECTS = ["Math", "Science", "History", "Art", "Music", "Chemistry", "Geography"]
TEACHERS = [fake.name() for _ in range(5)]
STUDENTS = [fake.name() for _ in range(50)]
GROUPS = ["Alpha", "Beta", "Gamma"]

# --- SQLAlchemy Model Definition ---

# Base class for declarative class definitions
class Base(DeclarativeBase):
    pass

class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str] = mapped_column(String(10), unique=True)

    def __repr__(self):
        return f"<Group(name='{self.group_name}')>"

class Teacher(Base):
    __tablename__ = "teachers"
    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_name: Mapped[str] = mapped_column(String(50))

    def __repr__(self):
        return f"<Teacher(name='{self.teacher_name}')>"

class Subject(Base):
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_name: Mapped[str] = mapped_column(String(10))
    # Foreign Key referencing Teacher
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))

    def __repr__(self):
        return f"<Subject(name='{self.subject_name}')>"

class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    # Foreign Key referencing Group
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"))

    def __repr__(self):
        return f"<Student(name='{self.name}')>"

class Mark(Base):
    __tablename__ = "marks"
    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[int] = mapped_column(Integer)
    # Foreign Keys
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    date: Mapped[Date] = mapped_column(Date, default=func.now())

    def __repr__(self):
        return f"<Mark(score={self.score}, student_id={self.student_id})>"


# --- Database Initialization and Insertion Logic ---

def initialize_database(engine) -> None:
    """Creates all tables defined by the Base model."""
    Base.metadata.create_all(engine)
    print("Database initialized and tables created successfully.")

def seed_data(session: Session):
    """Inserts sample data into the database."""
    print("\n--- Seeding Data ---")

    # 1. Insert Teachers
    teachers_to_add = [Teacher(teacher_name=t) for t in TEACHERS]
    session.add_all(teachers_to_add)
    session.commit()
    
    # Helper: Get Teacher IDs
    teacher_ids = [t.id for t in session.scalars(select(Teacher)).all()]
    num_teachers = len(teacher_ids)

    # 2. Insert Groups
    groups_to_add = [Group(group_name=g) for g in GROUPS]
    session.add_all(groups_to_add)
    session.commit()
    
    # Helper: Get Group IDs
    group_ids = [g.id for g in session.scalars(select(Group)).all()]
    num_groups = len(group_ids)

    # 3. Insert Subjects (Requires Teacher IDs)
    subjects_to_add = []
    for subject in SUBJECTS:
        # Randomly assign a teacher ID
        teacher_id = randint(1, num_teachers)
        subjects_to_add.append(Subject(subject_name=subject, teacher_id=teacher_id))
        
    session.add_all(subjects_to_add)
    session.commit()

    # Helper: Get Subject IDs
    subject_ids = [s.id for s in session.scalars(select(Subject)).all()]
    num_subjects = len(subject_ids)

    # 4. Insert Students (Requires Group IDs)
    students_to_add = []
    for student in STUDENTS:
        # Randomly assign a group ID
        group_id = randint(1, num_groups)
        students_to_add.append(Student(name=student, group_id=group_id))

    session.add_all(students_to_add)
    session.commit()

    # Helper: Get Student IDs
    student_ids = [s.id for s in session.scalars(select(Student)).all()]

    # 5. Insert Marks (The most complex insertion)
    print("Inserting marks...")
    for _ in range(20): # Repeat the outer loop 21 times
        for student_id in student_ids:
            # Random scores, subjects, and dates
            score = randint(1, 12)
            subject_id = randint(1, num_subjects)
            
            # Use a random date object instead of relying on the database default
            mark_date = fake.date_this_year()
            
            mark = Mark(score=score, subject_id=subject_id, student_id=student_id, date=mark_date)
            session.add(mark)
    
    session.commit()
    print("Data insertion completed successfully.")


def main():
    """Main function to run the database operations."""
    # 1. Setup Engine (The connection factory)
    # echo=True prints all generated SQL statements
    engine = create_engine("postgresql+psycopg2://postgres:example@localhost/postgres", echo=False) 
    
    # 2. Initialize tables
    initialize_database(engine)

    # 3. Use a Session Context Manager for CRUD operations
    try:
        with Session(engine) as session:
            seed_data(session)
            
            # Optional: Example Query (Demonstrates how to read data)
            print("\n--- Example Query: Fetching all students and their groups ---")
            
            # Join Student and Group tables
            average_score = func.round(func.avg(Mark.score), 3).label("average_score")
            stmt = select(Student.name, average_score).join(Mark,Mark.student_id == Student.id).group_by(Student.id, Student.name).order_by(desc(average_score)).limit(5)
            
            results = session.execute(stmt).all()
            print((results))
            # for student, group in results:
            #     print(f"Student: {student.name:<20} belongs to Group:{group.group_name}")

    except Exception as e:
        print(f"\n[CRITICAL ERROR] An error occurred during database operations: {e}")
    finally:
        print("\n--- Database operations finished ---")
        # Session and Engine automatically clean up when exiting the 'with' block

if __name__ == "__main__":
    main()
