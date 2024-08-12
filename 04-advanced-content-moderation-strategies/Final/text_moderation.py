# Import packages
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory, AnalyzeTextOutputType

# Funtion call to check if the text is safe for publication
def moderate_text(client,text):
    # Construct a request
    request = AnalyzeTextOptions(text=text, output_type=AnalyzeTextOutputType.EIGHT_SEVERITY_LEVELS)

    # Analyze text
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze text failed.")
        if e.error:
            print(f"Error code: {e.error.code}")
            print(f"Error message: {e.error.message}")
            raise
        print(e)
        raise

    # Extract results
    categories = {
        TextCategory.HATE: None,
        TextCategory.SELF_HARM: None,
        TextCategory.SEXUAL: None,
        TextCategory.VIOLENCE: None
    }

    for item in response.categories_analysis:
        if item.category in categories:
            categories[item.category] = item

    hate_result = categories[TextCategory.HATE]
    self_harm_result = categories[TextCategory.SELF_HARM]
    sexual_result = categories[TextCategory.SEXUAL]
    violence_result = categories[TextCategory.VIOLENCE]

    # Check for inappropriate content
    violations = {}
    if hate_result and hate_result.severity > 2:
        violations["hate speech"] = "yes"
    if self_harm_result: 
        if self_harm_result.severity > 4:
            violations["self-harm"] = "yes"
        elif self_harm_result.severity > 3:
            violations["self-harm"] = "likely"
    if sexual_result:
        if sexual_result.severity > 1:
            violations["sexual"] = "yes"
        elif sexual_result.severity > 2:
            violations["sexual"] = "likely"
    if violence_result and violence_result.severity > 2:
        violations["violent references"] = "yes"

    return violations