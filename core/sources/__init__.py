"""Source connectors that produce candidate skills for the wiki wash."""
from .base import CandidateSkill, SourceConnector
from .article import ArticleConnector
from .github import GitHubConnector
from .static_artifact import StaticArtifactConnector
from .youtube import YouTubeConnector

__all__ = [
    "CandidateSkill",
    "SourceConnector",
    "ArticleConnector",
    "GitHubConnector",
    "StaticArtifactConnector",
    "YouTubeConnector",
]
