#!/usr/bin/env python3
"""
Generate comprehensive synthetic datasets for:
- Objective 1: Conflict Resolution (5000+ scenarios)
- Objective 2: Time-Aware Prediction (2000+ scenarios)
- Objective 3: Verification & Reporting (3000+ scenarios)
"""

import json
import random
import os
from datetime import datetime, timedelta

random.seed(42)

# ============================================================================
# COMMON DATA
# ============================================================================

CITIES = [
    {"name": "Bangalore", "state": "Karnataka", "zone": "II", "lat": 12.9716, "lon": 77.5946},
    {"name": "Chennai", "state": "Tamil Nadu", "zone": "III", "lat": 13.0827, "lon": 80.2707},
    {"name": "Delhi", "state": "Delhi", "zone": "IV", "lat": 28.7041, "lon": 77.1025},
    {"name": "Mumbai", "state": "Maharashtra", "zone": "III", "lat": 19.0760, "lon": 72.8777},
    {"name": "Hyderabad", "state": "Telangana", "zone": "II", "lat": 17.3850, "lon": 78.4867},
]

CATEGORIES = [
    "Building Construction", "Environment", "Water", "Air",
    "Road & Infrastructure", "Housing", "Industry"
]

BUILDING_TYPES = [
    "Residential - Individual House", "Residential - Apartment Complex",
    "Residential - Affordable Housing", "Commercial - Office",
    "Commercial - Retail Mall", "Commercial - Hotel",
    "Industrial - Manufacturing", "Industrial - Warehouse",
    "Mixed Use", "Institutional - School", "Institutional - Hospital",
    "Infrastructure - Road", "Infrastructure - Bridge"
]

PROJECT_SIZES = ["Small (< 500 sq.m)", "Medium (500-2000 sq.m)", "Large (2000-10000 sq.m)", "Mega (> 10000 sq.m)"]

AGENTS = [
    "Local Municipal Authority", "State Environment Board", "Fire Services",
    "Water Board", "Pollution Control Board", "Town Planning Authority",
    "Heritage Conservation Authority", "Airport Authority",
    "Highway Authority", "Forest Department", "Housing Board"
]

RESOLUTION_STRATEGIES = [
    "Apply higher authority rule", "Identify grandfather clause",
    "Apply strictest standard", "Seek variance/exception",
    "Apply temporal priority rule", "Invoke public interest override",
    "Combine standards additively", "Defer to court precedent",
    "Apply jurisdiction-specific exemption", "Request joint committee review"
]


def gen_id(prefix, idx):
    return f"{prefix}-{idx:05d}"


# ============================================================================
# OBJECTIVE 1: CONFLICT RESOLUTION DATASET
# ============================================================================

CONFLICT_TYPES = [
    "Jurisdictional Overlap", "Standard Discrepancy", "Temporal Conflict",
    "Requirement Contradiction", "Authority Dispute", "Zoning Conflict",
    "Environmental vs Development", "Safety vs Accessibility", "Heritage vs Modern",
    "Water Rights vs Construction", "Fire Safety vs Ventilation",
    "Parking vs Green Space", "Height vs Aviation", "Noise vs Industry",
    "Flood Zone vs Building", "CRZ vs Housing", "Highway vs Access",
    "Forest vs Development", "Air Quality vs Industry", "Heritage vs TDR"
]

SCENARIO_TEMPLATES = [
    {
        "type": "Jurisdictional Overlap",
        "template": "A {building_type} project in {city} falls under overlapping jurisdiction of {agent1} ({rule1}) and {agent2} ({rule2}), creating a compliance conflict regarding {aspect}.",
        "aspects": ["building height", "setback requirements", "parking norms", "fire safety", "environmental clearance"],
        "rules_local": ["municipal bye-laws set maximum height at {val1}m", "local rules require {val1}m setback from road"],
        "rules_state": ["state regulations allow {val2}m height in this zone", "state code requires {val2}m minimum setback"],
        "rules_federal": ["national code permits {val3}m under NBC standards", "EIA notification requires {val3}m buffer"]
    },
    {
        "type": "Standard Discrepancy",
        "template": "The {building_type} project in {city} must comply with both {standard1} requiring {req1} and {standard2} requiring {req2}, which are contradictory for {aspect}.",
        "standards": ["NBC 2016", "State Building Rules", "Municipal Bye-Laws", "CRZ Notification", "EIA Notification", "Fire Safety Rules", "RERA Act"],
        "aspects": ["structural load", "fire escape width", "parking ratio", "FAR calculation", "green cover percentage", "noise limits", "water recycling rate"]
    },
    {
        "type": "Temporal Conflict",
        "template": "A {building_type} project approved in {year_old} under {old_rule} now faces {year_new} requirements under {new_rule} for {aspect}. The developer must decide compliance path.",
        "aspects": ["fire safety upgrades", "seismic retrofitting", "accessibility compliance", "environmental norms", "parking requirements"]
    },
    {
        "type": "Environmental vs Development",
        "template": "A {building_type} project in {city} is proposed within {distance}m of {env_feature}, where {env_rule} conflicts with {dev_rule} for the {aspect}.",
        "env_features": ["a notified wetland", "a CRZ zone", "a river floodplain", "a heritage monument", "a forest area", "a wildlife corridor"],
        "aspects": ["construction footprint", "building height", "ground coverage", "vegetation removal", "access road"]
    },
    {
        "type": "Fire Safety vs Ventilation",
        "template": "For the {building_type} in {city}, fire safety regulations require {fire_req} while ventilation/air quality standards require {vent_req}, creating a conflict in the {aspect}.",
        "aspects": ["staircase design", "window placement", "basement ventilation", "corridor width", "lounge area design"]
    },
    {
        "type": "Water Rights vs Construction",
        "template": "The {building_type} project in {city} requires {water_req} per {water_rule}, but construction activities will impact {impact} under {env_rule}.",
        "aspects": ["water connection", "STP capacity", "groundwater extraction", "rainwater harvesting", "stormwater management"]
    }
]


