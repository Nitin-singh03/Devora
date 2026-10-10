from app.mcp.server import mcp
from app.mcp.context import MCPContext

from app.modules.dsa.progress.service import (
    get_overall_progress,
    get_topic_progress as fetch_topic_progress,
    get_weak_topics as fetch_weak_topics,
)
from app.modules.dsa.recommendations.service import get_recommendations
from app.modules.dsa.revisions.service import (
    get_due_revisions as fetch_due_revisions,
)
from app.modules.dsa.planner.service import create_study_plan


@mcp.tool()
def get_progress():
    """
    Get the authenticated user's overall DSA progress.
    """
    context = MCPContext()

    try:
        return get_overall_progress(
            context.user_id,
            context.db
        )
    finally:
        context.close()


@mcp.tool()
def get_topic_progress():
    """
    Get the authenticated user's topic-wise DSA progress.
    """
    context = MCPContext()

    try:
        return fetch_topic_progress(
            context.user_id,
            context.db
        )
    finally:
        context.close()


@mcp.tool()
def get_weak_topics():
    """
    Get the authenticated user's weak DSA topics.
    """
    context = MCPContext()

    try:
        return fetch_weak_topics(
            context.user_id,
            context.db
        )
    finally:
        context.close()


@mcp.tool()
def recommend_problems(
    limit: int = 5
):
    """
    Get personalized DSA problem recommendations for the authenticated user.
    """
    context = MCPContext()

    try:
        return get_recommendations(
            context.user_id,
            context.db,
            limit=limit
        )
    finally:
        context.close()


@mcp.tool()
def get_due_revisions():
    """
    Get the authenticated user's DSA problems currently due for revision.
    """
    context = MCPContext()

    try:
        revisions = fetch_due_revisions(
            context.user_id,
            context.db
        )

        return [
            {
                "problem_id": revision.problem_id,
                "revision_count": revision.revision_count,
                "confidence": revision.confidence,
                "next_revision_at": revision.next_revision_at.isoformat()
                if revision.next_revision_at
                else None
            }
            for revision in revisions
        ]
    finally:
        context.close()


@mcp.tool()
def get_today_plan():
    """
    Get the authenticated user's personalized study plan for today.
    """
    context = MCPContext()

    try:
        return create_study_plan(
            context.user_id,
            context.db
        )
    finally:
        context.close()

