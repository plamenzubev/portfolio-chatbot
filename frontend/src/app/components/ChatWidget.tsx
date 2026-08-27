"use client";

import { useState } from "react";

type Source = { title: string; snippet: string };
type ChatMessage = { role: "user" | "assistant"; content: string; sources?: Source[] };

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function sendMessage() {
    const text = input.trim();
    if (!text || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/chat/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: text,
          ...(sessionId ? { session_id: sessionId } : {}),
        }),
      });
      if (!response.ok) throw new Error(`Request failed: ${response.status}`);

      const data: { session_id: string; reply: string; sources: Source[] } = await response.json();
      setSessionId(data.session_id);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.reply, sources: data.sources },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, something went wrong. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">
      {open && (
        <div className="mb-3 flex h-[28rem] w-80 flex-col overflow-hidden rounded-xl border border-black/10 bg-white shadow-xl dark:border-white/10 dark:bg-neutral-900">
          <div className="border-b border-black/10 px-4 py-3 font-medium dark:border-white/10">
            Ask me anything
          </div>

          <div className="flex-1 space-y-3 overflow-y-auto px-4 py-3 text-sm">
            {messages.length === 0 && (
              <p className="text-neutral-500">
                Ask about my projects, stack, or availability.
              </p>
            )}
            {messages.map((message, index) => (
              <div key={index}>
                <div
                  className={
                    message.role === "user"
                      ? "ml-auto max-w-[85%] rounded-lg bg-blue-600 px-3 py-2 text-white"
                      : "max-w-[85%] rounded-lg bg-neutral-100 px-3 py-2 dark:bg-neutral-800"
                  }
                >
                  {message.content}
                </div>
                {message.sources && message.sources.length > 0 && (
                  <div className="mt-1 space-y-1 text-xs text-neutral-500">
                    {message.sources.map((source, sourceIndex) => (
                      <div key={sourceIndex}>Source: {source.title}</div>
                    ))}
                  </div>
                )}
              </div>
            ))}
            {loading && <div className="text-neutral-500">Thinking…</div>}
          </div>

          <div className="flex gap-2 border-t border-black/10 p-3 dark:border-white/10">
            <input
              className="flex-1 rounded-md border border-black/10 bg-transparent px-3 py-2 text-sm outline-none dark:border-white/10"
              placeholder="Type a question…"
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={(event) => event.key === "Enter" && sendMessage()}
            />
            <button
              onClick={sendMessage}
              disabled={loading}
              className="rounded-md bg-blue-600 px-3 py-2 text-sm text-white disabled:opacity-50"
            >
              Send
            </button>
          </div>
        </div>
      )}

      <button
        onClick={() => setOpen((value) => !value)}
        className="rounded-full bg-blue-600 px-5 py-3 text-sm font-medium text-white shadow-lg"
      >
        {open ? "Close chat" : "Chat with me"}
      </button>
    </div>
  );
}
