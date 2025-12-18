"""
Write tests for classes in module_2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""

import pytest
import datetime
from module_2_python_part_2.task_classes import Homework
from module_2_python_part_2.task_classes import Teacher
from module_2_python_part_2.task_classes import Student

@pytest.mark.homework_creation
def test_homework_creation():
    hw = Homework("test", 3)
    assert hw.text == "test"
    assert isinstance(hw.created, datetime.datetime)
    assert isinstance(hw.deadline, datetime.datetime)


@pytest.mark.is_active
def test_is_active():
    hw = Homework("test", 1)
    assert hw.is_active() == True


@pytest.mark.is_not_active
def test_is_not_active():
    hw = Homework("test", -1)
    assert hw.is_active() == False


@pytest.mark.student_creation
def test_teacher_creation():
    student = Student('Vladislav', 'Popov')
    assert student.first_name == "Vladislav"
    assert student.last_name == "Popov"


@pytest.mark.do_homework_active
def test_do_homework_active():
    student = Student('Vladislav', 'Popov')
    hw = Homework("test", 1)
    assert student.do_homework(hw) == hw


@pytest.mark.do_homework_not_active
def test_do_homework_not_active():
    student = Student('Vladislav', 'Popov')
    hw = Homework("test", -1)
    assert student.do_homework(hw) is None


@pytest.mark.teacher_creation
def test_teacher_creation():
    teacher = Teacher('Dmitry', 'Orlyakov')
    assert teacher.first_name == "Dmitry"
    assert teacher.last_name == "Orlyakov"


@pytest.mark.create_homework_active
def test_create_homework_active():
    teacher = Teacher('Dmitry', 'Orlyakov')
    hw = teacher.create_homework('Learn functions', 1)
    assert isinstance(hw.created, datetime.datetime)
    assert isinstance(hw.deadline, datetime.datetime)
    assert hw.text == 'Learn functions'


@pytest.mark.create_homework_not_active
def test_create_homework_not_active():
    teacher = Teacher('Dmitry', 'Orlyakov')
    hw = teacher.create_homework('Learn functions', -1)
    assert isinstance(hw.created, datetime.datetime)
    assert isinstance(hw.deadline, datetime.datetime)
    assert hw.text == 'Learn functions'