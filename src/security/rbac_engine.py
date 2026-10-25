class RBACEngine:
    """Enforces Role-Based Access Control (RBAC) across data clearance levels and action gates."""

    ROLE_CLEARANCE_MAP = {
        "junior_chemist": 1,
        "senior_chemist": 2,
        "principal_investigator": 3,
    }

    @classmethod
    def authorize(cls, user_role: str, required_clearance: int) -> bool:
        """Validates if user role clearance level meets or exceeds the required clearance threshold."""
        user_clearance = cls.ROLE_CLEARANCE_MAP.get(user_role.lower(), 0)
        return user_clearance >= required_clearance

    @classmethod
    def can_approve_docking(cls, user_role: str) -> bool:
        """Determines if the user possesses sign-off privileges for expensive GPU docking / synthesis jobs."""
        return cls.authorize(user_role, required_clearance=2)


if __name__ == "__main__":
    print(
        "Junior Chemist Access Level 2 Resource:",
        RBACEngine.authorize("junior_chemist", 2),
    )
    print(
        "Senior Chemist Access Level 2 Resource:",
        RBACEngine.authorize("senior_chemist", 2),
    )