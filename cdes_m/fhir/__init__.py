"""CDES-M to FHIR R4 Conversion Module

This module provides bidirectional mapping between CDES-M entities and FHIR R4 resources.
Enables interoperability with EHR systems, health information exchanges, and healthcare APIs.

FHIR Mapping Reference:
- Provider  Practitioner (R4)
- Patient  Patient (R4)  
- Condition  Condition (R4)
- Recommendation  MedicationRequest (R4)
- EfficacyReport  Observation (R4)
- SecureMessage  Communication (R4)
"""
from typing import Optional, Dict, Any, TYPE_CHECKING
from datetime import date, datetime
from uuid import UUID

# Only import fhir.resources if available (optional dependency for basic usage)
try:
    from fhir.resources.practitioner import Practitioner
    from fhir.resources.patient import Patient as FHIRPatient
    from fhir.resources.condition import Condition as FHIRCondition
    from fhir.resources.medicationrequest import MedicationRequest
    from fhir.resources.observation import Observation
    from fhir.resources.communication import Communication
    from fhir.resources.humanname import HumanName
    from fhir.resources.identifier import Identifier
    from fhir.resources.contactpoint import ContactPoint
    from fhir.resources.codeableconcept import CodeableConcept
    from fhir.resources.coding import Coding
    from fhir.resources.reference import Reference
    from fhir.resources.dosage import Dosage
    from fhir.resources.quantity import Quantity
    FHIR_AVAILABLE = True
except ImportError:
    FHIR_AVAILABLE = False
    Practitioner = Any
    FHIRPatient = Any
    FHIRCondition = Any
    MedicationRequest = Any
    Observation = Any
    Communication = Any

if TYPE_CHECKING:
    from ..models import (
        Provider, Patient, Condition, Recommendation, 
        EfficacyReport, SecureMessage
    )

# CDES-M namespace for custom identifiers
CDES_M_SYSTEM = "https://cdes.acidni.net/fhir/cdes-m"
NPI_SYSTEM = "http://hl7.org/fhir/sid/us-npi"
ICD10_SYSTEM = "http://hl7.org/fhir/sid/icd-10-cm"
SNOMED_SYSTEM = "http://snomed.info/sct"
LOINC_SYSTEM = "http://loinc.org"


def check_fhir_available():
    """Check if FHIR resources are available"""
    if not FHIR_AVAILABLE:
        raise ImportError(
            "FHIR resources not available. Install with: pip install fhir.resources>=7.0.0"
        )


def provider_to_practitioner(provider: "Provider") -> "Practitioner":
    """
    Convert CDES-M Provider to FHIR R4 Practitioner
    
    Args:
        provider: CDES-M Provider object
        
    Returns:
        FHIR R4 Practitioner resource
    """
    check_fhir_available()
    
    identifiers = [
        Identifier(
            system=CDES_M_SYSTEM,
            value=str(provider.id),
            type=CodeableConcept(
                coding=[Coding(system=CDES_M_SYSTEM, code="CDES-M-ID")]
            )
        ),
        Identifier(
            system=NPI_SYSTEM,
            value=provider.npi,
            type=CodeableConcept(
                coding=[Coding(
                    system="http://terminology.hl7.org/CodeSystem/v2-0203",
                    code="NPI",
                    display="National Provider Identifier"
                )]
            )
        ),
        Identifier(
            system=f"https://license.{provider.license_state.lower()}.gov",
            value=provider.license_number,
            type=CodeableConcept(
                coding=[Coding(
                    system="http://terminology.hl7.org/CodeSystem/v2-0203",
                    code="MD",
                    display="Medical License number"
                )]
            )
        )
    ]
    
    if provider.dea_number:
        identifiers.append(
            Identifier(
                system="https://www.deadiversion.usdoj.gov",
                value=provider.dea_number,
                type=CodeableConcept(
                    coding=[Coding(
                        system="http://terminology.hl7.org/CodeSystem/v2-0203",
                        code="DEA",
                        display="DEA Registration Number"
                    )]
                )
            )
        )
    
    telecom = []
    if provider.contact:
        if provider.contact.email:
            telecom.append(ContactPoint(system="email", value=provider.contact.email))
        if provider.contact.phone:
            telecom.append(ContactPoint(system="phone", value=provider.contact.phone))
        if provider.contact.fax:
            telecom.append(ContactPoint(system="fax", value=provider.contact.fax))
    
    return Practitioner(
        id=str(provider.id),
        identifier=identifiers,
        active=True,
        telecom=telecom if telecom else None,
        qualification=[
            {
                "identifier": [
                    {
                        "system": f"https://license.{provider.license_state.lower()}.gov",
                        "value": provider.license_number
                    }
                ],
                "code": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/v2-0360",
                            "code": provider.license_type.value,
                            "display": provider.license_type.name
                        }
                    ]
                },
                "period": {
                    "end": provider.license_expiration.isoformat()
                }
            }
        ]
    )


