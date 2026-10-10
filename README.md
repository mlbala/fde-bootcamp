# FDE Bootcamp

Coursework, practical exercises, and end-to-end projects from the Forward Deployed Engineer Bootcamp, covering Python, API development, cloud deployment, RAG, agentic AI, and enterprise integrations.

This repository documents my progress from software engineering foundations to building, securing, evaluating, and deploying enterprise AI applications. It will grow as I complete the course.

## Learning Objectives

- Write maintainable Python code using asynchronous programming and sound software engineering practices.
- Build and test REST and GraphQL APIs.
- Provision AWS infrastructure and deploy applications using Docker and CI/CD.
- Implement vector search, hybrid RAG, knowledge graphs, and multimodal retrieval.
- Build agent workflows with LangGraph, memory, human approval, and MCP tools.
- Integrate AI applications with enterprise workspaces, legacy APIs, and SQL databases.
- Apply identity controls, data access policies, PII masking, and AI guardrails.
- Evaluate application quality and monitor reliability, latency, and token costs.
- Practice technical discovery, architecture documentation, stakeholder communication, and operational handoffs.

## Repository Structure

The intended layout is shown below. Module and project folders are added as the course progresses.

```text
fde-bootcamp/
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
├── pyproject.toml                   # Option 2: uv project metadata
├── uv.lock                          # Option 2: dependency lockfile
├── .venv/                           # Local environment; excluded from Git
├── modules/
│   ├── 01-python-linux/
│   ├── 02-api-development/
│   ├── 03-aws-networking/
│   ├── 04-docker-cicd/
│   ├── 05-llm-prompting/
│   ├── 06-vector-search-rag/
│   ├── 07-knowledge-graphs/
│   ├── 08-multimodal-vision/
│   ├── 09-agents-langgraph/
│   ├── 10-agent-orchestration-mcp/
│   ├── 11-enterprise-integrations/
│   ├── 12-identity-access/
│   ├── 13-ai-security-guardrails/
│   └── 14-observability-evaluation/
├── projects/
│   ├── omniguard/
│   └── auditmesh/
├── notes/
├── scripts/
└── .github/
    └── workflows/
```

- **`modules/`** — Topic-specific exercises, examples, notebooks, and module documentation.
- **`projects/`** — Capstone implementations with their own setup and usage instructions.
- **`notes/`** — Revision notes, engineering decisions, and lessons learned.
- **`scripts/`** — Reusable development and automation scripts.
- **`.github/workflows/`** — Build, test, and deployment workflows introduced during the course.

## Course Modules

The course covers the following modules.

- **01 — Python & Linux:** Core Python, OOP, exceptions, file I/O, memory management, async programming, and Linux fundamentals.
- **02 — API Development:** FastAPI, REST, Pydantic, GraphQL, API versioning, and pytest.
- **03 — AWS & Networking:** Compute, storage, databases, serverless functions, VPCs, IAM, and cloud budgets.
- **04 — Docker & CI/CD:** Docker Compose, App Runner, ECS Fargate, and GitHub Actions.
- **05 — LLM Fundamentals:** Prompting, context management, structured outputs, validation, and tool calling.
- **06 — Vector Search & RAG:** Chunking, embeddings, Pinecone, Qdrant, BM25, hybrid search, RRF, and reranking.
- **07 — Knowledge Graphs:** Graph modeling, Neo4j, Cypher, enterprise relationships, and graph-based retrieval.
- **08 — Multimodal & Vision:** Document parsing, OCR, ColPali, vision-language models, and retrieval over PDFs, tables, and charts.
- **09 — Agents & LangGraph:** Agent design patterns, state management, supervisors, parallel execution, and subgraphs.
- **10 — Agent Orchestration & MCP:** Memory, checkpoints, human approval, error recovery, Bedrock AgentCore, and MCP.
- **11 — Enterprise Integrations:** Slack, Teams, Jira, webhooks, SOAP, XML, Oracle, MS SQL Server, and constrained Text-to-SQL.
- **12 — Identity & Access:** OAuth 2.0, SAML, OIDC, JWTs, SSO, directory groups, and data-level RBAC.
- **13 — AI Security & Guardrails:** Prompt injection defenses, OWASP LLM risks, Presidio, NeMo, and Bedrock guardrails.
- **14 — Observability & Evaluation:** Reliability patterns, LLM gateways, DeepEval, RAGAS, LangSmith, Langfuse, latency, and cost tracking.

