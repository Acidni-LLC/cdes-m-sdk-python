"""CDES-M Pydantic Models"""
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, EmailStr

from .enums import (
    ProviderLicenseType,
    ConsumptionMethod,
    RecommendationStatus,
    RecommendationIntent,
    ConditionCategory,
    ExperienceLevel,
    ThcTolerance,
    Severity,
    SideEffect,
)


class MMJCertification(BaseModel):
    """MMJ certification details"""
    state: str
    certification_number: str
    expiration: date
    authorized_to_recommend: bool = True


class Contact(BaseModel):
    """Contact information"""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    fax: Optional[str] = None


class Provider(BaseModel):
    """A licensed healthcare provider authorized to recommend cannabis"""
    id: UUID = Field(default_factory=uuid4)
    fhir_practitioner_id: Optional[str] = None
    npi: str = Field(..., pattern=r"^[0-9]{10}$", description="National Provider Identifier")
    license_number: str
    license_state: str = Field(..., pattern=r"^[A-Z]{2}$")
    license_type: ProviderLicenseType = ProviderLicenseType.MD
    license_expiration: date
    dea_number: Optional[str] = None
    mmj_certification: Optional[MMJCertification] = None
    specialty: List[str] = Field(default_factory=list)
    organization: Optional[str] = None
    contact: Optional[Contact] = None
    tos_accepted: datetime
    baa_signed: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Condition(BaseModel):
    """A medical condition with ICD-10-CM coding"""
    id: UUID = Field(default_factory=uuid4)
    fhir_condition_id: Optional[str] = None
    icd10_code: Optional[str] = Field(None, pattern=r"^[A-Z][0-9]{2}(\.[0-9A-Z]{1,4})?$")
    snomed_code: Optional[str] = None
    display_name: str
    category: ConditionCategory
    severity: Optional[Severity] = None
    onset_date: Optional[date] = None
    is_qualifying: bool = True


class CannabisHistory(BaseModel):
    """Patient cannabis use history"""
    experience_level: ExperienceLevel = ExperienceLevel.NAIVE
    preferred_methods: List[ConsumptionMethod] = Field(default_factory=list)
    thc_tolerance: ThcTolerance = ThcTolerance.LOW
    sensitivities: List[str] = Field(default_factory=list)
    previous_strains: List[str] = Field(default_factory=list)


class TerpeneFingerprint(BaseModel):
    """Patient personalized terpene response profile"""
    positive_effects: List[str] = Field(default_factory=list)
    negative_effects: List[str] = Field(default_factory=list)
    neutral: List[str] = Field(default_factory=list)


class PatientConsent(BaseModel):
    """Patient consent preferences"""
    data_sharing: bool = False
    research_participation: bool = False
    efficacy_tracking: bool = True
    fhir_export: bool = False
    consent_date: datetime
    consent_version: str = "1.0"


class Patient(BaseModel):
    """A patient receiving cannabis recommendations (PHI - HIPAA Protected)"""
    id: UUID = Field(default_factory=uuid4)
    fhir_patient_id: Optional[str] = None
    mrn: Optional[str] = None
    mmj_card_number: Optional[str] = None
    mmj_card_state: Optional[str] = Field(None, pattern=r"^[A-Z]{2}$")
    mmj_card_expiration: Optional[date] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    zip_code: Optional[str] = None
    conditions: List[Condition] = Field(default_factory=list)
    allergies: List[str] = Field(default_factory=list)
    cannabis_history: Optional[CannabisHistory] = None
    terpene_fingerprint: Optional[TerpeneFingerprint] = None
    consent: PatientConsent
    primary_provider_id: Optional[UUID] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CannabinoidTargets(BaseModel):
    """Target cannabinoid ranges"""
    thc_min: Optional[float] = None
    thc_max: Optional[float] = None
    cbd_min: Optional[float] = None
    cbd_max: Optional[float] = None
    ratio_thc_cbd: Optional[str] = None


class TargetProfile(BaseModel):
    """Target terpene/cannabinoid profile for recommendations"""
    terpene_profile: Dict[str, float] = Field(default_factory=dict)
    cannabinoid_targets: Optional[CannabinoidTargets] = None
    product_categories: List[str] = Field(default_factory=list)
    consumption_methods: List[ConsumptionMethod] = Field(default_factory=list)


class DosingGuidance(BaseModel):
    """Dosing instructions"""
    route: Optional[ConsumptionMethod] = None
    frequency: Optional[str] = None
    dose_low: Optional[str] = None
    dose_high: Optional[str] = None
    max_daily: Optional[str] = None
    titration_instructions: Optional[str] = None
    special_instructions: Optional[str] = None


