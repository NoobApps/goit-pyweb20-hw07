from sqlalchemy import  Integer, String, ForeignKey, Date, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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