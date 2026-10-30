# evaluation/locustfile.py
from locust import HttpUser, task, between

class LeadOptLoadTester(HttpUser):
    wait_time = between(1, 3)  # Simulate user pause between requests

    @task
    def test_optimization_pipeline(self):
        payload = {
            "smiles": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",
            "target_pdb_id": "1CX2",
            "user_role": "senior_chemist"
        }
        self.client.post("/api/v1/optimize", json=payload)