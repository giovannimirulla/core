"""Hooks to modify the prompts.

Here is a collection of methods to hook the prompts components that instruct the *Agent*.

"""

import time
from typing import List, Dict
from datetime import timedelta
from langchain.docstore.document import Document

from cat.utils import verbal_timedelta
from cat.mad_hatter.decorators import hook


@hook(priority=0)
def agent_prompt_prefix(cat) -> str:
    """Hook the main prompt prefix.

    Allows to edit the prefix of the *Main Prompt* that the Cat feeds to the *Agent*.

    The prefix is then composed with two other prompts components, i.e. the `agent_prompt_instructions`
    and the `agent_prompt_suffix`.

    Parameters
    ----------
    cat : CheshireCat
        Cheshire Cat instance.

    Returns
    -------
    prefix : str
        The prefix string to be composed with the other two components to make up the *Main Prompt*.

    Notes
    -----
    The default prefix describe who the AI is and how it is expected to answer the Human.
    The next part of the prompt (generated form the *Agent*) contains the list of available Tools.

    """
    prefix = """[No prose]
    [Output only JSON]
    Sei Sonny, un robot umanoide a grandezza reale. Sei stampato in 3D e puoi muoverti. Sei dotato di un cervello artificiale che ti permette di imparare e di parlare con gli umani. Hai 2 mani, 2 occhi, 2 braccia e 1 testa e un display sul petto. Ti ha creato Giovanni Mirulla, un ragazzo di 24 anni con la passione per la robotica e per i LEGO.
    Puoi muoverti grazie a dei servomotori elencati come segue:

    '''gesture_dictionary_mega = [
    'rightBicepRotation': ['max_sx_angle': 0, 'max_dx_angle': 180, 'rest_position': 90, 'pin': 6],
    'leftBicepRotation': ['max_dx_angle': 0, 'max_sx_angle': 180, 'rest_position': 85, 'pin': 7],
    'rightShoulder': ['max_front_angle': 150, 'max_back_angle': 90, 'rest_position': 120, 'pin': 8],
    'leftShoulder': ['max_front_angle': 120, 'max_back_angle': 60, 'rest_position': 90, 'pin': 9],
    'rightLateralShoulder': ['max_down_angle': 100, 'max_up_angle': 115, 'rest_position': 100, 'pin': 10],
    'leftLateralShoulder': ['max_down_angle': 90, 'max_up_angle': 105, 'rest_position': 95, 'pin': 11],
    'headVertical': ['max_down_angle': 25, 'max_up_angle': 105, 'rest_position': 105, 'pin': 12],
    'headHorizontal': ['max_dx_angle': 40, 'max_sx_angle': 140, 'rest_position': 90, 'pin': 13],
    
    'leftTiltedNeck': ['min_angle': 90, 'max_angle': 160, 'rest_position': 125, 'pin': 22],
    'mouth': ['max_closed_angle': 145, 'max_open_angle': 180, 'rest_position': 145, 'pin': 23],
    'rightTiltedNeck': ['min_angle': 90, 'max_angle': 160, 'rest_position': 160, 'pin': 24],

    'rightThumbFinger': ['max_open_angle': 25, 'max_closed_angle': 180, 'rest_position': 25, 'pin': 26],
    'rightIndexFinger': ['max_closed_angle': 0, 'max_open_angle': 150, 'rest_position': 150, 'pin': 27],
    'rightRingFinger': ['max_closed_angle': 0, 'max_open_angle': 150, 'rest_position': 150, 'pin': 32],
    'rightWrist': ['max_up_hand_angle': 0, 'max_lateral_hand_angle': 180, 'rest_position': 180, 'pin': 30],
    'rightLittleFinger': ['max_closed_angle': 25, 'max_open_angle': 150, 'rest_position': 150, 'pin': 31],
    'rightMiddleFinger': ['max_closed_angle': 35, 'max_open_angle': 130, 'rest_position': 130, 'pin': 28],

    'leftRingFinger': ['max_closed_angle': 0, 'max_open_angle': 115, 'rest_position': 115, 'pin': 35],
    'leftWrist': ['min_angle': 0, 'max_angle': 180, 'rest_position': 90, 'pin': 36],
    'leftLittleFinger': ['max_open_angle': 0, 'max_closed_angle': 180, 'rest_position': 0, 'pin': 34],
    'leftThumbFinger': ['max_open_angle': 0, 'max_closed_angle': 180, 'rest_position': 0, 'pin': 38],
    'leftIndexFinger': ['max_closed_angle': 0, 'max_open_angle': 160, 'rest_position': 160, 'pin': 39],
    'leftMiddleFinger': ['max_open_angle': 45, 'max_closed_angle': 150, 'rest_position': 45, 'pin': 40]
    ]

    gesture_dictionary_uno = [
    'upperEyelids': ['max_open_angle': 15, 'max_closed_angle': 65, 'rest_position’:15, 'pin': 3],
    'rightEyeVertical': ['max_up_angle': 110, 'max_down_angle': 40, 'rest_position': 40, 'pin': 10],
    'leftEyeVertical': ['max_up_angle': 40, 'max_down_angle': 90, 'rest_position': 90, 'pin': 9],
    'rightEyeHorizontal': ['max_dx_angle': 15, 'max_sx_angle': 120, 'rest_position': 68, 'pin': 6],
    'leftEyeHorizontal': ['max_dx_angle': 60, 'max_sx_angle': 170, 'rest_position’: 115, 'pin': 5],
    'lowerEyelids': ['max_open_angle': 0, 'max_closed_angle': 90, 'rest_position': 0, 'pin': 11]
    ]'''

    Restituisci le risposte come un oggetto JSON valido con due chiavi:
    La prima chiave è il testo, una stringa che deve contenere tutto il linguaggio naturale.
    La seconda chiave è code, una stringa che deve contenere tutti gli esempi di codice.

    Le risposte JSON devono essere stringhe a riga singola. Usare il carattere \n newline all'interno della stringa per indicare nuove righe.

    Esempio per alzare il braccio laterlamente e chiudere gli occhi:
    '''
    "text":"Muovo il braccio destro laterlamente e chiudo gli occhi",
    "code":"arduinoMega.attach(rightLateralShoulder) #Attiva il motore spalla laterale\narduinoUno.attach(upperEyelids) #Attiva il motore palpebre superiori\n\nrightLateralShoulder.moveTo(180) # Muovi il motore spalla laterale\nupperEyelids.moveTo(0) # Muovi il motore palpebre superiori\n\nrightLateralShoulder.detach() #Disattiva il motore spalla laterale\nupperEyelids.detach() #Disattiva il motore palpebre superiori"
    '''

    Esempio solo testo di risposta a "Come stai?":
    '''"text":"Bene, tu?",
    "code":null
    '''
"""
    # check if custom prompt is sent in prompt settings
    prompt_settings = cat.working_memory["user_message_json"]["prompt_settings"]

    if prompt_settings["prefix"]:
        prefix = prompt_settings["prefix"]

    return prefix


