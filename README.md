# Trading Ontology Chatbot (student repo)

Gradio 6.30.0 chatbot, OpenAI Responses API with built-in web search, one central ontology server. **All students receive shared general ontology plus exactly one bond/equity/commodity ontology per question.** The ontologies themselves live outside the student repo.

## Codespaces setup

1. Upload files including `.devcontainer/devcontainer.json` to a GitHub repository; create a Codespace. Packages install via `postCreateCommand` without venv/shell scripts.
2. Configure these **Codespaces repository secrets** (Settings → Secrets and variables → Codespaces):
   - `OPENAI_API_KEY` = your OpenAI API key (sensitive; never commit).
   - `ONTOLOGY_BASE_URL` = `https://YOUR-CODESPACE-NAME-8000.app.github.dev` or your deployed ontology service root. No trailing `/bundle/...`.
   - Optional `OPENAI_MODEL` = model ID supported by your API account; default is `gpt-5.4`.
3. **Rebuild/restart** the Codespace as needed after adding secrets so environment variables become available.
4. Ensure the instructor's ontology server is running and port 8000 is public.
5. Run `python app.py`, then open port **7860**.

## Research adviser and web search

- The agent instructions are in `researcher_instructions.md` and are loaded from disk for every new app process. They establish the chatbot as a trade-advisement **research analyst**, not an executing broker.
- OpenAI Responses API `tools=[{"type":"web_search"}]` gives the model discretion to use web search when current or external evidence is needed. This uses the **same `OPENAI_API_KEY`**, not a separate search API key. Web search may incur additional API costs.
- Encourage students to verify source dates, distinguish facts from analysis, and provide balanced bull/bear views.
- The ontology server and its URL are unchanged; no changes to the instructor server repository are required.
- Reference: https://developers.openai.com/api/docs/guides/tools-web-search

## Behavior

- Domain routing is based on unambiguous keyword matching or an LLM routing call for ambiguous questions.
- `GET /bundle/<chosen-domain>` returns two ontologies in one network request: always `general`, then one domain. Live JSON fetched **on every chat turn**, so professor edits are reflected without redeploying the student app.
- ChatInterface maintains in-session history; user and assistant messages (last 12) are sent back to OpenAI. History can be saved through Gradio's `save_history` feature.
- Each model response identifies which ontologies and versions were used.
- If the ontology service is unavailable, the chatbot reports an error instead of silently answering with a stale or missing ontology.

## Teaching notes

The ontology server is a JSON/REST reference-data service, **not an MCP server**. You could wrap endpoints in MCP later, but ordinary HTTP is simpler for centrally maintained shared data. The files explicitly encode definitions and typed directed relationships, but do not implement OWL reasoning or represent all legally applicable regulations. The routing picks only one domain even when questions mention multiple markets; explore multi-domain routing as an extension.

## Render deployment (optional)

Use a Python web service with build `pip install -r requirements.txt` and start `python app.py`; on Render you may need to use a hosting-compatible `PORT` for Gradio, or edit `app.py` to read the service's `PORT` environment variable. Add OpenAI and ontology environment variables in Render service settings.
