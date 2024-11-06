from crewai import Crew
from textwrap import dedent
from trip_agents import TripAgents
from trip_tasks import TripTasks

from dotenv import load_dotenv
load_dotenv()


class TripCrew:

    def __init__(self, city, days, interests):
        self.city = city
        self.days = days
        self.interests = interests

    def run(self):
        agents = TripAgents()
        tasks = TripTasks()

        local_expert = agents.local_expert()

        gather_task = tasks.gather_task(
            local_expert,
            self.city,
            self.interests,
            self.days
        )

        travel_concierge = agents.travel_concierge()

        plan_task = tasks.plan_task(
            travel_concierge,
            self.city,
            self.interests,
            self.days
        )

        editor_blog = agents.editor_blog()

        editor_task = tasks.editor_task(
            editor_blog,
            self.city,
            self.interests,
            self.days
        )

        crew = Crew(
            agents=[local_expert, travel_concierge, editor_blog],
            tasks=[gather_task, plan_task, editor_task],
            verbose=True
        )

        result = crew.kickoff()
        return result


if __name__ == "__main__":
    print("## Bienvenido al Planificador de Itinerarios")
    print('----------------------------------------------')
    city = input(
        dedent("""
        ¿En qué ciudad te gustaría organizar tu itinerario?
        """))
    days = input(
        dedent("""
        ¿Cuántos días tienes disponibles para este viaje?
        """))
    interests = input(
        dedent("""
        ¿Cuáles son algunos de tus intereses principales para este viaje?
        """))

    trip_crew = TripCrew(city, days, interests)
    result = trip_crew.run()
    print("\n\n########################")
    print("## Aquí tienes tu Itinerario de Viaje")
    print("########################\n")
    print(result)