def generate_obj1_scenario(idx):
    city = random.choice(CITIES)
    building_type = random.choice(BUILDING_TYPES)
    project_size = random.choice(PROJECT_SIZES)
    
    conflict_type = random.choice(CONFLICT_TYPES)
    
    # Generate jurisdictional conflict
    agent1 = random.choice(AGENTS)
    agent2 = random.choice([a for a in AGENTS if a != agent1])
    
    val1 = random.choice([3, 4, 5, 6, 9, 12, 15, 18, 24, 30, 45])
    val2 = val1 + random.choice([-2, -1, 1, 2, 3, 5])
    val3 = random.choice([val1, val2, val1 + 3, val2 - 1])
    
    aspect = random.choice([
        "building height restrictions", "setback requirements", "parking space ratio",
        "floor area ratio (FAR)", "ground coverage percentage", "fire escape specifications",
        "environmental clearance requirements", "water recycling mandate",
        "seismic design category", "accessibility compliance", "noise level limits",
        "air emission standards", "CRZ setback distance", "heritage buffer zone",
        "industrial buffer zone", "tree replacement ratio", "solar panel requirement",
        "structural load standards", "underground water extraction limits"
    ])
    
    # Generate the conflict description
    if val2 > val1:
        strict_agent = agent1
        lenient_agent = agent2
        strict_val = val1
        lenient_val = val2
    else:
        strict_agent = agent2
        lenient_agent = agent1
        strict_val = val2
        lenient_val = val1
    
    # Generate applicable laws
    city_laws = {
        "Bangalore": "Karnataka Town and Country Planning Act, 1961",
        "Chennai": "Tamil Nadu Building Rules, 2019",
        "Delhi": "Delhi Building Bye-Laws 2021",
        "Mumbai": "Maharashtra Regional and Town Planning Act, 1966",
        "Hyderabad": "Telangana State Building Rules, 2012",
    }
    law_pool = [
        city_laws.get(city["name"], "Municipal Building Rules"),
        "National Building Code of India 2016",
        "Environmental Impact Assessment Notification, 2006",
        "Coastal Regulation Zone Notification, 2019",
        "Water Act, 1974", "Air Act, 1981",
        "Fire Services Act (State)", "Real Estate Regulatory Authority Act, 2016",
        "C&D Waste Management Rules, 2016",
    ]
    law_set = random.sample(law_pool, k=min(random.randint(3, 6), len(law_pool)))
    
    # Generate reasoning chain
    reasoning_steps = [
        f"Step 1: Identify that the project falls within {city['name']}, {city['state']} jurisdiction.",
        f"Step 2: Recognize that {strict_agent} mandates a maximum/minimum of {strict_val} for {aspect}.",
        f"Step 3: Note that {lenient_agent} allows up to {lenient_val} for the same {aspect}.",
        f"Step 4: Apply the doctrine of harmonious construction.",
        f"Step 5: Determine which standard applies as per the hierarchy of laws.",
        f"Step 6: Apply resolution strategy to reconcile the conflict."
    ]
    
    resolution = random.choice(RESOLUTION_STRATEGIES)
    
    # Generate compliance impact
    if strict_val < lenient_val:
        impact_desc = f"Strict compliance requires meeting {strict_agent}'s standard of {strict_val}. This limits {aspect} compared to {lenient_agent}'s allowance of {lenient_val}."
    else:
        impact_desc = f"Under harmonious construction, both standards must be met. The more restrictive standard of {strict_val} from {strict_agent} applies."
    
    risk_level = random.choice(["Low", "Medium", "High", "Critical"])
    estimated_cost_impact = random.choice([
        "No additional cost", "5-10% increase", "10-20% increase",
        "20-30% increase", "30-50% increase", "Potential project redesign"
    ])
    
    scenario = {
        "id": gen_id("OBJ1", idx),
        "city": city["name"],
        "state": city["state"],
        "country": "India",
        "building_type": building_type,
        "project_size": project_size,
        "conflict_type": conflict_type,
        "aspect": aspect,
        "jurisdiction1": {
            "authority": agent1,
            "jurisdiction_level": random.choice(["Local/Municipal", "State", "Federal/National"]),
            "requirement": f"Maximum/minimum {aspect} of {random.choice([val1, val2, val3])}",
            "source_law": random.choice(law_set)
        },
        "jurisdiction2": {
            "authority": agent2,
            "jurisdiction_level": random.choice(["Local/Municipal", "State", "Federal/National"]),
            "requirement": f"Maximum/minimum {aspect} of {random.choice([val1, val2, val3])}",
            "source_law": random.choice(law_set)
        },
        "conflict_description": (
            f"A {building_type} project ({project_size}) in {city['name']} faces a {conflict_type.lower()} conflict "
            f"regarding {aspect}. {agent1} requires {strict_val} while {lenient_agent} allows {lenient_val}."
        ),
        "applicable_laws": law_set[:4],
        "reasoning_chain": reasoning_steps,
        "resolution_strategy": resolution,
        "resolution_description": (
            f"Apply '{resolution}' strategy. The system should recommend: {impact_desc}"
        ),
        "expected_outcome": {
            "compliant_value": f"{strict_val}",
            "risk_level": risk_level,
            "estimated_cost_impact": estimated_cost_impact,
            "recommended_action": f"Comply with {strict_agent}'s standard of {strict_val} for {aspect}. Seek {resolution.lower()} if lenient standard is desired."
        },
        "priority": random.choice(["Low", "Medium", "High"]),
        "tags": [conflict_type.lower(), city["name"].lower(), aspect.lower().replace(" ", "_")]
    }
    
    return scenario


