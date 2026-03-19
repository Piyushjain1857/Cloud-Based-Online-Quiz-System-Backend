from app import app
from core.models import db, User, Quiz, Question, Option, Notification, UserSetting
from core.data import users, notifications as mock_notifications, upcoming_quizzes, full_quizzes, user_settings

def seed_database():
    with app.app_context():
        # Re-create tables to reflect schema changes
        db.drop_all()
        db.create_all()

        # Seed Users
        for user_data in users:
            user = User.query.filter_by(email=user_data['email']).first()
            if not user:
                user = User(
                    name=user_data['name'],
                    email=user_data['email'],
                    password=user_data['password'],
                    role=user_data.get('role', 'user'),
                    profile_image=user_data.get('profileImage')
                )
                db.session.add(user)
                db.session.commit() # Commit to get ID for settings

            # Seed User Settings if they don't exist
            if not UserSetting.query.filter_by(user_id=user.id).first():
                settings = UserSetting(
                    user_id=user.id,
                    email_notifications=user_settings['notifications']['email'],
                    push_notifications=user_settings['notifications']['push'],
                    quiz_reminders=user_settings['notifications']['quizReminders'],
                    theme=user_settings['preferences']['theme'],
                    language=user_settings['preferences']['language']
                )
                db.session.add(settings)

        # Seed Quizzes and Questions
        for quiz_data in full_quizzes:
            if not Quiz.query.filter_by(title=quiz_data['title']).first():
                # Try to get extra info from upcoming_quizzes
                meta = next((q for q in upcoming_quizzes if q['id'] == quiz_data['id']), {})
                
                quiz = Quiz(
                    title=quiz_data['title'],
                    subject=quiz_data['subject'],
                    date=quiz_data.get('date') or meta.get('date') or '2026-03-30',
                    time=quiz_data.get('time') or meta.get('time') or '10:00 AM',
                    duration=quiz_data.get('duration') or meta.get('duration') or '30 Mins',
                    points=quiz_data.get('points', 100),
                    status='upcoming',
                    participants=0
                )
                db.session.add(quiz)
                db.session.flush() # Get quiz ID

                for q_data in quiz_data['questions']:
                    question = Question(
                        quiz_id=quiz.id,
                        text=q_data['text'],
                        correct_answer=q_data['correctAnswer']
                    )
                    db.session.add(question)
                    db.session.flush() # Get question ID

                    for opt_text in q_data['options']:
                        option = Option(
                            question_id=question.id,
                            text=opt_text
                        )
                        db.session.add(option)

        # Seed Upcoming Quizzes (those not in full_quizzes yet, if any)
        for quiz_data in upcoming_quizzes:
            if not Quiz.query.filter_by(title=quiz_data['title']).first():
                quiz = Quiz(
                    title=quiz_data['title'],
                    subject=quiz_data['subject'],
                    date=quiz_data['date'],
                    time=quiz_data['time'],
                    duration=quiz_data['duration'],
                    participants=quiz_data.get('participants', 0),
                    status=quiz_data.get('status', 'upcoming')
                )
                db.session.add(quiz)

        # Seed Notifications
        # For simplicity, assign to the first user
        first_user = User.query.first()
        if first_user:
            for n_data in mock_notifications:
                if not Notification.query.filter_by(title=n_data['title'], user_id=first_user.id).first():
                    notification = Notification(
                        user_id=first_user.id,
                        type=n_data['type'],
                        title=n_data['title'],
                        message=n_data['message'],
                        time_label=n_data['time'],
                        read=n_data['read']
                    )
                    db.session.add(notification)

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
