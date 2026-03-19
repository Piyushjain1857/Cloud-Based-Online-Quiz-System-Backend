from app import app
from core.models import Quiz, Notification, User
with app.app_context():
    print(f"Users: {User.query.count()}")
    print(f"Quizzes: {Quiz.query.count()}")
    print(f"Notifications: {Notification.query.count()}")
    last_notif = Notification.query.order_by(Notification.id.desc()).first()
    if last_notif:
        print(f"Last Notif Title: {last_notif.title}")
        print(f"Last Notif Message: {last_notif.message}")
    else:
        print("No notifications found.")

    # Check for specific notifications
    admin_test = Notification.query.filter_by(title='Admin Test').first()
    print(f"Admin Test Notif: {'Found' if admin_test else 'Not Found'}")
    
    quiz_notif = Notification.query.filter_by(title='New Quiz Published!').first()
    print(f"Quiz Published Notif: {'Found' if quiz_notif else 'Not Found'}")
