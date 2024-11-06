from crewai import Agent, Task, Crew

import os
from utils import get_openai_api_key

openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'

searcher = Agent(
    role="Buscador de Viajes",
    goal="Buscar y seleccionar los mejores sitios para visitar y comer en {topic}, "
         "teniendo en cuenta el destino, la duración del viaje y las preferencias del viajero.",
    backstory="Eres un experto en buscar los mejores lugares para disfrutar de un destino. "
              "Tu tarea es seleccionar los puntos de mayor interés, los mejores restaurantes con buena "
              "relación calidad-precio y algunos sitios secretos o curiosos que hagan el viaje especial. "
              "El objetivo es que las opciones sean asequibles, a menos que el viajero tenga otras preferencias "
              "especificadas en el '{topic}'.",
    allow_delegation=False,
    verbose=True
)

planner = Agent(
    role="Organizador de Viajes",
    goal="Organizar el itinerario de viaje en {topic}, "
         "optimizando las recomendaciones del Buscador y ajustándose al tiempo disponible.",
    backstory="Eres un experto en organizar itinerarios de viaje. "
              "Tu tarea es distribuir las actividades seleccionadas por el Buscador en un itinerario equilibrado, "
              "priorizando la cercanía entre los puntos de interés y evitando desplazamientos innecesarios. "
              "Además, agrupas las visitas según la relación temática para mejorar la experiencia del viajero, "
              "y te aseguras de que cada día incluya al menos una opción para comer y cenar.",
    allow_delegation=False,
    verbose=True
)

presenter = Agent(
    role="Presentador de Viajes",
    goal="Presentar el plan de viaje proporcionado por el Organizador en formato markdown, "
         "de manera atractiva, clara y cercana.",
    backstory="Eres un amigo que conoce bien el destino y tienes la misión de presentar "
              "el itinerario de una forma amena y cercana. Creas un plan fácil de seguir, "
              "organizado por días y actividades, con descripciones cálidas que hagan el viaje "
              "tan atractivo como interesante. Además, ofreces alternativas cuando las haya, "
              "presentándolas como opciones adicionales que podrían interesar al viajero.",
    allow_delegation=False,
    verbose=True
)

search_task = Task(
    description=(
        "1. Busca y selecciona los puntos de mayor interés turístico en {topic}, "
        "asegurando que cubran las principales atracciones del destino.\n"
        "2. Selecciona los mejores restaurantes y lugares donde comer, con un enfoque "
        "en opciones económicas, pero de buena calidad, salvo que en el '{topic}' se indique otra preferencia.\n"
        "3. Identifica sitios secretos o menos conocidos que puedan hacer el viaje especial, "
        "añadiendo un toque único a la experiencia.\n"
        "4. Proporciona una opción principal y al menos una alternativa tanto para visitas turísticas "
        "como para lugares donde comer o cenar."
    ),
    expected_output="Una lista de recomendaciones que incluya lugares de interés turístico, "
                    "restaurantes con buena relación calidad-precio, y sitios secretos o curiosos, "
                    "teniendo en cuenta las preferencias expresadas y el presupuesto económico.",
    agent=searcher,
)

plan_task = Task(
    description=(
        "1. Organiza las recomendaciones del Buscador en un itinerario diario, "
        "asegurándote de minimizar los desplazamientos innecesarios entre los puntos de interés.\n"
        "2. Agrupa las visitas y actividades por cercanía geográfica, "
        "y cuando sea posible, por relación temática para mejorar la experiencia del viaje.\n"
        "3. Ajusta el itinerario para que encaje con la duración del viaje y el tiempo disponible, "
        "respetando los horarios de llegada y partida.\n"
        "4. Incluye al menos un lugar para comer y otro para cenar cada día, "
        "según las recomendaciones del Buscador.\n"
        "5. Proporciona alternativas cuando sea posible, tanto en visitas como en opciones de comida y cena, "
        "para ofrecer flexibilidad al viajero.\n"
        "6. Proporciona un itinerario equilibrado, evitando que las jornadas sean demasiado intensas o desorganizadas."
    ),
    expected_output="Un itinerario diario optimizado y equilibrado, que incluya las actividades principales, "
                    "minimizando desplazamientos y agrupando los puntos de interés de manera lógica, "
                    "junto con opciones para comer, cenar y alternativas si las hay.",
    agent=planner,
)

present_task = Task(
    description=(
        "1. Presenta el itinerario organizado por el Planificador en formato markdown, "
        "dividiendo el plan por días y actividades, sin incluir horarios estrictos.\n"
        "2. Escribe descripciones breves, cálidas y en un lenguaje cercano y amigable, "
        "como si recomendaras el viaje a un amigo.\n"
        "3. Incluye una breve explicación de por qué cada actividad o lugar vale la pena visitar, "
        "haciendo que suene atractivo y especial.\n"
        "4. Ofrece las alternativas proporcionadas por el Planificador de forma amena, "
        "presentándolas como opciones adicionales para flexibilizar el viaje.\n"
        "5. Mantén el tono simpático y cercano en todo momento, asegurándote de que el viajero "
        "se sienta motivado a seguir el plan."
    ),
    expected_output="Un itinerario atractivo en formato markdown, organizado por días, con descripciones breves, "
                    "cercanas y cálidas, que incluyan las actividades principales y alternativas si las hay.",
    agent=presenter,
)

crew = Crew(
    agents=[searcher, planner, presenter],
    tasks=[search_task, plan_task, present_task],
    verbose=2
)

ruta = ("Visita a Roma. "
        "Salida el 19 de Diciembre a las 9:00h. desde Madrid "
        "y regreso el 23 de Diciembre a las 22:00h. desde Roma. "
        "Nuestro Hotel es Leonardo Boutique Hotel Rome Termini"
        "No pueden faltar la Fontana di Trevi, el Coliseo, "
        "El Panteón, La plaza Navona, el castillo de Sant'Angelo, "
        "el Vaticano, El Moises de Miguel Angel y la Plaza de España. ")

result = crew.kickoff(inputs={"topic": ruta})
