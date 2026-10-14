from connect_db import session
from models import *
from faker import Faker
from sqlalchemy import select
from random import randint

fake = Faker()


SUBJECTS = ["Math", "Science", "History", "Art", "Music", "Chemistry", "Geography"]
TEACHERS = [fake.name() for _ in range(5)]
STUDENTS = [fake.name() for _ in range(50)]
GROUPS = ["Alpha", "Beta", "Gamma"]

def seed_data(session):
    """Inserts sample data into the database."""
    print("\n--- Seeding Data ---")

    # 1. Insert Teachers
    if not session.scalars(select(Teacher)).first():
        teachers_to_add = [Teacher(teacher_name=t) for t in TEACHERS]
        session.add_all(teachers_to_add)
        session.commit()
    # Helper: Get Teacher IDs
        teacher_ids = [t.id for t in session.scalars(select(Teacher)).all()]
        num_teachers = len(teacher_ids)
    else:
        print("Teachers already exist. Skipping insertion.")

    # 2. Insert Groups
    if not session.scalars(select(Group)).first():
        groups_to_add = [Group(group_name=g) for g in GROUPS]
        session.add_all(groups_to_add)
        session.commit()
    
    # Helper: Get Group IDs
        group_ids = [g.id for g in session.scalars(select(Group)).all()]
        num_groups = len(group_ids)
    else:
        print("Groups already exist. Skipping insertion.")

    # 3. Insert Subjects (Requires Teacher IDs)
    if not session.scalars(select(Subject)).first():
        subjects_to_add = []
        for subject in SUBJECTS:
        # Randomly assign a teacher ID
            teacher_id = randint(1, num_teachers)
            subjects_to_add.append(Subject(subject_name=subject, teacher_id=teacher_id))
        
        session.add_all(subjects_to_add)
        session.commit()
    else:
        print("Subjects already exist. Skipping insertion.")

    # Helper: Get Subject IDs
    subject_ids = [s.id for s in session.scalars(select(Subject)).all()]
    num_subjects = len(subject_ids)

    # 4. Insert Students (Requires Group IDs)
    if not session.scalars(select(Student)).first():
        students_to_add = []
        for student in STUDENTS:
        # Randomly assign a group ID
            group_id = randint(1, num_groups)
            students_to_add.append(Student(name=student, group_id=group_id))

        session.add_all(students_to_add)
        session.commit()
    else:
        print("Students already exist. Skipping insertion.")

    # Helper: Get Student IDs
    student_ids = [s.id for s in session.scalars(select(Student)).all()]

    # 5. Insert Marks (The most complex insertion)
    print("Inserting marks...")
    if not session.scalars(select(Mark)).first():
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
    else:
        print("Marks already exist. Skipping insertion.")

if __name__ == '__main__':
    try:
        with session:
            seed_data(session)
    except Exception as e:
        print(f"\n[CRITICAL ERROR] An error occurred during database operations: {e}")
    finally:
        print("\n--- Database operations finished ---")
        print("Data insertion completed successfully.")