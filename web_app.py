"""
FIX Protocol Learning & Troubleshooting Web App
Backend: Flask + Anthropic Claude
"""

import json
import os
import sqlite3
import uuid
from datetime import datetime
from flask import Flask, render_template, request, Response, jsonify, stream_with_context
import anthropic

app = Flask(__name__)

SYSTEM_PROMPT = """You are an expert FIX (Financial Information Exchange) protocol advisor for a Fintech professional.
Your role covers three areas:

1. LEARNING — Teach the FIX protocol using FIXimate as the authoritative reference.
   - Explain message types, tags, and field values with precise FIXimate tag numbers
   - Clarify the rules for required vs optional fields
   - Provide concrete examples of raw FIX messages where helpful

2. TRADING WORKFLOWS — Guide through all 21 FIX trading workflows in lifecycle order:

   SESSION PHASE
   01. Logon       — Session establishment: MsgType=A, HeartBtInt(108), SenderCompID(49), TargetCompID(56)
   02. Heartbeat   — Session keepalive: MsgType=0, triggered by HeartBtInt timer or TestReqID(112)

   PRE-TRADE PHASE
   03. Market Data — Subscribe/publish via MarketDataRequest(V) and MarketDataSnapshotFullRefresh(W) / IncrementalRefresh(X)
   04. IOI         — Indication of Interest: MsgType=6, IOIid(23), Side(54), Instrument block
   05. RFQ         — Request for Quote: MsgType=AH (QuoteRequest), QuoteRespID(693), QuoteType(537)
   06. Security Definition — SecurityDefinitionRequest(c) / SecurityDefinition(d), SecurityID(48), SecurityIDSource(22)

   TRADE PHASE
   07. Single Order Lifecycle — NewOrderSingle(D) -> ExecutionReport(8) states: New/PendingNew/PartiallyFilled/Filled/Cancelled
   08. Order Status       — OrderStatusRequest(H) -> ExecutionReport(8) with ExecType(150)=I
   09. Basket/Program     — NewOrderList(E) -> ListStatus(N), ListExecInstType(433)
   10. Multileg           — NewOrderMultileg(AB), LegOrdAmt(58), legs via NoLegs(555) repeating group
   11. Cross Order        — NewOrderCross(s), CrossType(549), CrossPrioritization(550)
   12. Mass Cancel/Kill Switch — OrderMassCancelRequest(q), MassCancelRequestType(530)=7 for all orders

   POST-TRADE PHASE
   13. Execution Report   — MsgType=8: ExecID(17), ExecType(150), OrdStatus(39), LastQty(32), LastPx(31), CumQty(14), LeavesQty(151)
   14. Trade Capture      — TradeCaptureReport(AE), TradeReportID(571), TrdType(828)
   15. Allocation         — AllocationInstruction(J), AllocID(70), AllocTransType(71), NoAllocs(78) repeating group
   16. Trade Confirmation — Confirmation(AK), ConfirmID(664), ConfirmType(773), ConfirmStatus(665)
   17. Settlement Instruction — SettlInstMode(160), SettlInstSource(165), SettlType(63), SettlDate(64)
   18. Position & Collateral  — RequestForPositions(AN), PositionReport(AP), CollateralRequest(AX)

   RISK & OPS PHASE
   19. Drop Copy     — Session-level copy feed via SenderSubID(50)/TargetSubID(57) routing, DeliverToCompID(128)
   20. Session Logoff — Logout(5): Text(58) optional reason, graceful vs. forced disconnect handling
   21. Sequence Recovery/Gap Fill — ResendRequest(2): BeginSeqNo(7)/EndSeqNo(16), SequenceReset(4): GapFillFlag(123)=Y

3. TROUBLESHOOTING — Diagnose and resolve FIX connectivity errors.
   Common categories:
   - Session/Logon failures: comp ID mismatches, version mismatch, HeartBtInt negotiation
   - Sequence number issues: too high/low, gap fill procedures, PossDupFlag(43)/PossResend(97)
   - Heartbeat timeouts: TestRequest(1) / Heartbeat(0) flow, network latency
   - Message rejection: BusinessMessageReject(j) RefMsgType(372), SessionReject(3) SessionRejectReason(373)
   - Field-level errors: required tag missing, invalid value, incorrect data format
   - Order lifecycle errors: OrdStatus transitions, duplicate ClOrdID(11), unknown order
   - Market data issues: subscription failures, stale data, MDReqID(262) mismatch

Always reference FIXimate tag numbers precisely. Format FIX messages in Tag=Value|Tag=Value notation
using pipe (|) as the field delimiter. When showing message examples, include standard header tags:
8(BeginString), 9(BodyLength), 35(MsgType), 49(SenderCompID), 56(TargetCompID), 34(MsgSeqNum),
52(SendingTime), 10(CheckSum). Use markdown formatting for clarity."""


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

