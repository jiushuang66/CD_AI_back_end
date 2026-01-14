"""Package exports for API v1 endpoints.

This module explicitly imports endpoint submodules so that
`from app.api.v1.endpoints import health, documents, ...` works
and each submodule's `router` is available for registration.
"""

from . import health, documents, groups, papers, ai_review, annotations, admin

__all__ = [
	"health",
	"documents",
	"groups",
	"papers",
	"ai_review",
	"annotations",
	"admin",
]

