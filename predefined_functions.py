
from SimplerLLM.tools.rapid_api import RapidAPIClient

def get_seo_page_report(url: str):
    api_url = "https://website-seo-analyzer.p.rapidapi.com/seo/seo-audit-basic"
    api_params = {'url': url}
    api_client = RapidAPIClient()
    response = api_client.call_api(api_url, method='GET', params=api_params)
    return response

# Dictionary of predefined tools with their descriptions
PREDEFINED_TOOLS = {
    "get_seo_page_report": {
        "function": get_seo_page_report,
        "description": "Fetches an SEO report for the given URL. Parameters: url (str)"
    }
}