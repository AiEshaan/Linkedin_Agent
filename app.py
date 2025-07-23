from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn
import os
import asyncio
import time
from dotenv import load_dotenv
from functools import lru_cache

# Import both search methods
from agent import agent_executor, search_linkedin_profiles
from serp_agent import search_linkedin_profiles_with_serpapi

# Load environment variables
load_dotenv()

app = FastAPI(title="LinkedIn Founder Finder API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "https://founder-finder-frontend.vercel.app"],  # Allow both local development and production frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchInput(BaseModel):
    domain: str
    location: str
    role: str = "Founder"  # Default to 'Founder'

class FounderProfile(BaseModel):
    name: str
    linkedin_url: str

class SearchResponse(BaseModel):
    success: bool
    data: List[FounderProfile] = []
    query: str = ""
    error: str = ""

@app.get("/")
def read_root():
    return {"status": "LinkedIn Founder Finder API is running"}

# Cache for search results
search_cache = {}
search_cache_ttl = 3600  # 1 hour in seconds

@lru_cache(maxsize=50)
def get_cached_search_results(domain: str, location: str, role: str) -> tuple:
    """Get cached search results or perform a new search"""
    cache_key = f"{domain.lower()}:{location.lower()}:{role.lower()}"
    current_time = time.time()
    
    if cache_key in search_cache:
        cache_entry = search_cache[cache_key]
        if current_time - cache_entry['timestamp'] < search_cache_ttl:
            return cache_entry['profiles'], cache_entry['query']
    
    # Not in cache or expired, perform new search
    try:
        # Try SerpAPI first if available
        if os.getenv("SERPAPI_API_KEY"):
            profiles = search_linkedin_profiles_with_serpapi(
                domain=domain,
                location=location,
                role=role
            )
        else:
            # Fall back to DuckDuckGo if no SerpAPI key
            profiles = search_linkedin_profiles(
                domain=domain,
                location=location,
                role=role
            )
    except Exception as e:
        # If SerpAPI fails, fall back to DuckDuckGo
        print(f"SerpAPI search failed: {str(e)}. Falling back to DuckDuckGo.")
        profiles = search_linkedin_profiles(
            domain=domain,
            location=location,
            role=role
        )
    
    query = f"{role} {domain} {location} site:linkedin.com/in"
    
    # Update cache
    search_cache[cache_key] = {
        'profiles': profiles,
        'query': query,
        'timestamp': current_time
    }
    
    return profiles, query

@app.post("/api/find-founders", response_model=SearchResponse)
async def find_founders(data: SearchInput, background_tasks: BackgroundTasks):
    try:
        # Use cached results if available
        profiles, query = get_cached_search_results(
            domain=data.domain,
            location=data.location,
            role=data.role
        )
        
        # Convert profiles to response format
        founders = [FounderProfile(name=profile["name"], linkedin_url=profile["linkedin_url"]) 
                   for profile in profiles]
        
        # Refresh cache in background for next request
        background_tasks.add_task(
            get_cached_search_results,
            domain=data.domain,
            location=data.location,
            role=data.role
        )
        
        return SearchResponse(
            success=True,
            data=founders,
            query=query
        )
    except Exception as e:
        return SearchResponse(
            success=False,
            error=str(e)
        )

# Legacy endpoint for backward compatibility
@app.post("/search")
async def search_founders(request: SearchInput, background_tasks: BackgroundTasks):
    response = await find_founders(request, background_tasks)
    if not response.success:
        raise HTTPException(status_code=500, detail=response.error)
    return {
        "founders": response.data,
        "query": response.query
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)