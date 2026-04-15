import requests
import logging

logger = logging.getLogger(__name__)


class FieldValidator:
    """Utility class for validating fields in nested dictionaries"""

    @staticmethod
    def validate_fields(data, fields_spec, error_prefix=""):
        """
        Validate that all specified fields exist and are not empty

        Args:
            data (dict): The data dictionary to validate
            fields_spec (list): List of field specifications
                Each item can be:
                - str: simple field name (checks top level)
                - tuple: (field_path, field_name) where field_path is dot-separated path
                Example: [
                    ("trackingNo", "Tracking Number"),
                    ("data.shopDetailData.shopHeader.shopName", "Shop Name"),
                    ("data.shopDetailData.shopHeader.momoAsk.entpCode", "Enterprise Code"),
                ]
            error_prefix (str): Prefix for error messages

        Returns:
            dict: Dictionary of {field_name: field_value} for all validated fields

        Raises:
            AssertionError: If any field is missing or empty
        """
        results = {}

        for field_spec in fields_spec:
            if isinstance(field_spec, tuple):
                field_path, field_name = field_spec
            else:
                field_path = field_spec
                field_name = field_spec

            # Navigate through nested structure
            value = data
            path_parts = field_path.split(".")

            for part in path_parts:
                if isinstance(value, dict):
                    value = value.get(part)
                else:
                    value = None
                    break

            # Validate field exists and has value
            assert value, f"{error_prefix}{field_name} (path: {field_path}) is missing or empty"

            results[field_name] = value
            logger.info(f"{field_name}: {value}")

        return results


class MomoAPIConfig:
    """Configuration for Momo API"""

    URL = "https://3pf.momo.com.tw/shop/app/info/detail/query/v1"

    HEADERS = {
        "content-type": "application/json",
        "rc": "",
        "User-Agent": "Mozilla/5.0"
    }


class MomoAPIClient:
    """Client for interacting with Momo API"""

    def __init__(self, config=None):
        """
        Initialize the Momo API Client

        Args:
            config: MomoAPIConfig instance, uses default if not provided
        """
        self.config = config or MomoAPIConfig()

    def get_shop_detail(self, entp_code):
        """
        Get shop detail information from Momo API

        Args:
            entp_code (str): Enterprise code for the shop

        Returns:
            dict: API response data

        Raises:
            AssertionError: If API response status is not 200
        """
        payload = {
            "host": "momoshop",
            "data": {
                "entpCode": entp_code
            }
        }

        logger.info(f"Fetching shop detail for entpCode: {entp_code}")
        response = requests.post(
            self.config.URL,
            headers=self.config.HEADERS,
            json=payload,
            verify=False
        )

        logger.info(f"Response status code: {response.status_code}")
        assert response.status_code == 200, f"Not 200, {response.status_code}"

        res_data = response.json()
        logger.info(f"Response received with tracking number: {res_data.get('trackingNo')}")

        return res_data