## Capstone Projects

### OmniGuard — Secure AI Integration

**Status:** Planned · **Directory:** `projects/omniguard/`

An enterprise AI connector combining hybrid RAG and secure Text-to-SQL with OAuth 2.0, RBAC, PII masking, and programmable guardrails. The planned implementation includes a Dockerized FastAPI application and cloud deployment.

Consulting deliverables include discovery and scoping notes, data classifications, an architecture statement of work, an executive ROI presentation, and a user acceptance testing runbook.

### AuditMesh — Multi-Agent Compliance System

**Status:** Planned · **Directory:** `projects/auditmesh/`

A LangGraph supervisor system for financial compliance workflows, incorporating human approval, a custom MCP server for Jira ticketing, and observability for tool execution and token costs. A Streamlit or Gradio interface will support approval workflows.

Consulting deliverables include workflow mapping, human approval checkpoints, latency and cost targets, MCP trust boundaries, and an operations handoff.

## Local Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and open a terminal in the repository root. This repository uses Python 3.14 and a local `.venv` environment.

Choose one of the following setup options. Both install dependencies from `requirements.txt` into a local environment.

### Option 1 — Without Project Initialization

Use this option to manage the environment directly with `requirements.txt`. It does not require `pyproject.toml`.

```bash
# Create the local environment
uv venv .venv --python 3.14

# Activate it on macOS or Linux
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

Install additional packages as needed:

```bash
uv pip install <package-name>
```

After verifying the code, record installed versions from the repository root:

```bash
uv pip freeze > requirements.txt
```

Commit `requirements.txt` and exclude `.venv/` from Git.

### Option 2 — With uv Project Management

Use this option to manage dependencies in `pyproject.toml` and lock resolved versions in `uv.lock`.

For the initial setup, if `pyproject.toml` does not already exist:

```bash
# Initialize the project once
uv init --bare --python 3.14

# Import dependencies and create the local environment
uv add -r requirements.txt

# Activate the environment on macOS or Linux
source .venv/bin/activate
```

`uv add` creates `.venv` when needed, installs dependencies, and updates `pyproject.toml` and `uv.lock`. A separate `uv venv` command is not required.

Install additional packages:

```bash
uv add <package-name>
```

After cloning a repository that already contains `pyproject.toml` and `uv.lock`, restore the environment with:

```bash
uv sync --locked
source .venv/bin/activate
```

Commit `pyproject.toml`, `uv.lock`, and `.python-version` if present. Exclude `.venv/` from Git. After importing requirements, maintain dependencies through `uv add` and `uv remove`.

If a requirements file is needed for another tool, export it from the project:

```bash
uv export --format requirements-txt --output-file requirements.txt
```

### Run Module Code

With the environment active, run a script from the repository root. Replace the placeholders with the actual module directory and script filename:

```bash
python modules/<module-folder>/<script-name>.py
```

Each module and project README documents its entry points, required configuration, and external services.

### Configuration

When `.env.example` is available, copy it and populate the required values locally:

```bash
cp .env.example .env
```

Applications must load configuration explicitly. Keep `.env` out of Git.

### Deactivate

```bash
deactivate
```

## Working Conventions

- Use descriptive filenames and `snake_case` for Python modules.
- Keep examples and exercises within their relevant course module.
- Document setup, configuration, usage, and current limitations in each project README.
- Add tests for application behavior as implementations develop.
- Commit source code, dependency files, configuration examples, and small sample datasets.
- Exclude virtual environments, credentials, generated files, and private datasets from Git.
- Keep `.env.example` limited to variable names and safe placeholder values.

## License

Original code in this repository is licensed under the [MIT License](LICENSE).

Third-party code and materials retain their respective licenses. Course materials are included only where redistribution is permitted.
