"""
RAG System for Nepal Tourism Chatbot
Combines vector search with local LLM for accurate question answering
No external API dependencies - fully local implementation
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from nepal_knowledge import get_knowledge_chunks, NEPAL_TOURISM_DATA
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import warnings
warnings.filterwarnings("ignore")

class NepalTourismRAG:
    def __init__(self):
        print("Initializing Nepal Tourism RAG System...")
        
        # Initialize ChromaDB for vector storage
        self.client = chromadb.Client(Settings(
            anonymized_telemetry=False,
            allow_reset=True,
            is_persistent=False
        ))
        
        # Create or get collection
        try:
            self.collection = self.client.get_collection("nepal_tourism")
            print("Loaded existing knowledge base")
        except:
            self.collection = self.client.create_collection("nepal_tourism")
            print("Created new knowledge base")
            self._build_knowledge_base()
        
        # Load lightweight embedding model
        print("Loading embedding model (all-MiniLM-L6-v2)...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load small local LLM for response generation
        print("Loading local LLM (TinyLlama-1.1B)...")
        self.llm_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        self.tokenizer = AutoTokenizer.from_pretrained(self.llm_name)
        self.llm = AutoModelForCausalLM.from_pretrained(
            self.llm_name,
            torch_dtype=torch.float32,
            device_map="auto",
            trust_remote_code=True
        )
        print("RAG System initialized successfully!")
    
    def _build_knowledge_base(self):
        """Build the knowledge base from Nepal tourism data"""
        chunks = get_knowledge_chunks()
        
        if len(self.collection.get()["ids"]) > 0:
            self.client.delete_collection("nepal_tourism")
            self.collection = self.client.create_collection("nepal_tourism")
        
        documents = []
        metadatas = []
        ids = []
        
        for i, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({"source": "nepal_tourism", "chunk_id": i})
            ids.append(f"chunk_{i}")
        
        # Add to collection with embeddings
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Indexed {len(documents)} knowledge chunks")
    
    def _get_embedding(self, text):
        """Generate embedding for text"""
        return self.embedding_model.encode(text).tolist()
    
    def retrieve_context(self, query, top_k=3):
        """Retrieve relevant context from knowledge base"""
        query_embedding = self._get_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        contexts = []
        if results and results['documents']:
            contexts = results['documents'][0]
        
        return contexts
    
    def generate_response(self, query, context):
        """Generate response using local LLM with retrieved context"""
        
        # Create prompt with context
        system_prompt = """You are a helpful Nepal Tourism Assistant. Use the provided context to answer questions about Nepal tourism accurately. If the context doesn't contain relevant information, use your general knowledge about Nepal tourism. Be friendly, informative, and helpful.

Context from knowledge base:
"""
        
        context_text = "\n\n".join(context) if context else "No specific context available."
        
        prompt = f"""{system_prompt}
{context_text}

User Question: {query}

