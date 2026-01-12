# CDES-M Python SDK

[![PyPI version](https://badge.fury.io/py/cdes-m.svg)](https://pypi.org/project/cdes-m/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0%20%2F%20Commercial-green.svg)](LICENSE)

**Cannabis Data Exchange Standard - Medical Extension**

A Python SDK implementing CDES-M, the bridge specification connecting cannabis data 
(CDES) to established healthcare interoperability standards.

## Overview

CDES-M extends the [Cannabis Data Exchange Standard (CDES)](https://cdes.acidni.net) 
with medical-specific entities and mappings to healthcare standards:

| CDES-M Entity | FHIR R4 Resource | Healthcare Codes |
|---------------|------------------|------------------|
| Provider | Practitioner | NPI, State License, DEA |
| Patient | Patient | MRN, MMJ Card |
| Condition | Condition | ICD-10-CM, SNOMED CT |
| Recommendation | MedicationRequest | Custom cannabis profile |
| EfficacyReport | Observation | LOINC PRO codes |

## Installation

```bash
pip install cdes-m
```

For FHIR conversion support:
```bash
pip install cdes-m[fhir]
```

## Quick Start

```python
from datetime import date, datetime
from cdes_m import (
    Provider, Patient, Condition, Recommendation,
    ProviderLicenseType, ConditionCategory, ConsumptionMethod
)

# Create a provider
provider = Provider(
    npi="1234567890",
    license_number="ME123456",
    license_state="FL",
    license_type=ProviderLicenseType.MD,
    license_expiration=date(2026, 12, 31),
    specialty=["Pulmonology"],
    tos_accepted=datetime.utcnow(),
    baa_signed=datetime.utcnow()
)

# Create a patient condition
copd = Condition(
    icd10_code="J44.9",
    snomed_code="13645005",
    display_name="Chronic obstructive pulmonary disease",
    category=ConditionCategory.RESPIRATORY
)

# Create a recommendation
from cdes_m import TargetProfile, DosingGuidance

recommendation = Recommendation(
    patient_id=patient.id,
    provider_id=provider.id,
    condition_ids=[copd.id],
    target_profile=TargetProfile(
        terpene_profile={"myrcene": 0.8, "caryophyllene": 0.5, "limonene": 0.3},
        consumption_methods=[ConsumptionMethod.VAPORIZER]
    ),
    dosing_guidance=DosingGuidance(
        route=ConsumptionMethod.VAPORIZER,
        frequency="As needed, up to 3x daily",
        dose_low="2.5mg THC",
        dose_high="5mg THC"
    ),
    rationale="High myrcene for anti-inflammatory, caryophyllene for bronchodilation"
)
```

## FHIR Conversion

Convert CDES-M entities to FHIR R4 resources:

```python
from cdes_m.fhir import (
    provider_to_practitioner,
    patient_to_fhir,
    condition_to_fhir,
    recommendation_to_medication_request,
    efficacy_report_to_observation
)

# Convert provider to FHIR Practitioner
practitioner = provider_to_practitioner(provider)
print(practitioner.json(indent=2))

# Convert to FHIR MedicationRequest
med_request = recommendation_to_medication_request(
    recommendation, patient.id, provider.id
)
```

## Core Entities

### Provider
Licensed healthcare provider with NPI, state license, optional DEA number, 
and MMJ certification.

### Patient (PHI - HIPAA Protected)
Medical marijuana patient with conditions, cannabis history, 
terpene fingerprint, and consent preferences.

### Condition
Medical condition with ICD-10-CM and SNOMED CT coding.

### Recommendation
Provider recommendation including target terpene/cannabinoid profile 
and dosing guidance.

### EfficacyReport
Patient-reported outcome tracking treatment effectiveness.

### TreatmentProtocol
Evidence-based mapping of conditions to recommended cannabis profiles.

## Standards Mapping

CDES-M bridges to these healthcare standards:

| Standard | Purpose | CDES-M Usage |
|----------|---------|--------------|
| **FHIR R4** | Healthcare interoperability | Full resource mapping |
| **ICD-10-CM** | Diagnosis codes | Condition.icd10_code |
| **SNOMED CT** | Clinical terminology | Condition.snomed_code |
| **NPI** | Provider identification | Provider.npi |
| **LOINC** | Lab observations | EfficacyReport codes |

## Licensing

**Dual Licensed:**

- **Apache 2.0**: Free for non-commercial, research, and educational use
- **Commercial License**: Required for commercial applications

Contact [cdes@acidni.net](mailto:cdes@acidni.net) for commercial licensing.

## Resources

- **Website**: [https://cdes.acidni.net/cdes-m](https://cdes.acidni.net/cdes-m)
- **Specification**: [https://github.com/Acidni-LLC/cdes-m-spec](https://github.com/Acidni-LLC/cdes-m-spec)
- **CDES Core**: [https://cdes.acidni.net](https://cdes.acidni.net)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## Support

- **GitHub Issues**: Bug reports and feature requests
- **Email**: [cdes@acidni.net](mailto:cdes@acidni.net)
- **Community**: Join our working groups (see specification)

---

** 2025 Acidni LLC** - Advancing cannabis data interoperability
