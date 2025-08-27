"use client";

import { useState } from "react";
import ChatInput from "./ChatInput";
import PresetButtons from "./PresetButtons";
import AnswerDisplay from "./AnswerDisplay";

export default function PujaWidget() {
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState(null);

  const handleAsk = async (query) => {
    if (!query.trim()) return;
    setLoading(true);
    setAnswer(null);

    let timeoutId;
    const controller = new AbortController();
    try {
      timeoutId = setTimeout(() => controller.abort(), 120000);
      const response = await fetch('http://localhost:8000/api/compose', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ topic: query, books: [] }),
        signal: controller.signal,
      });

      let data = null;
      try {
        data = await response.json();
      } catch (_) {
        // ignore JSON parse errors
      }

      if (!response.ok) {
        if (data && (data.summary || data.content_markdown)) {
          setAnswer({
            summary: data.summary || 'Request failed',
            steps: data.steps || [],
            materials: data.materials || [],
            timings: data.timings || [],
            mantras: data.mantras || [],
            sources: data.sources || [],
            notes: data.notes || null,
            content_markdown: data.content_markdown || '',
          });
        } else {
          setAnswer({
            summary: `Backend returned ${response.status} ${response.statusText}`,
            steps: [],
            materials: [],
            timings: [],
            mantras: [],
            sources: [],
            notes: 'Please adjust your query and try again.',
            content_markdown: '',
          });
        }
        return;
      }

      setAnswer(data || {
        summary: 'No data returned from backend',
        steps: [],
        materials: [],
        timings: [],
        mantras: [],
        sources: [],
        notes: null,
        content_markdown: '',
      });
    } catch (error) {
      if (error?.name === 'AbortError') {
        setAnswer({
          summary: "The request timed out. Please try again; first runs may take longer.",
          steps: [],
          materials: [],
          timings: [],
          mantras: [],
          sources: [],
          notes: "If this keeps happening, reduce the topic scope or try a preset.",
          content_markdown: ""
        });
        return;
      }
      console.error('Error fetching from backend:', error);
      setAnswer({
        summary: "Error connecting to backend",
        steps: [],
        materials: [],
        timings: [],
        mantras: [],
        sources: [],
        notes: "Please check if the backend server is running and try again.",
        content_markdown: ""
      });
    } finally {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-6">
      <PresetButtons onSelect={handleAsk} />
      <ChatInput onAsk={handleAsk} loading={loading} />
      <AnswerDisplay loading={loading} answer={answer} />
    </div>
  );
}