Please provide a helpful, detailed answer based on the context above. If the context doesn't have specific information, supplement with your general knowledge about Nepal tourism. Keep your response concise but informative (2-4 sentences)."""

        # Tokenize and generate
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.llm.device)
        
        with torch.no_grad():
            outputs = self.llm.generate(
                **inputs,
                max_new_tokens=256,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
        
        # Clean up response
        response = response.strip()
        if "User Question:" in response:
            response = response.split("User Question:")[0].strip()
        
        return response
    
    def query(self, question):
        """Main query function combining retrieval and generation"""
        print(f"\nProcessing query: {question}")
        
        # Retrieve relevant context
        context = self.retrieve_context(question)
        
        # Generate response
        response = self.generate_response(question, context)
        
        return response, context


# Simple rule-based fallback for common queries
def rule_based_response(query):
    """Fallback responses for common queries when LLM is unavailable"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["hello", "hi", "namaste", "greet"]):
        return "Namaste! Welcome to Nepal Tourism Chatbot. I'm here to help you plan your perfect Nepal adventure. What would you like to know?", []
    
    if any(word in query_lower for word in ["visa", "permission", "entry"]):
        return "Tourist visas are available on arrival for most nationalities at Tribhuvan International Airport. Options: 15 days ($30), 30 days ($50), or 90 days ($125). You'll need a valid passport (6 months validity), passport photos, completed form, and USD cash.", []
    
    if any(word in query_lower for word in ["best time", "when to visit", "season"]):
        return "The best times to visit Nepal are October-November (clear skies, best mountain views) and March-April (warmer weather, rhododendron blooms). Winter (Dec-Feb) is good for lower altitude treks, while monsoon (Jun-Sep) offers lush greenery but possible disruptions.", []
    
    if any(word in query_lower for word in ["trek", "trekking", "hike", "hiking"]):
        return "Nepal offers world-class trekking! Popular routes include Everest Base Camp (challenging, 12-14 days), Annapurna Circuit (moderate-challenging, 15-20 days), Langtang Valley (moderate, 7-10 days), and Ghorepani Poon Hill (easy, 4-5 days). You'll need TIMS card and relevant permits.", []
    
    if any(word in query_lower for word in ["pokhara", "lake", "paragliding"]):
        return "Pokhara is Nepal's tourism capital, famous for Phewa Lake, stunning mountain views, and adventure activities. Must-see spots include Davis Fall, Gupteshwor Cave, World Peace Pagoda, and Sarangkot for sunrise. Perfect for boating, paragliding, zip-lining, and cave exploration!", []
    
    if any(word in query_lower for word in ["everest", "base camp", "sagarmatha"]):
        return "Mount Everest (8848.86m) is the world's highest peak! The Everest Base Camp trek takes 12-14 days, passing through Namche Bazaar and Tengboche Monastery. Best seasons are March-May and September-November. Helicopter tours are also available for those short on time.", []
    
    if any(word in query_lower for word in ["chitwan", "wildlife", "safari", "jungle"]):
        return "Chitwan National Park is a UNESCO World Heritage Site famous for one-horned rhinoceros and Bengal tigers. Enjoy jungle safaris, bird watching, canoe rides on Rapti River, elephant bathing, and Tharu cultural shows. Best visited October-February.", []
    
    if any(word in query_lower for word in ["lumbini", "buddha", "pilgrimage"]):
        return "Lumbini is the birthplace of Lord Buddha and a major Buddhist pilgrimage site. Key attractions include Maya Devi Temple, Ashoka Pillar, Sacred Garden, and the Monastic Zone with monasteries from various countries. Best visited October-April.", []
    
    if any(word in query_lower for word in ["food", "cuisine", "eat", "dal bhat", "momo"]):
        return "Nepali cuisine is delicious! Must-try dishes include Dal Bhat (lentil soup with rice and curry - the staple meal), Momo (dumplings filled with meat or vegetables), Sel Roti (ring-shaped bread), and Thukpa (noodle soup). Newari cuisine offers rich traditional flavors.", []
    
    if any(word in query_lower for word in ["kathmandu", "capital", "thamel"]):
        return "Kathmandu, the 'City of Temples', houses seven UNESCO World Heritage Sites! Don't miss Kathmandu Durbar Square, Swayambhunath (Monkey Temple), Boudhanath Stupa, and Pashupatinath Temple. Thamel is the tourist hub for shopping, dining, and accommodation.", []
    
    if any(word in query_lower for word in ["itinerary", "plan", "schedule", "days"]):
        return "For a first visit, consider: 7 days (Kathmandu + Pokhara highlights), 10 days (add Chitwan safari), or 14 days (complete experience including Lumbini). Peak season bookings should be made in advance. Would you like a detailed day-by-day itinerary?", []
    
    if any(word in query_lower for word in ["cost", "budget", "expensive", "cheap", "money", "currency"]):
        return "Nepal uses Nepalese Rupee (NPR), approximately 1 USD = 130-135 NPR. Budget travelers can manage on $20-40/day, mid-range $50-100/day, and luxury $150+/day. ATMs are available in cities; carry cash for remote areas. Trekking costs vary by route and duration.", []
    
    return None, []


class NepalChatbot:
    def __init__(self):
        self.rag_system = None
        self.initialized = False
    
    def initialize(self):
        """Initialize the RAG system"""
        try:
            self.rag_system = NepalTourismRAG()
            self.initialized = True
            return True
        except Exception as e:
            print(f"Warning: Could not initialize full RAG system: {e}")
            print("Using rule-based responses only.")
            self.initialized = False
            return False
    
    def respond(self, query):
        """Get response to user query"""
        if self.initialized and self.rag_system:
            try:
                response, context = self.rag_system.query(query)
                if response and len(response) > 10:
                    return response
            except Exception as e:
                print(f"LLM query failed: {e}")
        
        # Fallback to rule-based
        response, _ = rule_based_response(query)
        if response:
            return response
        
        return "I'd love to help you with information about Nepal tourism! Please ask me about destinations (Kathmandu, Pokhara, Everest, Chitwan, Lumbini), activities (trekking, wildlife safari, adventure sports), visa requirements, best time to visit, food, culture, or itinerary planning. Namaste!"


if __name__ == "__main__":
    # Test the RAG system
    chatbot = NepalChatbot()
    chatbot.initialize()
    
    test_queries = [
        "What is the best time to visit Nepal?",
        "Tell me about trekking in Everest region",
        "What should I know about getting a visa for Nepal?"
    ]
    
    for query in test_queries:
        print("\n" + "="*60)
        print(f"Query: {query}")
        response = chatbot.respond(query)
        print(f"Response: {response}")
        print("="*60)
