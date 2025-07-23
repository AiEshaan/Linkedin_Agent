# LinkedIn Founder Finder

A full-stack, AI-powered SaaS tool that helps users find startup founders in specific industries and locations by searching public LinkedIn profiles. It uses an AI Agent built with LangChain and a clean frontend built with Next.js + Tailwind + shadcn/ui.

## 🚀 Example Input

```
Domain: Sportstech
Location: Bangalore
Role: Founder
```

## 🎯 Example Output

| Name | LinkedIn URL |
|--------------|-------------------------------------------|
| Jane Doe | `https://linkedin.com/in/janedoe` |
| Rahul Mehta | `https://linkedin.com/in/rahulmehta` |

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Agent Engine | LangChain (Python) |
| Search Tool | DuckDuckGo Search |
| Backend API | FastAPI |
| Frontend UI | Next.js + Tailwind CSS |
| UI Library | shadcn/ui |
| Hosting | Vercel + Render |

## 📂 Project Structure

```
linkedin-founder-finder/
├── backend/
│   ├── app.py               # FastAPI server
│   ├── agent.py             # LangChain Agent
│   ├── search_tool.py       # DuckDuckGo LinkedIn search
│   ├── serp_agent.py        # SerpAPI LinkedIn search (optional)
│   ├── serpapi_tool.py      # SerpAPI tool implementation
│   ├── main.py              # Entry point for Render deployment
│   └── .env                 # OpenAI or API keys
├── frontend/
│   ├── pages/               # Form UI + Results
│   ├── components/          # Table, InputBox, etc.
│   ├── styles/              # Tailwind styling
├── requirements.txt
├── README.md
└── .env.example
```

## 📦 Installation

### Backend

1. Clone the repository
2. Navigate to the project directory
3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the backend directory with your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
PORT=8000
```

5. Start the backend server:

```bash
cd backend
python app.py
```

### Frontend

1. Navigate to the frontend directory
2. Install the required packages:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

## ✅ Features

- 🔍 Search founders based on domain, location, role
- ⚙️ AI agent generates and executes search queries
- 📎 Extracts public LinkedIn profiles from DuckDuckGo
- 📋 Clean table of names + profile links
- 🖼️ Responsive UI (SaaS style)
- 🌍 Easy to deploy (Vercel + Render)

## 🚀 Deployment

### Backend Deployment (Render)

1. Push your backend code to GitHub:
   ```bash
   cd backend
   git init
   git remote add origin https://github.com/AiEshaan/Linkedin_Agent
   git add .
   git commit -m "Add FastAPI backend"
   git push -u origin main
   ```

2. Create a free Render account at https://render.com and sign in with GitHub

3. Deploy the FastAPI app:
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Select your backend repo
   - Fill in the setup:
     - Name: founder-finder-backend
     - Runtime: Python
     - Build Command: pip install -r requirements.txt
     - Start Command: uvicorn main:app --host 0.0.0.0 --port 10000
     - Environment: Python 3.11 or later

4. Add Environment Variables:
   - OPENAI_API_KEY: your_openai_api_key
   - SERPAPI_API_KEY: your_serpapi_api_key (optional)

5. Once deployed, you'll get a public URL like: https://founder-finder-backend.onrender.com

### Frontend Configuration

1. Update your frontend API base URL in `.env.local`:
   ```
   BACKEND_URL=https://founder-finder-backend.onrender.com
   ```

2. Deploy your frontend to Vercel or your preferred hosting platform.

## 📝 Notes on SerpAPI

This project can use either:
- SerpAPI for Google Search results (requires API key)
- DuckDuckGo search (free, no API key required)

If you don't provide a SERPAPI_API_KEY, the application will automatically fall back to using DuckDuckGo search.

## 📝 License

MIT