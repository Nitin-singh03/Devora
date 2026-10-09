from app.mcp.server import mcp


@mcp.tool()
def get_progress():
    """
    Return the authenticated user's overall DSA progress.
    """
    return {
        "status": "ready"
    }


@mcp.tool()
def get_topic_progress():
    """
    Return the authenticated user's topic-wise DSA progress.
    """
    return {
        "status": "ready"
    }


@mcp.tool()
def get_weak_topics():
    """
    Return the user's weak DSA topics.
    """
    return {
        "status": "ready"
    }


@mcp.tool()
def get_due_revisions():
    """
    Return problems that are currently due for revision.
    """
    return {
        "status": "ready"
    }


@mcp.tool()
def recommend_problems():
    """
    Return personalized DSA problem recommendations.
    """
    return {
        "status": "ready"
    }


@mcp.tool()
def get_today_plan():
    """
    Return the user's personalized study plan for today.
    """
    return {
        "status": "ready"
    }
