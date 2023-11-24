from icecream import ic
from openai_handler import *
import asyncio

async def generate(user_input):
    ic(user_input)
    
    thread = client.beta.threads.create()
    
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    ic(client.beta.threads.messages.list(thread_id=thread.id).data)
    
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
        instructions="""
Generate a multiple-choice question with four options and return it in the following JSON format:

json
Copy code
{
    "question": "Write the question here.",
    "options": {
        "1": "Option 1",
        "2": "Option 2",
        "3": "Option 3",
        "4": "Option 4"
    },
    "answer": "Option(x) with a one-line explanation."
}
        """
    )    
    
    

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        await asyncio.sleep(3)
        print(run.status)
        print(user_input[:10])
        if run.status in ("completed", "failed"):
            break
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    latest_message = messages.data[0]
    text = latest_message.content[0].text.value

    # deleting the thread
    response = client.beta.threads.delete(thread.id)
    ic(response)

    return text
        