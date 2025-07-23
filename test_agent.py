from agent import agent_executor
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_direct_function():
    """Test the direct search_linkedin_profiles function"""
    from agent import search_linkedin_profiles
    
    print("\n=== Testing Direct Function ===\n")
    profiles = search_linkedin_profiles(
        domain="Fintech", 
        location="Delhi", 
        role="Founder"
    )
    
    print(f"Found {len(profiles)} profiles:")
    for profile in profiles:
        print(f"- {profile['name']} - {profile['linkedin_url']}")

def test_agent_with_dict_string():
    """Test the agent with a dictionary string input"""
    print("\n=== Testing Agent with Dictionary String ===\n")
    input_str = "{'domain': 'Fintech', 'location': 'Delhi', 'role': 'Founder'}"
    response = agent_executor.invoke({"input": input_str})
    print("Agent Response:")
    print(response["output"])

def test_agent_with_natural_language():
    """Test the agent with a natural language query"""
    print("\n=== Testing Agent with Natural Language ===\n")
    query = "Find founders in Edtech domain based in Mumbai"
    response = agent_executor.invoke({"input": query})
    print("Agent Response:")
    print(response["output"])

if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY is not set. Please set it in your .env file.")
    
    # Run the tests
    test_direct_function()
    test_agent_with_dict_string()
    test_agent_with_natural_language()