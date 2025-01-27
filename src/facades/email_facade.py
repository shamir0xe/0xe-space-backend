import logging
from src.factories.email_template_key_factory import EmailTemplateKeyFactory
from src.orchestrators.backbone_server import BackboneServer
from src.models.general import General
from src.repositories.general_repository import GeneralRepository
from src.types.email_templates import EmailTemplates

LOGGER = logging.getLogger(__name__)


class EmailFacade:
    @staticmethod
    def send(email: str, template: EmailTemplates, **kwargs) -> str:
        """Delegate the sending email to the email-sender server"""
        # Read the required template
        general, _ = GeneralRepository(General).read_by_key(
            EmailTemplateKeyFactory(template).create()
        )
        body = general.value
        title = ""
        if template is EmailTemplates.VERIFICATION_CODE:
            if not ("code" in kwargs and "username" in kwargs and "user_id" in kwargs):
                raise Exception("Need to provide code as an argument")
            code = kwargs["code"]
            username = kwargs["username"]
            user_id = kwargs["user_id"]
            validating_hash = "#"

            body = body.replace("{code}", code)
            body = body.replace("{user_id}", user_id)
            body = body.replace("{username}", username)
            body = body.replace("{validating_hash}", validating_hash)
            LOGGER.info(body)

            title = "Verification Code"
        response = BackboneServer().send_mail(email=email, body=body, title=title)
        if response.status == 200:
            return "Sent Successfully"
        # Failed
        return f"Failure: {response.message}"
