"use client";

import { useState } from 'react';

export default function Search({ onSearch }) {
  const [term, setTerm] = useState('');

  const onSubmit = (e) => {
    e.preventDefault();
    onSearch(term);
  };

  return (
    <form onSubmit={onSubmit} className='flex items-center'>
      <input
        type="text"
        value={term}
        onChange={(e) => setTerm(e.target.value)}
        className="border p-2 rounded input-box"
      />
      <button type="submit" className="bg-green-700 text-white p-2 rounded ml-2">
        Search
      </button>
    </form>
  );
}