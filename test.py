from SimplerLLM.language.llm import LLMProvider

from SimplerLLM.tools.generic_loader import load_content

from agent_class_extended import Agent

from predefined_functions import get_seo_page_report


def load_content_from_url(url:str):
    """
    Load content from a given URL.
    :param url: str, URL to load content from
    :return: str, content
    """
    content = load_content(url)
    return content.content



# Create an agent instance
agent = Agent(LLMProvider.OPENAI, model_name="gpt-4")

# Add a predefined tool without needing a description
agent.add_tool("get_seo_page_report")


agent.add_tool("load_content_from_url", load_content_from_url,"Extract content from any web page. Parameters: url (str)")



user_query_1 = """
what is the response time of this web page: learnwithhasan.com?"""

user_query_2 = """
generate a conside bullet point summary of the following article: 
https://learnwithhasan.com/generate-content-ideas-ai/?"""

user_query_3 = """
When was Isaac Newton born?"""


# Generate a response
agent.generate_response(user_query_2)