class Recommendation(BaseModel):
    """A provider recommendation of a cannabis product/profile for a patient"""
    id: UUID = Field(default_factory=uuid4)
    fhir_medication_request_id: Optional[str] = None
    patient_id: UUID
    provider_id: UUID
    status: RecommendationStatus = RecommendationStatus.DRAFT
    intent: RecommendationIntent = RecommendationIntent.PROPOSAL
    condition_ids: List[UUID] = Field(default_factory=list)
    target_profile: TargetProfile
    dosing_guidance: Optional[DosingGuidance] = None
    rationale: Optional[str] = None
    contraindications_reviewed: bool = False
    drug_interactions_reviewed: bool = False
    valid_from: Optional[date] = None
    valid_until: Optional[date] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    signed_at: Optional[datetime] = None


class Effectiveness(BaseModel):
    """Effectiveness ratings"""
    overall_rating: int = Field(..., ge=1, le=5)
    symptom_relief: Optional[int] = Field(None, ge=1, le=5)
    duration_hours: Optional[float] = None
    onset_minutes: Optional[float] = None
    would_use_again: Optional[bool] = None
    would_recommend: Optional[bool] = None


class SymptomScore(BaseModel):
    """Individual symptom tracking"""
    condition_id: Optional[UUID] = None
    symptom: str
    score_before: int = Field(..., ge=0, le=10)
    score_after: int = Field(..., ge=0, le=10)
    improvement: int = Field(..., ge=-10, le=10)


class SideEffectReport(BaseModel):
    """Reported side effect"""
    effect: SideEffect
    severity: Severity
    duration_hours: Optional[float] = None
    notes: Optional[str] = None


class EfficacyReport(BaseModel):
    """Patient-reported outcome for tracking treatment effectiveness"""
    id: UUID = Field(default_factory=uuid4)
    fhir_observation_id: Optional[str] = None
    patient_id: UUID
    recommendation_id: UUID
    product_used: Optional[Dict[str, Any]] = None
    consumption: Optional[Dict[str, Any]] = None
    effectiveness: Effectiveness
    symptom_scores: List[SymptomScore] = Field(default_factory=list)
    side_effects: List[SideEffectReport] = Field(default_factory=list)
    notes: Optional[str] = None
    reported_at: datetime = Field(default_factory=datetime.utcnow)
    reported_by: str = "patient"


class MonitorSettings(BaseModel):
    """Background monitoring settings for saved profiles"""
    enabled: bool = False
    notify_on_match: bool = True
    notify_on_price_drop: bool = False
    notify_on_back_in_stock: bool = False
    check_frequency: str = "daily"
    notification_channels: List[str] = Field(default_factory=lambda: ["email"])


class SavedProfile(BaseModel):
    """A saved search profile for ongoing product matching"""
    id: UUID = Field(default_factory=uuid4)
    provider_id: UUID
    patient_id: Optional[UUID] = None
    name: str
    description: Optional[str] = None
    target_profile: TargetProfile
    monitor_settings: Optional[MonitorSettings] = None
    last_match_count: int = 0
    last_checked: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TreatmentProtocol(BaseModel):
    """Evidence-based mapping of conditions to cannabis profiles"""
    id: UUID = Field(default_factory=uuid4)
    name: str
    version: str = "1.0"
    status: str = "draft"
    condition_category: ConditionCategory
    icd10_codes: List[str] = Field(default_factory=list)
    description: Optional[str] = None
    evidence_level: str = "anecdotal"
    recommended_profile: TargetProfile
    dosing_guidance: Optional[DosingGuidance] = None
    contraindications: List[str] = Field(default_factory=list)
    drug_interactions: List[str] = Field(default_factory=list)
    references: List[Dict[str, str]] = Field(default_factory=list)
    created_by: Optional[str] = None
    approved_by: Optional[str] = None
    effective_date: Optional[date] = None
    review_date: Optional[date] = None


class SecureMessage(BaseModel):
    """HIPAA-compliant provider-patient communication"""
    id: UUID = Field(default_factory=uuid4)
    fhir_communication_id: Optional[str] = None
    thread_id: UUID
    sender_type: str
    sender_id: UUID
    recipient_type: str
    recipient_id: UUID
    subject: Optional[str] = None
    body: str
    attachments: List[Dict[str, Any]] = Field(default_factory=list)
    related_recommendation_id: Optional[UUID] = None
    priority: str = "routine"
    status: str = "sent"
    read_at: Optional[datetime] = None
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
