__author__ = "Adnan Karol"
__version__ = "1.0.0"
__maintainer__ = "Adnan Karol"
__email__ = "adnanmushtaq5@gmail.com"


# Import Dependencies
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate


class KnowledgeBase:
    """
    This class is responsible for handling the knowledge base, which includes embedding and storing text
    in a FAISS vector store for efficient similarity search.
    """

    def __init__(self, model_name: str, file_path: str):
        self.embeddings = HuggingFaceEmbeddings(model_name=model_name)
        self.knowledge_base = self._initialize_knowledge_base(file_path)

    def _initialize_knowledge_base(self, file_path: str):
        """
        Initializes the knowledge base from a given text file by embedding the text and storing it in FAISS.
        """
        with open(file_path, "r") as file:
            content = file.read()
        sections = content.split("**")
        return FAISS.from_texts(sections, self.embeddings)

    def retrieve_context(self, user_input: str, k: int = 3):
        """
        Retrieves relevant context from the knowledge base based on user input.
        """
        retrieved_docs = self.knowledge_base.similarity_search(user_input, k=k)
        return "\n".join([doc.page_content for doc in retrieved_docs])


class Chatbot:
    """
    This class manages the conversation flow between the user and the AI model.
    It combines the context with user input to provide appropriate responses.
    """

    def __init__(self, model_name: str, knowledge_base: KnowledgeBase):
        self.model = OllamaLLM(model=model_name)
        self.chain = self._initialize_chat_chain()
        self.knowledge_base = knowledge_base
        self.context = ""  # Stores conversation history

    def _initialize_chat_chain(self):
        """
        Initializes the chat chain, which connects the chat prompt template with the AI model.
        """
        template = """
        Answer the question below using the given context.

        Here is the conversation history:
        {context}

        Question: {question}

        Answer:
        """
        prompt = ChatPromptTemplate.from_template(template)
        return prompt | self.model

    def handle_input(self, user_input: str):
        """
        Handles the user input, retrieves relevant context, and generates a response.
        """
        # Retrieve context from the knowledge base based on user input
        retrieved_text = self.knowledge_base.retrieve_context(user_input)

        # Generate response from the model using the context and user input
        result = self.chain.invoke(
            {"context": retrieved_text + self.context, "question": user_input}
        )
        return result

    def start_conversation(self):
        """
        Starts and manages the conversation between the user and the chatbot.
        """
        print("Welcome to RagMind 🤖💬, type 'exit' to quit!")

        while True:
            user_input = input("You 👤: ")
            if user_input.lower() == "exit":
                print("Goodbye! 👋")
                break

            # Generate response based on user input and context
            response = self.handle_input(user_input)

            print(f"RagBot 🤖: {response}")
            self.context += (
                f"\nUser: {user_input} \nAI: {response}"  # Update conversation history
            )


if __name__ == "__main__":
    # Initialize the knowledge base and chatbot
    knowledge_base = KnowledgeBase(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        file_path="Internal_Data.txt",
    )
    chatbot = Chatbot(model_name="llama3", knowledge_base=knowledge_base)

    # Start the chatbot conversation
    chatbot.start_conversation()
