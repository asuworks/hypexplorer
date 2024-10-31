from dataclasses import dataclass

from langchain_ollama import OllamaLLM
from temporalio import activity

from langchain_core.prompts import ChatPromptTemplate


@dataclass
class TranslateParams:
    phrase: str
    language: str


@activity.defn
async def translate_phrase(phrase: str, language: str) -> dict:
    # LangChain setup
    template = """You are a helpful assistant who translates between languages.
    Translate the following phrase into the specified language: {phrase}
    Language: {language}"""
    chat_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            ("human", "Translate"),
        ]
    )
    model = OllamaLLM(model="llama3.1", base_url="http://localhost:11434")

    chain = chat_prompt | model
    # Use the asynchronous invoke method
    response = await chain.ainvoke({"phrase": phrase, "language": language})
    translation = {"content": response}
    return translation
