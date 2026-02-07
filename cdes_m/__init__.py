"""CDES-M Python SDK

Cannabis Data Exchange Standard - Medical Extension
Bridge specification connecting CDES cannabis data to healthcare standards.

Standards Supported:
- HL7 FHIR R4 (Healthcare interoperability)
- ICD-10-CM (Diagnosis codes)
- SNOMED CT (Clinical terminology)
- LOINC (Lab observations)
- CPT (Billing codes)
- NPI (Provider identifiers)

Installation:
    pip install cdes-m

Usage:
    from cdes_m import Provider, Patient, Recommendation
    from cdes_m.fhir import provider_to_practitioner

License:
    Dual licensed:
    - Open Source: Apache 2.0 for non-commercial use
    - Commercial: Enterprise license required (contact cdes@acidni.net)

Website: https://cdes.acidni.net/cdes-m
GitHub: https://github.com/Acidni-LLC/cdes-m-sdk-python
"""

__version__ = "1.0.1"
__author__ = "Acidni LLC"
__email__ = "cdes@acidni.net"

# Core models
from .models import (
    Provider,
    Patient,
    Condition,
    Recommendation,
    EfficacyReport,
    SavedProfile,
    TreatmentProtocol,
    SecureMessage,
    MMJCertification,
    Contact,
    CannabisHistory,
    TerpeneFingerprint,
    PatientConsent,
    CannabinoidTargets,
    TargetProfile,
    DosingGuidance,
    Effectiveness,
    SymptomScore,
    SideEffectReport,
    MonitorSettings,
)

# Enumerations
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

# FHIR module available via cdes_m.fhir
from . import fhir

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    # Core models
    "Provider",
    "Patient",
    "Condition",
    "Recommendation",
    "EfficacyReport",
    "SavedProfile",
    "TreatmentProtocol",
    "SecureMessage",
    "MMJCertification",
    "Contact",
    "CannabisHistory",
    "TerpeneFingerprint",
    "PatientConsent",
    "CannabinoidTargets",
    "TargetProfile",
    "DosingGuidance",
    "Effectiveness",
    "SymptomScore",
    "SideEffectReport",
    "MonitorSettings",
    # Enums
    "ProviderLicenseType",
    "ConsumptionMethod",
    "RecommendationStatus",
    "RecommendationIntent",
    "ConditionCategory",
    "ExperienceLevel",
    "ThcTolerance",
    "Severity",
    "SideEffect",
    # FHIR module
    "fhir",
]
