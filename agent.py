from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from search_tool import DuckDuckGoLinkedInSearch
import os
from dotenv import load_dotenv
from typing import Dict, List, Any

# Load OpenAI API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize LLM
llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")

# Initialize the search tool
search_tool = DuckDuckGoLinkedInSearch()

def search_linkedin_profiles(domain: str, location: str, role: str = "Founder") -> List[Dict[str, str]]:
    """
    Search for LinkedIn profiles based on domain, location, and role.
    
    Args:
        domain: The industry or domain (e.g., 'Sportstech')
        location: The location (e.g., 'Bangalore')
        role: The role (e.g., 'Founder')
        
    Returns:
        A list of dictionaries containing name and LinkedIn URL
    """
    # Create a search query
    query = f"{role} {domain} {location} site:linkedin.com/in"
    
    # Execute the search
    results_str = search_tool.search(query)
    
    # Extract profiles from the results string
    profiles = []
    import re
    
    # Extract LinkedIn profile URLs and names
    linkedin_pattern = r"([\w\s]+)\s*[\-|]\s*(https?://(?:www\.)?linkedin\.com/in/[\w\-]+)"
    matches = re.findall(linkedin_pattern, results_str)
    
    for name, url in matches:
        profiles.append({
            "name": name.strip(),
            "linkedin_url": url.strip()
        })
    
    return profiles

# Wrap the search function in a LangChain Tool
linkedin_tool = Tool(
    name="LinkedIn Profile Search Tool",
    func=lambda x: str(search_linkedin_profiles(**eval(x))),
    description="""
    Use this tool to find LinkedIn founders based on input:
    domain (e.g., 'Sportstech'), location (e.g., 'Bangalore'),
    and role (e.g., 'Founder').
    
    Input must be a dictionary string like:
    "{'domain': 'Sportstech', 'location': 'Bangalore', 'role': 'Founder'}"
    """
)

# Initialize the Agent with the tool
agent_executor = initialize_agent(
    tools=[linkedin_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# For backward compatibility with the existing app.py
class LinkedInFinderAgent:
    def __init__(self):
        self.agent_executor = agent_executor
    
    def search(self, domain: str, location: str, role: str = "Founder") -> tuple:
        """Execute the search for LinkedIn profiles"""
        # Generate a search query
        search_query = f"{role} {domain} {location} site:linkedin.com/in"
        
        # Use the direct search function instead of the agent for more reliable results
        profiles = search_linkedin_profiles(domain=domain, location=location, role=role)
        
        return profiles, search_query