"use client";

import { useState } from "react";

export default function ChatInput({ onAsk, loading }) {
  const [query, setQuery] = useState("");

  const handleSubmit = () => {
    if (!query.trim()) return;
    onAsk(query);
    setQuery("");
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="w-full bg-white shadow-lg rounded-xl p-6 border border-gray-200">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-purple-700 mb-2">🔍 Ask About Any Puja</h3>
        <p className="text-gray-600 text-sm">
          Get detailed, authentic information from your uploaded books
        </p>
      </div>
      
      <div className="space-y-4">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Examples:
• How to perform Sai Baba puja?
• What materials are needed for Lakshmi puja?
• What are the mantras for Durga puja?
• Best timing for Shiva puja
• Step by step Chandi puja procedure"
          className="w-full border-2 border-gray-200 rounded-lg p-4 text-gray-700 focus:ring-2 focus:ring-purple-500 focus:border-purple-500 focus:outline-none resize-none transition-all"
          rows="4"
        />
        
        <div className="flex items-center justify-between">
          <div className="text-xs text-gray-500">
            💡 Press Enter to submit, Shift+Enter for new line
          </div>
          <button
            onClick={handleSubmit}
            disabled={loading || !query.trim()}
            className="bg-gradient-to-r from-purple-600 to-blue-600 text-white py-3 px-6 rounded-lg hover:from-purple-700 hover:to-blue-700 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed font-semibold shadow-md hover:shadow-lg"
          >
            {loading ? (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Searching Books...
              </div>
            ) : (
              <div className="flex items-center">
                <span className="mr-2">🔍</span>
                Search Authentic Texts
              </div>
            )}
          </button>
        </div>
      </div>
      
      <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
        <div className="flex items-start">
          <div className="text-blue-600 mr-2 mt-1">💡</div>
          <div className="text-sm text-blue-800">
            <strong>Tip:</strong> Be specific in your questions to get the most detailed information from your books. 
            The system will search through all your uploaded PDFs and provide authentic, sourced responses.
          </div>
        </div>
      </div>
    </div>
  );
}
