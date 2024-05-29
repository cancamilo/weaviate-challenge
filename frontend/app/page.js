"use client";

import { useState } from 'react';
import Search from './components/Search';

export default function Home() {
  const data = [
    {summary: "In its latest market commentary sent to Telegram channel subscribers on May 28, trading firm QCP Capital dismissed recent “bouts of supply anxiety.", published_at: "10-02-2024"},
    {summary: "Bitcoin bulls have little to worry about when it comes to the BTC price uptrend, QCP Capital argues.", published_at: "10-02-2024"},
    {summary: "Low trading fees help traders get the most crypto for their money. This platform is leading the way with commission-free trading.", published_at: "10-02-2024"},
    {summary: "Need to know what happened in crypto today? Here is the latest news on daily trends and events impacting Bitcoin price, blockchain, DeFi, NFTs, Web3 and crypto regulation.", published_at: "10-02-2024"},
  ]

  const commonSearches = ["Bitcoin ETFS", "New partnerships", "Adoption",
  "Regulatory news", "Macroeconomic events", "FOMO"
  ]

  const [results, setResults] = useState(data);

  const [expandedItemIndex, setExpandedItemIndex] = useState(null);

  const search = async (term) => {
    const res = await fetch(`https://api.example.com/search?q=${term}`);
    const data = await res.json();
    setResults(data);
  };

  return (
    <main className="flex flex-col items-center justify-start min-h-screen p-24 space-y-4">
      <h1 className="text-2xl font-bold text-center">Crypto News Rag</h1>
      <Search onSearch={search} />
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
    <div className='list-container'>
      <ul className="list-disc">
        {results.map((result, index) => (
          <li key={index}
          className="border p-4 rounded-lg cursor-pointer w-full" 
          onClick={() => setExpandedItemIndex(index === expandedItemIndex ? null : index)}>
            <h2 className="font-bold mb-2">
                  {result.summary.substring(0, 50) + "..."}
            </h2>
            {index === expandedItemIndex && 
              <div className="mt-2 text-left">
                {result.summary}
              </div>
            }
            <p className="text-sm text-gray-500">{result.published_at}</p>
          </li>
        ))}
      </ul>
      </div>
    </main>
  );

  // return (
  //   <main className="flex min-h-screen flex-col items-center justify-between p-24">
  //     <div>
  //       <h1 className="text-2xl font-bold mb-2 text-center">Crypto News Rag</h1>
  //       <Search onSearch={search} />
  //     </div>
  //     <ul>
  //       {results.map((result, index) => (
  //         <li key={index}>{result}</li>
  //       ))}
  //     </ul>
  //     </main>
  // );
}
