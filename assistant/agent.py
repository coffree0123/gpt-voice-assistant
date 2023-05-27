import faiss
from assistant.prompt.conversation import load_assistant_prompt

from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from langchain.experimental import AutoGPT
from langchain.chat_models import ChatOpenAI


def build_gpt_agent(prompt: str = 'en_assistant'):
    # Prepare prompt for chatgpt agent. You can add any prompt templete as you wish.
    # Chek prompts folder for more information.
    prompt = load_assistant_prompt(prompt)

    tools = [
        WriteFileTool(),
        ReadFileTool(),
    ]

    # Define your embedding model
    embeddings_model = OpenAIEmbeddings()
    # Initialize the vectorstore as empty

    embedding_size = 1536
    index = faiss.IndexFlatL2(embedding_size)
    vectorstore = FAISS(embeddings_model.embed_query,
                        index, InMemoryDocstore({}), {})
    # Prepare agent chain for ai-assistant.
    agent = AutoGPT.from_llm_and_tools(
        ai_name="Coffree",
        ai_role="Assistant",
        tools=tools,
        llm=ChatOpenAI(model='gpt-3.5-turbo', temperature=0),
        memory=vectorstore.as_retriever()
    )
    # Set verbose to be true
    agent.chain.verbose = True

    # agent = LLMChain(
    #     # You can change model to gpt-4 as well.
    #     llm=ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo'),
    #     prompt=prompt,
    #     verbose=True,
    #     memory=ConversationBufferWindowMemory(k=2),
    # )

    return agent
