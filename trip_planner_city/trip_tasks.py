from crewai import Task
from textwrap import dedent
# from datetime import date


class TripTasks:

    def editor_task(self, agent, city, interests, range):
        return Task(
            description=dedent(f"""
                Debes presentar el plan de viaje como lo haría un intimo amigo que conociera muy bien el Destino.
                Describe de forma atractiva y cercana lo que vamos a hacer en la ciudad.

                Utiliza formato markdown para presentar la información de forma clara y atractiva. 
                No agobies mucho con las horas, pero presenta el plan en actividades diarias.

                Valida que NO HAYA DESPLAZAMIENTOS INNECESARIOS y que las actividades sean coherentes con los 
                intereses del viajero.

                Convence al viajero mediante un parrafo o dos por recomendación de por qué debería visitar o comer en ese lugar.
                {self.__tip_section()}

                Destino: {city}
                Duración del Viaje: {range}
                Intereses del Viajero: {interests}
            """),
            agent=agent,
            expected_output="documento markdown con el plan de viaje."
        )

    def gather_task(self, agent, city, interests, range):
        return Task(
            description=dedent(f"""
                Como experto local en esta ciudad, debes compilar una guía 
                completa para alguien que viaje allí y quiera tener ¡LA MEJOR 
                experiencia de viaje!
                Recopila información sobre las principales atracciones, 
                costumbres locales, eventos especiales y recomendaciones diarias 
                de actividades. Encuentra los mejores lugares, esos que solo 
                un local conocería.
                Esta guía debe proporcionar una visión completa de lo que 
                la ciudad tiene para ofrecer, incluyendo joyas ocultas, 
                puntos culturales, lugares imprescindibles.

                La respuesta final debe ser una guía de la ciudad 
                detallada, rica en perspectivas culturales y consejos 
                prácticos, adaptada para mejorar la experiencia de viaje.
                {self.__tip_section()}

                Ciudad Destino: {city}
                Duración del Viaje: {range}
                Intereses del Viajero: {interests}
            """),
            agent=agent,
            expected_output="Guía completa de la ciudad incluyendo joyas ocultas, puntos culturales y consejos "
            "prácticos para el viaje"
        )

    def plan_task(self, agent, city, interests, range):
        return Task(
            description=dedent(f"""
                Expande esta guía en un itinerario completo de viaje 
                durante {range} con planes detallados por día, lugares para comer, y un desglose del presupuesto.

                DEBES sugerir lugares específicos para visitar, sitios poco conocidos que visitar,
                y restaurantes concretos donde comer.

                Este itinerario debe cubrir todos los aspectos del viaje, 
                desde la llegada hasta la salida, integrando la información 
                de la guía de la ciudad con la logística práctica del viaje.

                Tu respuesta final DEBE ser un plan de viaje completo 
                y expandido, en formato markdown, que abarque un horario 
                diario, y un desglose detallado 
                del presupuesto, asegurando ¡LA MEJOR EXPERIENCIA DE VIAJE! 
                Sé específico y da una razón de por qué eliges cada lugar, ¡qué los hace especiales!
                {self.__tip_section()}

                Ciudad Destino: {city}
                Duración del Viaje: {range}
                Intereses del Viajero: {interests}
            """),
            agent=agent,
            expected_output="Plan de viaje completo y detallado con horario diario y desglose del presupuesto"
        )

    def __tip_section(self):
        return "¡Si haces tu MEJOR TRABAJO, te daré una propina de 100$!"
