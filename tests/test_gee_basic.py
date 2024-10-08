import unittest
from dataclasses import dataclass
from unittest.mock import patch

from src.gee.auth import authenticate


@dataclass
class Configuration:
    project: str
    credentials: str
    email: str
    env: str


def get_configuration():
    from src.config import (
        ENVIRONMENT,
        GOOGLE_EARTH_ENGINE_SERVICE_ACCOUNT_EMAIL,
        GOOGLE_PROJECT_ID,
    )

    return Configuration(
        project=GOOGLE_PROJECT_ID,
        credentials=ENVIRONMENT,
        email=GOOGLE_EARTH_ENGINE_SERVICE_ACCOUNT_EMAIL,
        env=ENVIRONMENT,
    )


class TestAuthenticate(unittest.TestCase):
    @patch("src.gee.auth.ee.Initialize")
    @patch("src.gee.auth.ee.Authenticate")
    @patch("src.gee.auth.ee.ServiceAccountCredentials")
    @patch("src.config.GOOGLE_PROJECT_ID", "project_mock")
    @patch("src.config.GOOGLE_EARTH_ENGINE_SERVICE_ACCOUNT_EMAIL", "email_mock")
    @patch("src.config.ENVIRONMENT", "LOCAL")
    def test_authenticate_local(
        self, mock_service_account_credentials, mock_authenticate, mock_initialize
    ):
        config = get_configuration()
        authenticate()
        mock_authenticate.assert_called_once()
        mock_initialize.assert_called_once_with(project=config.project)

    @patch("src.gee.auth.ee.Initialize")
    @patch("src.gee.auth.ee.Authenticate")
    @patch("src.gee.auth.ee.ServiceAccountCredentials")
    @patch("base64.b64decode")
    @patch("src.config.GOOGLE_PROJECT_ID", "test_project")
    @patch("src.config.GOOGLE_EARTH_ENGINE_SERVICE_ACCOUNT_EMAIL", "test_cmail")
    @patch("src.config.ENVIRONMENT", "DEVELOPMENT")
    def test_authenticate_development(
        self,
        mock_b64decode,
        mock_service_account_credentials,
        mock_authenticate,
        mock_initialize,
    ):
        config = get_configuration()
        authenticate()
        mock_service_account_credentials.assert_called_once()
        mock_initialize.assert_called_once()

    @patch("src.gee.auth.ee.Initialize")
    @patch("src.gee.auth.ee.Authenticate")
    @patch("src.gee.auth.ee.ServiceAccountCredentials")
    @patch("base64.b64decode")
    @patch("src.config.GOOGLE_PROJECT_ID", "test_project")
    @patch("src.config.GOOGLE_EARTH_ENGINE_SERVICE_ACCOUNT_EMAIL", "test_cmail")
    @patch("src.config.ENVIRONMENT", "_INVVALID_ENVIRONMENT")
    def test_authenticate_with_invalid_env(
        self,
        mock_b64decode,
        mock_service_account_credentials,
        mock_authenticate,
        mock_initialize,
    ):
        config = get_configuration()
        try:
            authenticate()
        except Exception as e:
            self.assertEqual(str(e), "Invalid environment:" + config.env)
        mock_authenticate.assert_not_called()
        mock_service_account_credentials.assert_not_called()
        mock_initialize.assert_not_called()
