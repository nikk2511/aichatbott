"use client";

export default function AnswerDisplay({ loading, answer }) {
  if (loading) {
    return (
      <div className="p-8 bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl shadow-lg text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
        <p className="text-purple-700 font-semibold text-lg">🔍 Searching through your authentic books...</p>
        <p className="text-gray-600 mt-2">Extracting detailed information from your uploaded PDFs</p>
      </div>
    );
  }

  if (!answer) {
    return (
      <div className="p-8 bg-gradient-to-r from-gray-50 to-blue-50 rounded-xl text-center border-2 border-dashed border-gray-300">
        <div className="text-6xl mb-4">🕉</div>
        <h3 className="text-xl font-semibold text-gray-700 mb-2">Welcome to Puja AI</h3>
        <p className="text-gray-600">Ask about any puja to get detailed, authentic information from your uploaded books.</p>
        <div className="mt-4 text-sm text-gray-500">
          <p>📚 Available: Sai Baba, Lakshmi, Durga, Shiva, Chandi pujas</p>
        </div>
      </div>
    );
  }

  const hasMarkdown = !!answer.content_markdown && answer.content_markdown.trim().length > 0;

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header with Book Sources */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6 rounded-xl shadow-lg">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold mb-2">📖 Authentic Puja Information</h1>
            <p className="text-purple-100">Sourced directly from your uploaded books</p>
          </div>
          <div className="text-right">
            <div className="text-3xl">🕉</div>
          </div>
        </div>
      </div>

      {/* Polished Markdown Content (from ChatGPT compose) */}
      {hasMarkdown && (
        <div className="bg-white border border-gray-200 p-6 rounded-lg shadow-md">
          <div className="flex items-center mb-4">
            <div className="text-2xl mr-3">🪔</div>
            <h2 className="text-xl font-bold text-purple-700">Guided Puja (Polished)</h2>
          </div>
          <div className="prose max-w-none whitespace-pre-wrap leading-relaxed text-gray-800">
            {answer.content_markdown}
          </div>
        </div>
      )}

      {/* Summary Section */}
      {!hasMarkdown && (
        <div className="bg-white border-l-4 border-purple-500 p-6 rounded-lg shadow-md">
          <div className="flex items-center mb-4">
            <div className="text-2xl mr-3">📝</div>
            <h2 className="text-xl font-bold text-purple-700">Summary</h2>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <p className="text-gray-800 leading-relaxed">{answer.summary}</p>
          </div>
        </div>
      )}

      {/* Detailed Steps Section */}
      {!hasMarkdown && answer.steps?.length > 0 && (
        <div className="bg-white border border-gray-200 p-6 rounded-lg shadow-md">
          <div className="flex items-center mb-4">
            <div className="text-2xl mr-3">📋</div>
            <h2 className="text-xl font-bold text-purple-700">Step-by-Step Instructions</h2>
          </div>
          <div className="space-y-4">
            {answer.steps.map((step, index) => (
              <div key={index} className="flex items-start space-x-4 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border-l-4 border-blue-500">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center font-bold text-sm">
                  {index + 1}
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-blue-800 mb-1">{step.title}</h3>
                  <p className="text-gray-700 leading-relaxed">{step.instruction}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Materials Section */}
      {!hasMarkdown && answer.materials?.length > 0 && (
        <div className="bg-white border border-gray-200 p-6 rounded-lg shadow-md">
          <div className="flex items-center mb-4">
            <div className="text-2xl mr-3">🛒</div>
            <h2 className="text-xl font-bold text-purple-700">Required Materials</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {answer.materials.map((material, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-green-50 rounded-lg border border-green-200">
                <div className="flex items-center">
                  <div className="text-green-600 mr-3">🪔</div>
                  <span className="font-medium text-gray-800">{material.name}</span>
                </div>
                {material.product_match && (
                  <a
                    href={material.product_match}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-green-600 text-white px-3 py-1 rounded-full text-sm font-medium hover:bg-green-700 transition-colors"
                  >
                    Buy Now
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Timings Section */}
      {!hasMarkdown && answer.timings?.length > 0 && (
        <div className="bg-white border border-gray-200 p-6 rounded-lg shadow-md">
          <div className="flex items-center mb-4">
            <div className="text-2xl mr-3">⏰</div>
            <h2 className="text-xl font-bold text-purple-700">Best Timings</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {answer.timings.map((timing, index) => (
              <div key={index} className="flex items-center p-3 bg-orange-50 rounded-lg border border-orange-200">
                <div className="text-orange-600 mr-3">🌅</div>
                <span className="text-gray-800 font-medium">{timing}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Mantras Section */}
      {!hasMarkdown && answer.mantras?.length > 0 && (
        <div className="bg-white border border-gray-200 p-6 rounded-lg shadow-md">
          <div className="flex items-center mb-4">
            <div className="text-2xl mr-3">🎵</div>
            <h2 className="text-xl font-bold text-purple-700">Sacred Mantras</h2>
          </div>
          <div className="space-y-3">
            {answer.mantras.map((mantra, index) => (
              <div key={index} className="p-4 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-lg border-l-4 border-yellow-500">
                <div className="flex items-start">
                  <div className="text-yellow-600 mr-3 mt-1">🕉</div>
                  <div>
                    <p className="text-gray-800 font-sanskrit text-lg leading-relaxed">{mantra}</p>
                    <p className="text-sm text-gray-600 mt-2">Sacred chant from authentic texts</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Sources Section - Most Important */}
      {!hasMarkdown && answer.sources?.length > 0 && (
        <div className="bg-white border border-gray-200 p-6 rounded-lg shadow-md">
          <div className="flex items-center mb-4">
            <div className="text-2xl mr-3">📚</div>
            <h2 className="text-xl font-bold text-purple-700">Source References</h2>
          </div>
          <div className="space-y-4">
            {answer.sources.map((source, index) => (
              <div key={index} className="border border-gray-200 rounded-lg overflow-hidden">
                <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-3">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold">📖 {source.book}</h3>
                    <span className="bg-white text-purple-600 px-2 py-1 rounded text-sm font-bold">
                      Page {source.page}
                    </span>
                  </div>
                </div>
                <div className="p-4 bg-gray-50">
                  <p className="text-gray-700 italic leading-relaxed">"{source.snippet}"</p>
                  <div className="mt-3 flex items-center text-sm text-gray-600">
                    <span className="mr-4">📄 Direct quote from your book</span>
                    <span className="bg-green-100 text-green-800 px-2 py-1 rounded">Authentic Source</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Notes Section */}
      {!hasMarkdown && answer.notes && (
        <div className="bg-white border border-gray-200 p-6 rounded-lg shadow-md">
          <div className="flex items-center mb-4">
            <div className="text-2xl mr-3">💡</div>
            <h2 className="text-xl font-bold text-purple-700">Important Notes</h2>
          </div>
          <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
            <p className="text-gray-800 leading-relaxed">{answer.notes}</p>
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="bg-gradient-to-r from-green-50 to-blue-50 p-6 rounded-lg border border-green-200 text-center">
        <div className="flex items-center justify-center mb-2">
          <div className="text-2xl mr-2">✅</div>
          <h3 className="text-lg font-semibold text-green-800">Authentic Information Verified</h3>
        </div>
        <p className="text-gray-700">
          All information is extracted directly from your uploaded authentic texts. 
          Please consult with learned priests for proper guidance.
        </p>
      </div>
    </div>
  );
}
