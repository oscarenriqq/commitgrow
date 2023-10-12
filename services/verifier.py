from datetime import datetime

from config.db import get_conn, database
from models.contract import contracts
from models.penalty import penalties
from models.streak import streaks
from utils import todoist
from services.email import send_email

async def verify_contracts():
    
    query = contracts.select().where(contracts.c.status == 1)
    all_contracts = await database.fetch_all(query)
    
    todoist_tasks = todoist.get_todoist_tasks()
    
    date_format = '%Y-%m-%d'
        
    for contract in all_contracts:
        for task in todoist_tasks:
            if contract.task_id == task["task_id"]:
                
                #Obtenemos la tarea de todoist
                todoist_task = todoist.get_todoist_task(task["task_id"])
                
                """ Diferentes escenarios.
                1. Si la fecha de la tarea, es la misma que la fecha de hoy, entonces el contrato no se cumplió
                2. Si la fecha de la tarea, es menor a la fecha de hoy, entonces el contrato no se cumplió
                3. Si la fecha de la tarea, es mayor a la fecha de hoy, entonces el contrato se cumplió
                Si esta condición se cumple, entonces el contrato ¡NO se cumplió! """
                if datetime.strptime(todoist_task["task_due"], date_format) <= datetime.now():
                    
                    #obtenemos el correo del supervisor y del responsable
                    email_supervisor = contract.supervisor_email
                    email_responsible = contract.responsible_email
                    
                    print(contract)
                    
                    #se registra la penalización en la base de datos
                    query_insert = penalties.insert().values(
                        contract_id=contract.id,
                        description=contract.penalty
                    )
                    await database.execute(query_insert)
                    
                    is_send = send_email(
                        supervisor_email=email_supervisor,
                        responsible_email=email_responsible,
                        subject="Contrato incumplido por parte de {}".format(contract.responsible_name),
                        responsible_name=contract.responsible_name,
                        habit=contract.habit,
                        penalty=contract.penalty
                    )
                    
                    if is_send:
                        query_insert_streak = streaks.insert().values(contract_id=contract.id)
                        await database.execute(query_insert_streak)
    else:
        print("No hay contratos activos")
                    
                    
                    
                    
        
