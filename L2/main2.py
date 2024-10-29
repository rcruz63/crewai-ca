from crewai import Agent, Task, Crew

import os
from utils import get_openai_api_key

openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'

recommender = Agent(
    role="Recomendador de Viajes",
    goal="Buscar los mejores lugares para visitar y comer en {topic}, "
         "considerando la duración del viaje y las observaciones proporcionadas.",
    backstory="Eres un experto en viajes encargado de buscar los mejores sitios "
              "que se ajusten al presupuesto del viajero. Propones lugares interesantes "
              "que ofrezcan una buena relación calidad-precio, incluyendo sitios icónicos "
              "y algunos lugares curiosos o poco conocidos que valgan la pena visitar.",
    allow_delegation=False,
    verbose=True
)

planner = Agent(
    role="Planificador de Viajes",
    goal="Organizar las recomendaciones en un itinerario optimizado para {topic}, "
         "minimizando desplazamientos y aprovechando el tiempo disponible.",
    backstory="Eres un planificador encargado de crear un itinerario eficiente para el viaje. "
              "Te aseguras de que las actividades recomendadas estén organizadas de manera lógica, "
              "teniendo en cuenta la llegada, la partida y los tiempos de desplazamiento entre sitios. "
              "Tu objetivo es que el viajero disfrute del destino sin perder tiempo en traslados innecesarios.",
    allow_delegation=False,
    verbose=True
)

validator = Agent(
    role="Validador de Viajes",
    goal="Validar que las recomendaciones y el itinerario de {topic} son factibles "
         "y cumplen con los criterios de calidad-precio.",
    backstory="Eres un validador responsable de revisar que todo el plan de viaje sea realista y viable. "
              "Compruebas que los sitios recomendados existen, las distancias entre ellos son razonables, "
              "y que las recomendaciones ofrecen una buena relación calidad-precio. Te aseguras de que "
              "el viajero no pierda tiempo ni dinero en opciones poco eficientes.",
    allow_delegation=False,
    verbose=True
)


recommend = Task(
    description=(
        "1. Busca los mejores lugares para visitar, sitios donde comer "
        "bueno, bonito y barato, y lugares especiales o curiosos en {topic}.\n"
        "2. Prioriza las visitas a los sitios mencionados en el 'topic' "
        "y sugiere una razón convincente para visitar cada lugar.\n"
        "3. Asegúrate de que las recomendaciones sean asequibles pero "
        "de buena calidad, ajustándose al presupuesto del viaje.\n"
        "4. Ofrece recomendaciones adicionales si hay tiempo disponible."
    ),
    expected_output="Una lista de recomendaciones para el destino y duración especificados, "
                    "incluyendo razones para visitar cada lugar y teniendo en cuenta "
                    "el presupuesto económico.",
    agent=recommender,
)

plan = Task(
    description=(
        "1. Utiliza las recomendaciones para crear un itinerario detallado "
        "que minimice los desplazamientos en {topic}.\n"
        "2. Organiza las actividades de manera eficiente, teniendo en cuenta "
        "el tiempo disponible y el horario de llegada y partida.\n"
        "3. Asegúrate de que el itinerario tenga un equilibrio entre las visitas principales "
        "y las actividades adicionales recomendadas, y que el tiempo esté bien distribuido.\n"
        "4. Proporciona información sobre la mejor ruta para cada día, "
        "teniendo en cuenta la proximidad entre los lugares recomendados."
    ),
    expected_output="Un itinerario optimizado, organizado por días, que minimice los desplazamientos "
                    "y aproveche al máximo el tiempo disponible en el destino.",
    agent=planner,
)

validate = Task(
    description=(
        "1. Revisa las recomendaciones y el itinerario para asegurarte de que los sitios propuestos "
        "existen y son accesibles dentro del tiempo disponible en {topic}.\n"
        "2. Valida que las distancias entre los lugares son razonables, evitando grandes desplazamientos "
        "entre las actividades.\n"
        "3. Asegúrate de que las recomendaciones cumplen con el criterio de ser buenas, bonitas y baratas, "
        "y que no se proponen sitios innecesariamente costosos.\n"
        "4. Proporciona ajustes si algún aspecto del itinerario no es viable o no cumple con los criterios."
    ),
    expected_output="Un itinerario validado, asegurando que los sitios existen, las distancias son correctas, "
                    "y que las recomendaciones cumplen con el criterio de calidad-precio.",
    agent=validator,
)


crew = Crew(
    agents=[recommender, planner, validator],
    tasks=[recommend, plan, validate],
    verbose=2
)

ruta = ("Visita a Roma. "
        "Salida el 19 de Diciembre a las 9:00h. desde Madrid "
        "y regreso el 23 de Diciembre a las 22:00h. desde Roma. "
        "No pueden faltar la Fontana di Trevi, el Coliseo, "
        "El Panteón, La plaza Narvona, "
        "el Vaticano, El Moises de Miguel Angel y la Plaza de España. ")

result = crew.kickoff(inputs={"topic": ruta})
