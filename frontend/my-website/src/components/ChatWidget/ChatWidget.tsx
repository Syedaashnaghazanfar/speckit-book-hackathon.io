/**
 * ChatWidget Component
 *
 * A floating chatbot widget powered by Gemini via our RAG backend.
 * Features:
 * - Floating button that opens chat interface
 * - Message history
 * - Loading states
 * - Error handling
 * - Source citations
 * - Scoped queries from text selection
 */

import React, {
  useState,
  useRef,
  useEffect,
  useImperativeHandle,
  forwardRef,
} from "react";
// import { useLanguage } from "../../hooks/useLanguage";
import styles from "./ChatWidget.module.css";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  confidence?: string;
  timestamp: Date;
}

interface Source {
  excerpt_num: number;
  week: number;
  section: string;
  score: number;
}

interface ChatResponse {
  answer: string;
  sources: Source[];
  has_answer: boolean;
  confidence: string;
  num_sources: number;
  query_processed: string;
}

export interface ChatWidgetRef {
  askAboutSelection: (selectedText: string) => void;
}

const ChatWidget = forwardRef<ChatWidgetRef>((props, ref) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content:
        "👋 Hi! I'm your AI textbook assistant powered by Gemini. Ask me anything about Physical AI and Humanoid Robotics!\nYou can also select text from the book and right click to ask me about it.",
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
    }
  }, [isOpen]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: inputValue.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue("");
    setIsLoading(true);
    setError(null);

    try {
      // Detect environment and use appropriate API URL
      // In production (deployed), use Hugging Face Space URL
      // In development (localhost), use local backend
      const apiUrl = window.location.hostname === "localhost"
        ? "http://localhost:8000"
        : "https://ashnaali22-hackhathon-backend.hf.space";

      const response = await fetch(`${apiUrl}/api/chat/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: userMessage.content,
          top_k: 5,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.answer,
        sources: data.sources,
        confidence: data.confidence,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to get response");
      console.error("Chat error:", err);

      // Add error message to chat
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          "❌ Sorry, I encountered an error. Please make sure the backend server is running and try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  // Expose method to handle text selection queries
  const askAboutSelection = (selectedText: string) => {
    // Open chat if closed
    if (!isOpen) {
      setIsOpen(true);
    }

    setError(null); // Clear previous errors

    const MIN_SELECTION_LENGTH = 3;
    const MAX_SELECTION_LENGTH = 500;

    if (selectedText.length < MIN_SELECTION_LENGTH) {
      setError(`Please select at least ${MIN_SELECTION_LENGTH} characters.`);
      return;
    }

    if (selectedText.length > MAX_SELECTION_LENGTH) {
      setError(`Selected text is too long (max ${MAX_SELECTION_LENGTH} characters).`);
      return;
    }

    // Create a scoped query message
    const scopedQuery = `Based on the following selected text, please answer my question:\n\n"${selectedText}"\n\nQuestion: What does this text mean? Explain it to me.`;

    setInputValue(scopedQuery);

    // Automatically send the query after a short delay to ensure chat is open and state is updated
    setTimeout(() => {
      handleSendMessage();
    }, 300);
  };

  useImperativeHandle(ref, () => ({
    askAboutSelection,
  }));

  // Helper function to render basic Markdown
  const renderMarkdown = (text: string) => {
    // Bold: **text** or __text__
    let html = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');
    // Italics: *text* or _text_
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    html = html.replace(/_(.*?)_/g, '<em>$1</em>');
    // Blockquote: > text
    html = html.replace(/^>\s*(.*)$/gm, '<blockquote>$1</blockquote>');
    // Remove inline source citations: [Source: ...]
    html = html.replace(/\[Source:\s*([^\]]+)\]/g, '');
    // Newlines to <br> for simple paragraph breaks (optional, but makes blocks look cleaner)
    html = html.replace(/\n/g, '<br />');

    return html;
  };

  return (
    <div className={styles.chatWidget}>
      {/* Floating Button */}
      <button
        className={`${styles.floatingButton} ${isOpen ? styles.open : ""}`}
        onClick={toggleChat}
        aria-label="Toggle chat"
      >
        {isOpen ? "✕" : "💬"}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className={styles.chatWindow}>
          {/* Header */}
          <div className={styles.header}>
            <div className={styles.headerContent}>
              <span className={styles.title}>🤖 AI Assistant</span>
              <span className={styles.subtitle}>Powered by Gemini</span>
            </div>
          </div>

          {/* Messages */}
          <div className={styles.messages}>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`${styles.message} ${
                  message.role === "user"
                    ? styles.userMessage
                    : styles.assistantMessage
                }`}
              >
                <div className={styles.messageContent}>
                  <div className={styles.messageText} dangerouslySetInnerHTML={{ __html: renderMarkdown(message.content) }}></div>

                  {/* Sources */}
                  {message.sources && message.sources.length > 0 && (
                    <div className={styles.sources}>
                      <div className={styles.sourcesTitle}>📚 Sources:</div>
                      {message.sources.map((source) => (
                        <div key={source.excerpt_num} className={styles.source}>
                          Week {source.week} - {source.section}
                          <span className={styles.sourceScore}>
                            ({(source.score * 100).toFixed(0)}% relevant)
                          </span>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Confidence Badge */}
                  {message.confidence && (
                    <div
                      className={`${styles.confidence} ${styles[`confidence${message.confidence}`]}`}
                    >
                      {message.confidence} confidence
                    </div>
                  )}
                </div>

                <div className={styles.timestamp}>
                  {message.timestamp.toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </div>
              </div>
            ))}

            {/* Loading Indicator */}
            {isLoading && (
              <div className={`${styles.message} ${styles.assistantMessage}`}>
                <div className={styles.messageContent}>
                  <div className={styles.typing}>
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className={styles.inputContainer}>
            <input
              ref={inputRef}
              type="text"
              className={styles.input}
              placeholder="Ask about ROS, Gazebo, Isaac Sim..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
            />
            <button
              className={styles.sendButton}
              onClick={handleSendMessage}
              disabled={isLoading || !inputValue.trim()}
              aria-label="Send message"
            >
              {isLoading ? "⏳" : "🚀"}
            </button>
          </div>

          {/* Error Display */}
          {error && <div className={styles.error}>{error}</div>}
        </div>
      )}
    </div>
  );
});

ChatWidget.displayName = "ChatWidget";

export default ChatWidget;
