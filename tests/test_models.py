"""Tests for CDES-M Python SDK"""
import pytest
from datetime import date, datetime
from uuid import uuid4

from cdes_m import (
    Provider, Patient, Condition, Recommendation, EfficacyReport,
    ProviderLicenseType, ConsumptionMethod, ConditionCategory,
    RecommendationStatus, ExperienceLevel, ThcTolerance, Severity,
    TargetProfile, DosingGuidance, PatientConsent, CannabisHistory,
    Effectiveness, SideEffect
)


class TestProvider:
    """Test Provider model"""
    
    def test_create_provider_minimal(self):
        """Test creating a provider with minimal required fields"""
        provider = Provider(
            npi="1234567890",
            license_number="ME123456",
            license_state="FL",
            license_expiration=date(2026, 12, 31),
            tos_accepted=datetime.utcnow(),
            baa_signed=datetime.utcnow()
        )
        assert provider.npi == "1234567890"
        assert provider.license_state == "FL"
        assert provider.license_type == ProviderLicenseType.MD  # default
    
    def test_create_provider_full(self):
        """Test creating a provider with all fields"""
        provider = Provider(
            npi="1234567890",
            license_number="DO789012",
            license_state="FL",
            license_type=ProviderLicenseType.DO,
            license_expiration=date(2026, 12, 31),
            dea_number="AB1234567",
            specialty=["Pulmonology", "Internal Medicine"],
            organization="Pulmonary Associates of Tampa",
            tos_accepted=datetime.utcnow(),
            baa_signed=datetime.utcnow()
        )
        assert provider.license_type == ProviderLicenseType.DO
        assert "Pulmonology" in provider.specialty
        assert provider.dea_number == "AB1234567"
    
    def test_provider_npi_validation(self):
        """Test NPI validation (10 digits)"""
        with pytest.raises(ValueError):
            Provider(
                npi="12345",  # Invalid - not 10 digits
                license_number="ME123456",
                license_state="FL",
                license_expiration=date(2026, 12, 31),
                tos_accepted=datetime.utcnow(),
                baa_signed=datetime.utcnow()
            )


class TestCondition:
    """Test Condition model"""
    
    def test_create_condition_with_icd10(self):
        """Test creating a condition with ICD-10 code"""
        condition = Condition(
            icd10_code="J44.9",
            display_name="Chronic obstructive pulmonary disease",
            category=ConditionCategory.RESPIRATORY
        )
        assert condition.icd10_code == "J44.9"
        assert condition.category == ConditionCategory.RESPIRATORY
    
    def test_create_condition_with_snomed(self):
        """Test creating a condition with SNOMED code"""
        condition = Condition(
            snomed_code="13645005",
            display_name="COPD",
            category=ConditionCategory.RESPIRATORY,
            severity=Severity.MODERATE
        )
        assert condition.snomed_code == "13645005"
        assert condition.severity == Severity.MODERATE
    
    def test_icd10_validation(self):
        """Test ICD-10 code format validation"""
        # Valid ICD-10 format
        condition = Condition(
            icd10_code="C34.90",  # Lung cancer
            display_name="Lung cancer",
            category=ConditionCategory.CANCER
        )
        assert condition.icd10_code == "C34.90"


class TestPatient:
    """Test Patient model"""
    
    def test_create_patient_minimal(self):
        """Test creating a patient with minimal fields"""
        patient = Patient(
            consent=PatientConsent(consent_date=datetime.utcnow())
        )
        assert patient.id is not None
        assert patient.consent.efficacy_tracking == True  # default
    
    def test_create_patient_with_cannabis_history(self):
        """Test patient with cannabis history"""
        patient = Patient(
            mmj_card_number="MMJ12345",
            mmj_card_state="FL",
            mmj_card_expiration=date(2026, 6, 30),
            cannabis_history=CannabisHistory(
                experience_level=ExperienceLevel.EXPERIENCED,
                preferred_methods=[ConsumptionMethod.VAPORIZER, ConsumptionMethod.TINCTURE],
                thc_tolerance=ThcTolerance.MODERATE,
                sensitivities=["limonene"]
            ),
            consent=PatientConsent(
                consent_date=datetime.utcnow(),
                data_sharing=True,
                research_participation=True
            )
        )
        assert patient.cannabis_history.experience_level == ExperienceLevel.EXPERIENCED
        assert patient.consent.research_participation == True


class TestRecommendation:
    """Test Recommendation model"""
    
    def test_create_recommendation(self):
        """Test creating a recommendation"""
        patient_id = uuid4()
        provider_id = uuid4()
        condition_id = uuid4()
        
        recommendation = Recommendation(
            patient_id=patient_id,
            provider_id=provider_id,
            condition_ids=[condition_id],
            target_profile=TargetProfile(
                terpene_profile={
                    "myrcene": 0.8,
                    "caryophyllene": 0.5,
                    "limonene": 0.3
                },
                consumption_methods=[ConsumptionMethod.VAPORIZER]
            ),
            dosing_guidance=DosingGuidance(
                route=ConsumptionMethod.VAPORIZER,
                frequency="As needed, up to 3x daily",
                dose_low="2.5mg THC",
                dose_high="5mg THC",
                max_daily="15mg THC"
            ),
            rationale="High myrcene for bronchodilation"
        )
        assert recommendation.status == RecommendationStatus.DRAFT
        assert "myrcene" in recommendation.target_profile.terpene_profile
        assert recommendation.dosing_guidance.route == ConsumptionMethod.VAPORIZER


class TestEfficacyReport:
    """Test EfficacyReport model"""
    
    def test_create_efficacy_report(self):
        """Test creating an efficacy report"""
        report = EfficacyReport(
            patient_id=uuid4(),
            recommendation_id=uuid4(),
            effectiveness=Effectiveness(
                overall_rating=4,
                symptom_relief=4,
                duration_hours=4.0,
                onset_minutes=15.0,
                would_use_again=True
            )
        )
        assert report.effectiveness.overall_rating == 4
        assert report.reported_by == "patient"


class TestEnums:
    """Test enumeration values"""
    
    def test_provider_license_types(self):
        """Test all provider license types exist"""
        assert ProviderLicenseType.MD.value == "MD"
        assert ProviderLicenseType.DO.value == "DO"
        assert ProviderLicenseType.NP.value == "NP"
        assert ProviderLicenseType.PA.value == "PA"
    
    def test_consumption_methods(self):
        """Test consumption methods"""
        assert ConsumptionMethod.INHALATION.value == "inhalation"
        assert ConsumptionMethod.VAPORIZER.value == "vaporizer"
        assert ConsumptionMethod.EDIBLE.value == "edible"
        assert ConsumptionMethod.SUBLINGUAL.value == "sublingual"
    
    def test_condition_categories(self):
        """Test condition categories"""
        assert ConditionCategory.CANCER.value == "cancer"
        assert ConditionCategory.CHRONIC_PAIN.value == "chronic_pain"
        assert ConditionCategory.RESPIRATORY.value == "respiratory"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
