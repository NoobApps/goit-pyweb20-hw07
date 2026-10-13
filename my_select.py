from connect_db import session
from models import *
from sqlalchemy import select, and_, desc, func
from sqlalchemy.exc import SQLAlchemyError

def select_1(session):
    """
    Executes the SQL query to find the top 5 students based on their average score.
    """
    try:
        average_score = func.round(func.avg(Mark.score), 3).label("average_score")
        stmt = (
            select(
                Student.name,           
                average_score           
            )
            .join(Mark, Mark.student_id == Student.id)
            .group_by(Student.id)
            .order_by(desc(average_score))
            .limit(5)
        )
        results = session.execute(stmt).all()
        return results

    except SQLAlchemyError as e:
        print(f"Database error occurred during select_1: {e}")
        return []

def select_2(session):
    """
    Executes the query to find the top student (by average score) 
    for a specific subject (ID=1).
    """
    try:
        average_mark = func.round(func.avg(Mark.score), 2).label("mark")
        stmt = (
            select(
                Subject.subject_name, 
                Student.name, 
                average_mark
            )
            .join(Student, Mark.student_id == Student.id)
            .join(Subject, Mark.subject_id == Subject.id)
            .where(Subject.id == 1)
            .group_by(Student.name, Subject.subject_name)
             .order_by(desc(average_mark))
            .limit(1)
        )
        
        results = session.execute(stmt).all()
        return results

    except SQLAlchemyError as e:
        print(f"Database error occurred during select_2: {e}")
        return []

def select_3(session):
    """
    Executes the query to calculate the average score per group 
    for a specific subject (ID=1).
    """
    try:
        average_mark = func.round(func.avg(Mark.score), 1).label("AverageMark")
        stmt = (
            select(
                Subject.subject_name, 
                Group.group_name, 
                average_mark
            )
            .join(Student, Group.id == Student.group_id)
            .join(Mark, Student.id == Mark.student_id)
            .join(Subject, Mark.subject_id == Subject.id)
            .where(Subject.id == 1)
            .group_by(Group.group_name, Subject.subject_name)
        )
        results = session.execute(stmt).all()
        return results

    except SQLAlchemyError as e:
        print(f"Database error occurred during select_3: {e}")
        return []

def select_4(session):
    """
    Executes the query to calculate the overall average score across all records in the marks table, 
    rounded to 3 decimal places.
    """
    try:
        average_score = func.round(func.avg(Mark.score), 3).label("AverageScore")
        stmt = select(average_score)
        results = session.execute(stmt).all()
        return results
        
    except SQLAlchemyError as e:
        print(f"Database error occurred during select_4: {e}")
        return []

def select_5(session) :
    """
    Executes the query to list all subject names and the corresponding 
    teacher name for a specific teacher ID (teacher_id = 1).
    """
    try:
        stmt = (
            select(
                Subject.subject_name, 
                Teacher.teacher_name
            )
            .join(Teacher, Subject.teacher_id == Teacher.id)
            .where(Teacher.id == 1)
        )
        
        results = session.execute(stmt).all()
        return results

    except SQLAlchemyError as e:
        print(f"Database error occurred during select_5: {e}")
        return []

def select_6(session):
    """
    Executes the query to list all students belonging to a specific group (Group ID 1),
    ordered by their name
    """
    try:
        stmt = (
            select(
                Student.name, 
                Group.group_name
            )
            .join(Group, Student.group_id == Group.id)
            .where(Group.id == 1)
            .order_by(Student.name.asc())
        )
        
        results = session.execute(stmt).all()
        return results

    except SQLAlchemyError as e:
        print(f"Database error occurred during select_6: {e}")
        return []

def select_7(session):
    """
    Executes the query to retrieve the subject name, group name, student name, 
    and score for all marks that fall within a specific group (Group ID 1) 
    and a specific subject (Subject ID 1). Results are ordered by score descending
    """
    try:
        stmt = (
            select(
                Subject.subject_name, 
                Group.group_name, 
                Student.name, 
                Mark.score
            )
            .join(Student, Group.id == Student.group_id)
            .join(Mark, Student.id == Mark.student_id)
            .join(Subject, Mark.subject_id == Subject.id)
            .where(Group.id == 1)
            .where(Subject.id == 1)
            .order_by(Mark.score.desc())
        )
        
        results = session.execute(stmt).all()
        return results

    except SQLAlchemyError as e:
        print(f"Database error occurred during select_7: {e}")
        return []

def select_8(session):
    """
    Executes the query to calculate the average score per teacher, 
    filtered only for Teacher ID 4, rounded to 2 decimal places
    """
    try:
        average_score = func.round(func.avg(Mark.score), 2).label("averageScore")
        stmt = (
            select(
                Teacher.teacher_name, 
                average_score
            )
            .join(Subject, Mark.subject_id == Subject.id)
            .join(Teacher, Subject.teacher_id == Teacher.id)
            .where(Teacher.id == 4)
            .group_by(Teacher.teacher_name)
        )
        
        results = session.execute(stmt).all()
        return results

    except SQLAlchemyError as e:
        print(f"Database error occurred during select_8: {e}")
        return []

def select_9(session):
    """
    Executes the query to find the name and subject name for all subjects 
    a specific student (ID 1) is enrolled in
    """
    try:
        stmt = (
            select(
                Student.name, 
                Subject.subject_name
            )
            .join(Mark, Student.id == Mark.student_id)
            .join(Subject, Mark.subject_id == Subject.id)
            .where(Student.id == 1)
            .group_by(Subject.id, Student.name)
            .order_by(Subject.subject_name.asc())
        )
        
        results = session.execute(stmt).all()
        return results

    except SQLAlchemyError as e:
        print(f"Database error occurred during select_9: {e}")
        return []

def select_10(session):
    """
    Executes the query to list the subject name, student name, and teacher name 
    for a specific student (ID 1) taught by a specific teacher (ID 4)
    """
    try:
        stmt = (
            select(
                Teacher.teacher_name, 
                Student.name.label("student_name"),
                Subject.subject_name
            )
            .join(Subject, Teacher.id == Subject.teacher_id)
            .join(Mark, Subject.id == Mark.subject_id)
            .join(Student, Mark.student_id == Student.id)
            .where(Teacher.id == 4)
            .where(Student.id == 1)
            .group_by(Teacher.id, Student.id, Subject.id)
            .order_by(Subject.subject_name.asc())
        )
        
        results = session.execute(stmt).all()
        return results

    except SQLAlchemyError as e:
        print(f"Database error occurred during select_10: {e}")
        return []


if __name__ == '__main__':
    print(select_1(session))
    # print(select_2(session))
    # print(select_3(session))
    # print(select_4(session))
    # print(select_5(session))
    # print(select_6(session))
    # print(select_7(session))
    # print(select_8(session))
    # print(select_9(session))
    # print(select_10(session))