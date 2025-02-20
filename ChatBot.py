__author__ = "Adnan Karol"
__version__ = "1.0.0"
__maintainer__ = "Adnan Karol"
__email__ = "adnanmushtaq5@gmail.com"

# Import Dependencies
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate


class Chatbot:
    """
    This class manages the conversation flow between the user and the AI model.
    It combines the context with user input to provide appropriate responses.
    """

    def __init__(self, model_name: str):
        """
        Initializes the Chatbot instance with the given AI model name.
        """
        self.model = OllamaLLM(model=model_name)
        self.chain = self._initialize_chat_chain()
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
        # Generate response from the model using the context and user input
        result = self.chain.invoke(
            {"context": user_input + self.context, "question": user_input}
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

            print(f"ChatBot 🤖: {response}")
            self.context += (
                f"\nUser: {user_input} \nAI: {response}"  # Update conversation history
            )


if __name__ == "__main__":
    # Initialize the chatbot
    chatbot = Chatbot(model_name="llama3")

    # Start the chatbot conversation
    chatbot.start_conversation()
