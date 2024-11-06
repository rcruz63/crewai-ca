from openai import OpenAI
from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html


class BrowserTools:

    @tool("Extraer contenido de la web")
    def scrape_and_summarize_website(website):
        """
        Útil para extraer y resumir el contenido de un sitio web usando la API de OpenAI.

        Args:
            website (str): URL del sitio web para extraer y resumir.

        Returns:
            str: Contenido resumido del sitio web.
        """

        client = OpenAI()

        # Utilizamos un prompt en OpenAI para simular el scraping y obtención del contenido del sitio web
        prompt = (
            f"Por favor, obtén y resume el contenido principal del sitio web {website}. "
            "Incluye solo la información más relevante y devuelve un resumen claro y conciso."
        )

        # Llamada al modelo de OpenAI para generar la respuesta
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Eres un asistente útil que extrae y resume el contenido de sitios web."},
                      {"role": "user", "content": prompt}]
        )

        content = response['choices'][0]['message']['content']
        elements = partition_html(text=content)

        # Dividir el contenido si es demasiado largo
        content_chunks = [str(el) for el in elements]
        content = "\n\n".join(content_chunks)
        content = [content[i: i + 8000] for i in range(0, len(content), 8000)]

        summaries = []
        for chunk in content:
            agent = Agent(
                role="Investigador Principal",
                goal="Realiza investigaciones y resúmenes sorprendentes basados en el contenido con el que trabajas",
                backstory="Eres un Investigador Principal en una gran empresa y necesitas hacer una investigación "
                "sobre un tema dado.",
                allow_delegation=False,
            )
            task = Task(
                agent=agent,
                description="Analiza y resume el contenido a continuación, asegurándote de incluir la información más relevante "
                            "en el resumen, devuelve solo el resumen, nada más.\n\nCONTENIDO\n----------\n{chunk}",
            )
            summary = task.execute()
            summaries.append(summary)
        return "\n\n".join(summaries)
