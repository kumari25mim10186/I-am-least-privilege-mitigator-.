import json
import os


def save_policy(policy, filename):

    os.makedirs("output", exist_ok=True)

    with open(
        os.path.join("output", filename),
        "w"
    ) as file:

        json.dump(
            policy,
            file,
            indent=4
        )


class IAMAgent:

    def __init__(self, data_path="data"):
        self.data_path = data_path

        self.roles = self.load_json("iam_roles.json")
        self.logs = self.load_json("access_logs.json")
        self.dependencies = self.load_json("service_dependencies.json")

        self.current_policy = {}
        self.candidates = []
        self.evidence = []
        self.iteration = 0

    def load_json(self, filename):
        path = os.path.join(self.data_path, filename)

        with open(path, "r") as file:
            return json.load(file)

    def analyze(self):

        events = {
            event["permission"]: event["count"]
            for event in self.logs["access_events"]
        }

        for role in self.roles["roles"]:

            role_name = role["role_name"]

            self.current_policy[role_name] = list(
                role["permissions"]
            )

            for permission in role["permissions"]:

                usage = events.get(permission, 0)

                if usage == 0:

                    self.candidates.append({
                        "role": role_name,
                        "permission": permission,
                        "reason": "No access observed"
                    })

        return self.candidates

    def check_dependency(self, permission):

        for service in self.dependencies["services"]:

            if permission in service["requires"]:

                return service["service"]

        return None

    def generate_policy(self):

        proposed_policy = {
            role: list(permissions)
            for role, permissions
            in self.current_policy.items()
        }

        for candidate in self.candidates:

            permission = candidate["permission"]

            dependency = self.check_dependency(permission)

            if dependency is None:

                role = candidate["role"]

                if permission in proposed_policy[role]:

                    proposed_policy[role].remove(permission)

                    self.evidence.append({
                        "permission": permission,
                        "action": "removed",
                        "reason": "Unused permission with no service dependency"
                    })

        return proposed_policy