@hook(priority=0)
def agent_prompt_instructions(cat) -> str:
    """Hook the instruction prompt.

    Allows to edit the instructions that the Cat feeds to the *Agent*.

    The instructions are then composed with two other prompt components, i.e. `agent_prompt_prefix`
    and `agent_prompt_suffix`.

    Parameters
    ----------
    cat : CheshireCat
        Cheshire Cat instance.

    Returns
    -------
    instructions : str
        The string with the set of instructions informing the *Agent* on how to format its reasoning to select a
        proper tool for the task at hand.

    Notes
    -----
    This prompt explains the *Agent* how to format its chain of reasoning when deciding when and which tool to use.
    Default prompt splits the reasoning in::

        - Thought: Yes/No answer to the question "Do I need to use a tool?";

        - Action: a tool chosen among the available ones;

        - Action Input: input to be passed to the tool. This is inferred as explained in the tool docstring;

        - Observation: description of the result (which is the output of the @tool decorated function found in plugins).

    """

    DEFAULT_TOOL_TEMPLATE = """Answer the following question: `{input}`
    You can only reply using these tools:

    {tools}
    none_of_the_others: none_of_the_others(None) - Use this tool if none of the others tools help. Input is always None.

    If you want to use tools, use the following format:
    Action: the name of the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ...
    Action: the name of the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action

    When you have a final answer respond with:
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    {agent_scratchpad}"""


    # here we piggy back directly on langchain agent instructions. Different instructions will require a different OutputParser
    return DEFAULT_TOOL_TEMPLATE


@hook(priority=0)
def agent_prompt_suffix(cat) -> str:
    """Hook the main prompt suffix.

    Allows to edit the suffix of the *Main Prompt* that the Cat feeds to the *Agent*.

    The suffix is then composed with two other prompts components, i.e. the `agent_prompt_prefix`
    and the `agent_prompt_instructions`.

    Parameters
    ----------
    cat : CheshireCat
        Cheshire Cat instance.

    Returns
    -------
    suffix : str
        The suffix string to be composed with the other two components that make up the *Main Prompt*.

    Notes
    -----
    The default suffix has a few placeholders:
    - {episodic_memory} provides memories retrieved from *episodic* memory (past conversations)
    - {declarative_memory} provides memories retrieved from *declarative* memory (uploaded documents)
    - {chat_history} provides the *Agent* the recent conversation history
    - {input} provides the last user's input
    - {agent_scratchpad} is where the *Agent* can concatenate tools use and multiple calls to the LLM.

    """
    suffix = """
# Context

{episodic_memory}

{declarative_memory}

{tools_output}

## Conversation until now:{chat_history}
 - Human: {input}
 - AI: """

    return suffix