def patient_to_fhir(patient: "Patient") -> "FHIRPatient":
    """
    Convert CDES-M Patient to FHIR R4 Patient
    
    Args:
        patient: CDES-M Patient object
        
    Returns:
        FHIR R4 Patient resource
    """
    check_fhir_available()
    
    identifiers = [
        Identifier(
            system=CDES_M_SYSTEM,
            value=str(patient.id),
            type=CodeableConcept(
                coding=[Coding(system=CDES_M_SYSTEM, code="CDES-M-ID")]
            )
        )
    ]
    
    if patient.mrn:
        identifiers.append(
            Identifier(
                system="http://hospital.example.org/mrn",
                value=patient.mrn,
                type=CodeableConcept(
                    coding=[Coding(
                        system="http://terminology.hl7.org/CodeSystem/v2-0203",
                        code="MR",
                        display="Medical Record Number"
                    )]
                )
            )
        )
    
    if patient.mmj_card_number and patient.mmj_card_state:
        identifiers.append(
            Identifier(
                system=f"https://mmj.{patient.mmj_card_state.lower()}.gov",
                value=patient.mmj_card_number,
                type=CodeableConcept(
                    coding=[Coding(system=CDES_M_SYSTEM, code="MMJ-CARD")]
                ),
                period={"end": patient.mmj_card_expiration.isoformat()} if patient.mmj_card_expiration else None
            )
        )
    
    return FHIRPatient(
        id=str(patient.id),
        identifier=identifiers,
        active=True,
        gender=patient.gender,
        birthDate=patient.birth_date.isoformat() if patient.birth_date else None,
        address=[{"postalCode": patient.zip_code}] if patient.zip_code else None
    )


def condition_to_fhir(condition: "Condition", patient_id: UUID) -> "FHIRCondition":
    """
    Convert CDES-M Condition to FHIR R4 Condition
    
    Args:
        condition: CDES-M Condition object
        patient_id: UUID of the patient
        
    Returns:
        FHIR R4 Condition resource
    """
    check_fhir_available()
    
    coding = []
    
    if condition.icd10_code:
        coding.append(
            Coding(
                system=ICD10_SYSTEM,
                code=condition.icd10_code,
                display=condition.display_name
            )
        )
    
    if condition.snomed_code:
        coding.append(
            Coding(
                system=SNOMED_SYSTEM,
                code=condition.snomed_code,
                display=condition.display_name
            )
        )
    
    return FHIRCondition(
        id=str(condition.id),
        identifier=[
            Identifier(system=CDES_M_SYSTEM, value=str(condition.id))
        ],
        clinicalStatus=CodeableConcept(
            coding=[Coding(
                system="http://terminology.hl7.org/CodeSystem/condition-clinical",
                code="active"
            )]
        ),
        category=[
            CodeableConcept(
                coding=[Coding(
                    system=CDES_M_SYSTEM + "/condition-category",
                    code=condition.category.value,
                    display=condition.category.name.replace("_", " ").title()
                )]
            )
        ],
        severity=CodeableConcept(
            coding=[Coding(
                system="http://snomed.info/sct",
                code=_severity_to_snomed(condition.severity.value) if condition.severity else "6736007",
                display=condition.severity.value.title() if condition.severity else "Moderate"
            )]
        ) if condition.severity else None,
        code=CodeableConcept(coding=coding, text=condition.display_name),
        subject=Reference(reference=f"Patient/{patient_id}"),
        onsetDateTime=condition.onset_date.isoformat() if condition.onset_date else None
    )


def recommendation_to_medication_request(
    recommendation: "Recommendation",
    patient_id: UUID,
    provider_id: UUID
) -> "MedicationRequest":
    """
    Convert CDES-M Recommendation to FHIR R4 MedicationRequest
    
    Note: Cannabis recommendations map to MedicationRequest with specific
    coding to indicate this is a cannabis recommendation rather than 
    a traditional prescription.
    
    Args:
        recommendation: CDES-M Recommendation object
        patient_id: UUID of the patient
        provider_id: UUID of the provider
        
    Returns:
        FHIR R4 MedicationRequest resource
    """
    check_fhir_available()
    
    # Build dosage instructions
    dosage_instruction = None
    if recommendation.dosing_guidance:
        dg = recommendation.dosing_guidance
        dosage_instruction = [
            Dosage(
                route=CodeableConcept(
                    coding=[Coding(
                        system=CDES_M_SYSTEM + "/consumption-method",
                        code=dg.route.value if dg.route else "oral",
                        display=dg.route.value.replace("_", " ").title() if dg.route else "Oral"
                    )]
                ) if dg.route else None,
                timing={"code": {"text": dg.frequency}} if dg.frequency else None,
                doseAndRate=[
                    {
                        "doseRange": {
                            "low": {"value": float(dg.dose_low.replace("mg", "").strip()), "unit": "mg"} if dg.dose_low else None,
                            "high": {"value": float(dg.dose_high.replace("mg", "").strip()), "unit": "mg"} if dg.dose_high else None
                        }
                    }
                ] if dg.dose_low or dg.dose_high else None,
                maxDosePerPeriod={
                    "numerator": {"value": float(dg.max_daily.replace("mg", "").strip()), "unit": "mg"},
                    "denominator": {"value": 1, "unit": "d"}
                } if dg.max_daily else None,
                patientInstruction=dg.special_instructions
            )
        ]
    
    return MedicationRequest(
        id=str(recommendation.id),
        identifier=[
            Identifier(system=CDES_M_SYSTEM, value=str(recommendation.id))
        ],
        status=recommendation.status.value.lower(),
        intent=recommendation.intent.value.lower(),
        category=[
            CodeableConcept(
                coding=[Coding(
                    system=CDES_M_SYSTEM,
                    code="cannabis-recommendation",
                    display="Cannabis Recommendation"
                )]
            )
        ],
        medicationCodeableConcept=CodeableConcept(
            coding=[Coding(
                system=CDES_M_SYSTEM + "/terpene-profile",
                code="custom-profile",
                display="Custom Cannabis Profile"
            )],
            text=f"Cannabis profile with target terpenes: {', '.join(recommendation.target_profile.terpene_profile.keys())}"
        ),
        subject=Reference(reference=f"Patient/{patient_id}"),
        requester=Reference(reference=f"Practitioner/{provider_id}"),
        reasonReference=[
            Reference(reference=f"Condition/{cid}") 
            for cid in recommendation.condition_ids
        ] if recommendation.condition_ids else None,
        dosageInstruction=dosage_instruction,
        note=[{"text": recommendation.rationale}] if recommendation.rationale else None,
        dispenseRequest={
            "validityPeriod": {
                "start": recommendation.valid_from.isoformat() if recommendation.valid_from else None,
                "end": recommendation.valid_until.isoformat() if recommendation.valid_until else None
            }
        } if recommendation.valid_from or recommendation.valid_until else None
    )


