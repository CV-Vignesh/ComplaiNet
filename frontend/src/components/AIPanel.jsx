import React, { useState, useRef, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { addMessage, setProcessing } from '../store/chatSlice';
import { updateEntireComplaint } from '../store/complaintSlice';
import { aiProcessPrompt, aiProcessDocument } from '../services/api';
import { Send, UploadCloud, FileText } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

const AIPanel = () => {
  const dispatch = useDispatch();
  const { messages, isProcessing } = useSelector((state) => state.chat);
  const currentFormData = useSelector((state) => state.complaint.data);
  const [input, setInput] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const chatEndRef = useRef(null);
  const fileInputRef = useRef(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendPrompt = async (e) => {
    e.preventDefault();
    if (!input.trim() || isProcessing) return;

    const userMsg = input.trim();
    setInput('');
    
    // Add user message to UI
    dispatch(addMessage({
      id: Date.now().toString(),
      sender: 'user',
      text: userMsg,
      timestamp: new Date().toISOString()
    }));
    
    dispatch(setProcessing(true));

    try {
      const response = await aiProcessPrompt(userMsg, currentFormData);
      
      // Update form if AI extracted data
      if (response.extracted_data) {
        dispatch(updateEntireComplaint(response.extracted_data));
      }
      
      // Add AI response to UI
      dispatch(addMessage({
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: response.ai_message || "I have processed your request.",
        timestamp: new Date().toISOString()
      }));
    } catch (error) {
      console.error(error);
      dispatch(addMessage({
        id: Date.now().toString(),
        sender: 'system-error',
        text: 'Error connecting to the AI backend. Please ensure the server is running.',
        timestamp: new Date().toISOString()
      }));
    } finally {
      dispatch(setProcessing(false));
    }
  };

  const handleFileUpload = async (file) => {
    if (!file || isProcessing) return;
    
    dispatch(addMessage({
      id: Date.now().toString(),
      sender: 'user',
      text: `*Uploaded Document: ${file.name}*`,
      timestamp: new Date().toISOString()
    }));
    
    dispatch(setProcessing(true));

    try {
      const response = await aiProcessDocument(file, currentFormData);
      
      if (response.extracted_data) {
        dispatch(updateEntireComplaint(response.extracted_data));
      }
      
      dispatch(addMessage({
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text: response.ai_message || `I have analyzed ${file.name} and extracted the data into the form.`,
        timestamp: new Date().toISOString()
      }));
    } catch (error) {
      console.error(error);
      dispatch(addMessage({
        id: Date.now().toString(),
        sender: 'system-error',
        text: `Failed to process ${file.name}. Ensure the backend is running.`,
        timestamp: new Date().toISOString()
      }));
    } finally {
      dispatch(setProcessing(false));
    }
  };

  // Drag and Drop Handlers
  const onDragOver = (e) => { e.preventDefault(); setIsDragging(true); };
  const onDragLeave = (e) => { e.preventDefault(); setIsDragging(false); };
  const onDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  return (
    <>
      <div className="chat-container">
        {messages.map((msg) => (
          <div key={msg.id} className={`chat-message ${msg.sender}`}>
            {msg.sender === 'ai' ? (
              <ReactMarkdown>{msg.text}</ReactMarkdown>
            ) : (
              msg.text
            )}
          </div>
        ))}
        {isProcessing && (
          <div className="chat-message ai loading-dots">
            Analyzing
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      <div className="chat-input-area">
        {/* Drag and Drop Zone */}
        <div 
          className={`dropzone ${isDragging ? 'active' : ''}`}
          onDragOver={onDragOver} onDragLeave={onDragLeave} onDrop={onDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <UploadCloud size={24} className="dropzone-icon" />
          <div>Drag & Drop a PDF/DOCX/EML here, or click to browse.</div>
          <input 
            type="file" ref={fileInputRef} style={{ display: 'none' }}
            onChange={(e) => { if(e.target.files?.[0]) handleFileUpload(e.target.files[0]); }}
            accept=".pdf,.docx,.doc,.txt,.eml"
          />
        </div>

        {/* Text Input */}
        <form className="chat-form" onSubmit={handleSendPrompt}>
          <input
            type="text"
            className="chat-input"
            placeholder="Type your instructions (e.g. 'Log a complaint for Aspirin...')"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isProcessing}
          />
          <button type="submit" className="chat-submit-btn" disabled={isProcessing || !input.trim()}>
            <Send size={16} />
          </button>
        </form>
      </div>
    </>
  );
};

export default AIPanel;
