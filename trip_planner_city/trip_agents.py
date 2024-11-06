from crewai import Agent
# from langchain.llms import OpenAI
# from langchain.chat_models import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from tools.scraper_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools

from dotenv import load_dotenv
load_dotenv()


class TripAgents:

    llm = ChatOpenAI(model='gpt-4o-mini')

    def editor_blog(self):
        return Agent(
            role="Amigo editor experto de guias de viaje",
            goal="Describir de forma atractiva y cercana lo que vamos a hacer en la ciudad",
            backstory="Es un amigo que conoce muy bien el destino y nos va a contar todo lo que necesitamos saber",
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
            ],
            llm=self.llm,
            verbose=True,
        )

    def local_expert(self):
        return Agent(
            role="Experto Local en esta ciudad",
            goal="Proporcionar los MEJORES consejos sobre la ciudad seleccionada",
            backstory="""Un guía local con gran conocimiento y amplia información
        sobre la ciudad, sus atracciones, los mejores sitios donde comer y los sitios sorprendentes y poco conocidos""",
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
            ],
            llm=self.llm,
            verbose=True,
        )

    def travel_concierge(self):
        return Agent(
            role="Asistente de Viaje Extraordinario",
            goal="Crear los itinerarios de viaje más increíbles ajustados a la duración del viaje y "
            "con mejor relación calidad precio para el viajero",
            backstory="Especialista en planificación y logística de viajes con "
                      "décadas de experiencia",
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
                CalculatorTools.calculate,
            ],
            llm=self.llm,
            verbose=True,
        )
