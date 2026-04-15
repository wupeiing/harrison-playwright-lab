import logging
from jsonschema import validate, ValidationError
from momo_client import MomoAPIClient, FieldValidator

logger = logging.getLogger(__name__)

# Define the schema for Momo API response
MOMO_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["success", "resultCode", "resultMessage", "timestamp", "trackingNo", "data"],
    "properties": {
        "success": {"type": "boolean"},
        "resultCode": {"type": "string"},
        "resultMessage": {"type": "string"},
        "resultException": {"type": "string"},
        "timestamp": {"type": "string"},
        "trackingNo": {"type": "string"},
        "data": {
            "type": "object",
            "required": ["shopDetailData"],
            "properties": {
                "shopDetailData": {
                    "type": "object",
                    "required": ["shopHeader", "shopInfo"],
                    "properties": {
                        "shopHeader": {
                            "type": "object",
                            "required": ["shopName", "shopIcon", "shopFitRate", "commentCount", "isFollow"],
                            "properties": {
                                "shopNamsse": {"type": "string"},
                                "shopIcon": {"type": "string"},
                                "shopFitRate": {"type": "string"},
                                "commentCount": {"type": "string"},
                                "followCount": {"type": "string"},
                                "isFollow": {"type": "boolean"},
                                "backgroundURL": {"type": "string"},
                                "crossBorderShop": {"type": "string"},
                                "momoAsk": {
                                    "type": "object",
                                    "required": ["entpCode", "deliveryType"],
                                    "properties": {
                                        "entpCode": {"type": "string"},
                                        "deliveryType": {"type": "string"},
                                        "allowReply": {"type": "boolean"}
                                    }
                                }
                            }
                        },
                        "shopInfo": {
                            "type": "object",
                            "required": ["askResponseRate", "shopIntro"],
                            "properties": {
                                "askResponseRate": {"type": "string"},
                                "shopIntro": {"type": "string"},
                                "stockCount": {"type": "string"},
                                "shopCreateDate": {"type": "string"},
                                "companyName": {"type": "string"},
                                "taxId": {"type": "string"},
                                "shopURL": {"type": "string"},
                                "displayShopURL": {"type": "string"},
                                "hasComments": {"type": "boolean"},
                                "returnInfo": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "paragraphType": {"type": "string"},
                                            "title": {"type": "string"},
                                            "content": {
                                                "type": "array",
                                                "items": {"type": "string"}
                                            }
                                        }
                                    }
                                },
                                "defectiveRateInfo": {
                                    "type": "object",
                                    "properties": {
                                        "defectiveRate": {"type": "string"},
                                        "hidden": {"type": "boolean"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "ConsumerExecuteTime": {"type": "string"},
        "inQueueWaitTime": {"type": "string"},
        "finishDateTime": {"type": "string"}
    }
}


class TestMomo:

    def setup_method(self):
        """Setup test fixtures"""
        self.client = MomoAPIClient()
        self.entp_code = "TP0007070"

    def test_run_api(self):
        """Test basic API call and key field presence"""
        res_contact = self.client.get_shop_detail(self.entp_code)
        logger.info(res_contact)

        tracking_no = res_contact.get("trackingNo", None)
        assert tracking_no is not None and isinstance(tracking_no, str)

        # key field is not empty
        store_name = res_contact.get("data", None).get("shopDetailData", None).get("shopHeader", None).get("shopName", None)
        logger.info(store_name)
        entp_code = res_contact.get("data", None).get("shopDetailData", None).get("shopHeader", None).get("momoAsk", None).get("entpCode", None)
        logger.info(entp_code)

        assert store_name and entp_code, "store name or entpcode is not there"

    def test_schema_validation(self):
        """Validate the Momo API response against the defined schema"""
        res_data = self.client.get_shop_detail(self.entp_code)
        logger.info("Response received, validating schema...")

        try:
            validate(instance=res_data, schema=MOMO_RESPONSE_SCHEMA)
            logger.info("Schema validation passed!")
        except ValidationError as e:
            logger.error(f"Schema validation failed: {e.message}")
            raise AssertionError(f"Response does not match schema: {e.message}")

        # Validate top-level fields
        assert res_data.get("success") is True, "success should be true"
        assert res_data.get("resultCode") == "200", "resultCode should be 200"

        # Define required fields with their display names
        required_fields = [
            ("trackingNo", "Tracking Number"),
            ("data.shopDetailData.shopHeader.shopName", "Shop Name"),
            ("data.shopDetailData.shopHeader.shopIcon", "Shop Icon"),
            ("data.shopDetailData.shopHeader.shopFitRate", "Shop Fit Rate"),
            ("data.shopDetailData.shopHeader.momoAsk.entpCode", "Enterprise Code"),
            ("data.shopDetailData.shopHeader.momoAsk.deliveryType", "Delivery Type"),
            ("data.shopDetailData.shopInfo.askResponseRate", "Ask Response Rate"),
            ("data.shopDetailData.shopInfo.shopIntro", "Shop Introduction"),
            ("data.shopDetailData.shopInfo.companyName", "Company Name"),
            ("data.shopDetailData.shopInfo.taxId", "Tax ID"),
        ]

        logger.info("Validating key fields...")
        validated_fields = FieldValidator.validate_fields(res_data, required_fields)
        logger.info("All field validations passed!")



        