# ============================================================================
# OBJECTIVE 2: TIME-AWARE PREDICTION DATASET
# ============================================================================

CODE_CHANGE_TYPES = [
    "FAR Increase", "FAR Decrease", "Setback Modification", "Height Restriction Change",
    "Parking Requirement Update", "Fire Safety Upgrade", "Environmental Norm Tightening",
    "Environmental Norm Relaxation", "CRZ Boundary Modification", "Heritage Zone Expansion",
    "Industrial Zone Rezoning", "Affordable Housing Mandate", "Green Building Incentive",
    "Water Harvesting Mandate Update", "Noise Restriction Tightening", "Airport Height Change",
    "Metro Corridor Buffer", "Road Widening Project", "Flood Zone Reclassification",
    "Groundwater Restriction", "C&D Waste Rule Update", "RERA Amendment",
    "Accessibility Requirement Upgrade", "Solar Mandate", "EV Charging Requirement"
]

PROJECT_PHASES = [
    "Planning/Approval", "Foundation", "Structure - Lower Floors",
    "Structure - Upper Floors", "MEP Rough-in", "Interior Finishing",
    "External Works", "Commissioning", "Pre-Occupancy"
]

VIOLATION_TYPES = [
    "Height Exceedance", "Setback Violation", "FAR Violation", "Parking Deficiency",
    "Fire Safety Gap", "Environmental Clearance Missing", "CRZ Violation",
    "Water Harvesting Non-Compliance", "Waste Management Gap", "Accessibility Gap",
    "Structural Non-Compliance", "Noise Violation", "Heritage Violation",
    "Tree Cutting Without Permission", "Groundwater Over-extraction"
]


