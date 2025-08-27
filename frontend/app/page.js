"use client";

import PujaWidget from "./components/PujaWidget";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-100 p-6">
      {/* App Header */}
      <h1 className="text-3xl font-bold text-purple-700 mb-6">
        🕉 Puja AI Chatbot
      </h1>

      {/* Chatbot Widget */}
      <div className="w-full max-w-3xl">
        <PujaWidget />
      </div>
    </main>
  );
}

// "use client"; // only if using app/ directory

// import { useState } from "react";
// import { askBackend } from "../utils/api";

// export default function Chat() {
//   const [input, setInput] = useState("");
//   const [messages, setMessages] = useState([]);

//   const sendMessage = async () => {
//     if (!input.trim()) return;

//     // Add user message
//     setMessages([...messages, { role: "user", content: input }]);

//     try {
//       const res = await askBackend(input);

//       // Add assistant response
//       setMessages((prev) => [
//         ...prev,
//         { role: "assistant", content: res.answer },
//       ]);
//     } catch (err) {
//       setMessages((prev) => [
//         ...prev,
//         { role: "assistant", content: "Error: Could not reach backend." },
//       ]);
//     }

//     setInput("");
//   };

//   return (
//     <div className="p-4 max-w-xl mx-auto">
//       <div className="border rounded-lg p-3 h-80 overflow-y-auto bg-gray-50">
//         {messages.map((m, i) => (
//           <p key={i} className="mb-1">
//             <b>{m.role}:</b> {m.content}
//           </p>
//         ))}
//       </div>

//       <div className="flex mt-3">
//         <input
//           className="border flex-1 p-2 rounded-l-lg"
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//           placeholder="Ask something..."
//         />
//         <button
//           onClick={sendMessage}
//           className="bg-blue-500 text-white px-4 rounded-r-lg"
//         >
//           Send
//         </button>
//       </div>
//     </div>
//   );
// }