def efficacy_report_to_observation(
    report: "EfficacyReport",
    patient_id: UUID
) -> "Observation":
    """
    Convert CDES-M EfficacyReport to FHIR R4 Observation (Patient-Reported Outcome)
    
    Args:
        report: CDES-M EfficacyReport object
        patient_id: UUID of the patient
        
    Returns:
        FHIR R4 Observation resource
    """
    check_fhir_available()
    
    components = []
    
    # Overall effectiveness
    components.append({
        "code": CodeableConcept(
            coding=[Coding(
                system=CDES_M_SYSTEM + "/efficacy",
                code="overall-rating",
                display="Overall Effectiveness Rating"
            )]
        ),
        "valueInteger": report.effectiveness.overall_rating
    })
    
    # Symptom relief
    if report.effectiveness.symptom_relief:
        components.append({
            "code": CodeableConcept(
                coding=[Coding(
                    system=CDES_M_SYSTEM + "/efficacy",
                    code="symptom-relief",
                    display="Symptom Relief Rating"
                )]
            ),
            "valueInteger": report.effectiveness.symptom_relief
        })
    
    # Symptom scores
    for score in report.symptom_scores:
        components.append({
            "code": CodeableConcept(
                coding=[Coding(
                    system=CDES_M_SYSTEM + "/symptom",
                    code=score.symptom.lower().replace(" ", "-"),
                    display=score.symptom
                )]
            ),
            "valueQuantity": Quantity(
                value=score.improvement,
                unit="points",
                system="http://unitsofmeasure.org"
            )
        })
    
    return Observation(
        id=str(report.id),
        identifier=[
            Identifier(system=CDES_M_SYSTEM, value=str(report.id))
        ],
        status="final",
        category=[
            CodeableConcept(
                coding=[Coding(
                    system="http://terminology.hl7.org/CodeSystem/observation-category",
                    code="survey",
                    display="Survey"
                )]
            )
        ],
        code=CodeableConcept(
            coding=[
                Coding(
                    system=LOINC_SYSTEM,
                    code="77580-4",
                    display="Patient reported outcome measure"
                ),
                Coding(
                    system=CDES_M_SYSTEM,
                    code="cannabis-efficacy-report",
                    display="Cannabis Efficacy Report"
                )
            ]
        ),
        subject=Reference(reference=f"Patient/{patient_id}"),
        effectiveDateTime=report.reported_at.isoformat(),
        performer=[Reference(reference=f"Patient/{patient_id}")],
        basedOn=[Reference(reference=f"MedicationRequest/{report.recommendation_id}")],
        component=components,
        note=[{"text": report.notes}] if report.notes else None
    )


def _severity_to_snomed(severity: str) -> str:
    """Map CDES-M severity to SNOMED CT codes"""
    mapping = {
        "mild": "255604002",
        "moderate": "6736007",
        "severe": "24484000",
        "critical": "442452003"
    }
    return mapping.get(severity.lower(), "6736007")


# Export all conversion functions
__all__ = [
    "FHIR_AVAILABLE",
    "check_fhir_available",
    "provider_to_practitioner",
    "patient_to_fhir",
    "condition_to_fhir",
    "recommendation_to_medication_request",
    "efficacy_report_to_observation",
    "CDES_M_SYSTEM",
    "NPI_SYSTEM",
    "ICD10_SYSTEM",
    "SNOMED_SYSTEM",
    "LOINC_SYSTEM",
]
