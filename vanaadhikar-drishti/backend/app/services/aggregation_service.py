from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app.models.claim import Claim
from app.models.grievance import Grievance
from app.models.officer import Officer
from app.models.village import Village
from app.schemas.domain import ClaimRead, GrievanceRead, OfficerRead, VillageRead
from app.services.cache_service import CacheService

STATE_METADATA = {
    "MP": {"name": "Madhya Pradesh", "slug": "madhya-pradesh", "color": "#1E88E5"},
    "OD": {"name": "Odisha", "slug": "odisha", "color": "#43A047"},
    "TR": {"name": "Tripura", "slug": "tripura", "color": "#FB8C00"},
    "TG": {"name": "Telangana", "slug": "telangana", "color": "#8E24AA"},
}

PIPELINE_STEPS = [
    {
        "id": "received",
        "label": "Received",
        "color": "#9FA8DA",
        "label_hi": "प्राप्त",
        "db_statuses": ["RECEIVED"],
    },
    {
        "id": "frc-verified",
        "label": "FRC Verified",
        "color": "#64B5F6",
        "label_hi": "पुष्टि",
        "db_statuses": ["FRC_VERIFIED"],
    },
    {
        "id": "sdlc-approved",
        "label": "SDLC Approved",
        "color": "#81C784",
        "label_hi": "एसडीएलसी",
        "db_statuses": ["SDLC_APPROVED"],
    },
    {
        "id": "dlc-approved",
        "label": "DLC Approved",
        "color": "#4DB6AC",
        "label_hi": "डीएलसी",
        "db_statuses": ["DLC_APPROVED"],
    },
    {
        "id": "granted",
        "label": "Granted",
        "color": "#388E3C",
        "label_hi": "अनुमोदित",
        "db_statuses": ["APPROVED"],
    },
]


