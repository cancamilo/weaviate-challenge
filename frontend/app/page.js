"use client";

import { useState } from 'react';
import Search from './components/Search';

export default function Home() {
  const answer = ""
  const hits = []
  const initState = {
    "answer": answer,
    "hits": hits
  }

  const commonSearches = ["Bitcoin ETFS", "New partnerships", "Adoption",
  "Regulatory news", "Macroeconomic events", "New developments"
  ]

  const [results, setResults] = useState(initState);
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [expandedItemIndex, setExpandedItemIndex] = useState(null);

  const search = async (term) => {
    setIsLoading(true)
    setSearchTerm(term)
    try {
      const res = await fetch('http://localhost:8000/search', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ query: term })
      });
      const data = await res.json();
      setResults(data["result"]);
    } catch (error) {
      console.log("Could not fetch results", error)
      setResults(initState)
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex flex-col items-center justify-start min-h-screen p-24 space-y-4">
      <h1 className="text-2xl font-bold text-center">Crypto News Rag</h1>
      <Search onSearch={search} searchTerm={searchTerm} isLoading={isLoading}/>
      <div>Try with these searches...</div>
      <div className="grid grid-cols-3 gap-4">
      {commonSearches.map((suggestion, index) => (
        <button
          key={index}
          className="bg-green-700 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
          onClick={() => search(suggestion)}
        >
          {suggestion}
        </button>
      ))}
    </div>
    {isLoading? <div className="coin"></div> : <div className='answer-box'>Answer: {results.answer}</div> }
    {isLoading? <div></div> :
    <div className='list-container'>
      Reference Context:
      <ul className="list-disc">
        {results.hits.map((result, index) => (
          <li key={index}
          className="border p-4 rounded-lg cursor-pointer w-full" 
          onClick={() => setExpandedItemIndex(index === expandedItemIndex ? null : index)}>
            <h2 className="font-bold mb-2">
                  {result.title}
            </h2>
            {index === expandedItemIndex && 
              <div className="mt-2 text-left">
                {result.content}
              </div>
            }
            <p className="text-sm text-gray-500">{result.published_at}</p>
          </li>
        ))}
      </ul>
      </div>
    }
    </main>
  );
}
