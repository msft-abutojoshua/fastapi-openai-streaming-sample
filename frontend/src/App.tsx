import { useState } from "react";
import axios from "axios";
 
interface Message {
  role: "system" | "user" | "assistant";
  content: string;
}
 
const App: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { role: "system", content: "You are a helpful assistant." },
  ]);
  const [input, setInput] = useState<string>("");
  const [response, setResponse] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
 
  const handleSendMessage = async () => {
    if (!input.trim()) return;
 
    const newMessages: Message[] = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setResponse("");
    setLoading(true);
 
    try {
const eventSource = new EventSource("http://127.0.0.1:8000/chat-stream");
 
      eventSource.onmessage = (event: MessageEvent) => {
setResponse((prev) => prev + event.data);
      };
 
      eventSource.onerror = () => {
        eventSource.close();
        setLoading(false);
      };
 
      eventSource.addEventListener("close", () => {
        eventSource.close();
        setLoading(false);
      });
 
await axios.post("http://127.0.0.1:8000/chat-stream", {
        messages: newMessages,
        temperature: 0.7,
        max_tokens: 500,
      });
    } catch (error) {
      console.error("Error:", error);
      setLoading(false);
    }
  };
 
  return (
    <div style={{ maxWidth: "600px", margin: "0 auto", padding: "20px" }}>
      <h1>Chat with GPT</h1>
      <div style={{ border: "1px solid #ccc", padding: "10px", minHeight: "200px" }}>
        {response || (loading ? "Thinking..." : "Ask me anything!")}
      </div>
      <input
        type="text"
        value={input}
onChange={(e) => setInput(e.target.value)}
        style={{ width: "100%", padding: "10px", marginTop: "10px" }}
        placeholder="Type a message..."
      />
      <button onClick={handleSendMessage} style={{ width: "100%", padding: "10px", marginTop: "10px" }}>
        Send
      </button>
    </div>
  );
};
 
export default App;