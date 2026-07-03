class Planner:

    def __init__(self):

        self.tool_map = {

            "chat": {
                "tool": "chat"
            },

            "terminal": {
                "tool": "terminal"
            },

            "lanforge": {
                "tool": "lanforge"
            },

            "rag": {
                "tool": "rag"
            },

            "report": {
                "tool": "report"
            },

            "inventory": {
                "tool": "inventory"
            }

        }

    def plan(self, intent, question):

        plan = self.tool_map.get(
            intent,
            {
                "tool": "chat"
            }
        ).copy()

        plan["intent"] = intent

        plan["question"] = question

        return plan