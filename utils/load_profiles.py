import random
from pathlib import Path

import yaml

"""
load_profiles.py - loads in cancer & molecular profiles
"""


class ProfileLoader:
    def __init__(self):
        base_dir = Path(__file__).parent.parent
        self.profiles_dir = base_dir / "config" / "profiles"
        self.all_profiles = []
        self.profile_files = []

    def load_all_profiles(self):
        self.profile_files = sorted(self.profiles_dir.glob("*.yml"))
        self.all_profiles = []

        for profile_file in self.profile_files:
            profiles = self._load_profiles_from_file(profile_file)
            self.all_profiles.extend(profiles)

        return self.all_profiles

    def load_profiles_from_files(self, filenames):
        self.all_profiles = []
        for filename in filenames:
            file_path = self.profiles_dir / filename
            if not file_path.exists():
                raise FileNotFoundError(f"Profile file not found: {file_path}")
            profiles = self._load_profiles_from_file(file_path)
            self.all_profiles.extend(profiles)
        return self.all_profiles

    def _load_profiles_from_file(self, file_path):
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)

        profiles = []
        cancer_type = file_path.stem

        for profile_id, profile_data in data.items():
            profiles.append(
                {
                    "profile_id": profile_id,
                    "cancer_type": cancer_type,
                    "source_file": file_path.name,
                    "morphology": profile_data.get("morphology", "UNKNOWN"),
                    "descriptive_name": profile_data.get("descriptive_name", ""),
                    "biomarker_profile": profile_data.get("biomarker_profile", ""),
                }
            )

        return profiles

    def get_random_profile(self):
        if not self.all_profiles:
            raise ValueError("No profiles loaded.")
        return random.choice(self.all_profiles)

    def get_sequential_profiles(self):
        if not self.all_profiles:
            raise ValueError("No profiles loaded.")
        for profile in self.all_profiles:
            yield profile

    def format_profile_prompt(self, profile):
        lines = ["## USE THIS PRIMARY CANCER PROFILE"]
        lines.append("")
        lines.append(
            f"**Primary Diagnosis that should appear verbatim in document:** {profile['descriptive_name']}"
        )
        lines.append("")
        lines.append(
            f"**Biomarker Profile - Note that these are the ONLY molecular biomarker results that should be given for this patient:** {profile['biomarker_profile']}"
        )
        lines.append("")
        return "\n".join(lines)

    def get_profile_count(self):
        return len(self.all_profiles)
