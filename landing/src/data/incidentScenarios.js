export const incidentScenarios = {
  sql: {
    id: "sql",
    name: "DevOps Agent // Accidental DROP TABLE Attempt",
    badge: "CRITICAL SEVERITY",
    badgeColor: "bg-red-500/10 text-red-400 border-red-500/30",
    agentName: "InfraOrchestrator-v3",
    framework: "LangGraph + PostgreSQL Toolset",
    earliestDivergenceStep: 3,
    crashStep: 4,
    detectedInMs: 11.4,
    steps: [
      {
        step: 1,
        name: "Intent Analysis",
        tool: "llm_intent_parser",
        time: "10:42:01.120",
        status: "success",
        statusLabel: "OK",
        description: "Parse user request: 'Clean up stale test databases from staging cluster'",
        expected: "Identify databases matching prefix 'test_2024_*' and target 'staging_cluster_02'",
        actual: "Identified prefix 'test_*' with ambiguous scope across all reachable clusters",
        tokens: 312,
      },
      {
        step: 2,
        name: "Cluster Inventory Query",
        tool: "pg_catalog_query",
        time: "10:42:01.350",
        status: "success",
        statusLabel: "OK",
        description: "Fetch schema metadata for 18 schemas in cluster",
        expected: "Filter exclusively on environment='staging' and created_at < NOW() - INTERVAL '30 days'",
        actual: "Catalog query returned 18 tables including production shard 'core_ledger_v2'",
        tokens: 580,
      },
      {
        step: 3,
        name: "Migration & Drop Plan Synthesis",
        tool: "query_planner_agent",
        time: "10:42:01.890",
        status: "divergence",
        statusLabel: "ROOT CAUSE DIVERGENCE",
        divergenceNote: "EARLIEST POINT OF FAILURE IDENTIFIED HERE",
        description: "Agent synthesizes SQL plan containing: DROP TABLE core_ledger_v2 CASCADE;",
        expected: "Synthesize DROP TABLE for only 'test_scratch_temp' tables with dry-run confirmation",
        actual: "Hallucinated that 'core_ledger_v2' was a deprecated staging copy due to lack of environment parameter binding.",
        delta: "Missing constraint WHERE is_production = false. Semantic drift = 94.2%",
        tokens: 890,
      },
      {
        step: 4,
        name: "Database Execution Attempt",
        tool: "pg_execute_destructive",
        time: "10:42:02.105",
        status: "blocked",
        statusLabel: "BLOCKED BY SAFETY ENGINE",
        description: "Attempted execution of raw query: DROP TABLE core_ledger_v2 CASCADE;",
        safetyRule: "Policy Rule #SEC-801: Destructive DDL command on non-staging schema blocked",
        actionTaken: "Execution aborted. Zero bytes altered. Incident ticket BF-8942 generated.",
        tokens: 210,
      },
      {
        step: 5,
        name: "Synthesized Patch & CI Replay",
        tool: "bifura_auto_fixer",
        time: "10:42:02.430",
        status: "verified",
        statusLabel: "REPLAY PASS 100%",
        description: "Applied semantic guard constraint & strict Pydantic query validator.",
        expected: "Replay executes cleanly with 0 dropped production tables.",
        actual: "Deterministic replay against 24 regression test cases passed in 840ms.",
        tokens: 440,
      },
    ],
    blastRadius: [
      { id: "db_core", name: "PostgreSQL: core_ledger_v2", type: "Database Table", status: "PROTECTED", detail: "Safety engine blocked drop command. 4,280,000 records preserved." },
      { id: "stripe_sync", name: "Stripe Webhook Worker", type: "Downstream API", status: "SAVED_FROM_FAILURE", detail: "Avoided unhandled cascading 500 error loop across payment reconciliations." },
      { id: "audit_log", name: "Datadog Incident Hook", type: "Monitoring", status: "ALERT_EMITTED", detail: "Instant high-priority Slack & PagerDuty telemetry emitted with root cause diff." },
      { id: "cache_redis", name: "Redis In-Memory State", type: "Cache Layer", status: "CLEARED", detail: "Orphaned transaction caches sanitized automatically." },
    ],
    safetyClassification: {
      actionAttempted: "pg_execute_destructive('DROP TABLE core_ledger_v2 CASCADE;')",
      verdict: "BLOCK",
      confidence: "99.98%",
      triggeredRules: [
        { code: "CRIT-01", name: "Destructive DDL without explicit human PIN signature", risk: "CRITICAL" },
        { code: "ENV-04", name: "Cross-environment isolation breach (Staging -> Production)", risk: "SEVERE" }
      ],
      allowAlternatives: [
        "ALLOW pg_read_schema",
        "REVIEW pg_drop_test_partition",
        "BLOCK pg_drop_unfiltered"
      ]
    },
    verifiedFix: {
      diffBefore: `// Flawed prompt instruction:
"Execute table drops on any table matching test patterns returned by the catalog."`,
      diffAfter: `// Certified Bifura Patch (#FIX-8942):
"CRITICAL INSTRUCTION: You MUST verify schema.is_production == false.
You are strictly forbidden from issuing DROP queries against tables outside 'staging_temp_*'.
Required validation schema:
{
  target_schema: 'staging_temp_*',
  dry_run_hash: verified_checksum,
  requires_safety_token: true
}"`,
      replayStats: {
        testsRun: 24,
        regressionsFound: 0,
        replayDuration: "840ms",
        status: "CERTIFIED BY REPLAY HARNESS"
      }
    }
  },
  financial: {
    id: "financial",
    name: "FinTech Agent // Arbitrage Loop & Double Refund",
    badge: "HIGH SEVERITY",
    badgeColor: "bg-amber-500/10 text-amber-400 border-amber-500/30",
    agentName: "DisputeResolver-Agent",
    framework: "CrewAI Multi-Role Agent",
    earliestDivergenceStep: 2,
    crashStep: 4,
    detectedInMs: 14.1,
    steps: [
      {
        step: 1,
        name: "Dispute Intake",
        tool: "zendesk_ticket_parser",
        time: "14:15:20.040",
        status: "success",
        statusLabel: "OK",
        description: "Customer requested partial refund for damaged order #EUR-9831",
        expected: "Extract claim amount (€45.00) and link to transaction tx_88291",
        actual: "Correctly extracted €45.00 claim amount and tx_88291",
        tokens: 410,
      },
      {
        step: 2,
        name: "Ledger State Inspection",
        tool: "ledger_lookup",
        time: "14:15:20.450",
        status: "divergence",
        statusLabel: "ROOT CAUSE DIVERGENCE",
        divergenceNote: "EARLIEST POINT OF FAILURE IDENTIFIED HERE",
        description: "Agent misinterprets pending authorization status as failed capture",
        expected: "Read pending capture flag and queue webhook wait for bank settlement",
        actual: "Agent hallucinated that transaction had timed out and initiated duplicate parallel reimbursement sequence.",
        delta: "State confusion between 'PENDING_CAPTURE' and 'VOIDED'. Delta: 87.4%",
        tokens: 620,
      },
      {
        step: 3,
        name: "Payment Gateway Dispatch",
        tool: "stripe_refund_create",
        time: "14:15:20.910",
        status: "success",
        statusLabel: "OK (First Call)",
        description: "Dispatched refund for €45.00",
        expected: "Mark ticket as settled and finalize state machine",
        actual: "Refund 1 succeeded. Agent immediately triggered second refund tool invocation due to lingering state loop.",
        tokens: 380,
      },
      {
        step: 4,
        name: "Duplicate Payout Attempt",
        tool: "stripe_refund_create",
        time: "14:15:21.140",
        status: "blocked",
        statusLabel: "BLOCKED BY SAFETY ENGINE",
        description: "Attempted duplicate refund of €45.00 on the same order within 230ms",
        safetyRule: "Policy Rule #FIN-402: Idempotency breach & velocity limit exceeded",
        actionTaken: "Blocked duplicate transaction. Ledger integrity intact.",
        tokens: 280,
      },
      {
        step: 5,
        name: "Patch & State Machine Seal",
        tool: "bifura_auto_fixer",
        time: "14:15:21.480",
        status: "verified",
        statusLabel: "REPLAY PASS 100%",
        description: "Added strict idempotency token and state lock in agent graph.",
        expected: "Replay executes single refund and gracefully exits.",
        actual: "18 historical dispute replay suites executed: 0 over-refunds.",
        tokens: 390,
      },
    ],
    blastRadius: [
      { id: "stripe_acc", name: "Merchant Stripe Balance", type: "Financial Account", status: "PROTECTED", detail: "Prevented unauthorized duplicate €45.00 debit and merchant dispute fee." },
      { id: "erp_sync", name: "NetSuite ERP Ledger", type: "Accounting System", status: "SAVED_FROM_FAILURE", detail: "Prevented reconciliation discrepancy in end-of-month financial closing." },
      { id: "user_mail", name: "Customer Notification", type: "Email Dispatcher", status: "SANITIZED", detail: "Only one single receipt email was dispatched to end customer." },
    ],
    safetyClassification: {
      actionAttempted: "stripe_refund_create(order_id='EUR-9831', amount=45.00, retry_count=1)",
      verdict: "BLOCK",
      confidence: "99.91%",
      triggeredRules: [
        { code: "FIN-402", name: "Velocity threshold: duplicate tool invocation on same entity within 5s", risk: "HIGH" },
        { code: "IDEMP-01", name: "Missing cryptographic client idempotency key", risk: "MEDIUM" }
      ],
      allowAlternatives: [
        "ALLOW ledger_read_balance",
        "REVIEW manual_finance_override",
        "BLOCK duplicate_payout"
      ]
    },
    verifiedFix: {
      diffBefore: `// Vulnerable loop logic:
"If refund status confirmation is not immediately returned in tool response, retry Stripe refund API."`,
      diffAfter: `// Certified Bifura Patch (#FIX-4021):
"CRITICAL INSTRUCTION: Generate a deterministic idempotency key format:
idempotency_key = sha256(order_id + '_' + dispute_id)
NEVER reissue refund tool if ledger status is PENDING_CAPTURE.
Wait for webhook confirmation event."`,
      replayStats: {
        testsRun: 18,
        regressionsFound: 0,
        replayDuration: "620ms",
        status: "CERTIFIED BY REPLAY HARNESS"
      }
    }
  },
  pii: {
    id: "pii",
    name: "HR Talent Agent // Confidential PII Data Leak",
    badge: "MEDIUM SEVERITY",
    badgeColor: "bg-blue-500/10 text-cyan-400 border-cyan-500/30",
    agentName: "CompensationAnalyst-v2",
    framework: "Custom In-House Agentic Loop",
    earliestDivergenceStep: 2,
    crashStep: 3,
    detectedInMs: 9.8,
    steps: [
      {
        step: 1,
        name: "Prompt Interpretation",
        tool: "hr_query_handler",
        time: "16:04:12.110",
        status: "success",
        statusLabel: "OK",
        description: "Prompt: 'Synthesize average market percentile for Senior Backend Engineers in Paris'",
        expected: "Aggregate anonymized statistics across salary bands",
        actual: "Parsed salary band query accurately",
        tokens: 280,
      },
      {
        step: 2,
        name: "Internal Payroll Query",
        tool: "workday_salary_export",
        time: "16:04:12.390",
        status: "divergence",
        statusLabel: "ROOT CAUSE DIVERGENCE",
        divergenceNote: "EARLIEST POINT OF FAILURE IDENTIFIED HERE",
        description: "Agent exported raw employee records including full names, IBANs, and bonuses",
        expected: "Call anonymize_dataset(columns=['name', 'iban', 'national_id']) before reasoning",
        actual: "Bypassed data sanitization node due to relaxed prompt condition and stored plain text in scratchpad.",
        delta: "PII leak vector: 14 employee names & individual base salaries loaded into unmasked context.",
        tokens: 740,
      },
      {
        step: 3,
        name: "Public Webhook Delivery Attempt",
        tool: "slack_post_message",
        time: "16:04:12.720",
        status: "blocked",
        statusLabel: "BLOCKED BY SAFETY ENGINE",
        description: "Attempted to broadcast unmasked spreadsheet to channel #general-engineering",
        safetyRule: "Policy Rule #GDPR-109: Unmasked PII / compensation data transmission to public channel blocked",
        actionTaken: "Message intercepted. Transmission halted. Audit alert sent to DPO.",
        tokens: 510,
      },
      {
        step: 4,
        name: "Targeted Fix & Automated Anonymization Filter",
        tool: "bifura_auto_fixer",
        time: "16:04:13.010",
        status: "verified",
        statusLabel: "REPLAY PASS 100%",
        description: "Injected irreversible differential privacy masking filter at data fetch boundary.",
        expected: "Only k-anonymized percentile distributions (p50, p75, p90) permitted in output context.",
        actual: "Replay verified against 30 GDPR test cases: 0 PII leaks detected.",
        tokens: 310,
      },
    ],
    blastRadius: [
      { id: "slack_chan", name: "Slack #general-engineering", type: "Internal Comms", status: "PROTECTED", detail: "Intercepted broadcast before any employee could view executive compensation table." },
      { id: "cnil_audit", name: "GDPR / CNIL Regulatory Exposure", type: "Legal Compliance", status: "ZERO_INCIDENT", detail: "Zero data breach notification required; incident contained within isolated memory boundary." },
      { id: "dpo_inbox", name: "DPO Security Log", type: "Audit Log", status: "LOGGED", detail: "Full incident trace captured with cryptographic hash proof of non-exposure." },
    ],
    safetyClassification: {
      actionAttempted: "slack_post_message(channel='#general-engineering', attachment='salaries_raw_2026.csv')",
      verdict: "BLOCK",
      confidence: "99.99%",
      triggeredRules: [
        { code: "GDPR-109", name: "High-risk PII pattern detected in payload (Salary, IBAN, Full Name)", risk: "CRITICAL" },
        { code: "ACCESS-03", name: "Audience scope mismatch: Executive HR data targeted at broad channel", risk: "HIGH" }
      ],
      allowAlternatives: [
        "ALLOW anonymize_and_aggregate",
        "REVIEW route_to_private_dpo_dm",
        "BLOCK public_channel_broadcast"
      ]
    },
    verifiedFix: {
      diffBefore: `// Unsafe data retrieval:
"Fetch raw employee rows from Workday and format summary table directly for Slack."`,
      diffAfter: `// Certified Bifura Patch (#FIX-GDPR-109):
"MANDATORY SANITIZATION STEP:
Input payload MUST pass through DifferentialPrivacyFilter(epsilon=0.5).
Any field containing [Full Name, Salary, IBAN, TaxID] must be stripped.
Output MUST ONLY contain statistical percentiles: {p25, p50, p75, p90}."`,
      replayStats: {
        testsRun: 30,
        regressionsFound: 0,
        replayDuration: "510ms",
        status: "CERTIFIED BY REPLAY HARNESS"
      }
    }
  }
};
