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

The current layout is shown below. Folders fill in as the course progresses.

```text
fde-bootcamp/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example                     # Variable names only; copy to .env, which is excluded from Git
├── requirements.txt
├── .venv/                           # Local environment; excluded from Git
├── Assignment/                      # Class assignments, one folder per session
│   ├── README.md                    # Index of sessions and projects, and how to run them
│   ├── s04-python-1/
│   ├── s05-python-2-hash/
│   └── s06-python-3/
│       ├── README.md                # Problem statement, approach, how to run, learnings
│       ├── *.ipynb                  # One notebook per topic
│       ├── solution.py              # Code for the assignment
│       ├── test_solution.py         # pytest tests for solution.py
│       └── project-N/               # Small apps in topic order: project.txt, <app>.py, test_<app>.py
├── modules/                         # One folder per course module: README.md, notebooks/, src/, tests/
│   ├── 01-python-linux/
│   ├── 02-api-development/
│   ├── 03-cloud-networking/
│   ├── 04-docker-cicd/
│   ├── 05-llm-prompting/
│   ├── 06-vector-search-rag/
│   ├── 07-graph-architecture/
│   ├── 08-multimodal-rag/
│   ├── 09-langgraph/
│   ├── 10-agent-orchestration/
│   ├── 11-legacy-integrations/
│   ├── 12-identity-access/
│   ├── 13-ai-security-guardrails/
│   └── 14-observability-gateway/
├── projects/                        # Capstone projects: README.md, docs/, src/, tests/
│   ├── 01-omniguard/
│   └── 02-auditmesh/
├── shared/                          # Reusable code, importable as the shared package
│   └── utils/
└── notes/                           # Revision notes and lessons learned
```

- **`Assignment/`** — Class assignments, one folder per session (`sNN-<topic>`). Each holds the assignment as given in class, notebooks, a solution with pytest tests, a README, and small projects that follow the order the topics are taught. [Assignment/README.md](Assignment/README.md) has the index of sessions and projects, and how to run them.
- **`modules/`** — The 14 course modules, each with a README, `notebooks/`, `src/` and `tests/`. The class notebooks for module 01 are in `modules/01-python-linux/notebooks/`.
- **`projects/`** — The OmniGuard and AuditMesh capstone projects, each with `docs/`, `src/`, `tests/` and its own setup and usage instructions.
- **`shared/`** — Reusable utilities in `shared/utils/`, for use across modules and projects.
- **`notes/`** — Revision notes, engineering decisions, and lessons learned.

Added later, when the course needs them: `pyproject.toml` and `uv.lock` (only with setup Option 2 below), `scripts/` for development and automation scripts, and `.github/workflows/` for build, test, and deployment workflows.

## Course Modules

The course covers the following modules.

- **01 — Python & Linux Foundations:** Core data structures, memory management, OOP, exception handling, and file I/O; async programming with the event loop, coroutines, and ThreadPoolExecutor; Linux file system, permissions, processes, shell scripting, and environment variables.
- **02 — Modern API Development:** FastAPI REST APIs with Pydantic validation, dependency injection, and CORS; GraphQL with Strawberry or Graphene, and API versioning; pytest fixtures, mocking, and coverage, and VS Code debugging.
- **03 — Cloud Fundamentals & Networking:** AWS compute, object storage, managed databases, and serverless functions; VPCs, subnets, NAT, and security groups; IAM least privilege, cross-account roles, and cloud budgets.
- **04 — Containerization & CI/CD:** Docker and Docker Compose; serverless containers on AWS App Runner and ECS Fargate; CI/CD pipelines with GitHub Actions.
- **05 — LLM Fundamentals & Prompting:** Prompt engineering and context management; structured outputs with Pydantic validation; tool and function calling.
- **06 — Vector Search & Core RAG:** Chunking, embedding models, and BM25; Pinecone and Qdrant vector databases; vanilla RAG and hybrid search with RRF; retrieval evaluation and reranking.
- **07 — Enterprise Graph Architecture:** Knowledge graph concepts and data modeling; Neo4j, AuraDB, and Cypher; Amazon Neptune and graph-based retrieval for AI chatbots.
- **08 — Multimodal RAG & Vision AI:** Document parsing with OCR and ColPali; vision-language models and visual embeddings; scanned PDFs, tables, and charts.
- **09 — Agentic Frameworks & LangGraph:** Agent design patterns such as ReAct, plan-and-execute, supervisor, and router; multi-agent systems in LangGraph; parallel execution and subgraphs.
- **10 — Advanced Agent Orchestration:** Memory and human-in-the-loop workflows; error handling and AWS Bedrock AgentCore; Model Context Protocol (MCP).
- **11 — Legacy Systems & Integrations:** Slack, Teams, and Jira; SOAP APIs and XML parsing; Oracle and MS SQL Server integration with constrained Text-to-SQL.
- **12 — Identity & Access Management:** Enterprise SSO with OAuth 2.0, SAML, OIDC, and JWTs; Active Directory groups and data-level RBAC.
- **13 — Production AI Security & Guardrails:** OWASP LLM Top 10 and prompt injection defenses; PII detection and masking with Presidio; NeMo and Bedrock guardrails.
- **14 — AI Observability & Gateway Management:** Production reliability and LLM gateways such as LiteLLM and Portkey; evaluation with DeepEval and RAGAS; observability with LangSmith and Langfuse.

## Capstone Projects

### OmniGuard — Secure AI Integration

**Status:** Planned · **Directory:** `projects/01-omniguard/`

An enterprise AI connector combining hybrid RAG and secure Text-to-SQL with OAuth 2.0, RBAC, PII masking, and programmable guardrails. The planned implementation includes a Dockerized FastAPI application and cloud deployment.

Consulting deliverables include discovery and scoping notes, data classifications, an architecture statement of work, an executive ROI presentation, and a user acceptance testing runbook.

### AuditMesh — Multi-Agent Compliance System

**Status:** Planned · **Directory:** `projects/02-auditmesh/`

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

Each module and project README documents its entry points, required configuration, and external services. To run the assignments, their projects, and their tests, see [Assignment/README.md](Assignment/README.md).

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

## Setup

Activate the shared environment with `fdevenv`, then copy the example environment file:

```bash
fdevenv
cp .env.example .env
```

Add your credentials to `.env`; never commit that file.
