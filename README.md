# JARVIS

## **Features**
✅ Task Management  

---

## **Tech Stack**
| Component | Technology |
|---|---|
| **Frontend** | Next.js |
| **Primary Backend** | Go |
| **Secondary Backend** | Python |
| **Database** | PostgreSQL (user data) + ChromaDB (for RAG) |
| **LLM Provider** | Ollama |
| **Model** | LLaMA 3.2 (3B) |

---

## **Architecture Overview**
### **Primary Backend**
- Contains all the tools  
- Handles authentication  
- Uses PostgreSQL  
- Written in Go  

### **Secondary Backend**
- Manages chat with memory  
- Handles tool orchestration  
- Connects with ChromaDB  

---

## **Phase 1: Building Primary Backend**
### **1. Build Tools**
- [ ] Create Task Tool  
- [ ] Get Task Tool  
- [ ] Delete Task Tool  
- [ ] Update Task Tool  

---

### **2. Build an API Layer**
- [ ] RESTful or gRPC endpoints for tool functions  
- [ ] Versioned API design for future compatibility  
- [ ] Request/response validation  

---

### **3. Authentication & Authorization**
- [ ] User authentication system (JWT or similar)  
- [ ] Role-based access control for different tools  
- [ ] API key validation for service-to-service communication with the Python layer  

---

### **4. Logging & Monitoring**
- [ ] Structured logging  
- [ ] Basic metrics for API usage  
- [ ] Request tracing  

---

## **Phase 2: Building Secondary Backend**
### **1. LLM Integration**
- [ ] Connection to LLM API (Anthropic, OpenAI, etc.)  
- [ ] Prompt template management  
- [ ] Response parsing and handling  

---

### **2. Tool Selection Logic**
- [ ] Analyze user requests and determine appropriate tools  
- [ ] Planning logic for multi-step operations  
- [ ] Error recovery and fallback mechanisms  

---

### **3. Communication with Primary Backend**
- [ ] Authenticated API client for Go backend  
- [ ] Request formatting and response parsing  
- [ ] Error handling for backend failures  

---

### **4. User Interaction Management**
- [ ] Context tracking across conversation turns  
- [ ] State management for ongoing operations  
- [ ] Handling clarification requests when needed  

---

## **Bonus Features (Future Enhancements)**
- 🔹 **Natural conversation flow** – LLM-driven dialogue engine  
- 🔹 **Real-time speech processing** – Whisper + text-to-speech  
- 🔹 **Auto-learn new functions** – From docs/code snippets  
- 🔹 **Multi-agent collaboration** – JARVIS delegates tasks to sub-agents  

---
