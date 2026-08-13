from pathlib import Path
from tempfile import TemporaryDirectory

from django.test import TestCase, override_settings


class HealthApiTests(TestCase):
    def test_health_reports_an_empty_catalogue(self):
        with TemporaryDirectory() as directory:
            with override_settings(CARD_CATALOGUE_DIR=Path(directory)):
                response = self.client.get("/api/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["catalogue"]["cards"], 0)
