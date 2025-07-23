from duckduckgo_search import DDGS
import re
from typing import List, Dict, Any, Optional
import pandas as pd
import time
from functools import lru_cache

class DuckDuckGoLinkedInSearch:
    def __init__(self):
        self.ddgs = DDGS()
        self.cache = {}
        self.cache_ttl = 3600  # Cache TTL in seconds (1 hour)
    
    @lru_cache(maxsize=100)
    def search(self, query: str) -> str:
        """Search for LinkedIn profiles using DuckDuckGo with caching"""
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
        results = self.ddgs.text(query, max_results=15)  # Increased results for better matches
        
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
    
    def _extract_profiles(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract LinkedIn profiles from search results"""
        profiles = []
        
        for result in results:
            # Check if it's a LinkedIn profile
            if "linkedin.com/in/" in result.get("href", ""):
                # Extract the name from the title
                title = result.get("title", "")
                name = self._extract_name(title)
                
                # Add to profiles if we have a name
                if name:
                    profiles.append({
                        "name": name,
                        "url": result.get("href"),
                        "description": result.get("body", "")
                    })
        
        return profiles
    
    def _extract_name(self, title: str) -> str:
        """Extract the person's name from the LinkedIn title"""
        # Common patterns in LinkedIn titles
        patterns = [
            r"^([\w\s]+)\s+\|\s+LinkedIn$",  # Name | LinkedIn
            r"^([\w\s]+)\s+\-\s+LinkedIn$",  # Name - LinkedIn
            r"^([\w\s]+)'s Profile\s+\|\s+LinkedIn$",  # Name's Profile | LinkedIn
            r"^([\w\s]+)\s+\|\s+Professional Profile\s+\|\s+LinkedIn$"  # Name | Professional Profile | LinkedIn
        ]
        
        for pattern in patterns:
            match = re.search(pattern, title)
            if match:
                return match.group(1).strip()
        
        # If no pattern matches, return the title without "LinkedIn"
        return title.replace("LinkedIn", "").replace("|", "").replace("-", "").strip()
    
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