"use client";

export default function PresetButtons({ onSelect }) {
  const presets = [
    {
      title: "Sai Baba Puja",
      description: "Sai Divya Pooja from authentic texts",
      icon: "🕉",
      query: "Sai Baba puja"
    },
    {
      title: "Lakshmi Puja",
      description: "Complete Lakshmi worship procedure",
      icon: "🪔",
      query: "Lakshmi puja"
    },
    {
      title: "Durga Puja",
      description: "Durga worship from traditional texts",
      icon: "🕉",
      query: "Durga puja"
    },
    {
      title: "Shiva Puja",
      description: "Shiva worship from Siva Puranam",
      icon: "🕉",
      query: "Shiva puja"
    },
    {
      title: "Chandi Puja",
      description: "Chandi worship rituals",
      icon: "🕉",
      query: "Chandi puja"
    }
  ];

  return (
    <div className="mb-6">
      <div className="text-center mb-4">
        <h2 className="text-xl font-bold text-purple-700 mb-2">📚 Available Pujas from Your Books</h2>
        <p className="text-gray-600">Click any puja to get detailed, authentic information</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {presets.map((preset, idx) => (
          <button
            key={idx}
            onClick={() => onSelect(preset.query)}
            className="group bg-white border-2 border-purple-200 p-4 rounded-xl text-left hover:border-purple-400 hover:shadow-lg transition-all duration-300 hover:scale-105"
          >
            <div className="flex items-start space-x-3">
              <div className="text-2xl group-hover:scale-110 transition-transform">
                {preset.icon}
              </div>
              <div className="flex-1">
                <h3 className="font-bold text-purple-700 text-lg mb-1 group-hover:text-purple-800">
                  {preset.title}
                </h3>
                <p className="text-gray-600 text-sm leading-relaxed">
                  {preset.description}
                </p>
                <div className="mt-2 text-xs text-purple-500 font-medium">
                  📖 From your uploaded books
                </div>
              </div>
            </div>
          </button>
        ))}
      </div>
      
      <div className="mt-4 text-center">
        <p className="text-sm text-gray-500">
          💡 You can also type custom questions about specific rituals or procedures
        </p>
      </div>
    </div>
  );
}
