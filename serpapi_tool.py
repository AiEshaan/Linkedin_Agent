from serpapi import GoogleSearch
import os
from typing import List, Dict, Any
import pandas as pd
import time
from functools import lru_cache

class SerpApiLinkedInSearch:
    def __init__(self):
        self.api_key = os.getenv("SERPAPI_API_KEY")
        if not self.api_key:
            print("Warning: SERPAPI_API_KEY environment variable not set. Some functionality may be limited.")
        self.cache = {}
        self.cache_ttl = 3600  # Cache TTL in seconds (1 hour)
    
    @lru_cache(maxsize=100)
    def search(self, query: str) -> str:
        """Search for LinkedIn profiles using SerpAPI with caching"""
        # Check if API key is set
        if not self.api_key:
            raise ValueError("SERPAPI_API_KEY environment variable not set. Cannot perform SerpAPI search.")
            
        # Check cache first
        cache_key = query.lower()
        current_time = time.time()
        
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            # If cache is still valid
            if current_time - cache_entry['timestamp'] < self.cache_ttl:
                return cache_entry['result']
        
        # Ensure the query includes LinkedIn
        if "linkedin.com" not in query.lower():
            query += " site:linkedin.com/in"
        
        # Execute the search
        search = GoogleSearch({
            "q": query,
            "api_key": self.api_key,
            "engine": "google",  # Using Google search engine
            "num": 15,  # Increased number of results
            "gl": "us",  # Set country to US for consistent results
            "hl": "en"   # Set language to English
        })
        results = search.get_dict()
        
        # Process the results
        profiles = self._extract_profiles(results)
        
        # Format the results as a string
        result = self._format_results(profiles)
        
        # Update cache
        self.cache[cache_key] = {
            'result': result,
            'timestamp': current_time
        }
        
        return result
    
    def _extract_profiles(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract LinkedIn profiles from search results"""
        profiles = []
        
        # Extract organic results
        if "organic_results" in results:
            for result in results["organic_results"]:
                if "linkedin.com/in/" in result.get("link", ""):
                    profiles.append({
                        "name": self._extract_name(result.get("title", "")),
                        "url": result.get("link", ""),
                        "description": result.get("snippet", "")
                    })
        
        return profiles
    
    def _extract_name(self, title: str) -> str:
        """Extract the person's name from the LinkedIn title"""
        # Remove LinkedIn suffix
        name = title.replace(" | LinkedIn", "")
        name = name.replace(" - LinkedIn", "")
        name = name.replace(" | Professional Profile | LinkedIn", "")
        name = name.replace("'s Profile | LinkedIn", "")
        
        # Return cleaned name
        return name.strip()
    
    def _format_results(self, profiles: List[Dict[str, Any]]) -> str:
        """Format the profiles as a string"""
        if not profiles:
            return "No LinkedIn profiles found."
        
        # Create a DataFrame for easier formatting
        df = pd.DataFrame(profiles)
        
        # Format the results
        result = "Found the following LinkedIn profiles:\n\n"
        
        for _, row in df.iterrows():
            result += f"{row['name']} - {row['url']}\n"
        
        return result