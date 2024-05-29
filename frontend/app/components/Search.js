"use client";

import { useState, useEffect } from 'react';

export default function Search({ onSearch, searchTerm, isLoading }) {
  const [localSearchTerm, setLocalSearchTerm] = useState(searchTerm);

  useEffect(() => {
    setLocalSearchTerm(searchTerm);
  }, [searchTerm]);

  const onSubmit = async (e) => {
    e.preventDefault();
    await onSearch(localSearchTerm);
  };

  return (
    <form onSubmit={onSubmit} className='flex items-center'>
      <input
        type="text"
        value={localSearchTerm}
        onChange={(e) => setLocalSearchTerm(e.target.value)}
        className="border p-2 rounded input-box"
        disabled={isLoading}
      />
      {isLoading ?
      <div className="bg-green-700 text-white p-2 rounded ml-2"> Loading </div> :
      <button type="submit" className="bg-green-700 text-white p-2 rounded ml-2">
        Search
      </button>
      }
    </form>
  );
}