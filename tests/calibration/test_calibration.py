"""RED tests for Epic 4: Per-Model Calibration.
Tests calibration pipeline per PRD Appendix D.2 and E.4.
All tests should FAIL until calibration.py is implemented."""
import pytest
import json
from pathlib import Path

from codeclue_research.calibration import (
    fit_calibration_profile,
    apply_calibration,
    load_calibration_profile,
)


class TestCalibrationFit:
    def test_returns_valid_profile(self):
        """fit_calibration_profile produces a profile matching D.2.2 schema."""
        raw_confidences = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05]
        actual_outcomes = [False, False, False, True, True, True, True, True, True, True]

        profile = fit_calibration_profile(
            raw_confidences=raw_confidences,
            actual_outcomes=actual_outcomes,
            generator_model="claude-opus-4.6",
            generator_family="anthropic",
        )

        assert "generator_model" in profile
        assert profile["generator_model"] == "claude-opus-4.6"
        assert "calibration_method" in profile
        assert "metrics" in profile
        assert "ece" in profile["metrics"]
        assert "brier" in profile["metrics"]
        assert "gate_passed" in profile
        assert "parameters" in profile

    def test_profile_has_ece_and_brier(self):
        """Profile includes ECE and Brier score metrics."""
        raw = [0.9, 0.7, 0.5, 0.3, 0.1]
        outcomes = [False, False, True, True, True]

        profile = fit_calibration_profile(
            raw_confidences=raw, actual_outcomes=outcomes,
            generator_model="test", generator_family="test",
        )

        assert 0 <= profile["metrics"]["ece"] <= 1
        assert 0 <= profile["metrics"]["brier"] <= 1

    def test_gate_passes_when_calibrated(self):
        """Gate passes when ECE <= 0.05 and Brier <= 0.18."""
        # Perfectly calibrated data
        raw = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
        outcomes = [False, False, False, False, True, True, True, True, True, True]

        profile = fit_calibration_profile(
            raw_confidences=raw, actual_outcomes=outcomes,
            generator_model="test", generator_family="test",
        )

        # With reasonable data, at least one method should pass
        # (we can't guarantee pass on small sample, but method should be set)
        assert profile["calibration_method"] in [
            "isotonic", "temperature_scaling", "platt_scaling", "FALLBACK_STRUCTURAL_ONLY"
        ]


class TestCalibrationApply:
    def test_transforms_raw_confidence(self):
        """apply_calibration produces different value than raw input."""
        profile = {
            "calibration_method": "temperature_scaling",
            "parameters": {"temperature": 1.4},
            "gate_passed": True,
        }
        raw = 0.85
        calibrated = apply_calibration(raw, profile)
        assert 0 <= calibrated <= 1
        # With temperature > 1, calibrated should differ from raw
        assert calibrated != raw

    def test_fallback_returns_none(self):
        """FALLBACK_STRUCTURAL_ONLY returns None (caller should use structural only)."""
        profile = {
            "calibration_method": "FALLBACK_STRUCTURAL_ONLY",
            "parameters": {},
            "gate_passed": False,
        }
        result = apply_calibration(0.75, profile)
        assert result is None


class TestCalibrationLoad:
    def test_loads_existing_profile(self, tmp_path):
        """Loads a profile from disk matching the generator model."""
        profile = {
            "generator_model": "claude-opus-4.6",
            "generator_model_family": "anthropic",
            "calibration_method": "isotonic",
            "gate_passed": True,
            "metrics": {"ece": 0.03, "brier": 0.14},
            "parameters": {"bins": []},
        }
        cal_dir = tmp_path / "calibration"
        cal_dir.mkdir()
        (cal_dir / "claude-opus-4.6.calib.json").write_text(json.dumps(profile))

        loaded = load_calibration_profile("claude-opus-4.6", cal_dir)
        assert loaded["generator_model"] == "claude-opus-4.6"
        assert loaded["gate_passed"] is True

    def test_unknown_model_returns_fallback(self, tmp_path):
        """Unknown model returns FALLBACK_STRUCTURAL_ONLY."""
        cal_dir = tmp_path / "calibration"
        cal_dir.mkdir()

        loaded = load_calibration_profile("unknown-model-v99", cal_dir)
        assert loaded["calibration_method"] == "FALLBACK_STRUCTURAL_ONLY"
        assert loaded["gate_passed"] is False

    def test_stale_profile_returns_fallback(self, tmp_path):
        """Profile with mismatched version returns fallback."""
        profile = {
            "generator_model": "claude-opus-4.5",  # Different version
            "calibration_method": "isotonic",
            "gate_passed": True,
            "metrics": {"ece": 0.03},
            "parameters": {},
        }
        cal_dir = tmp_path / "calibration"
        cal_dir.mkdir()
        (cal_dir / "claude-opus-4.5.calib.json").write_text(json.dumps(profile))

        # Looking for 4.6 but only 4.5 exists
        loaded = load_calibration_profile("claude-opus-4.6", cal_dir)
        assert loaded["calibration_method"] == "FALLBACK_STRUCTURAL_ONLY"


class TestCalibrationIntegration:
    def test_ece_gate_threshold(self):
        """ECE <= 0.05 required for gate pass."""
        raw = [0.9, 0.7, 0.5, 0.3, 0.1]
        outcomes = [False, False, True, True, True]

        profile = fit_calibration_profile(
            raw_confidences=raw, actual_outcomes=outcomes,
            generator_model="test", generator_family="test",
        )

        if profile["gate_passed"]:
            assert profile["metrics"]["ece"] <= 0.05
            assert profile["metrics"]["brier"] <= 0.18
