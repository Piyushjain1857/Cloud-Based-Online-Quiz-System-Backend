from flask import Blueprint, request, jsonify
from core.models import db, Quiz, Question, Option, User, Notification

quizzes_bp = Blueprint('quizzes', __name__)

def check_admin():
    user_id = request.headers.get('X-User-ID')
    if not user_id:
        return False, jsonify({'error': 'Unauthorized. User ID required.'}), 401
    
    user = User.query.get(user_id)
    if not user or user.role != 'admin':
        return False, jsonify({'error': 'Forbidden. Admin access required.'}), 403
    
    return True, None, None

def quiz_to_dict(quiz):
    return {
        'id': str(quiz.id),
        'title': quiz.title,
        'subject': quiz.subject,
        'date': quiz.date,
        'time': quiz.time,
        'duration': quiz.duration,
        'participants': quiz.participants,
        'status': quiz.status
    }

@quizzes_bp.route('/upcoming', methods=['GET'])
def get_upcoming_quizzes():
    quizzes = Quiz.query.filter_by(status='upcoming').order_by(Quiz.id.desc()).all()
    return jsonify({
        'message': 'Upcoming quizzes fetched successfully.',
        'quizzes': [quiz_to_dict(q) for q in quizzes]
    }), 200

@quizzes_bp.route('/my-quizzes', methods=['GET'])
def get_my_quizzes():
    # For now, return all upcoming quizzes as "my quizzes" mock behavior
    quizzes = Quiz.query.limit(10).all()
    return jsonify({
        'message': 'My quizzes fetched successfully.',
        'quizzes': [quiz_to_dict(q) for q in quizzes]
    }), 200

@quizzes_bp.route('', methods=['POST'])
def create_quiz():
    is_admin, error_resp, status_code = check_admin()
    if not is_admin:
        return error_resp, status_code

    data = request.json
    title = data.get('title')
    subject = data.get('subject')
    duration = data.get('duration')
    date_val = data.get('date')
    time_val = data.get('time')

    if not title or not subject or not duration or not date_val or not time_val:
        return jsonify({'error': 'All fields are required.'}), 400

    new_quiz = Quiz(
        title=title,
        subject=subject,
        date=date_val,
        time=time_val,
        duration=f"{duration} Mins",
        participants=0,
        status='upcoming'
    )

    db.session.add(new_quiz)
    db.session.commit()

    return jsonify({
        'message': 'Quiz created successfully',
        'quiz': quiz_to_dict(new_quiz)
    }), 201

@quizzes_bp.route('/<quiz_id>', methods=['GET'])
def get_quiz_details(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    # Format questions and options
    questions_data = []
    for q in quiz.questions:
        questions_data.append({
            'id': q.id,
            'text': q.text,
            'options': [opt.text for opt in q.options],
            'correctAnswer': q.correct_answer
        })

    result = quiz_to_dict(quiz)
    result['points'] = quiz.points
    result['questions'] = questions_data
    
    return jsonify(result), 200

@quizzes_bp.route('/<quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    is_admin, error_resp, status_code = check_admin()
    if not is_admin:
        return error_resp, status_code

    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    db.session.delete(quiz)
    db.session.commit()
    
    return jsonify({'message': 'Quiz deleted successfully'}), 200

@quizzes_bp.route('/<quiz_id>/submit', methods=['POST'])
def submit_quiz(quiz_id):
    data = request.json
    answers = data.get('answers', []) # List of indices
    
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    score = 0
    results = []
    
    for i, question in enumerate(quiz.questions):
        user_answer = answers[i] if i < len(answers) else None
        is_correct = user_answer == question.correct_answer
        if is_correct:
            score += 1
        results.append({
            'question_id': question.id,
            'correct': is_correct,
            'correct_answer': question.correct_answer
        })

    total_questions = len(quiz.questions)
    final_score_pct = (score / total_questions) * 100 if total_questions > 0 else 0
    
    return jsonify({
        'message': 'Quiz submitted successfully',
        'score': score,
        'total_questions': total_questions,
        'percentage': final_score_pct,
        'results': results
    }), 200

@quizzes_bp.route('/full', methods=['POST'])
def create_full_quiz():
    is_admin, error_resp, status_code = check_admin()
    if not is_admin:
        return error_resp, status_code

    data = request.json
    title = data.get('title')
    subject = data.get('subject')
    duration = data.get('duration')
    points = data.get('points', 100)
    date_val = data.get('date')
    time_val = data.get('time')
    questions_list = data.get('questions', [])

    if not title or not subject or not duration or not date_val or not time_val or not questions_list:
        return jsonify({'error': 'All fields and at least one question are required.'}), 400

    new_quiz = Quiz(
        title=title,
        subject=subject,
        date=date_val,
        time=time_val,
        duration=f"{duration} Mins",
        points=points,
        participants=0,
        status='upcoming'
    )

    db.session.add(new_quiz)
    db.session.flush() # Get ID

    for q_data in questions_list:
        question = Question(
            quiz_id=new_quiz.id,
            text=q_data.get('text'),
            correct_answer=q_data.get('correctAnswer')
        )
        db.session.add(question)
        db.session.flush()

        for opt_text in q_data.get('options', []):
            option = Option(
                question_id=question.id,
                text=opt_text
            )
            db.session.add(option)

    db.session.commit()

    # Broadcast notification to all users
    users = User.query.all()
    for user in users:
        new_notif = Notification(
            user_id=user.id,
            type='quiz',
            title='New Quiz Published!',
            message=f"The quiz '{new_quiz.title}' is now available in {new_quiz.subject}.",
            time_label='Just now',
            read=False
        )
        db.session.add(new_notif)
    db.session.commit()

    return jsonify({
        'message': 'Full quiz created successfully and broadcasted.',
        'quiz_id': str(new_quiz.id)
    }), 201

@quizzes_bp.route('/search', methods=['GET'])
def search_quizzes():
    query_str = request.args.get('q', '').lower()
    if not query_str:
        return jsonify({'quizzes': []}), 200
    
    results = Quiz.query.filter(
        (Quiz.title.ilike(f'%{query_str}%')) | 
        (Quiz.subject.ilike(f'%{query_str}%'))
    ).all()
    
    return jsonify({
        'message': f'Found {len(results)} quizzes.',
        'quizzes': [quiz_to_dict(q) for q in results]
    }), 200
