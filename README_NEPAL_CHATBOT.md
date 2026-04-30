# 🏔️ Nepal Tourism Chatbot

A lightweight, offline-capable tourism chatbot for Nepal built with **RAG (Retrieval-Augmented Generation)** and **local LLMs**. No external API dependencies required - perfect for course projects and demonstrations.

## ✨ Features

### Core Functions
- **Travel Inquiries**: Visa requirements, best time to visit, currency, transportation
- **Attraction Introductions**: Kathmandu, Pokhara, Everest, Chitwan, Lumbini, and more
- **Itinerary Planning**: 7-day, 10-day, and 14-day sample itineraries
- **Local Service Consultation**: Accommodation, food, activities, cultural etiquette
- **Activity Recommendations**: Trekking, wildlife safari, adventure sports, cultural tours

### Technical Features
- **RAG Architecture**: Combines vector search with local LLM for accurate responses
- **Local LLM**: Uses TinyLlama-1.1B for response generation (no API calls)
- **Vector Database**: ChromaDB for efficient knowledge retrieval
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2) for semantic search
- **GUI Interface**: Clean Tkinter-based desktop application
- **Fallback System**: Rule-based responses when LLM is unavailable

## 📁 Project Structure

```
/workspace/
├── nepal_knowledge.py      # Comprehensive Nepal tourism knowledge base
├── rag_system.py           # RAG implementation with local LLM
├── chatbot_gui.py          # Tkinter GUI interface
├── README.md               # This file
└── requirements.txt        # Python dependencies
```

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install chromadb sentence-transformers transformers torch nltk

# Run the GUI chatbot
python chatbot_gui.py
```

### Usage

1. **Launch the application**: Run `python chatbot_gui.py`
2. **Wait for initialization**: The system will load the knowledge base and local LLM
3. **Ask questions**: Type your Nepal tourism questions or use quick question buttons
4. **Get responses**: Receive accurate, context-aware answers

### Example Questions

- "What is the best time to visit Nepal?"
- "Tell me about trekking in Everest region"
- "What are the visa requirements for Nepal?"
- "What should I do in Pokhara?"
- "Recommend a 7-day itinerary for Nepal"
- "What food should I try in Nepal?"
- "How much does a trip to Nepal cost?"

## 🧠 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (Tkinter)                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    NepalChatbot Controller                   │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│   RAG System (Primary)  │     │  Rule-Based (Fallback)  │
│  ┌───────────────────┐  │     │  ┌───────────────────┐  │
│  │  ChromaDB Vector  │  │     │  │  Pattern Matching │  │
│  │     Search        │  │     │  │     Responses     │  │
│  └───────────────────┘  │     │  └───────────────────┘  │
│           │             │     └─────────────────────────┘
│           ▼             │
│  ┌───────────────────┐  │
│  │  TinyLlama-1.1B   │  │
│  │  Local LLM        │  │
│  └───────────────────┘  │
└─────────────────────────┘
```

## 📚 Knowledge Base Content

### Destinations Covered
- **Kathmandu**: City of Temples, UNESCO World Heritage Sites
- **Pokhara**: Lakes, mountains, adventure activities
- **Chitwan**: Wildlife safari, jungle experiences
- **Everest Region**: Base Camp trek, Sherpa culture
- **Annapurna Region**: Trekking paradise
- **Lumbini**: Birthplace of Buddha
- **Bhaktapur**: Medieval city, pottery
- **Nagarkot**: Himalayan sunrise views
- **Langtang**: Valley of Glaciers

### Topics Covered
- Visa requirements and entry procedures
- Best times to visit (seasonal guide)
- Trekking routes and difficulty levels
- Wildlife safari opportunities
- Adventure sports (paragliding, bungee, rafting)
- Cultural festivals and traditions
- Nepali cuisine and dining
- Transportation options
- Accommodation types and booking
- Health, safety, and travel insurance
- Currency and budgeting
- Cultural etiquette

## 🛠️ Technical Details

### Dependencies
- **chromadb**: Vector database for knowledge storage
- **sentence-transformers**: Text embeddings (all-MiniLM-L6-v2)
- **transformers**: Hugging Face transformers library
- **torch**: PyTorch for LLM inference
- **tkinter**: GUI framework (built-in with Python)

### Local LLM
- **Model**: TinyLlama/TinyLlama-1.1B-Chat-v1.0
- **Size**: ~1.1 billion parameters
- **Advantages**: Lightweight, fast inference, no API costs
- **Device**: Runs on CPU (GPU optional for faster inference)

### RAG Process
1. **User Query**: User asks a question about Nepal tourism
2. **Embedding**: Query is converted to vector embedding
3. **Retrieval**: Top-k relevant documents retrieved from ChromaDB
4. **Augmentation**: Context combined with query into prompt
5. **Generation**: Local LLM generates informed response
6. **Response**: Answer displayed to user

## 🎯 Course Requirements Compliance

✅ **No External APIs**: Fully local implementation  
✅ **Lightweight LLM**: TinyLlama-1.1B runs locally  
✅ **RAG Architecture**: Vector search + LLM generation  
✅ **Simple Interface**: Tkinter GUI, easy to use  
✅ **Nepal-Focused**: Comprehensive tourism knowledge base  
✅ **Stable & Accurate**: Fallback system ensures reliability  

## 💡 Customization

### Adding New Knowledge
Edit `nepal_knowledge.py` to add new destinations, activities, or information:

```python
NEPAL_TOURISM_DATA["destinations"]["NewPlace"] = {
    "description": "Description of new place",
    "highlights": ["Highlight 1", "Highlight 2"],
    "best_time": "Best visiting time",
    "activities": ["Activity 1", "Activity 2"]
}
```

### Modifying Responses
Adjust the system prompt in `rag_system.py` to change the bot's personality or response style.

### Extending Fallback Rules
Add new patterns to `rule_based_response()` function for common queries.

## 📝 License

This project is created for educational purposes. Feel free to modify and use for your course projects.

## 🙏 Acknowledgments

- **TinyLlama Team**: For the lightweight open-source LLM
- **Sentence Transformers**: For efficient embedding models
- **ChromaDB**: For simple vector database solution
- **Nepal Tourism Board**: For inspiration and information

---

**Namaste! 🙏 Happy exploring Nepal!**
