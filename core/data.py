import time

# In-memory "database"
users = [
    {
        'id': '1',
        'name': 'Piyush Jain',
        'email': 'piyush@example.com',
        'password': 'password123',
        'profileImage': None,
        'role': 'admin'
    },
    {
        'id': '2',
        'name': 'Demo User',
        'email': 'demo@example.com',
        'password': 'password123',
        'profileImage': None,
        'role': 'user'
    },
    {
        'id': '3',
        'name': 'Guest User',
        'email': 'guest@example.com',
        'password': 'password123',
        'profileImage': None,
        'role': 'user'
    }
]

# Mock Notifications
notifications = [
    {
        'id': '1',
        'type': 'quiz',
        'title': 'New Quiz Assigned',
        'message': 'Advanced Python Concepts quiz has been assigned to you.',
        'time': '2 hours ago',
        'read': False
    },
    {
        'id': '2',
        'type': 'system',
        'title': 'System Maintenance',
        'message': 'Cloud Quiz will be down for maintenance on Saturday at 2 AM.',
        'time': '5 hours ago',
        'read': False
    },
    {
        'id': '3',
        'type': 'performance',
        'title': 'Weekly Performance Out!',
        'message': 'Your weekly performance report for last week is now available.',
        'time': '1 day ago',
        'read': True
    }
]

# Mock User Settings
user_settings = {
    'notifications': {
        'email': True,
        'push': False,
        'quizReminders': True
    },
    'preferences': {
        'theme': 'light',
        'language': 'English'
    }
}

# Mock Data for Upcoming Quizzes
upcoming_quizzes = [
    {
        'id': '101',
        'title': 'Advanced Python Concepts',
        'subject': 'Computer Science',
        'date': '2026-03-20',
        'time': '10:00 AM',
        'duration': '45 Mins',
        'participants': 120,
        'status': 'upcoming'
    },
    {
        'id': '102',
        'title': 'World History: WWII',
        'subject': 'History',
        'date': '2026-03-22',
        'time': '02:00 PM',
        'duration': '60 Mins',
        'participants': 85,
        'status': 'upcoming'
    },
    {
        'id': '103',
        'title': 'Calculus II Midterm',
        'subject': 'Mathematics',
        'date': '2026-03-25',
        'time': '09:00 AM',
        'duration': '90 Mins',
        'participants': 200,
        'status': 'upcoming'
    }
]

# In-memory store for full quizzes
full_quizzes = [
    {
        'id': '101',
        'title': 'Advanced Python Concepts',
        'subject': 'Computer Science',
        'duration': '45 Mins',
        'points': 100,
        'questions': [
            {
                'id': 1,
                'text': 'What is a decorator in Python?',
                'options': [
                    'A way to modify the behavior of a function or class',
                    'A graphical element in a GUI',
                    'A type of loop',
                    'A mathematical operator'
                ],
                'correctAnswer': 0
            },
            {
                'id': 2,
                'text': 'What does PEP 8 stand for?',
                'options': [
                    'Python Extension Protocol 8',
                    'Python Enhancement Proposal 8',
                    'Programming Essentials Part 8',
                    'Public Email Policy 8'
                ],
                'correctAnswer': 1
            },
            {
                'id': 3,
                'text': 'Which of the following is used to manage virtual environments in Python?',
                'options': [
                    'npm',
                    'pip',
                    'venv',
                    'git'
                ],
                'correctAnswer': 2
            }
        ]
    }
]
