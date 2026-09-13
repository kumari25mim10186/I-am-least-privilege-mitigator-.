class CloudSimulator:

    def __init__(self, dependencies):

        self.dependencies = dependencies

    def simulate(self, policy):

        results = []

        for service in self.dependencies["services"]:

            required_permissions = service["requires"]

            available_permissions = []

            for role_permissions in policy.values():
                available_permissions.extend(
                    role_permissions
                )

            missing = [
                permission
                for permission in required_permissions
                if permission not in available_permissions
            ]

            if missing:

                results.append({
                    "service": service["service"],
                    "status": "FAILED",
                    "missing_permissions": missing
                })

            else:

                results.append({
                    "service": service["service"],
                    "status": "PASSED",
                    "missing_permissions": []
                })

        return results