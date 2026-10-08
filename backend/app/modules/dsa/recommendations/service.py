from datetime import datetime
from sqlalchemy.orm import Session

from app.modules.dsa.problems.models import Problem
from app.modules.dsa.progress.models import UserProblemProgress
from app.modules.dsa.topics.models import Topic
from app.modules.dsa.topics.problem_topics import ProblemTopic
from app.modules.dsa.progress.service import get_topic_progress


def get_problem_topics(problem_id: int, db: Session):
    return db.query(Topic).join(
        ProblemTopic,
        ProblemTopic.topic_id == Topic.id
    ).filter(
        ProblemTopic.problem_id == problem_id
    ).all()


def _score_interview(
    problem: Problem,
    progress: UserProblemProgress | None,
    topics: list[Topic],
    weak_topic_scores: dict[int, float]
) -> tuple[float, list[str]] | None:
    if progress and progress.status == "solved":
        return None

    score = 0.0
    reasons = []

    for topic in topics:
        success_rate = weak_topic_scores.get(topic.id, 0.0)
        if success_rate < 40:
            score += 40
            reasons.append(f"Weak topic: {topic.name}")
        elif success_rate < 60:
            score += 25
            reasons.append(f"Needs improvement: {topic.name}")

    if problem.difficulty:
        diff = problem.difficulty.lower()
        if diff == "medium":
            score += 30
            reasons.append("Interview core difficulty (Medium)")
        elif diff == "easy":
            score += 20
            reasons.append("Foundational interview pattern (Easy)")
        elif diff == "hard":
            score += 10
            reasons.append("Advanced interview challenge (Hard)")

    if not progress:
        score += 20
        reasons.append("Not attempted yet")
    elif progress.attempts >= 3:
        score += 15
        reasons.append("Struggled previously - revisit")

    if not reasons:
        reasons.append("Standard interview pattern")

    return score, reasons


def _score_contest(
    problem: Problem,
    progress: UserProblemProgress | None,
    topics: list[Topic],
    weak_topic_scores: dict[int, float]
) -> tuple[float, list[str]] | None:
    if progress and progress.status == "solved":
        return None

    score = 0.0
    reasons = []

    if problem.difficulty:
        diff = problem.difficulty.lower()
        if diff == "hard":
            score += 35
            reasons.append("High contest impact (Hard)")
        elif diff == "medium":
            score += 25
            reasons.append("Contest benchmark level (Medium)")
        elif diff == "easy":
            score += 10

    if problem.rating:
        if problem.rating >= 1800:
            score += 30
            reasons.append(f"High contest rating ({problem.rating})")
        elif problem.rating >= 1400:
            score += 20
            reasons.append(f"Competitive rating ({problem.rating})")
        else:
            score += 10
            reasons.append(f"Warm-up rating ({problem.rating})")

    for topic in topics:
        success_rate = weak_topic_scores.get(topic.id, 0.0)
        if success_rate < 40:
            score += 30
            reasons.append(f"Contest weakness: {topic.name}")
        elif success_rate < 60:
            score += 15
            reasons.append(f"Speed/accuracy improvement: {topic.name}")

    if not progress:
        score += 15
        reasons.append("Unseen contest problem")
    else:
        score += 15
        reasons.append("Unresolved contest challenge")

    if not reasons:
        reasons.append("Competitive contest practice")

    return score, reasons


def _score_revision(
    problem: Problem,
    progress: UserProblemProgress | None,
    topics: list[Topic],
    weak_topic_scores: dict[int, float]
) -> tuple[float, list[str]] | None:
    # Revision only targets problems the user has previously attempted or solved
    if not progress:
        return None

    score = 0.0
    reasons = []

    if progress.status == "solved":
        score += 25
        reasons.append("Previously solved")

        if progress.last_solved_at:
            days_ago = (datetime.utcnow() - progress.last_solved_at).days
            if days_ago >= 14:
                score += 35
                reasons.append(f"Solved {days_ago} days ago (revision due)")
            elif days_ago >= 7:
                score += 25
                reasons.append(f"Solved {days_ago} days ago")
            elif days_ago >= 3:
                score += 15
                reasons.append(f"Solved {days_ago} days ago")

        if progress.attempts >= 3:
            score += 20
            reasons.append(f"Struggled before solve ({progress.attempts} attempts)")
    else:
        score += 35
        reasons.append("Attempted but unsolved")
        if progress.attempts >= 3:
            score += 25
            reasons.append(f"High failed attempts ({progress.attempts})")

    for topic in topics:
        success_rate = weak_topic_scores.get(topic.id, 0.0)
        if success_rate < 50:
            score += 20
            reasons.append(f"Weak topic revision: {topic.name}")
            break

    if not reasons:
        reasons.append("Revision candidate")

    return score, reasons


def get_recommendations(
    user_id: int,
    db: Session,
    goal: str = "interview",
    limit: int = 10
):
    topic_progress = get_topic_progress(
        user_id,
        db
    )

    weak_topic_scores = {
        topic["topic_id"]: topic["success_rate"]
        for topic in topic_progress
    }

    problems = db.query(Problem).all()
    recommendations = []
    goal_normalized = (goal or "interview").lower()

    for problem in problems:
        progress = db.query(UserProblemProgress).filter(
            UserProblemProgress.user_id == user_id,
            UserProblemProgress.problem_id == problem.id
        ).first()

        topics = get_problem_topics(
            problem.id,
            db
        )

        if goal_normalized == "contest":
            result = _score_contest(problem, progress, topics, weak_topic_scores)
        elif goal_normalized == "revision":
            result = _score_revision(problem, progress, topics, weak_topic_scores)
        else:
            result = _score_interview(problem, progress, topics, weak_topic_scores)

        if result is None:
            continue

        score, reasons = result

        recommendations.append({
            "problem_id": problem.id,
            "title": problem.title,
            "difficulty": problem.difficulty,
            "rating": problem.rating,
            "score": score,
            "reason": " · ".join(reasons)
        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations[:limit]
