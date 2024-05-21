
from SimplerLLM.language.llm import LLM, LLMProvider
from SimplerLLM.tools.json_helpers import extract_json_from_text
from predefined_functions import PREDEFINED_TOOLS

class Agent:
    def __init__(self, model_provider, model_name):
        self.llm_instance = LLM.create(model_provider, model_name=model_name)
        self.available_actions = {}
        self.system_prompt_template = """
                You run in a loop of Thought, Action, PAUSE, Action_Response.
                At the end of the loop you output an Answer.

                Use Thought to understand the question you have been asked.
                Use Action to run one of the actions available to you - then return PAUSE.
                Action_Response will be the result of running those actions.

                Your available actions are:

                {actions_list}

                To use an action, please use the following format:

                Thought: Do I need to use a tool? Yes

                Action:

                {{
                    "function_name": tool_name,
                    "function_parms": {{
                        "param": "value"
                    }}
                }}

                Action_Response: the result of the action""".strip()
        





    def add_tool(self, tool_name, tool_function=None, tool_description = "Custom tool provided by the user" ):
        if tool_name in PREDEFINED_TOOLS:
            tool_function = PREDEFINED_TOOLS[tool_name]["function"]
            description = PREDEFINED_TOOLS[tool_name]["description"]
        elif tool_function:
            description = tool_description
        else:
            raise ValueError(f"Tool {tool_name} not found in predefined tools and no function provided.")

        self.available_actions[tool_name] = {
            "function": tool_function,
            "description": tool_description
        }

    def construct_system_prompt(self):
        actions_description = "\n".join(
            [f"{name}:\n {details['description']}"
             for name, details in self.available_actions.items()]
        )
        return self.system_prompt_template.format(actions_list=actions_description)

    def generate_response(self, user_query, max_turns=5):
        react_system_prompt = self.construct_system_prompt()
        messages = [
            {"role": "system", "content": react_system_prompt},
            {"role": "user", "content": user_query}
        ]
        turn_count = 1

        while turn_count <= max_turns:
            print(f"Loop: {turn_count}")
            print("----------------------")
            turn_count += 1

            agent_response = self.llm_instance.generate_response(messages=messages)
            messages.append({"role": "assistant", "content": agent_response})
            print(agent_response)

            # Extract action JSON from text response.
            action_json = extract_json_from_text(agent_response)
            if action_json:
                function_name = action_json[0]['function_name']
                function_parms = action_json[0]['function_parms']
                if function_name not in self.available_actions:
                    raise Exception(f"Unknown action: {function_name}: {function_parms}")
                print(f" -- running {function_name} with {function_parms}")
                action_function = self.available_actions[function_name]["function"]
                result = action_function(**function_parms)
                print("Action_Response:", result)
                function_result_message = f"Action_Response: {result}"
                messages.append({"role": "user", "content": function_result_message})
                print("----------------------")
            else:
                break

