import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [dark, setDark] = useState(false);
  const [fileText, setFileText] = useState('');
  const [qaQuery, setQaQuery] = useState('');
  const [qaAnswer, setQaAnswer] = useState('');

  const send = async () => {
    const { data } = await axios.post('/api/chat/', { query });
    setMessages([...messages, { q: query, a: data.response }]);
    setQuery('');
  };

  const toggleDark = () => setDark(!dark);

  const upload = async e => {
    const file = e.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    const { data } = await axios.post('/api/upload/', formData);
    setFileText(data.text);
  };

  const askDoc = async () => {
    const fileInput = document.getElementById('docfile');
    const file = fileInput.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    formData.append('query', qaQuery);
    const { data } = await axios.post('/api/upload/qa', formData);
    setQaAnswer(data.answer);
  };

  return (
    <div className={dark ? 'dark' : ''}>
      <header>
        <h1>Vidhik Mitra</h1>
        <button onClick={toggleDark}>Toggle Theme</button>
      </header>
      <div className="chat">
        {messages.map((m, i) => (
          <div key={i} className="pair">
            <div className="query">{m.q}</div>
            <div className="answer">{m.a}</div>
          </div>
        ))}
      </div>
      <input value={query} onChange={e => setQuery(e.target.value)} />
      <button onClick={send}>Send</button>
      <input id="docfile" type="file" onChange={upload} />
      {fileText && (
        <div className="doc-section">
          <pre className="filetext">{fileText}</pre>
          <input
            value={qaQuery}
            onChange={e => setQaQuery(e.target.value)}
            placeholder="Ask about this document"
          />
          <button onClick={askDoc}>Ask</button>
          {qaAnswer && <div className="answer">{qaAnswer}</div>}
        </div>
      )}
      <div className="disclaimer">Responses are for informational purposes only and not legal advice.</div>
    </div>
  );
}

export default App;