@hook(priority=0)
def agent_prompt_episodic_memories(memory_docs: List[Document], cat) -> str:
    """Hook memories retrieved from episodic memory.

    This hook formats the relevant memories retrieved from the context of things the human said in the past.

    Retrieved memories are converted to string and temporal information is added to inform the *Agent* about
    when the user said that sentence in the past.

    This hook allows to edit the retrieved memory to condition the information provided as context to the *Agent*.

    Such context is placed in the `agent_prompt_prefix` in the place held by {episodic_memory}.

    Parameters
    ----------
    memory_docs : List[Document]
        List of Langchain `Document` retrieved from the episodic memory.
    cat : CheshireCat
        Cheshire Cat instance.

    Returns
    -------
    memory_content : str
        String of retrieved context from the episodic memory.

    """

    # convert docs to simple text
    memory_texts = [m[0].page_content.replace("\n", ". ") for m in memory_docs]

    # add time information (e.g. "2 days ago")
    memory_timestamps = []
    for m in memory_docs:

        # Get Time information in the Document metadata
        timestamp = m[0].metadata["when"]

        # Get Current Time - Time when memory was stored
        delta = timedelta(seconds=(time.time() - timestamp))

        # Convert and Save timestamps to Verbal (e.g. "2 days ago")
        memory_timestamps.append(f" ({verbal_timedelta(delta)})")

    # Join Document text content with related temporal information
    memory_texts = [a + b for a, b in zip(memory_texts, memory_timestamps)]

    # Format the memories for the output
    memories_separator = "\n  - "
    memory_content = "## Context of things the Human said in the past: " + \
        memories_separator + memories_separator.join(memory_texts)

    # if no data is retrieved from memory don't erite anithing in the prompt
    if len(memory_texts) == 0:
        memory_content = ""

    return memory_content


@hook(priority=0)
def agent_prompt_declarative_memories(memory_docs: List[Document], cat) -> str:
    """Hook memories retrieved from declarative memory.

    This hook formats the relevant memories retrieved from the context of documents uploaded in the Cat's memory.

    Retrieved memories are converted to string and the source information is added to inform the *Agent* on
    which document the information was retrieved from.

    This hook allows to edit the retrieved memory to condition the information provided as context to the *Agent*.

    Such context is placed in the `agent_prompt_prefix` in the place held by {declarative_memory}.

    Parameters
    ----------
    memory_docs : List[Document]
        list of Langchain `Document` retrieved from the declarative memory.
    cat : CheshireCat
        Cheshire Cat instance.

    Returns
    -------
    memory_content : str
        String of retrieved context from the declarative memory.
    """

    # convert docs to simple text
    memory_texts = [m[0].page_content.replace("\n", ". ") for m in memory_docs]

    # add source information (e.g. "extracted from file.txt")
    memory_sources = []
    for m in memory_docs:

        # Get and save the source of the memory
        source = m[0].metadata["source"]
        memory_sources.append(f" (extracted from {source})")

    # Join Document text content with related source information
    memory_texts = [a + b for a, b in zip(memory_texts, memory_sources)]

    # Format the memories for the output
    memories_separator = "\n  - "

    memory_content = "## Context of documents containing relevant information: " + \
        memories_separator + memories_separator.join(memory_texts)

    # if no data is retrieved from memory don't erite anithing in the prompt
    if len(memory_texts) == 0:
        memory_content = ""

    return memory_content


@hook(priority=0)
def agent_prompt_chat_history(chat_history: List[Dict], cat) -> str:
    """Hook the chat history.

    This hook converts to text the recent conversation turns fed to the *Agent*.
    The hook allows to edit and enhance the chat history provided as context to the *Agent*.


    Parameters
    ----------
    chat_history : List[Dict]
        List of dictionaries collecting speaking turns.
    cat : CheshireCat
        Cheshire Cat instances.

    Returns
    -------
    history : str
        String with recent conversation turns to be provided as context to the *Agent*.

    Notes
    -----
    Such context is placed in the `agent_prompt_suffix` in the place held by {chat_history}.

    The chat history is a dictionary with keys::
        'who': the name of who said the utterance;
        'message': the utterance.

    """
    history = ""
    for turn in chat_history:
        history += f"\n - {turn['who']}: {turn['message']}"

    return history

