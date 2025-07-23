import React, { useState } from 'react';
import Head from 'next/head';
import axios from 'axios';
import SearchForm from '../components/SearchForm';
import ResultsTable from '../components/ResultsTable';
import { ToastProvider, Toast, ToastTitle, ToastDescription, ToastViewport } from '../components/ui/toast';

export default function Home() {
  const [results, setResults] = useState([]);
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState({ title: '', description: '' });

  const handleSearch = async (formData) => {
    setIsLoading(true);
    try {
      const response = await axios.post(`${process.env.BACKEND_URL}/search`, formData);
      setResults(response.data.founders);
      setQuery(response.data.query);
    } catch (error) {
      console.error('Error searching for founders:', error);
      setToastMessage({
        title: 'Error',
        description: error.response?.data?.detail || 'Failed to search for founders. Please try again.'
      });
      setShowToast(true);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Head>
        <title>LinkedIn Founder Finder</title>
        <meta name="description" content="Find startup founders on LinkedIn by domain and location" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <ToastProvider>
        <main className="container mx-auto py-10 px-4 max-w-4xl">
          <div className="space-y-10">
            <div className="space-y-2 text-center">
              <h1 className="text-3xl font-bold tracking-tighter sm:text-4xl md:text-5xl">LinkedIn Founder Finder</h1>
              <p className="text-muted-foreground">
                Find startup founders in specific industries and locations using AI-powered search.
              </p>
            </div>

            <div className="grid gap-10 md:grid-cols-2">
              <div className="space-y-4">
                <div className="space-y-2">
                  <h2 className="text-xl font-semibold">Search Criteria</h2>
                  <p className="text-sm text-muted-foreground">
                    Enter the domain, location, and role to find relevant LinkedIn profiles.
                  </p>
                </div>
                <SearchForm onSearch={handleSearch} isLoading={isLoading} />
              </div>

              <div className="space-y-4">
                <div className="space-y-2">
                  <h2 className="text-xl font-semibold">Results</h2>
                  <p className="text-sm text-muted-foreground">
                    {results.length > 0
                      ? `Found ${results.length} profiles matching your criteria.`
                      : 'Search results will appear here.'}
                  </p>
                </div>
                {results.length > 0 && <ResultsTable results={results} query={query} />}
              </div>
            </div>

            <div className="text-center text-sm text-muted-foreground">
              <p>Powered by LangChain, FastAPI, Next.js, and Tailwind CSS</p>
            </div>
          </div>
        </main>

        {showToast && (
          <Toast variant="destructive" onOpenChange={setShowToast}>
            <ToastTitle>{toastMessage.title}</ToastTitle>
            <ToastDescription>{toastMessage.description}</ToastDescription>
          </Toast>
        )}
        <ToastViewport />
      </ToastProvider>
    </div>
  );
}