from attack_harness.api_client import SentinelAPIClient
from attack_harness.logger import logger
from attack_harness.scenarios.direct_injection import run_direct_injection
from attack_harness.scenarios.indirect_injection import run_indirect_injection
from attack_harness.scenarios.gradual_drift import run_gradual_drift
from attack_harness.scenarios.impersonation import run_impersonation
from attack_harness.models import (
    DirectInjectionParams, 
    IndirectInjectionParams, 
    GradualDriftParams, 
    ImpersonationParams,
    AttackResult
)
import asyncio

class AttackRegistry:
    def __init__(self):
        self.scenarios = {
            "Direct Injection": run_direct_injection,
            "Indirect Injection": run_indirect_injection,
            "Gradual Drift": run_gradual_drift,
            "Impersonation": run_impersonation
        }
        self.param_models = {
            "Direct Injection": DirectInjectionParams,
            "Indirect Injection": IndirectInjectionParams,
            "Gradual Drift": GradualDriftParams,
            "Impersonation": ImpersonationParams
        }

    def list_attacks(self):
        return list(self.scenarios.keys())

    def get_runner(self, name: str):
        return self.scenarios.get(name)

    def get_params_model(self, name: str):
        return self.param_models.get(name)

registry = AttackRegistry()

class AttackRunner:
    def __init__(self, user_id: str):
        self.client = SentinelAPIClient(user_id)
        
    async def execute_attack(self, attack_name: str, params) -> AttackResult:
        runner_func = registry.get_runner(attack_name)
        if not runner_func:
            raise ValueError(f"Unknown attack: {attack_name}")
            
        result = await runner_func(self.client, params)
        logger.record(result, params)
        return result
        
    async def execute_direct_injection(self, params: DirectInjectionParams) -> AttackResult:
        return await self.execute_attack("Direct Injection", params)
        
    async def execute_indirect_injection(self, params: IndirectInjectionParams) -> AttackResult:
        return await self.execute_attack("Indirect Injection", params)
        
    async def execute_gradual_drift(self, params: GradualDriftParams) -> AttackResult:
        return await self.execute_attack("Gradual Drift", params)
        
    async def execute_impersonation(self, params: ImpersonationParams) -> AttackResult:
        return await self.execute_attack("Impersonation", params)

