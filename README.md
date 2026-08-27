# NurtureHub

NurtureHub is a private family command center for multi-child calendars, meals, activity, growth records, and carefully bounded AI assistance.

The interface is a Next.js web app. The AI recommendation backend is implemented separately in Python under `agent_service/` so it can run behind AWS API Gateway and Lambda. Keeping the interface and agent separate prevents API keys and privileged data access from entering the browser or mobile bundle.

## Privacy and AI boundaries

- Family records are stored server-side and keyed to the authenticated adult's user ID.
- The browser never connects directly to the database.
- AI is intended only for explicit actions such as recipe suggestions, calendar summaries, conflict detection, and extracting proposed events.
- Saving or viewing ordinary family records does not require AI.
- Send only the minimum relevant context to an AI provider. Never use growth data for diagnosis.
- Store API keys only in backend secret management—never in frontend code, Git, or a mobile bundle.
- For children under 13, the Python service refuses to send data to OpenAI unless `OPENAI_ZDR_APPROVED=true`. This flag should be enabled only after the relevant OpenAI project has actually been approved and configured for Zero Data Retention.

## Python agent guardrails

The agent endpoint is `POST /v1/suggestions`. Its controls are enforced in code, outside the model:

- validates the Cognito JWT and derives the parent ID from its signed `sub` claim;
- loads the child only with the authenticated parent ID as part of the DynamoDB key;
- requires recorded parental consent before any AI request;
- sends an age band and a small preference/activity summary—not names, birthdays, growth measurements, school information, emails, or household IDs;
- sets `store=False` and requests a strict structured response;
- blocks medical diagnosis, treatment, weight-loss, BMI, and supplement-dose language;
- rejects output that mentions a saved allergen;
- marks every result as AI-generated and requiring parent review;
- gives the model no tools and no ability to write calendar, meal, growth, or activity records.

These are product guardrails, not a substitute for legal review, a child-safety assessment, security testing, or compliance with COPPA and other applicable laws.

## Current hosting

This checkout is configured for OpenAI Sites and Cloudflare D1. Its server route imports the Cloudflare runtime, so it cannot be moved unchanged to AWS.

## Recommended AWS architecture

| Concern | AWS service |
| --- | --- |
| Web application and SSR | AWS Amplify Hosting or an OpenNext deployment |
| Authentication | Amazon Cognito |
| Structured family data | Amazon DynamoDB |
| API keys and runtime secrets | AWS Secrets Manager |
| Email/calendar ingestion jobs | AWS Lambda + Amazon EventBridge |
| Python recommendation agent | AWS Lambda + API Gateway |
| Uploaded invitations or files | Amazon S3 |
| Logs and alerts | Amazon CloudWatch |

## Deploying on AWS

### 1. Prepare the application

1. Push this repository to GitHub.
2. Create a migration branch for AWS.
3. Replace the Vinext scripts with the standard Next.js scripts: `next dev`, `next build`, and `next start`.
4. Remove the Cloudflare-specific Sites plugin and D1 runtime imports.
5. Keep all secret files out of Git. Commit only an `.env.example` containing variable names.

### 2. Create authentication

1. Create an Amazon Cognito user pool.
2. Configure a web client and callback URLs for the deployed domain.
3. Protect every data API on the server.
4. Derive the household member ID from the verified Cognito token. Never trust a user ID sent in a request body.

### 3. Create the database

Create DynamoDB tables for:

- `households` — partition key `householdId`
- `householdMembers` — partition key `householdId`, sort key `userId`
- `children` — partition key `householdId`, sort key `childId`
- `events` — partition key `householdId`, sort key `eventDate#eventId`
- `childRecords` — partition key `childId`, sort key `recordType#recordDate`

Use authorization checks on every read and write to confirm that the authenticated user belongs to the requested household.

### 4. Replace the data route

Replace `app/api/family-data/route.ts` with AWS SDK calls using `@aws-sdk/client-dynamodb` and `@aws-sdk/lib-dynamodb`. Do not expose database credentials in the browser. On AWS, assign the server runtime an IAM role that can access only the required tables.

### 5. Configure secrets

Store sensitive values in AWS Secrets Manager, including any future `OPENAI_API_KEY`. Grant only the server runtime permission to retrieve each secret. Never prefix a secret with `NEXT_PUBLIC_`.

### 5a. Deploy the Python agent

1. Build a Lambda deployment package or container from `agent_service/requirements.txt`.
2. Set the handler to `agent_service.app.handler` and place it behind an API Gateway HTTP API.
3. Give the Lambda role read-only access to the child-context table and permission to read only the OpenAI secret.
4. Configure `COGNITO_ISSUER`, `COGNITO_CLIENT_ID`, `CHILD_CONTEXT_TABLE`, and `OPENAI_MODEL`.
5. Retrieve `OPENAI_API_KEY` from Secrets Manager during deployment or cold start; never expose it to Amplify.
6. Keep `OPENAI_ZDR_APPROVED=false` until the OpenAI project is approved and configured for Zero Data Retention. With the flag false, under-13 AI calls fail closed.
7. Add API Gateway throttling and AWS WAF rate limits. Do not log request or response bodies.
8. Point the web app’s server-side proxy at the API Gateway URL. The browser should never call the agent with AWS or OpenAI credentials.

### 6. Deploy with Amplify Hosting

1. In AWS Amplify, choose **New app → Host web app**.
2. Connect the GitHub repository and select the AWS migration branch.
3. Confirm Amplify detects the Next.js SSR build.
4. Add non-secret configuration in Amplify environment variables.
5. Reference Secrets Manager values from the server runtime.
6. Deploy and add the production URL to the Cognito callback and logout URL lists.

### 7. Validate before production

- Confirm one household cannot read another household's records.
- Confirm child profile filters cannot bypass server authorization.
- Confirm secrets are absent from client JavaScript and build artifacts.
- Confirm logs do not contain email bodies, child health data, or API keys.
- Test backup, deletion, export, invitation, and caregiver-removal workflows.
- Add retention policies and a privacy policy before inviting external users.

## Local development

The current Sites version uses:

```bash
npm install
npm run dev
```

For the AWS migration, switch to the standard Next.js runtime only after replacing the Cloudflare-specific database route and hosting plugin.
