import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient

from text_moderation import moderate_text
from image_moderation import moderate_image

# Load your Azure Safety API key and endpoint
load_dotenv()

key = os.environ["CONTENT_SAFETY_KEY"]
endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"]

# Create a Content Safety client
moderator_client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

def check_content_safety(text, image_data):
    # Check for the content safety
    text_moderate_result = moderate_text(client=moderator_client, text=text)
    image_moderate_result = moderate_image(client=moderator_client, image_data=image_data)

    if len(text_moderate_result) == 0 and len(image_moderate_result) == 0:
        return None
    

    text_violation_flags = text_moderate_result.values()
    image_violation_flags = image_moderate_result.values()


    if "likely" in text_violation_flags or "likely" in image_violation_flags:
        return {'status': "re-evaluation needed"}


    status_detail = f'Your post contains references that violate our community guidelines.'

    if text_moderate_result:
        status_detail = status_detail + '\n' + f'Violation found in text: {','.join(text_moderate_result)}'
    if image_moderate_result:
        status_detail = status_detail + '\n' + f'Violation found in image: {','.join(image_moderate_result)}'
    
    status_detail = status_detail + '\n' + 'Please modify your post to adhere to community guidelines.'

    return {'status': "violations found", 'details': status_detail}