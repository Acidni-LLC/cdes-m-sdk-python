"""CDES-M Enumerations"""
from enum import Enum


class ProviderLicenseType(str, Enum):
    """Types of provider licenses"""
    MD = "md"
    DO = "do"
    NP = "np"
    PA = "pa"
    APRN = "aprn"
    PHARMACIST = "pharmacist"
    OTHER = "other"


class ConsumptionMethod(str, Enum):
    """Cannabis consumption methods"""
    INHALATION_SMOKE = "inhalation_smoke"
    INHALATION_VAPE = "inhalation_vape"
    ORAL_EDIBLE = "oral_edible"
    ORAL_TINCTURE = "oral_tincture"
    ORAL_CAPSULE = "oral_capsule"
    SUBLINGUAL = "sublingual"
    TOPICAL = "topical"
    TRANSDERMAL = "transdermal"
    SUPPOSITORY = "suppository"


class RecommendationStatus(str, Enum):
    """Status of a cannabis recommendation"""
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ENTERED_IN_ERROR = "entered_in_error"


class RecommendationIntent(str, Enum):
    """Intent level of recommendation (FHIR aligned)"""
    PROPOSAL = "proposal"
    PLAN = "plan"
    ORDER = "order"


class ConditionCategory(str, Enum):
    """Categories of qualifying conditions for MMJ"""
    CHRONIC_PAIN = "chronic_pain"
    ANXIETY = "anxiety"
    PTSD = "ptsd"
    INSOMNIA = "insomnia"
    NAUSEA = "nausea"
    SEIZURES = "seizures"
    MUSCLE_SPASMS = "muscle_spasms"
    APPETITE_LOSS = "appetite_loss"
    GLAUCOMA = "glaucoma"
    CANCER = "cancer"
    HIV_AIDS = "hiv_aids"
    CROHNS = "crohns"
    PARKINSONS = "parkinsons"
    MS = "ms"
    ALS = "als"
    OTHER = "other"


class ExperienceLevel(str, Enum):
    """Patient cannabis experience level"""
    NAIVE = "naive"
    NOVICE = "novice"
    MODERATE = "moderate"
    EXPERIENCED = "experienced"


class ThcTolerance(str, Enum):
    """Patient THC tolerance level"""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class SideEffect(str, Enum):
    """Common cannabis side effects"""
    DRY_MOUTH = "dry_mouth"
    RED_EYES = "red_eyes"
    DROWSINESS = "drowsiness"
    ANXIETY = "anxiety"
    PARANOIA = "paranoia"
    DIZZINESS = "dizziness"
    HEADACHE = "headache"
    NAUSEA = "nausea"
    INCREASED_APPETITE = "increased_appetite"
    OTHER = "other"


class Severity(str, Enum):
    """Severity levels"""
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
