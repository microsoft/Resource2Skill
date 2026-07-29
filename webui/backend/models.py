from pydantic import BaseModel


class LLMTemplate(BaseModel):
    name: str
    provider: str = "deepseek"  # openai / azure / deepseek / ollama / custom
    endpoint: str = ""
    api_key: str = ""
    model: str = ""
    temperature: float = 0.2
    max_tokens: int = 4096
    reasoning: str = "low"  # none / low / medium / high / xhigh
    timeout: int = 120
    proxy: str = ""


class WebuiConfig(BaseModel):
    projects_root: str = ""
    active_project: str = ""
    active_domain: str = ""
    active_llm: str = ""
    templates: dict[str, LLMTemplate] = {}


class ProjectCreate(BaseModel):
    name: str
    description: str = ""


class DomainCreate(BaseModel):
    domain: str
    seed_from: str | None = None


class DistillRequest(BaseModel):
    dry_run: bool = False


class AgentRunRequest(BaseModel):
    domain: str
    task: str
    model: str = ""
    reasoning: str = ""        # none / low / medium / high / xhigh（空则用 LLM 模板值）
    max_iter: int = 12
    n_skills: int = 5
    top_k: int = 20
    dry_run: bool = False
