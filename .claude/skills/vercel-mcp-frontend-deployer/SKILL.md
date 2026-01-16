---
name: vercel-mcp-frontend-deployer
description: Safely deploy frontend applications using Vercel MCP server by performing pre-deployment error validation followed by automated deployment execution.
---

# Frontend Deployment via Vercel MCP Server

## Instructions

### Phase 1: Pre-Deployment Error Handling
Before starting deployment, always:

1. Validate project structure
   - Ensure `package.json` exists
   - Confirm build script is defined
   - Verify framework detection (Next.js / React / etc.)

2. Environment Variable Validation
   - Ensure required env vars exist
   - Confirm no secrets are missing
   - Validate `.env.production` compatibility

3. Dependency Integrity
   - Check for missing or conflicting packages
   - Run dependency resolution
   - Detect version mismatches

4. Build Validation
   - Run local build command
   - Fail deployment if build errors occur

5. MCP Tool Health Check
   - Confirm Vercel MCP server is reachable
   - Validate deployment tool permissions

If any error occurs:
- Return structured error
- Suggest fix
- STOP deployment

---

### Phase 2: Deployment Execution

Only if Phase 1 passes:

1. Invoke Vercel MCP deployment tool
2. Stream deployment logs
3. Capture deployment URL
4. Verify deployment success
5. Return deployment summary

---

## Deployment Rules
- Never deploy if pre-check fails
- Never suppress build errors
- Never expose secrets in logs
- Always confirm success or failure clearly
- Always return actionable error messages

---

## Successful Deployment Criteria
- Zero build errors
- Vercel deployment completes successfully
- Live URL returned
- Application accessible
- MCP server logs clean
