from flask import Blueprint, jsonify
from core.models import Quiz

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    quiz_count = Quiz.query.count()
    return jsonify({
        'total_quizzes': quiz_count,
        'total_participants': '1,204',
        'avg_score': '78%'
    }), 200

@analytics_bp.route('/analytics', methods=['GET'])
def get_analytics():
    # Mostly static/mock for now, could be expanded with real results later
    return jsonify({
        'summary': {
            'avg_score': 82,
            'quizzes_taken': 45,
            'pass_rate': 94,
            'total_points': 4200
        },
        'performance_trend': [
            {'date': '2026-03-10', 'score': 75},
            {'date': '2026-03-11', 'score': 80},
            {'date': '2026-03-12', 'score': 78},
            {'date': '2026-03-13', 'score': 85},
            {'date': '2026-03-14', 'score': 82},
            {'date': '2026-03-15', 'score': 88},
            {'date': '2026-03-16', 'score': 92}
        ],
        'subject_performance': [
            {'subject': 'Computer Science', 'score': 88},
            {'subject': 'Mathematics', 'score': 72},
            {'subject': 'History', 'score': 95},
            {'subject': 'Science', 'score': 78},
            {'subject': 'Geography', 'score': 84}
        ],
        'recent_achievements': [
            {'title': 'Python Pro', 'description': 'Scored 100% in Advanced Python', 'date': 'Today'},
            {'title': '3 Day Streak', 'description': 'Took quizzes for 3 days in a row', 'date': 'Yesterday'},
            {'title': 'Quick Learner', 'description': 'Completed World History in under 10 mins', 'date': '2 days ago'}
        ]
    }), 200
