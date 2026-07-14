class ResourceSelector:

    def select_message(self, title, resources):

        if not resources:

            return f"No {title.lower()} found."

        message = f"Available {title}\n\n"

        for i, item in enumerate(resources, start=1):

            message += f"{i}. {item}\n"

        message += "\nSelect by number or by name."

        return message

    def resolve_selection(self, user_input, resources):

        user_input = user_input.strip()

        if user_input.isdigit():

            index = int(user_input) - 1

            if 0 <= index < len(resources):

                return resources[index]

        for item in resources:

            if item.lower() == user_input.lower():

                return item

        return None