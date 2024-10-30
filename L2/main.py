from crewai import Agent, Task, Crew

import os
from utils import get_openai_api_key

openai_api_key = get_openai_api_key()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4o-mini'

planner = Agent(
    role="Planificador de Viajes",
    goal="Planificar un itinerario atractivo y completo para el destino y la duración especificados: {topic}",
    backstory="Estás trabajando en la planificación de un viaje. "
              "El cliente te ha pedido que le recomiendes las mejores actividades "
              "y lugares para visitar en el destino: {topic}. "
              "Tienes en cuenta tanto el destino como la duración del viaje, "
              "recopilando información sobre sitios turísticos imprescindibles, "
              "los mejores lugares para comer bien, bonito y barato, "
              "y experiencias locales que el viajero no se puede perder. "
              "Tu trabajo será la base para que el Redactor de Viajes "
              "cree una propuesta detallada y ajustada al tiempo disponible.",
    allow_delegation=False,
    verbose=True
)

writer = Agent(
    role="Redactor de Viajes",
    goal="Escribir un itinerario de viaje detallado y atractivo "
         "para el destino y la duración especificados: {topic}",
    backstory="Estás trabajando en la redacción de un itinerario de viaje "
              "basado en el destino y la duración especificados en {topic}. "
              "Te basas en el trabajo del Planificador de Viajes, "
              "quien te proporciona un esquema con las actividades y visitas recomendadas, "
              "incluyendo los mejores lugares para comer, sitios turísticos "
              "que no te puedes perder y actividades locales. "
              "Sigues las principales recomendaciones del Planificador de Viajes "
              "para asegurar que el itinerario esté equilibrado y cubra todos "
              "los aspectos esenciales dentro del tiempo disponible.",
    allow_delegation=False,
    verbose=True
)

editor = Agent(
    role="Editor de Viajes",
    goal="Editar el itinerario de viaje para alinearlo con las expectativas del cliente y la duración especificada.",
    backstory="Eres un editor que recibe un itinerario de viaje "
              "del Redactor de Viajes. "
              "Tu objetivo es revisar el itinerario para asegurarte de que "
              "incluye visitas recomendadas, lugares donde comer bien a buen precio, "
              "evita los desplazamientos innecesarios, "
              "y que el itinerario está bien equilibrado según la duración especificada "
              "en el destino: {topic}. Te aseguras de que no se omiten "
              "los lugares imprescindibles ni se agota el tiempo disponible innecesariamente.",
    allow_delegation=False,
    verbose=True
)

plan = Task(
    description=(
        "1. Prioriza los lugares más destacados y las actividades esenciales "
        "para el destino y la duración del viaje: {topic}, "
        "asegurando que el plan sea atractivo y ajustado a un coste económico.\n"
        "2. Incluye recomendaciones de lugares menos conocidos, curiosos o secretos "
        "que aporten un toque especial al viaje.\n"
        "3. Desarrolla un itinerario detallado que cubra las actividades principales, "
        "teniendo en cuenta el tiempo disponible y ofreciendo opciones alternativas "
        "por si quedara tiempo extra.\n"
        "4. Evista desplazamientos innecesarios y asegúrate de que el itinerario es equlibrado.\n"
        "5. No incluyas horas exactas, pero sugiere un orden lógico de actividades.\n"
        "6. Proporciona información relevante como costes aproximados, horarios, "
        "y consejos prácticos para aprovechar al máximo la estancia."
    ),
    expected_output="Un plan de viaje completo con un itinerario detallado, "
                    "que incluya lugares destacados, recomendaciones secretas, "
                    "actividades opcionales, y costes ajustados.",
    agent=planner,
)

write = Task(
    description=(
        "1. Utiliza el plan de viaje para redactar un itinerario organizado por días "
        "sobre {topic}. El primer día debe centrarse en la 'Llegada' "
        "y el último en la 'Partida'.\n"
        "2. Para cada día, describe las actividades principales, lugares recomendados "
        "y opciones alternativas en caso de tener tiempo adicional.\n"
        "3. Las secciones y subtítulos deben estar bien organizados y ser atractivos, "
        "nombrando cada día de manera clara (Día 1, Día 2, etc.).\n"
        "4. No incluyas horas exactas, pero sugiere un orden lógico de actividades.\n "
        "5. Añade una breve descripción de cada lugar o actividad.\n "
        "6. Asegúrate de que cada día del itinerario comience con una introducción breve "
        "y finalice con una recomendación sobre qué hacer o dónde comer, "
        "mientras mantienes el presupuesto bajo.\n"
        "7. Revisa la redacción para corregir errores gramaticales "
        "y asegúrate de que el itinerario siga una estructura lógica y fácil de seguir."
    ),
    expected_output="Un itinerario de viaje bien redactado en formato markdown, "
                    "organizado por días, desde 'Llegada' hasta 'Partida', "
                    "con 2 o 3 párrafos por sección.",
    agent=writer,
)

edit = Task(
    description=("Revisa el itinerario de viaje proporcionado para "
                 "corregir errores gramaticales y "
                 "asegurarte de que la estructura sea clara y fácil de seguir.\n"
                 "Verifica que cada sección esté bien organizada por días, "
                 "incluyendo la 'Llegada' y la 'Partida', y que las recomendaciones "
                 "sean coherentes con el tiempo disponible y el presupuesto."),
    expected_output="Un itinerario de viaje bien redactado en formato markdown, "
                    "organizado por días y revisado, listo para su uso, "
                    "con cada sección compuesta por 2 o 3 párrafos.",
    agent=editor
)

crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=2
)

ruta = ("Visita a Roma. "
        "Salida el 19 de Diciembre a las 9:00h. desde Madrid "
        "y regreso el 23 de Diciembre a las 22:00h. desde Roma. "
        "Nuestro Hotel es Leonardo Boutique Hotel Rome Termini"
        "No pueden faltar la Fontana di Trevi, el Coliseo, "
        "El Panteón, La plaza Navona, "
        "el Vaticano, El Moises de Miguel Angel y la Plaza de España. ")

result = crew.kickoff(inputs={"topic": ruta})
