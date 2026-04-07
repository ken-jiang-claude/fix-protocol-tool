# FIX Protocol Learning & Troubleshooting Tool
### User Manual

---

## What is this tool?

This is an AI-powered learning and troubleshooting assistant for the **Financial Information Exchange (FIX) Protocol** — the messaging standard used across financial markets for trading, market data, and post-trade processing.

The tool is built for Fintech professionals who need to:
- Learn FIX message types, tags, and workflows
- Understand the full trade lifecycle from session establishment to settlement
- Diagnose and resolve FIX connectivity errors quickly

**Live app:** https://fix-protocol-tool.onrender.com  
**Reference standard:** FIXimate

---

## Getting Started

Open the app in your browser. You will see three main areas:

| Area | Location | Purpose |
|---|---|---|
| Workflow Sidebar | Left panel | Quick access to all 21 FIX workflows |
| Chat Window | Centre | Ask questions, get answers |
| FIX Message Builder | Bottom (via button) | Build and validate FIX messages |

---

## The Two Modes

### Learn Mode (default)
Use this to study FIX concepts, message types, tag definitions, and workflow sequences.

Example questions:
- *"What are the FIX message types and their MsgType values?"*
- *"Explain the ExecutionReport (MsgType=8) OrdStatus transitions"*
- *"What tags are required in a NewOrderSingle?"*

### Troubleshoot Mode
Click the **Troubleshoot** button in the top-right to switch modes. A form appears where you:
1. Select the **error category** (e.g. Session/Logon, Sequence Number)
2. Select your **FIX version** (4.2, 4.4, 5.0 SP2, FIXT 1.1)
3. Paste the **error message or raw FIX message**
4. Click **Send** for a step-by-step diagnosis

---

## The 21 FIX Workflows (Sidebar)

Click any workflow in the left sidebar to instantly ask about it. They are grouped by phase:

### Session Phase
| # | Workflow | Key Messages |
|---|---|---|
| 01 | Logon | MsgType=A |
| 02 | Heartbeat | MsgType=0, TestRequest=1 |

### Pre-Trade Phase
| # | Workflow | Key Messages |
|---|---|---|
| 03 | Market Data | V, W, X |
| 04 | IOI | MsgType=6 |
| 05 | RFQ | MsgType=AH |
| 06 | Security Definition | c, d |

### Trade Phase
| # | Workflow | Key Messages |
|---|---|---|
| 07 | Single Order Lifecycle | D → 8 |
| 08 | Order Status | H → 8 |
| 09 | Basket / Program | E → N |
| 10 | Multileg | AB |
| 11 | Cross Order | s |
| 12 | Mass Cancel / Kill Switch | q |

### Post-Trade Phase
| # | Workflow | Key Messages |
|---|---|---|
| 13 | Execution Report | MsgType=8 |
| 14 | Trade Capture | AE |
| 15 | Allocation | J |
| 16 | Trade Confirmation | AK |
| 17 | Settlement Instruction | SettlType(63) |
| 18 | Position & Collateral | AN, AP, AX |

### Risk & Ops Phase
| # | Workflow | Key Messages |
|---|---|---|
| 19 | Drop Copy | SenderSubID(50) routing |
| 20 | Session Logoff | MsgType=5 |
| 21 | Sequence Recovery | MsgType=2, 4 |

---

## FIX Message Builder

Click the **Builder (⚙)** button in the input bar to open the message builder.

1. Select **BeginString** — FIX version (e.g. FIX.4.4)
2. Select **MsgType** — the message you want to build
3. Enter **SenderCompID** and **TargetCompID**
4. Set **MsgSeqNum**
5. Add any custom tags using **+ Add Tag**
6. The **Message Preview** updates in real time in standard `Tag=Value|` format
7. Click **Ask AI to Validate** — the AI will check for missing required tags and errors
8. Click **Copy Message** to copy the raw FIX string to clipboard

---

## Saving & Reloading Conversations

- Click **Save Conversation** (bottom of sidebar) to store the current chat
- Switch to the **History** tab to see all saved conversations
- Click any saved conversation to reload it
- Click **×** to delete a saved conversation

---

## Common Troubleshooting Scenarios

| Problem | Suggested Action |
|---|---|
| Logon rejected | Switch to Troubleshoot mode → select Session/Logon → paste the reject message |
| Sequence number too low/high | Select Sequence Number category → describe the gap |
| Heartbeat timeout | Select Heartbeat Timeout → provide the HeartBtInt value and logs |
| Order not acknowledged | Select Order Lifecycle → paste the NewOrderSingle and any response |
| Tag missing / invalid | Select Field/Tag Error → paste the full FIX message |

---

## Tips for Best Results

- **Paste raw FIX messages** when troubleshooting — the AI reads `Tag=Value` format directly
- **Use the sidebar** for workflow questions — each button sends a precise, detailed prompt
- **Save conversations** you want to revisit — history is stored locally on the server
- **Use the Builder** to construct test messages before sending them to a counterparty

---

*Powered by Claude AI | Reference: FIXimate | Built for Fintech professionals*