DB_PATH = os.path.join(os.path.dirname(__file__), "fix_history.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT,
                created_at TEXT,
                messages TEXT
            )
        """)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return jsonify({"error": "ANTHROPIC_API_KEY is not set on the server."}), 500

    client = anthropic.Anthropic(api_key=api_key)

    def generate():
        try:
            with client.messages.stream(
                model="claude-haiku-4-5",
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=messages,
            ) as stream:
                for text in stream.text_stream:
                    yield f"data: {json.dumps({'text': text})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/api/history", methods=["GET"])
def get_history():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT id, title, created_at FROM conversations ORDER BY created_at DESC"
        ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/history", methods=["POST"])
def save_history():
    data = request.get_json()
    conv_id = str(uuid.uuid4())
    title = data.get("title", "Untitled")[:80]
    messages = json.dumps(data.get("messages", []))
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    with get_db() as conn:
        conn.execute(
            "INSERT INTO conversations VALUES (?, ?, ?, ?)",
            (conv_id, title, created_at, messages),
        )
    return jsonify({"id": conv_id, "title": title, "created_at": created_at})


@app.route("/api/history/<conv_id>", methods=["GET"])
def load_history(conv_id):
    with get_db() as conn:
        row = conn.execute(
            "SELECT messages FROM conversations WHERE id = ?", (conv_id,)
        ).fetchone()
    if row:
        return jsonify({"messages": json.loads(row["messages"])})
    return jsonify({"error": "Not found"}), 404


@app.route("/api/history/<conv_id>", methods=["DELETE"])
def delete_history(conv_id):
    with get_db() as conn:
        conn.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
    return jsonify({"success": True})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def resolve_api_key():
    """Load API key from env var (cloud) or local file (local dev)."""
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if key:
        return key

    key_file = os.path.join(os.path.dirname(__file__), ".api_key")
    if os.path.exists(key_file):
        with open(key_file) as f:
            key = f.read().strip()
    if key:
        os.environ["ANTHROPIC_API_KEY"] = key
        return key

    # Interactive prompt for first-time local setup
    print("\n" + "=" * 50)
    print("  ANTHROPIC_API_KEY not found.")
    print("  Enter your key once — it will be saved locally.")
    print("=" * 50)
    key = input("  Paste your API key: ").strip()
    if not key:
        print("No key entered. Exiting.")
        raise SystemExit(1)
    with open(key_file, "w") as f:
        f.write(key)
    os.environ["ANTHROPIC_API_KEY"] = key
    print("  Key saved. You won't need to enter it again.\n")
    return key


if __name__ == "__main__":
    resolve_api_key()
    init_db()
    port = int(os.environ.get("PORT", 5000))
    print("\n" + "=" * 50)
    print("  FIX Protocol App is running!")
    print(f"  Open your browser at: http://localhost:{port}")
    print("=" * 50 + "\n")
    app.run(host="0.0.0.0", debug=False, port=port)