def gen_historical_change(idx):
    city = random.choice(CITIES)
    
    change_type = random.choice(CODE_CHANGE_TYPES)
    year = random.randint(2018, 2025)
    month = random.randint(1, 12)
    
    # Generate timeline
    change_date = datetime(year, month, 1)
    
    # Generate change details
    if "FAR" in change_type:
        old_val = round(random.uniform(1.5, 3.0), 2)
        new_val = round(old_val + random.uniform(-0.5, 0.5), 2)
        aspect = "Floor Area Ratio"
        unit = "FAR"
    elif "Setback" in change_type:
        old_val = random.uniform(1.5, 5.0)
        new_val = old_val + random.uniform(-1.0, 1.0)
        aspect = "Setback Distance"
        unit = "meters"
    elif "Height" in change_type:
        old_val = random.uniform(15, 60)
        new_val = old_val + random.uniform(-10, 15)
        aspect = "Building Height Limit"
        unit = "meters"
    elif "Parking" in change_type:
        old_val = round(random.uniform(0.5, 1.5), 2)
        new_val = round(old_val + random.uniform(-0.3, 0.5), 2)
        aspect = "Parking Ratio"
        unit = "ECS per 100 sq.m"
    else:
        old_val = round(random.uniform(0, 100), 1)
        new_val = round(old_val + random.uniform(-20, 30), 1)
        aspect = change_type
        unit = "varies"
    
    # Generate impact assessment
    affected_projects = random.randint(50, 5000)
    compliance_deadline_months = random.choice([3, 6, 9, 12, 18, 24])
    estimated_compliance_cost = random.choice([
        "Minimal (< 1% of project cost)",
        "Low (1-5%)",
        "Moderate (5-15%)",
        "High (15-30%)",
        "Very High (> 30%)"
    ])
    
    # Project context for prediction
    project_start = datetime(year + random.randint(0, 2), random.randint(1, 12), 1)
    project_duration_months = random.randint(12, 48)
    project_end = project_start + timedelta(days=project_duration_months * 30)
    
    # Risk assessment
    if new_val < old_val and change_type not in ["Relaxation", "Increase"]:
        risk = "High - Regulatory tightening during construction"
        risk_probability = random.uniform(0.6, 0.95)
    else:
        risk = "Low-Medium - Favorable or neutral change"
        risk_probability = random.uniform(0.1, 0.5)
    
    scenario = {
        "id": gen_id("OBJ2-HIST", idx),
        "city": city["name"],
        "state": city["state"],
        "country": "India",
        "historical_code_change": {
            "change_type": change_type,
            "effective_date": change_date.strftime("%Y-%m-%d"),
            "description": f"{change_type} in {city['name']}: {aspect} changed from {round(old_val, 2)} to {round(new_val, 2)} {unit}",
            "old_value": round(old_val, 2),
            "new_value": round(new_val, 2),
            "unit": unit,
            "aspect": aspect,
            "announced_date": (change_date - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
            "grace_period_months": compliance_deadline_months
        },
        "impact_assessment": {
            "affected_projects": affected_projects,
            "compliance_deadline_months": compliance_deadline_months,
            "estimated_compliance_cost": estimated_compliance_cost,
            "affected_building_types": random.sample(BUILDING_TYPES, k=random.randint(1, 4)),
            "retroactive": random.choice([True, True, True, False]),
            "grandfathering": random.choice(["None", "Partial", "Full for pre-approved projects"])
        },
        "context_features": {
            "political_climate": random.choice(["Stable", "Election year", "Policy reform period"]),
            "environmental_events": random.choice(["None", "Flood event", "Air quality crisis", "Drought", "Industrial accident"]),
            "population_growth_rate": round(random.uniform(1.5, 4.0), 1),
            "construction_permit_volume_trend": random.choice(["Increasing", "Stable", "Decreasing"]),
            "court_orders_active": random.choice([0, 0, 1, 2]),
            "public_sentiment": random.choice(["Supportive", "Neutral", "Opposed", "Mixed"])
        },
        "tags": [change_type.lower().replace(" ", "_"), city["name"].lower()]
    }
    
    return scenario


def generate_obj2_prediction_scenario(idx):
    city = random.choice(CITIES)
    building_type = random.choice(BUILDING_TYPES)
    project_size = random.choice(PROJECT_SIZES)
    
    project_start_year = random.randint(2024, 2026)
    project_start_month = random.randint(1, 12)
    project_duration = random.randint(12, 48)
    
    # Predicted code changes
    num_changes = random.randint(1, 4)
    predicted_changes = []
    for _ in range(num_changes):
        change_type = random.choice(CODE_CHANGE_TYPES)
        months_ahead = random.randint(1, 18)
        
        if "FAR" in change_type:
            predicted_val = round(random.uniform(1.5, 4.0), 2)
        elif "Height" in change_type:
            predicted_val = round(random.uniform(15, 80), 1)
        elif "Parking" in change_type:
            predicted_val = round(random.uniform(0.5, 2.0), 2)
        else:
            predicted_val = round(random.uniform(0, 100), 1)
        
        confidence = round(random.uniform(0.4, 0.95), 2)
        
        predicted_changes.append({
            "change_type": change_type,
            "predicted_direction": random.choice(["Tightening", "Relaxation", "No Change"]),
            "predicted_value": predicted_val,
            "months_ahead": months_ahead,
            "confidence": confidence,
            "confidence_interval_lower": round(max(0, confidence - 0.15), 2),
            "confidence_interval_upper": round(min(1.0, confidence + 0.10), 2),
            "key_indicators": random.sample([
                "Government policy statements", "Court orders", "Environmental data",
                "Political changes", "Public pressure", "Industry lobbying",
                "International standards alignment", "Historical pattern",
                "Infrastructure development", "Population pressure"
            ], k=random.randint(2, 5))
        })
    
    # Compliance roadmap
    roadmap_items = []
    cumulative_risk = 0
    for i, change in enumerate(predicted_changes):
        impact_months = change["months_ahead"]
        risk_score = change["confidence"] * random.uniform(0.5, 1.0)
        cumulative_risk += risk_score
        
        roadmap_items.append({
            "milestone": f"Prepare for {change['change_type']}",
            "timeline_months": impact_months,
            "action_required": f"Update design for {change['predicted_direction']} of {change['change_type']}",
            "risk_score": round(risk_score, 2),
            "estimated_cost_impact": random.choice([
                "Minimal", "Low (< 5%)", "Moderate (5-15%)", "High (> 15%)"
            ]),
            "prerequisites": random.sample([
                "Structural engineer consultation", "Legal review", "Budget revision",
                "Authority consultation", "Design modification", "Material specification change"
            ], k=random.randint(1, 3))
        })
    
    overall_risk = round(cumulative_risk / max(len(predicted_changes), 1), 2)
    
    scenario = {
        "id": gen_id("OBJ2-PRED", idx),
        "city": city["name"],
        "state": city["state"],
        "country": "India",
        "project_context": {
            "building_type": building_type,
            "project_size": project_size,
            "current_phase": random.choice(PROJECT_PHASES),
            "project_start": f"{project_start_year}-{project_start_month:02d}-01",
            "project_duration_months": project_duration,
            "project_end": f"{project_start_year + project_duration // 12}-{((project_start_month + project_duration % 12 - 1) % 12) + 1:02d}-01",
            "current_permits": random.sample([
                "Land use approval", "Building plan approval", "Environmental clearance",
                "Fire NOC", "Water connection", "Sewerage connection", "Power connection"
            ], k=random.randint(3, 6))
        },
        "predicted_code_changes": sorted(predicted_changes, key=lambda x: x["months_ahead"]),
        "compliance_roadmap": {
            "items": sorted(roadmap_items, key=lambda x: x["timeline_months"]),
            "overall_risk_score": overall_risk,
            "risk_level": "Low" if overall_risk < 0.3 else "Medium" if overall_risk < 0.6 else "High",
            "total_estimated_cost_impact": random.choice([
                "Minimal (< 2%)", "Low (2-8%)", "Moderate (8-20%)", "High (> 20%)"
            ])
        },
        "historical_precedents": [
            {
                "year": random.randint(2018, 2024),
                "change": f"Similar {random.choice(CODE_CHANGE_TYPES)} in {city['name']}",
                "outcome": random.choice([
                    "Affected 500+ projects", "6-month grace period", "Court stay applied",
                    "Partial implementation", "Full implementation", "Reversed after 2 years"
                ])
            }
            for _ in range(random.randint(1, 3))
        ],
        "recommendation": {
            "proactive_action": f"Consider preemptive compliance with predicted {random.choice(['tightening', 'expansion'])} to reduce future risk.",
            "contingency_plan": "Maintain design flexibility for regulatory changes within predicted timeline.",
            "monitoring_frequency": random.choice(["Monthly", "Bi-weekly", "Weekly"]),
            "review_triggers": random.sample([
                "Government policy announcements", "Court orders", "Election results",
                "Environmental reports", "Budget announcements", "International events"
            ], k=random.randint(2, 4))
        },
        "tags": [building_type.lower().split(" - ")[0], city["name"].lower(), "prediction"]
    }
    
    return scenario


# ============================================================================
# OBJECTIVE 3: VERIFICATION & REPORTING DATASET
# ============================================================================

INSPECTION_TYPES = [
    "Pre-construction Site Inspection", "Foundation Inspection", "Structural Frame Inspection",
    "MEP Inspection", "Fire Safety Inspection", "Environmental Compliance Inspection",
    "CRZ Compliance Inspection", "Occupancy Certificate Inspection",
    "Annual Compliance Audit", "Demolition Safety Inspection",
    "Accessibility Audit", "Green Building Certification Audit"
]

REPORT_TYPES = [
    "Compliance Certificate", "Non-Compliance Notice", "Conditional Approval",
    "Stop Work Order", "Demolition Recommendation", "Improvement Notice",
    "Penalty Assessment", "Environmental Monitoring Report", "Structural Safety Certificate",
    "Fire Safety Certificate", "Occupancy Certificate", "Completion Certificate"
]

COMPLIANCE_STATUSES = [
    "Fully Compliant", "Partially Compliant", "Non-Compliant",
    "Conditionally Compliant", "Requires Re-inspection"
]


def generate_obj3_scenario(idx):
    city = random.choice(CITIES)
    building_type = random.choice(BUILDING_TYPES)
    project_size = random.choice(PROJECT_SIZES)
    
    inspection_type = random.choice(INSPECTION_TYPES)
    num_findings = random.randint(2, 12)
    
    findings = []
    compliant_items = random.randint(3, 8)
    
    for i in range(num_findings):
        severity = random.choice(["Critical", "Major", "Minor", "Observation", "Compliant"])
        
        category = random.choice(CATEGORIES)
        if severity == "Critical":
            detail = random.choice([
                f"Building height ({random.randint(30, 60)}m) exceeds permitted height ({random.randint(15, 45)}m) for this zone.",
                f"Fire escape width ({round(random.uniform(0.5, 0.8), 1)}m) is below minimum requirement (1.0m).",
                f"Structural concrete grade M{random.randint(10, 15)} does not meet minimum M20 requirement.",
                f"Environmental clearance not obtained for project requiring EIA.",
                f"No structural stability certificate available.",
                f"Building constructed in CRZ-I zone where no construction is permitted.",
                f"Groundwater extraction without CGWB permission in over-exploited zone."
            ])
        elif severity == "Major":
            detail = random.choice([
                f"Setback of {round(random.uniform(1.0, 2.0), 1)}m is below minimum {round(random.uniform(3.0, 5.0), 1)}m required.",
                f"Parking provision ({round(random.uniform(0.3, 0.7), 2)} ECS/100sq.m) below required ratio.",
                f"Rainwater harvesting system not installed despite {random.randint(400, 2000)} sq.m built-up area.",
                f"Fire extinguisher count ({random.randint(2, 5)}) insufficient for {random.randint(500, 2000)} sq.m area.",
                f"STP capacity ({random.randint(10, 50)} KLD) insufficient for {random.randint(25, 100)} dwelling units.",
                f"Structural rebar spacing ({random.randint(250, 350)}mm) exceeds maximum ({random.randint(150, 200)}mm).",
                f"Accessibility ramp gradient (1:{random.randint(14, 20)}) exceeds maximum 1:12."
            ])
        elif severity == "Minor":
            detail = random.choice([
                f"Compound wall height ({round(random.uniform(1.3, 2.0), 1)}m) slightly exceeds {round(random.uniform(1.0, 1.5), 1)}m limit.",
                f"Signage not as per municipal standards.",
                f"Minor crack observed in external wall (width {round(random.uniform(0.1, 0.5), 1)}mm).",
                f"Water meter not installed at required location.",
                f"Electrical earthing resistance ({round(random.uniform(5, 8), 1)} ohms) slightly above 5 ohm limit.",
                f"Ventilation duct cross-section marginally below design spec."
            ])
        elif severity == "Observation":
            detail = random.choice([
                f"Construction material storage area could be better organized.",
                f"Worker safety signage partially missing.",
                f"Site drainage could be improved during construction phase.",
                f"Temporary fencing not consistently maintained."
            ])
        else:  # Compliant
            detail = random.choice([
                f"Structural concrete grade M{random.randint(20, 40)} meets all standards.",
                f"Fire escape width ({round(random.uniform(1.0, 1.5), 1)}m) exceeds minimum requirement.",
                f"Setback distances ({round(random.uniform(3.0, 6.0), 1)}m) comply with all norms.",
                f"Parking provision ({round(random.uniform(1.0, 2.0), 2)} ECS/100sq.m) meets or exceeds requirements.",
                f"Rainwater harvesting capacity ({random.randint(5000, 25000)} liters) compliant.",
                f"Elevator certification is current and valid.",
                f"Access ramp with Braille signage meets accessibility standards."
            ])
        
        finding = {
            "finding_id": f"F{idx:03d}-{i+1:02d}",
            "category": category,
            "severity": severity,
            "description": detail,
            "applicable_regulation": random.choice([
                "NBC 2016 Part 2", "NBC 2016 Part 4", "NBC 2016 Part 5",
                "NBC 2016 Part 6", "State Building Rules", "Municipal Bye-Laws",
                "EIA Notification 2006", "CRZ Notification 2019",
                "Fire Safety Rules", "RERA Act 2016",
                "Water Act 1974", "Air Act 1981",
                "C&D Waste Rules 2016", "RPWD Act 2016",
                "Factory Act 1948"
            ]),
            "reference_section": random.choice([
                "Section 3.2.1", "Section 5.1.3", "Section 7.4.2",
                "Section 9.1.1", "Section 12.3.4", "Annexure B",
                "Rule 4(2)", "Rule 10(1)", "Schedule I"
            ]),
            "evidence": {
                "measurement": f"{round(random.uniform(0.5, 10.0), 1)} measured vs {round(random.uniform(1.0, 12.0), 1)} required",
                "photograph_reference": f"IMG-{random.randint(1000, 9999)}",
                "document_reference": f"DOC-{random.randint(100, 999)}",
                "test_result": f"Lab report {random.choice(['pending', 'acceptable', 'below standard'])}"
            },
            "recommendation": random.choice([
                "Immediate rectification required before next inspection",
                "Rectification within 30 days recommended",
                "Rectification within 90 days acceptable",
                "Advisory - no immediate action required",
                "No action required - compliant"
            ]),
            "rectification_cost_estimate": random.choice([
                "₹10,000 - ₹50,000",
                "₹50,000 - ₹2,00,000",
                "₹2,00,000 - ₹10,00,000",
                "₹10,00,000 - ₹50,00,000",
                "₹50,00,000+",
                "Not estimable - requires redesign"
            ]),
            "rectification_timeline": random.choice([
                "1 week", "2 weeks", "1 month", "3 months", "6 months", "Requires redesign"
            ])
        }
        findings.append(finding)
    
    critical_count = sum(1 for f in findings if f["severity"] == "Critical")
    major_count = sum(1 for f in findings if f["severity"] == "Major")
    minor_count = sum(1 for f in findings if f["severity"] == "Minor")
    observation_count = sum(1 for f in findings if f["severity"] == "Observation")
    compliant_count = sum(1 for f in findings if f["severity"] == "Compliant")
    
    if critical_count > 0:
        overall_status = "Non-Compliant"
        report_type = random.choice(["Stop Work Order", "Non-Compliance Notice", "Demolition Recommendation"])
    elif major_count > 2:
        overall_status = "Non-Compliant"
        report_type = "Non-Compliance Notice"
    elif major_count > 0:
        overall_status = "Conditionally Compliant"
        report_type = "Conditional Approval"
    elif minor_count > 3:
        overall_status = "Partially Compliant"
        report_type = "Improvement Notice"
    else:
        overall_status = "Fully Compliant"
        report_type = random.choice(["Compliance Certificate", "Completion Certificate", "Occupancy Certificate"])
    
    inspector_name = random.choice([
        "Er. Rajesh Kumar, CE", "Er. Priya Sharma, SE", "Er. Anand Verma, EE",
        "Er. Sunita Reddy, AE", "Er. Mohammed Ali, CE", "Er. Deepa Nair, SE",
        "Er. Vikram Singh, CE", "Er. Lakshmi Iyer, AE"
    ])
    
    total_estimated_rectification = "₹" + str(random.randint(50000, 5000000)) + " (approx)"
    
    # Reasoning chain for the report
    reasoning_chain = [
        f"1. Inspection initiated on {datetime.now().strftime('%Y-%m-%d')} at the {building_type} project ({project_size}) in {city['name']}.",
        f"2. Inspection type: {inspection_type}.",
        f"3. Examined {num_findings + compliant_items} compliance parameters across {len(CATEGORIES)} categories.",
        f"4. Found {critical_count} critical, {major_count} major, {minor_count} minor issues, {observation_count} observations, and {compliant_count} compliant items.",
        f"5. Critical findings: {'None' if critical_count == 0 else f'{critical_count} issue(s) requiring immediate attention.'}",
        f"6. Major findings require rectification {'within 30 days' if major_count > 0 else 'N/A'}.",
        f"7. Overall assessment: {overall_status}.",
        f"8. Report type: {report_type}.",
        f"9. Estimated rectification cost: {total_estimated_rectification}.",
        f"10. Compliance verification complete."
    ]
    
    scenario = {
        "id": gen_id("OBJ3", idx),
        "city": city["name"],
        "state": city["state"],
        "country": "India",
        "project_context": {
            "building_type": building_type,
            "project_size": project_size,
            "project_name": f"Project-{city['name'][:3].upper()}-{random.randint(100, 999)}",
            "developer": f"Developer-{random.randint(1, 100)}",
            "approved_plan_date": (datetime.now() - timedelta(days=random.randint(100, 2000))).strftime("%Y-%m-%d"),
            "construction_start": (datetime.now() - timedelta(days=random.randint(50, 1500))).strftime("%Y-%m-%d"),
            "estimated_completion": (datetime.now() + timedelta(days=random.randint(100, 1000))).strftime("%Y-%m-%d")
        },
        "inspection_details": {
            "inspection_type": inspection_type,
            "inspection_date": datetime.now().strftime("%Y-%m-%d"),
            "inspector_name": inspector_name,
            "inspector_designation": random.choice(["Chief Engineer", "Structural Engineer", "Environmental Officer", "Fire Safety Officer", "Municipal Engineer"]),
            "agency": random.choice(AGENTS),
            "inspection_protocol_version": "2024.1",
            "documents_reviewed": random.sample([
                "Building Plan Approval", "Structural Stability Certificate",
                "Environmental Clearance", "Fire NOC", "CTE/CTO",
                "Soil Investigation Report", "Structural Drawing",
                "MEP Drawing", "RERA Registration", "Water Connection Approval",
                "Soil Test Results", "Material Test Certificates"
            ], k=random.randint(4, 8))
        },
        "findings": findings,
        "summary": {
            "total_parameters_checked": num_findings + compliant_items,
            "critical_findings": critical_count,
            "major_findings": major_count,
            "minor_findings": minor_count,
            "observations": observation_count,
            "compliant_items": compliant_count,
            "compliance_percentage": round((compliant_count / (num_findings + compliant_items)) * 100, 1),
            "overall_status": overall_status,
            "report_type": report_type
        },
        "compliance_report": {
            "report_id": f"RPT-{city['name'][:3].upper()}-{datetime.now().strftime('%Y%m')}-{random.randint(100, 999)}",
            "report_title": f"{inspection_type} Report - {building_type}",
            "generated_date": datetime.now().strftime("%Y-%m-%d"),
            "reporting_authority": random.choice(AGENTS),
            "legal_disclaimer": "This report is generated based on field inspections and document review. It serves as a compliance assessment and does not constitute legal advice.",
            "reasoning_chain": reasoning_chain,
            "executive_summary": (
                f"The {inspection_type.lower().replace('_', ' ')} of the {building_type} project ({project_size}) "
                f"in {city['name']}, {city['state']} was conducted on {datetime.now().strftime('%Y-%m-%d')}. "
                f"A total of {num_findings + compliant_items} compliance parameters were assessed. "
                f"The project is currently {overall_status.lower()} with {critical_count} critical and {major_count} major findings. "
                f"{'Immediate action is required for critical findings.' if critical_count > 0 else 'No critical issues were identified.'}"
            ),
            "min_change_recommendation": {
                "description": "Minimum changes required to achieve full compliance",
                "priority_items": [
                    f["description"] for f in findings if f["severity"] in ["Critical", "Major"]
                ][:5],
                "total_estimated_cost": total_estimated_rectification,
                "recommended_timeline": random.choice(["1 month", "3 months", "6 months"]),
                "compliance_after_changes": "Fully Compliant (expected)"
            }
        },
        "traceable_evidence": {
            "photographs": [f"IMG-{random.randint(1000, 9999)}.jpg" for _ in range(random.randint(5, 20))],
            "documents": [f"DOC-{random.randint(100, 999)}.pdf" for _ in range(random.randint(3, 10))],
            "lab_reports": [f"LAB-{random.randint(100, 999)}.pdf" for _ in range(random.randint(1, 5))],
            "measurements_log": [
                {
                    "parameter": f["category"],
                    "measured": f["evidence"]["measurement"].split(" vs ")[0].strip(),
                    "standard": f["evidence"]["measurement"].split(" vs ")[1].strip(),
                    "status": "Pass" if f["severity"] == "Compliant" else "Fail"
                }
                for f in findings if f["severity"] != "Observation"
            ]
        },
        "tags": [overall_status.lower().replace(" ", "_"), building_type.lower().split(" - ")[0], city["name"].lower()]
    }
    
    return scenario


# ============================================================================
# GENERATE ALL DATASETS
# ============================================================================

def main():
    print("=" * 60)
    print("SYNTHETIC DATASET GENERATOR")
    print("Multi-Agent Legal RAG - Construction & Zoning Compliance")
    print("=" * 60)
    
    # Objective 1: Conflict Resolution
    print("\n[1/3] Generating Objective 1: Conflict Resolution Dataset...")
    obj1_data = {
        "metadata": {
            "dataset_name": "Conflict Resolution Scenarios",
            "objective": "Objective 1: Multi-Agent Conflict Resolution",
            "description": "Scenarios involving contradictory legal requirements across overlapping jurisdictions",
            "target_count": 5500,
            "cities": [c["name"] for c in CITIES],
            "categories": CATEGORIES,
            "conflict_types": CONFLICT_TYPES,
            "generated_date": datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0"
        },
        "scenarios": []
    }
    
    for i in range(5500):
        obj1_data["scenarios"].append(generate_obj1_scenario(i + 1))
        if (i + 1) % 1000 == 0:
            print(f"  Generated {i + 1}/5500 conflict scenarios...")
    
    os.makedirs("datasets/objective1_conflict", exist_ok=True)
    with open("datasets/objective1_conflict/conflict_resolution_dataset.json", "w", encoding="utf-8") as f:
        json.dump(obj1_data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Saved {len(obj1_data['scenarios'])} conflict scenarios")
    
    # Objective 2: Time-Aware Prediction
    print("\n[2/3] Generating Objective 2: Time-Aware Prediction Dataset...")
    obj2_data = {
        "metadata": {
            "dataset_name": "Time-Aware Prediction Scenarios",
            "objective": "Objective 2: Future Compliance Violation Prediction",
            "description": "Historical code changes and predicted future violations with compliance roadmaps",
            "target_count_historical": 2500,
            "target_count_prediction": 2500,
            "cities": [c["name"] for c in CITIES],
            "categories": CATEGORIES,
            "code_change_types": CODE_CHANGE_TYPES,
            "generated_date": datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0"
        },
        "historical_changes": [],
        "prediction_scenarios": []
    }
    
    for i in range(2500):
        obj2_data["historical_changes"].append(gen_historical_change(i + 1))
        if (i + 1) % 500 == 0:
            print(f"  Generated {i + 1}/2500 historical changes...")
    
    for i in range(2500):
        obj2_data["prediction_scenarios"].append(generate_obj2_prediction_scenario(i + 1))
        if (i + 1) % 500 == 0:
            print(f"  Generated {i + 1}/2500 prediction scenarios...")
    
    os.makedirs("datasets/objective2_prediction", exist_ok=True)
    with open("datasets/objective2_prediction/prediction_dataset.json", "w", encoding="utf-8") as f:
        json.dump(obj2_data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Saved {len(obj2_data['historical_changes'])} historical + {len(obj2_data['prediction_scenarios'])} prediction scenarios")
    
    # Objective 3: Verification & Reporting
    print("\n[3/3] Generating Objective 3: Verification & Reporting Dataset...")
    obj3_data = {
        "metadata": {
            "dataset_name": "Verification & Reporting Scenarios",
            "objective": "Objective 3: Transparent Verification Agent Network",
            "description": "Annotated construction scenarios with compliance reports and reasoning chains",
            "target_count": 3500,
            "cities": [c["name"] for c in CITIES],
            "categories": CATEGORIES,
            "inspection_types": INSPECTION_TYPES,
            "report_types": REPORT_TYPES,
            "generated_date": datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0"
        },
        "scenarios": []
    }
    
    for i in range(3500):
        obj3_data["scenarios"].append(generate_obj3_scenario(i + 1))
        if (i + 1) % 500 == 0:
            print(f"  Generated {i + 1}/3500 verification scenarios...")
    
    os.makedirs("datasets/objective3_verification", exist_ok=True)
    with open("datasets/objective3_verification/verification_dataset.json", "w", encoding="utf-8") as f:
        json.dump(obj3_data, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Saved {len(obj3_data['scenarios'])} verification scenarios")
    
    # Print summary
    print("\n" + "=" * 60)
    print("DATASET GENERATION COMPLETE")
    print("=" * 60)
    print(f"  Knowledge Base:    {50 + 17} laws across {len(CITIES) + 1} jurisdictions")
    print(f"  Objective 1:       {len(obj1_data['scenarios'])} conflict scenarios")
    print(f"  Objective 2:       {len(obj2_data['historical_changes'])} historical + {len(obj2_data['prediction_scenarios'])} prediction")
    print(f"  Objective 3:       {len(obj3_data['scenarios'])} verification scenarios")
    print("=" * 60)


if __name__ == "__main__":
    main()
