from __future__ import annotations

from app.db.base_class import Base  # noqa

# Import models for Alembic metadata
from app.models.master_document import MasterDocument  # noqa
from app.models.doc_claim_forest_land import DocClaimForestLand  # noqa
from app.models.doc_claim_community_rights import DocClaimCommunityRights  # noqa
from app.models.doc_claim_community_forest_resource import DocClaimCommunityForestResource  # noqa
from app.models.doc_title_under_occupation import DocTitleUnderOccupation  # noqa
from app.models.doc_title_community_forest_rights import DocTitleCommunityForestRights  # noqa
from app.models.doc_title_community_forest_resources import DocTitleCommunityForestResources  # noqa
from app.models.claim import Claim  # noqa
from app.models.village import Village  # noqa
from app.models.officer import Officer  # noqa
from app.models.grievance import Grievance  # noqa
from app.models.user import User  # noqa
from app.models.data_blob import DataBlob  # noqa
