from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DEV_DATABASE_URL') or \
'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
db = SQLAlchemy(app)

# 导入模型类
from app.models import Lesson, Comment

import pandas as pd

df = pd.read_excel('tongshi.xlsx')

# 遍历每一行数据，创建并添加模型对象
with app.app_context():
    for index, row in df.iterrows():
        course = row['课程名称']
        existing_lesson = Lesson.query.filter_by(course=course).first()
        if existing_lesson is None:
            lesson = Lesson(
                course=row['课程名称'],
                kind=row['课程归属'],
                credit=row['学分'],
                teacher=row['教师'],
            )
            db.session.add(lesson)

    # Commit the changes, write the data to the database
    db.session.commit()



# lessons_to_update = Lesson.query.filter(Lesson.kind == '艺术鉴赏类/美育类').all()

# for lesson in lessons_to_update:
# print(lesson.examination)

# db.session.commit()

# import pandas as pd


# def read_excel(file_path):
#     df = pd.read_excel(file_path)
#     data_dict = df.set_index(df.columns[0]).to_dict()[df.columns[1]]
#     return data_dict


# my_dict = read_excel('lessons.xlsx')
# for key in my_dict.keys():
#     lessons = Lesson.query.filter_by(course=key).all()
#     for lesson in lessons:
#         id = lesson.id
#         comment = Comment(body=my_dict[key], lesson_id=id)
#         db.session.add(comment)
#     db.session.commit()
