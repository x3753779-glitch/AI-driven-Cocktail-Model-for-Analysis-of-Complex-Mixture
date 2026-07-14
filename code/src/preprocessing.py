from __future__ import annotations


class Preprocessor:
    def __init__(self, config: dict):
        self.config = config

    def run(self) -> dict:
        return {
            "normalization": self.config.get("normalization"),
            "interpolation": self.config.get("interpolation"),
            "remove_outliers": self.config.get("remove_outliers"),
        }
