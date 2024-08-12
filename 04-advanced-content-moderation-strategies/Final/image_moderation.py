# Import the packages
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeImageOptions, ImageData, AnalyzeImageOutputType, ImageCategory


def moderate_image(client, image_data):
    # Construct a request
    request = AnalyzeImageOptions(image=ImageData(content=image_data),
                                  output_type=AnalyzeImageOutputType.FOUR_SEVERITY_LEVELS)

    # Analyze image
    try:
        response = client.analyze_image(request)
    except HttpResponseError as e:
        print("Analyze image failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

    # Extract results
    categories = {
        ImageCategory.HATE: None,
        ImageCategory.SELF_HARM: None,
        ImageCategory.SEXUAL: None,
        ImageCategory.VIOLENCE: None
    }

    for item in response.categories_analysis:
        if item.category in categories:
            categories[item.category] = item

    hate_result = categories[ImageCategory.HATE]
    self_harm_result = categories[ImageCategory.SELF_HARM]
    sexual_result = categories[ImageCategory.SEXUAL]
    violence_result = categories[ImageCategory.VIOLENCE]

    # Check for inappropriate content
    violations = {}
    if hate_result and hate_result.severity > 2:
        violations["hate speech"] = "yes"
    if self_harm_result and self_harm_result.severity > 4:
        violations["self-harm references"] = "yes"
    if sexual_result and sexual_result.severity > 0:
        violations["sexual references"] = "yes"
    if violence_result and violence_result.severity > 2:
        violations["violent references"] = "yes"

    return violations