class AggregationService:
    """Service for aggregating data from multiple tables."""

    @staticmethod
    def get_dashboard_summary(db: Session) -> dict[str, Any]:
        """Get dashboard summary shaped to the frontend DashboardSummary contract."""
        cached = CacheService.get_with_ttl(db, CacheService.CACHE_KEYS["dashboard_summary"], ttl_minutes=15)
        if cached:
            return cached

        claims_stats = AggregationService._aggregate_claims(db)
        villages_stats = AggregationService._aggregate_villages(db)
        timeline = AggregationService._get_timeline_stats(db)

        summary = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "nationalStats": AggregationService._build_national_stats(db, claims_stats, villages_stats),
            "stateStats": AggregationService._build_state_stats(db),
            "districtStats": AggregationService._build_district_stats(db),
            "claims": AggregationService._serialize_claims(db),
            "villages": AggregationService._serialize_villages(db),
            "officers": AggregationService._serialize_officers(db),
            "grievances": AggregationService._serialize_grievances(db),
            "datasets": AggregationService._build_dataset_payload(db, timeline),
            "timeline": timeline,
        }

        CacheService.set(db, CacheService.CACHE_KEYS["dashboard_summary"], summary)
        return summary

    @staticmethod
    def _build_national_stats(db: Session, claim_stats: dict[str, Any], village_stats: dict[str, Any]) -> dict[str, Any]:
        total_ifr = claim_stats["by_type"].get("IFR", 0)
        total_cfr = claim_stats["by_type"].get("CFR", 0)
        total_cr = claim_stats["by_type"].get("CR", 0)
        total_pvtg_claims = claim_stats.get("pvtg_claims", 0)
        total_claims = claim_stats["total"]

        saturation_pct = (
            round((village_stats["granted_claims"] / village_stats["total_claims"] * 100), 2)
            if village_stats["total_claims"] > 0
            else 0
        )

        total_frc_active = (
            db.query(Officer)
            .filter(func.lower(Officer.designation).like("%frc%"))
            .count()
        )

        return {
            "totalClaims": total_claims,
            "totalGranted": claim_stats["approved"],
            "totalPending": claim_stats["pending"],
            "totalRejected": claim_stats["rejected"],
            "totalIFR": total_ifr,
            "totalCFR": total_cfr,
            "totalCR": total_cr,
            "ifrAreaAcres": claim_stats.get("ifr_area_acres", 0),
            "cfrAreaAcres": claim_stats.get("cfr_area_acres", 0),
            "crAreaAcres": claim_stats.get("cr_area_acres", 0),
            "totalVillagesCovered": village_stats["total"],
            "totalPattas": village_stats["total_claims"],
            "totalFRCActive": total_frc_active,
            "saturationPct": saturation_pct,
            "pvtgClaims": total_pvtg_claims,
        }

    @staticmethod
    def _build_state_stats(db: Session) -> list[dict[str, Any]]:
        district_map = AggregationService._build_district_stats(db)

        claim_rows = (
            db.query(
                Claim.state,
                func.count(Claim.id).label("total"),
                func.sum(case((Claim.status == "APPROVED", 1), else_=0)).label("approved"),
                func.sum(case((Claim.status == "PENDING", 1), else_=0)).label("pending"),
                func.sum(case((Claim.status == "REJECTED", 1), else_=0)).label("rejected"),
                func.sum(case((Claim.claim_type == "IFR", Claim.area_acres), else_=0)).label("ifr_area"),
                func.sum(case((Claim.claim_type == "CFR", Claim.area_acres), else_=0)).label("cfr_area"),
                func.sum(case((Claim.claim_type == "CR", Claim.area_acres), else_=0)).label("cr_area"),
                func.sum(case((Claim.claim_type == "CR", 1), else_=0)).label("cr_count"),
                func.sum(case((Claim.claim_type == "IFR", 1), else_=0)).label("ifr_count"),
                func.sum(case((Claim.claim_type == "CFR", 1), else_=0)).label("cfr_count"),
            )
            .group_by(Claim.state)
            .all()
        )

        villages_rows = (
            db.query(
                Village.state,
                func.count(Village.id).label("villages"),
                func.sum(case((Village.pvtg_present == True, 1), else_=0)).label("pvtg_count"),
            )
            .group_by(Village.state)
            .all()
        )

        tribal_rows = (
            db.query(Claim.state, Claim.tribal_group)
            .filter(Claim.tribal_group.isnot(None))
            .distinct()
            .all()
        )

        claim_stats: dict[str, Any] = {}
        for row in claim_rows:
            state_code = row.state
            if not state_code:
                continue
            claim_stats[state_code] = {
                "total": int(row.total or 0),
                "approved": int(row.approved or 0),
                "pending": int(row.pending or 0),
                "rejected": int(row.rejected or 0),
                "ifr_area": round(row.ifr_area or 0, 2),
                "cfr_area": round(row.cfr_area or 0, 2),
                "cr_area": round(row.cr_area or 0, 2),
                "cr_count": int(row.cr_count or 0),
                "by_type": {
                    "IFR": int(row.ifr_count or 0),
                    "CFR": int(row.cfr_count or 0),
                    "CR": int(row.cr_count or 0),
                },
            }

        villages_map = {
            row.state: {
                "villages": int(row.villages or 0),
                "pvtg_count": int(row.pvtg_count or 0),
            }
            for row in villages_rows
            if row.state
        }

        tribal_map: dict[str, set[str]] = defaultdict(set)
        for state_code, group in tribal_rows:
            if state_code and group:
                tribal_map[state_code].add(group)

        observed_states = (
            set(STATE_METADATA.keys())
            | set(claim_stats.keys())
            | set(villages_map.keys())
            | set(district_map.keys())
        )

        result: list[dict[str, Any]] = []
        for state_code in sorted(observed_states):
            metadata = STATE_METADATA.get(state_code, None)
            name = metadata["name"] if metadata else state_code or "Unknown"
            slug = metadata["slug"] if metadata else (state_code or "unknown").lower()
            color = metadata["color"] if metadata else "#607D8B"

            stats = claim_stats.get(state_code, {
                "total": 0,
                "approved": 0,
                "pending": 0,
                "rejected": 0,
                "ifr_area": 0.0,
                "cfr_area": 0.0,
                "cr_area": 0.0,
                "cr_count": 0,
                "by_type": {"IFR": 0, "CFR": 0, "CR": 0},
            })

            villages_info = villages_map.get(state_code, {"villages": 0, "pvtg_count": 0})
            district_entries = district_map.get(state_code, [])
            tribal_groups = sorted(list(tribal_map.get(state_code, set())))

            total_claims = stats["total"]
            granted = stats.get("approved", 0)
            saturation_pct = round((granted / total_claims * 100), 2) if total_claims > 0 else 0

            result.append(
                {
                    "id": state_code,
                    "name": name,
                    "slug": slug,
                    "color": color,
                    "totalClaims": total_claims,
                    "granted": granted,
                    "pending": stats.get("pending", 0),
                    "rejected": stats.get("rejected", 0),
                    "ifrArea": stats.get("ifr_area", 0.0),
                    "cfrArea": stats.get("cfr_area", 0.0),
                    "totalCR": stats.get("cr_count", 0),
                    "saturationPct": saturation_pct,
                    "districts": len(district_entries),
                    "villagesCovered": villages_info.get("villages", 0),
                    "tribalGroups": tribal_groups,
                    "pvtgCount": villages_info.get("pvtg_count", 0),
                    "fireAlerts": 0,
                    "dajguaSaturation": saturation_pct,
                }
            )

        return sorted(result, key=lambda entry: entry["totalClaims"], reverse=True)

    @staticmethod
    def _build_district_stats(db: Session) -> dict[str, list[dict[str, Any]]]:
        district_rows = (
            db.query(
                Claim.state,
                Claim.district,
                func.count(Claim.id).label("total"),
                func.sum(case((Claim.status == "APPROVED", 1), else_=0)).label("approved"),
                func.sum(case((Claim.status == "PENDING", 1), else_=0)).label("pending"),
                func.sum(case((Claim.status == "REJECTED", 1), else_=0)).label("rejected"),
            )
            .group_by(Claim.state, Claim.district)
            .all()
        )

        district_map: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in district_rows:
            state_code = row.state
            if not state_code:
                continue
            district_name = row.district or "Unknown"
            total = int(row.total or 0)
            approved = int(row.approved or 0)
            pending = int(row.pending or 0)
            rejected = int(row.rejected or 0)
            saturation = round((approved / total * 100), 2) if total > 0 else 0

            district_map[state_code].append(
                {
                    "id": f"{state_code}-{district_name.replace(' ', '-').lower()}",
                    "name": district_name,
                    "grants": approved,
                    "pending": pending,
                    "rejected": rejected,
                    "saturation": saturation,
                }
            )

        for state_code in STATE_METADATA:
            district_map.setdefault(state_code, [])

        return dict(district_map)

    @staticmethod
    def _serialize_claims(db: Session, limit: int = 20) -> list[dict[str, Any]]:
        claims = (
            db.query(Claim)
            .order_by(Claim.created_at.desc())
            .limit(limit)
            .all()
        )
        return [
            ClaimRead.model_validate(claim)
            .model_dump(by_alias=True, mode="json", exclude_none=True)
            for claim in claims
        ]

    @staticmethod
    def _serialize_villages(db: Session, limit: int = 20) -> list[dict[str, Any]]:
        villages = (
            db.query(Village)
            .order_by(Village.updated_at.desc())
            .limit(limit)
            .all()
        )
        return [
            VillageRead.model_validate(village)
            .model_dump(by_alias=True, mode="json", exclude_none=True)
            for village in villages
        ]

    @staticmethod
    def _serialize_officers(db: Session, limit: int = 20) -> list[dict[str, Any]]:
        officers = (
            db.query(Officer)
            .order_by(Officer.updated_at.desc())
            .limit(limit)
            .all()
        )
        return [
            OfficerRead.model_validate(officer)
            .model_dump(by_alias=True, mode="json", exclude_none=True)
            for officer in officers
        ]

    @staticmethod
    def _serialize_grievances(db: Session, limit: int = 20) -> list[dict[str, Any]]:
        grievances = (
            db.query(Grievance)
            .order_by(Grievance.updated_at.desc())
            .limit(limit)
            .all()
        )
        return [
            GrievanceRead.model_validate(grievance)
            .model_dump(by_alias=True, mode="json", exclude_none=True)
            for grievance in grievances
        ]

    @staticmethod
    def _build_dataset_payload(db: Session, timeline: dict[str, Any]) -> dict[str, Any]:
        return {
            "dajguaInterventions": [],
            "dssRecommendations": [],
            "monthlyProgress": AggregationService._build_monthly_progress(timeline),
            "forestFireAlerts": [],
            "fieldVisitReports": [],
            "ndviTrend": AggregationService._build_ndvi_trend(timeline),
            "claimPipeline": AggregationService._build_claim_pipeline(db),
        }

    @staticmethod
    def _build_monthly_progress(timeline: dict[str, Any]) -> list[dict[str, Any]]:
        entries = timeline.get("monthly_breakdown", []) if timeline else []
        state_code = next(iter(STATE_METADATA.keys()), "MP")
        result: list[dict[str, Any]] = []
        for entry in entries:
            month_label = entry.get("month", "")
            year_value = datetime.now().year
            if month_label:
                parts = month_label.split()
                if parts and parts[-1].isdigit():
                    year_value = int(parts[-1])

            claims_count = entry.get("claims", 0)

            result.append(
                {
                    "month": month_label,
                    "year": year_value,
                    "state": state_code,
                    "claimsReceived": claims_count,
                    "claimsVerified": int(claims_count * 0.6),
                    "claimsGranted": int(claims_count * 0.45),
                    "claimsRejected": int(claims_count * 0.15),
                    "claimsPending": max(claims_count - int(claims_count * 0.6), 0),
                    "totalPattas": 0,
                    "ifrPattas": 0,
                    "cfrPattas": 0,
                    "crPattas": 0,
                    "ifrAreaAcres": 0,
                    "cfrAreaAcres": 0,
                    "schemesSaturated": 0,
                }
            )
        return result

    @staticmethod
    def _build_ndvi_trend(timeline: dict[str, Any]) -> list[dict[str, Any]]:
        entries = timeline.get("monthly_breakdown", []) if timeline else []
        base_score = 0.65
        trend: list[dict[str, Any]] = []
        for idx, entry in enumerate(entries):
            score = min(base_score + idx * 0.01, 0.99)
            trend.append(
                {
                    "label": entry.get("month", f"Month {idx + 1}"),
                    "score": round(score, 3),
                    "claims": entry.get("claims", 0),
                    "grievances": entry.get("grievances", 0),
                }
            )
        return trend

    @staticmethod
    def _build_claim_pipeline(db: Session) -> list[dict[str, Any]]:
        status_rows = (
            db.query(Claim.status, func.count(Claim.id).label("count"))
            .group_by(Claim.status)
            .all()
        )
        status_counts = {row.status.upper(): int(row.count or 0) for row in status_rows}

        pipeline: list[dict[str, Any]] = []
        for step in PIPELINE_STEPS:
            count = sum(status_counts.get(status, 0) for status in step["db_statuses"])
            pipeline.append(
                {
                    "id": step["id"],
                    "label": step["label"],
                    "color": step["color"],
                    "count": count,
                    "labelHi": step["label_hi"],
                }
            )
        return pipeline

    @staticmethod
    def _aggregate_claims(db: Session) -> dict[str, Any]:
        """Aggregate claim statistics."""
        total = db.query(Claim).count()
        approved = db.query(Claim).filter(Claim.status == "APPROVED").count()
        pending = db.query(Claim).filter(Claim.status == "PENDING").count()
        rejected = db.query(Claim).filter(Claim.status == "REJECTED").count()

        ifr = db.query(Claim).filter(Claim.claim_type == "IFR").count()
        cfr = db.query(Claim).filter(Claim.claim_type == "CFR").count()
        cr = db.query(Claim).filter(Claim.claim_type == "CR").count()

        total_area = db.query(func.sum(Claim.area_acres)).scalar() or 0
        approved_area = (
            db.query(func.sum(Claim.area_acres))
            .filter(Claim.status == "APPROVED")
            .scalar()
            or 0
        )

        ifr_area = (
            db.query(func.sum(case((Claim.claim_type == "IFR", Claim.area_acres), else_=0))).scalar()
            or 0
        )
        cfr_area = (
            db.query(func.sum(case((Claim.claim_type == "CFR", Claim.area_acres), else_=0))).scalar()
            or 0
        )
        cr_area = (
            db.query(func.sum(case((Claim.claim_type == "CR", Claim.area_acres), else_=0))).scalar()
            or 0
        )

        pvtg = db.query(Claim).filter(Claim.is_pvtg == True).count()

        return {
            "total": total,
            "approved": approved,
            "pending": pending,
            "rejected": rejected,
            "approval_rate": round((approved / total * 100) if total > 0 else 0, 2),
            "by_type": {"IFR": ifr, "CFR": cfr, "CR": cr},
            "total_area_acres": round(total_area, 2),
            "approved_area_acres": round(approved_area, 2),
            "ifr_area_acres": round(ifr_area, 2),
            "cfr_area_acres": round(cfr_area, 2),
            "cr_area_acres": round(cr_area, 2),
            "pvtg_claims": pvtg,
        }

    @staticmethod
    def _aggregate_villages(db: Session) -> dict[str, Any]:
        """Aggregate village statistics."""
        total = db.query(Village).count()
        total_population = db.query(func.sum(Village.population)).scalar() or 0
        st_population = db.query(func.sum(Village.st_population)).scalar() or 0
        households = db.query(func.sum(Village.total_households)).scalar() or 0
        total_claims = db.query(func.sum(Village.total_claims)).scalar() or 0
        granted_claims = db.query(func.sum(Village.granted_claims)).scalar() or 0
        pending_claims = db.query(func.sum(Village.pending_claims)).scalar() or 0
        ifr_area = db.query(func.sum(Village.ifr_granted_area)).scalar() or 0
        cfr_area = db.query(func.sum(Village.cfr_granted_area)).scalar() or 0
        state_stats = (
            db.query(Village.state, func.count(Village.id).label("count"))
            .group_by(Village.state)
            .all()
        )
        pvtg_present = db.query(Village).filter(Village.pvtg_present == True).count()

        return {
            "total": total,
            "total_population": int(total_population),
            "st_population": int(st_population),
            "total_households": int(households),
            "st_percentage": round((st_population / total_population * 100) if total_population > 0 else 0, 2),
            "total_claims": int(total_claims),
            "granted_claims": int(granted_claims),
            "pending_claims": int(pending_claims),
            "claims_granted_rate": round((granted_claims / total_claims * 100) if total_claims > 0 else 0, 2),
            "ifr_granted_area": round(ifr_area, 2),
            "cfr_granted_area": round(cfr_area, 2),
            "total_granted_area": round(ifr_area + cfr_area, 2),
            "by_state": {state: count for state, count in state_stats},
            "pvtg_villages": pvtg_present,
            "pvtg_percentage": round((pvtg_present / total * 100) if total > 0 else 0, 2),
        }

    @staticmethod
    def _aggregate_grievances(db: Session) -> dict[str, Any]:
        """Aggregate grievance statistics."""
        total = db.query(Grievance).count()
        open_grievances = db.query(Grievance).filter(Grievance.status == "OPEN").count()
        pending = db.query(Grievance).filter(Grievance.status == "PENDING").count()
        resolved = db.query(Grievance).filter(Grievance.status == "RESOLVED").count()
        critical = db.query(Grievance).filter(Grievance.priority == "CRITICAL").count()
        high = db.query(Grievance).filter(Grievance.priority == "HIGH").count()
        medium = db.query(Grievance).filter(Grievance.priority == "MEDIUM").count()
        low = db.query(Grievance).filter(Grievance.priority == "LOW").count()
        category_stats = (
            db.query(Grievance.category, func.count(Grievance.id).label("count"))
            .group_by(Grievance.category)
            .all()
        )
        resolved_grievances = (
            db.query(Grievance)
            .filter(Grievance.status == "RESOLVED", Grievance.days_open.isnot(None))
            .all()
        )
        avg_resolution_days = (
            round(sum(g.days_open for g in resolved_grievances) / len(resolved_grievances), 1)
            if resolved_grievances
            else 0
        )

        return {
            "total": total,
            "open": open_grievances,
            "pending": pending,
            "resolved": resolved,
            "resolution_rate": round((resolved / total * 100) if total > 0 else 0, 2),
            "by_priority": {
                "CRITICAL": critical,
                "HIGH": high,
                "MEDIUM": medium,
                "LOW": low,
            },
            "by_category": {cat: count for cat, count in category_stats},
            "avg_resolution_days": avg_resolution_days,
        }

    @staticmethod
    def _aggregate_officers(db: Session) -> dict[str, Any]:
        """Aggregate officer statistics."""
        total = db.query(Officer).count()
        state_stats = (
            db.query(Officer.state, func.count(Officer.id).label("count"))
            .group_by(Officer.state)
            .all()
        )
        total_claims_handled = db.query(func.sum(Officer.total_claims_handled)).scalar() or 0
        pending_actions = db.query(func.sum(Officer.pending_actions)).scalar() or 0
        recent_threshold = datetime.now(timezone.utc) - timedelta(hours=24)
        recently_active = db.query(Officer).filter(Officer.last_active >= recent_threshold).count()

        return {
            "total": total,
            "by_state": {state: count for state, count in state_stats},
            "total_claims_handled": int(total_claims_handled),
            "total_pending_actions": int(pending_actions),
            "recently_active": recently_active,
            "active_percentage": round((recently_active / total * 100) if total > 0 else 0, 2),
        }

    @staticmethod
    def _get_timeline_stats(db: Session) -> dict[str, Any]:
        """Get timeline statistics (monthly/weekly trends)."""
        week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        last_week_claims = db.query(Claim).filter(Claim.created_at >= week_ago).count()
        last_week_grievances = db.query(Grievance).filter(Grievance.created_at >= week_ago).count()
        month_ago = datetime.now(timezone.utc) - timedelta(days=30)
        last_month_claims = db.query(Claim).filter(Claim.created_at >= month_ago).count()
        last_month_grievances = db.query(Grievance).filter(Grievance.created_at >= month_ago).count()
        monthly_stats: list[dict[str, Any]] = []
        for i in range(5, -1, -1):
            month_start = datetime.now(timezone.utc) - timedelta(days=30 * (i + 1))
            month_end = datetime.now(timezone.utc) - timedelta(days=30 * i)
            month_claims = (
                db.query(Claim)
                .filter(Claim.created_at >= month_start, Claim.created_at < month_end)
                .count()
            )
            month_grievances = (
                db.query(Grievance)
                .filter(Grievance.created_at >= month_start, Grievance.created_at < month_end)
                .count()
            )
            monthly_stats.append(
                {
                    "month": month_start.strftime("%B %Y"),
                    "claims": month_claims,
                    "grievances": month_grievances,
                }
            )

        return {
            "last_7_days": {
                "claims": last_week_claims,
                "grievances": last_week_grievances,
            },
            "last_30_days": {
                "claims": last_month_claims,
                "grievances": last_month_grievances,
            },
            "monthly_breakdown": monthly_stats,
        }

    @staticmethod
    def get_state_snapshot(db: Session, state: str) -> dict[str, Any]:
        cached = CacheService.get_with_ttl(db, f"state_snapshot_{state}", ttl_minutes=15)
        if cached:
            return cached

        snapshot = {
            "state": state,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "claims": AggregationService._aggregate_claims_by_state(db, state),
            "villages": AggregationService._aggregate_villages_by_state(db, state),
            "grievances": AggregationService._aggregate_grievances_by_state(db, state),
            "officers": AggregationService._aggregate_officers_by_state(db, state),
        }

        CacheService.set(db, f"state_snapshot_{state}", snapshot)
        return snapshot

    @staticmethod
    def _aggregate_claims_by_state(db: Session, state: str) -> dict[str, Any]:
        query = db.query(Claim).filter(Claim.state == state)
        total = query.count()
        approved = query.filter(Claim.status == "APPROVED").count()
        pending = query.filter(Claim.status == "PENDING").count()
        rejected = query.filter(Claim.status == "REJECTED").count()
        district_stats = (
            query.with_entities(Claim.district, func.count(Claim.id).label("count"))
            .group_by(Claim.district)
            .all()
        )

        return {
            "total": total,
            "approved": approved,
            "pending": pending,
            "rejected": rejected,
            "by_district": {dist: count for dist, count in district_stats},
        }

    @staticmethod
    def _aggregate_villages_by_state(db: Session, state: str) -> dict[str, Any]:
        query = db.query(Village).filter(Village.state == state)
        total = query.count()
        population = query.with_entities(func.sum(Village.population)).scalar() or 0

        return {"total": total, "population": int(population)}

    @staticmethod
    def _aggregate_grievances_by_state(db: Session, state: str) -> dict[str, Any]:
        query = db.query(Grievance).filter(Grievance.state == state)
        total = query.count()
        resolved = query.filter(Grievance.status == "RESOLVED").count()

        return {"total": total, "resolved": resolved, "open": total - resolved}

    @staticmethod
    def _aggregate_officers_by_state(db: Session, state: str) -> dict[str, Any]:
        query = db.query(Officer).filter(Officer.state == state)
        total = query.count()
        claims_handled = query.with_entities(func.sum(Officer.total_claims_handled)).scalar() or 0

        return {"total": total, "claims_handled": int(claims_handled)}