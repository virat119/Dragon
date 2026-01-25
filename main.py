import requests, json, time, random
from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "dragonpay_v4_ultra_2026"
app.permanent_session_lifetime = 86400 

# --- CONFIG ---
DB_URL = "https://user-name-4cc00-default-rtdb.firebaseio.com"
API_KEY = "AIzaSyDLnmiafYGn9P5Dq1ewq8l0UcEVK_errN8"

def fb(m, p, d=None):
    url = f"{DB_URL}/{p}.json?auth={API_KEY}"
    try:
        if m == 'GET': return requests.get(url).json()
        if m == 'DELETE': return requests.delete(url).json()
        return requests.patch(url, json.dumps(d)).json()
    except: return None

# --- UI CSS (MODERN LOOK) ---
CSS = """
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
<style>
    :root { --dragon: #ffc107; --dark: #121212; --bg: #f8f9fa; }
    body { background: var(--bg); font-family: 'Inter', sans-serif; margin: 0; padding-bottom: 90px; overflow-x: hidden; }
    .app-container { max-width: 500px; margin: 0 auto; min-height: 100vh; background: var(--bg); }
    .header-card { background: linear-gradient(180deg, #212529 0%, #343a40 100%); color: white; padding: 25px 20px; border-radius: 0 0 30px 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
    .dragon-card { background: white; border-radius: 20px; padding: 18px; margin-bottom: 15px; border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.04); }
    .action-card { text-align: center; padding: 20px; transition: 0.3s; cursor: pointer; border-bottom: 4px solid transparent; }
    .action-card:active { transform: scale(0.95); }
    .market-amt { font-size: 1.3rem; font-weight: 800; color: #1a1a1a; }
    .reward-badge { background: #e8f5e9; color: #2e7d32; padding: 4px 10px; border-radius: 8px; font-size: 0.75rem; font-weight: 700; }
    .nav-bottom { position: fixed; bottom: 0; width: 100%; max-width: 500px; background: white; display: flex; justify-content: space-around; padding: 12px; border-top: 1px solid #eee; z-index: 1000; box-shadow: 0 -5px 15px rgba(0,0,0,0.05); }
    .nav-item { text-align: center; color: #bbb; text-decoration: none; font-size: 11px; flex: 1; }
    .nav-item.active { color: var(--dragon); }
    .modal-content { border-radius: 25px; border: none; }
    .detail-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f1f1f1; }
    .btn-main { background: var(--dragon); color: black; font-weight: 800; border-radius: 15px; padding: 14px; border: none; width: 100%; box-shadow: 0 5px 15px rgba(255,193,7,0.3); }
    .fade-in { animation: fadeIn 0.5s ease-in; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    
    .support-btn { background: #0088cc; color: white; border-radius: 15px; padding: 12px; text-decoration: none; display: flex; align-items: center; justify-content: center; font-weight: 600; margin-top: 10px; }
    .support-btn:hover { color: white; opacity: 0.9; }

    /* Admin Specific Tabs */
    .admin-nav .nav-link { color: #666; font-weight: 600; border: none; border-bottom: 3px solid transparent; }
    .admin-nav .nav-link.active { color: #dc3545; border-bottom: 3px solid #dc3545; background: none; }
    .proof-img-box { width: 100%; height: 120px; border-radius: 10px; object-fit: cover; border: 2px solid #ffc107; cursor: pointer; }


</style>
"""

# --- ROUTES ---

@app.route('/')
def login():
    if 'user' in session: return redirect('/home')
    return render_template_string(f"""
    <html><head>{CSS}</head><body style="background:#121212"><div class="app-container d-flex align-items-center p-4">
        <div class="dragon-card w-100 p-4 shadow-lg text-center">
            <h2 class="fw-bold mb-4">DragonPay &#128009</h2>
            <form action="/auth" method="post">
                <input type="email" name="email" placeholder="Gmail Address" class="form-control mb-3 py-3 rounded-3" required>
                <input type="password" name="pw" placeholder="Password" class="form-control mb-4 py-3 rounded-3" required>
                <button name="act" value="login" class="btn-main mb-3">LOG IN</button>
                <button name="act" value="reg" class="btn btn-outline-dark w-100 py-3 rounded-3 fw-bold">CREATE ACCOUNT</button>
            </form>
        </div>
    </div></body></html>""")

@app.route('/auth', methods=['POST'])
def auth():
    email = request.form.get('email').replace('.', ',').lower()
    pw, act = request.form.get('pw'), request.form.get('act')
    u = fb('GET', f"users/{email}")
    if act == 'reg':
        if u: return "Email exists! <a href='/'>Back</a>"
        u = {"email": email, "password": pw, "balance": 0.0, "uuid": "DP"+str(random.randint(1000,9999)), "bank_acc":"", "upi_id":"", "bank_name":"", "ifsc":""}
        fb('PATCH', f"users/{email}", u)
    elif not u or u['password'] != pw: return "Error! <a href='/'>Back</a>"
    session['user'] = email
    return redirect('/home')

@app.route('/home')
def home():
    if 'user' not in session: return redirect('/')
    u = fb('GET', f"users/{session['user']}")
    all_o = fb('GET', 'orders') or {}
    pending = [v for k,v in all_o.items() if v.get('phone') == session['user'] and v.get('status') == 'Pending']
    
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="app-container">
    <div class="header-card">
        <div class="d-flex justify-content-between mb-3"><span class="fw-bold">DragonPay &#128009</span><i class="bi bi-gear"></i></div>
        <small class="opacity-75">Available Balance</small>
        <div class="display-5 fw-bold text-warning mb-2">&#8377;{{{{u.balance}}}}.00</div>
        <div class="badge bg-secondary">UID: {{{{u.uuid}}}}</div>
    </div>
    
    <div class="p-3">
        <div class="row g-3 mb-4">
            <div class="col-6"><div onclick="location.href='/buy'" class="dragon-card action-card shadow-sm" style="border-bottom-color: #ffc107"><i class="bi bi-graph-up-arrow text-warning fs-2"></i><div class="fw-bold mt-2">BUY COIN</div></div></div>
            <div class="col-6"><div onclick="location.href='/sell'" class="dragon-card action-card shadow-sm" style="border-bottom-color: #198754"><i class="bi bi-wallet2 text-success fs-2"></i><div class="fw-bold mt-2">SELL COIN</div></div></div>
        </div>

        <a href="https://t.me/Shinchain120" class="support-btn mb-4">
            <i class="bi bi-telegram me-2"></i> Contact Support (@Shinchain120)
        </a>

        {{% if pending %}}
        <h6 class="fw-bold mb-3 px-1"><i class="bi bi-hourglass-split"></i> Active Orders</h6>
        {{% for o in pending %}}
        <div class="dragon-card fade-in" style="background: #fffdf5; border-left: 5px solid #ffc107">
            <div class="d-flex justify-content-between align-items-center">
                <span><b>{{{{o.type}}}} Request</b><br><small class="text-muted">{{{{o.time}}}}</small></span>
                <span class="fw-bold text-warning small">PENDING...</span>
            </div>
            <div class="mt-2 fw-bold text-dark">&#8377;{{{{o.amt}}}}</div>
        </div>
        {{% endfor %}}
        {{% endif %}}
    </div>

    <div class="nav-bottom">
        <a href="/home" class="nav-item active"><i class="bi bi-house-door-fill fs-4"></i><br>Home</a>
        <a href="/orders" class="nav-item"><i class="bi bi-receipt-cutoff fs-4"></i><br>Orders</a>
        <a href="/profile" class="nav-item"><i class="bi bi-person-circle fs-4"></i><br>Profile</a>
    </div></div></body></html>""", u=u, pending=pending)

@app.route('/buy')
def buy():
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="app-container p-3">
    <h5 class="fw-bold mb-3"><i class="bi bi-chevron-left me-2" onclick="location.href='/home'"></i>Marketplace</h5>
    <ul class="nav nav-pills nav-justified mb-4" id="buyTabs">
        <li class="nav-item"><button class="nav-link active rounded-pill" data-bs-toggle="tab" data-bs-target="#small-t">Small Amount</button></li>
        <li class="nav-item"><button class="nav-link rounded-pill" data-bs-toggle="tab" data-bs-target="#big-t">Big Amount</button></li>
    </ul>
    
    <div class="tab-content">
        <div class="tab-pane fade show active" id="small-t"></div>
        <div class="tab-pane fade" id="big-t"></div>
    </div>

    <script>
        function updateMarket() {{
            const gen = (min, max, div, bonus) => {{
                let html = '';
                for(let i=0; i<6; i++){{
                    let amt = Math.floor(Math.random()*(max-min+1))+min;
                    let rew = (amt * (bonus/100)).toFixed(0);
                    html += `<div class="dragon-card d-flex justify-content-between align-items-center fade-in">
                        <div><div class="market-amt">&#8377;${{amt}}</div><span class="reward-badge">+&#8377;${{rew}} Bonus (DRB)</span></div>
                        <button onclick="location.href='/pay_mode/${{amt}}?reward=${{rew}}'" class="btn btn-warning btn-sm fw-bold px-4 rounded-pill">BUY</button>
                    </div>`;
                }}
                document.getElementById(div).innerHTML = html;
            }};
            gen(100, 2000, 'small-t', 5); gen(2001, 50000, 'big-t', 3);
        }}
        setInterval(updateMarket, 15000); updateMarket();
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </div></body></html>""")

@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if 'user' not in session: return redirect('/')
    u = fb('GET', f"users/{session['user']}")
    if request.method == 'POST':
        amt = int(request.form.get('amt', 0))
        if amt > u['balance']: return "<script>alert('Insufficient Balance!');window.location='/sell';</script>"
        if amt % 100 != 0: return "<script>alert('Please enter amount in multiples of 100!');window.location='/sell';</script>"
        if not u.get('bank_acc') and not u.get('upi_id'): return "<script>alert('Please add bank card first!');window.location='/profile';</script>"
        
        # Gathering withdrawal info for admin
        w_info = f"UPI: {u.get('upi_id')} | Bank: {u.get('bank_name')} | Acc: {u.get('bank_acc')} | IFSC: {u.get('ifsc')}"
        
        oid = "SELL"+str(int(time.time()))
        fb('PATCH', f"orders/{oid}", {"oid":oid, "phone":session['user'], "amt":amt, "status":"Pending", "type":"Sell", "time":time.strftime("%Y-%m-%d %H:%M"), "utr":"Withdrawal", "w_info": w_info})
        fb('PATCH', f"users/{session['user']}", {"balance": u['balance'] - amt})
        return redirect('/orders')
    
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="app-container p-3">
    <h5 class="fw-bold mb-4"><i class="bi bi-chevron-left me-2" onclick="location.href='/home'"></i>Sell Coins</h5>
    <div class="dragon-card text-white p-4" style="background:#198754">
        <small class="opacity-75">Current Balance</small>
        <h2 class="fw-bold">&#8377;{{{{u.balance}}}}.00</h2>
    </div>
    <form method="post" class="mt-4">
        <label class="small fw-bold mb-2">Withdraw Amount (Multiples of 100)</label>
        <input name="amt" type="number" class="form-control py-3 mb-3" placeholder="Ex: 500, 1000, 1500" required>
        <button class="btn-main shadow">WITHDRAW NOW</button>
    </form>
    </div></body></html>""", u=u)

@app.route('/profile')
def profile():
    # 1. Basic Session Check
    if 'user' not in session: 
        return redirect('/')
    
    # 2. Database se data lao
    u = fb('GET', f"users/{session['user']}")
    
    # 3. ðŸ”¥ CRASH PROTECTION: Agar user DB mein nahi mila
    if not u:
        session.clear() # Cookie khatam karo
        return redirect('/') # Wapas login page par bhej do
    
    # 4. Render with Safety: Har jagah .get() ka use kiya hai
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="app-container">
    <div class="header-card text-center">
        <h3 class="fw-bold mb-0 text-warning">&#8377;{{{{u.get('balance', 0)}}}}.00</h3>
        <small class="opacity-75">DRB BALANCE</small>
    </div>
    <div class="p-3">
        <div class="dragon-card mb-4 d-flex align-items-center">
            <i class="bi bi-person-circle fs-1 text-warning me-3"></i>
            <div>
                <div class="fw-bold">{{{{u.get('email', 'User').replace(',','.')}}}}</div>
                <small class="text-muted">UID: {{{{u.get('uuid', 'N/A')}}}}</small>
            </div>
        </div>

        <a href="https://t.me/Shinchain120" class="support-btn mb-4" style="background:#222;">
            <i class="bi bi-headset me-2"></i> 24/7 Telegram Support
        </a>

        <h6 class="fw-bold mb-3 px-1">Withdrawal Methods</h6>
        
        <div class="dragon-card" style="background: #f0f7ff; border: 1px dashed #0d6efd">
            <div class="d-flex justify-content-between align-items-center">
                <span><i class="bi bi-qr-code text-primary me-2"></i> <b>UPI ID</b></span>
                <button class="btn btn-sm btn-primary rounded-pill" onclick="document.getElementById('upiBox').style.display='block'">{{{{ 'Change' if u.get('upi_id') else 'Add' }}}}</button>
            </div>
            <div class="mt-2 fw-bold text-dark">{{{{ u.get('upi_id', 'Not Linked') }}}}</div>
        </div>
        
        <div class="dragon-card" style="background: #fff9f0; border: 1px dashed #ffc107">
            <div class="d-flex justify-content-between align-items-center">
                <span><i class="bi bi-bank text-warning me-2"></i> <b>Bank Card</b></span>
                <button class="btn btn-sm btn-warning rounded-pill" onclick="document.getElementById('bankBox').style.display='block'">{{{{ 'Change' if u.get('bank_acc') else 'Add' }}}}</button>
            </div>
            <div class="mt-2 small">
                <b>Acc No:</b> {{{{ u.get('bank_acc', 'N/A') }}}}<br>
                <b>IFSC:</b> {{{{ u.get('ifsc', 'N/A') }}}}
            </div>
        </div>

        <div id="upiBox" class="dragon-card fade-in" style="display:none">
            <form action="/update_profile" method="post">
                <input name="upi_id" class="form-control mb-2" placeholder="UPI ID" value="{{{{u.get('upi_id', '')}}}}">
                <button class="btn btn-primary w-100 btn-sm rounded-3">Update UPI</button>
            </form>
        </div>
        
        <div id="bankBox" class="dragon-card fade-in" style="display:none">
            <form action="/update_profile" method="post">
                <input name="bank_name" class="form-control mb-2" placeholder="Bank Name" value="{{{{u.get('bank_name', '')}}}}">
                <input name="bank_acc" class="form-control mb-2" placeholder="Account Number" value="{{{{u.get('bank_acc', '')}}}}">
                <input name="ifsc" class="form-control mb-2" placeholder="IFSC Code" value="{{{{u.get('ifsc', '')}}}}">
                <button class="btn btn-warning w-100 btn-sm rounded-3">Update Bank</button>
            </form>
        </div>

        <a href="/logout" class="btn btn-outline-danger w-100 py-3 rounded-4 mt-4 fw-bold">LOG OUT</a>
    </div>

    <div class="nav-bottom">
        <a href="/home" class="nav-item"><i class="bi bi-house-door-fill fs-4"></i><br>Home</a>
        <a href="/orders" class="nav-item"><i class="bi bi-receipt-cutoff fs-4"></i><br>Orders</a>
        <a href="/profile" class="nav-item active"><i class="bi bi-person-circle fs-4"></i><br>Profile</a>
    </div></div></body></html>""", u=u)


@app.route('/orders')
def orders():
    if 'user' not in session: return redirect('/')
    all_o = fb('GET', 'orders') or {}
    my_o = [v for k,v in all_o.items() if v.get('phone') == session['user']]
    buys = [o for o in my_o if o['type'] == 'Buy'][::-1]
    sells = [o for o in my_o if o['type'] == 'Sell'][::-1]
    
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="app-container p-3">
    <h5 class="fw-bold mb-4">Transaction History</h5>
    <ul class="nav nav-pills nav-justified mb-4" id="pills-tab">
        <li class="nav-item"><button class="nav-link active rounded-pill" data-bs-toggle="pill" data-bs-target="#b-logs">BUY</button></li>
        <li class="nav-item"><button class="nav-link rounded-pill" data-bs-toggle="pill" data-bs-target="#s-logs">SELL</button></li>
    </ul>
    
    <div class="tab-content">
        <div class="tab-pane fade show active" id="b-logs">
            {{% for o in buys %}}
            <div class="dragon-card d-flex justify-content-between align-items-center" onclick='showDet({{{{o|tojson}}}})'>
                <div><div class="fw-bold text-dark">&#8377;{{{{o.amt}}}}</div><small class="text-muted">{{{{o.time}}}}</small></div>
                <span class="badge {{{{ 'bg-success' if o.status=='Completed' else 'bg-danger' if o.status=='Rejected' else 'bg-warning text-dark' }}}}">{{{{o.status}}}}</span>
            </div>
            {{% endfor %}}
        </div>
        <div class="tab-pane fade" id="s-logs">
            {{% for o in sells %}}
            <div class="dragon-card d-flex justify-content-between align-items-center" onclick='showDet({{{{o|tojson}}}})'>
                <div><div class="fw-bold text-dark">&#8377;{{{{o.amt}}}}</div><small class="text-muted">{{{{o.time}}}}</small></div>
                <span class="badge {{{{ 'bg-success' if o.status=='Completed' else 'bg-danger' if o.status=='Rejected' else 'bg-warning text-dark' }}}}">{{{{o.status}}}}</span>
            </div>
            {{% endfor %}}
        </div>
    </div>

    <div id="detModal" class="modal fade" tabindex="-1"><div class="modal-dialog modal-dialog-centered"><div class="modal-content p-3 shadow-lg">
        <div class="modal-body">
            <h5 class="fw-bold mb-4 text-center">Transaction Details</h5>
            <div id="detBody"></div>
            <button class="btn btn-dark w-100 mt-4 rounded-3 py-3" data-bs-dismiss="modal">Close</button>
        </div>
    </div></div></div>

    <script>
        function showDet(o){{
            let html = `
                <div class="detail-row"><span>Order ID</span><span class="fw-bold">${{o.oid}}</span></div>
                <div class="detail-row"><span>Type</span><span class="fw-bold text-uppercase">${{o.type}}</span></div>
                <div class="detail-row"><span>Amount</span><span class="fw-bold text-success">₹${{o.amt}}</span></div>
                <div class="detail-row"><span>Reward</span><span class="fw-bold text-primary">₹${{o.reward || 0}}</span></div>
                <div class="detail-row"><span>Status</span><span class="badge ${{o.status=='Completed'?'bg-success':o.status=='Rejected'?'bg-danger':'bg-warning text-dark'}}">${{o.status}}</span></div>
                <div class="detail-row"><span>Date</span><span class="fw-bold text-muted" style="font-size:12px;">${{o.time}}</span></div>
                <div class="detail-row text-truncate"><span>UTR/Ref</span><span class="fw-bold">${{o.utr || 'N/A'}}</span></div>
            `;

            if(o.status === 'Rejected') {{
                html += `
                <div class="mt-3 p-3 rounded-3" style="background: #fff5f5; border: 1px dashed #dc3545;">
                    <small class="text-danger fw-bold d-block mb-1"><i class="bi bi-exclamation-triangle-fill"></i> REJECTION REASON:</small>
                    <span class="text-dark fw-bold">${{o.reason || 'Verification Failed'}}</span>
                </div>`;
            }}

            document.getElementById('detBody').innerHTML = html;
            new bootstrap.Modal(document.getElementById('detModal')).show();
        }}
    </script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <div class="nav-bottom">
        <a href="/home" class="nav-item"><i class="bi bi-house-door-fill fs-4"></i><br>Home</a>
        <a href="/orders" class="nav-item active"><i class="bi bi-receipt-cutoff fs-4"></i><br>Orders</a>
        <a href="/profile" class="nav-item"><i class="bi bi-person-circle fs-4"></i><br>Profile</a>
    </div></div></body></html>""", buys=buys, sells=sells)
    

@app.route('/update_profile', methods=['POST'])
def update_profile():
    d = {k:v for k,v in request.form.items() if v}
    fb('PATCH', f"users/{session['user']}", d)
    return redirect('/profile')

@app.route('/pay_mode/<amt>')
def pay_mode(amt):
    reward = request.args.get('reward', 0)
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="app-container p-3 text-center">
        <h5 class="fw-bold mb-4">Payment Method</h5>
        <div onclick="location.href='/pay_now/BANK/{amt}?reward={reward}'" class="dragon-card p-4 border shadow-sm">
            <i class="bi bi-bank fs-1 text-primary"></i><br><b>Bank Transfer</b>
        </div>
        <div onclick="location.href='/pay_now/UPI/{amt}?reward={reward}'" class="dragon-card p-4 border shadow-sm mt-3">
            <i class="bi bi-qr-code-scan fs-1 text-success"></i><br><b>UPI Payment</b>
        </div>
    </div></body></html>""")

@app.route('/pay_now/<mode>/<amt>')
def pay_now(mode, amt):
    reward = request.args.get('reward', 0)
    accounts = fb('GET', f'admin/bulk_{mode.lower()}') or {}
    
    details = "N/A"; hname = "N/A"; ifsc = "N/A"; bname = "N/A"; qr_url = ""
    if accounts:
        acc_id = random.choice(list(accounts.keys()))
        acc = accounts[acc_id]
        hname = acc.get('name', 'N/A')
        bname = acc.get('bank_name', 'Bank') if mode == 'BANK' else 'UPI'
        details = acc.get('acc_no', '') if mode == 'BANK' else acc.get('upi_id', '')
        ifsc = acc.get('ifsc', 'N/A')
        qr_url = acc.get('qr_url', '')

    html_content = """
    <html><head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <style>
        body { background-color: #f7f8fa; font-family: sans-serif; margin: 0; padding-bottom: 30px; }
        .header { background: white; padding: 15px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #eee; }
        .amount-card { background: white; margin: 10px; padding: 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.03); }
        .method-bar { background: #6f42c1; color: white; margin: 10px; padding: 12px; border-radius: 10px; text-align: center; font-weight: bold; }
        .info-box { background: white; margin: 10px; border-radius: 12px; overflow: hidden; }
        .info-row { display: flex; justify-content: space-between; padding: 15px; border-bottom: 1px solid #f9f9f9; font-size: 14px; }
        .copy-icon { color: #f39c12; cursor: pointer; margin-left: 10px; }

        /* --- Naya UTR Style --- */
        .input-label { font-weight: bold; font-size: 13px; margin: 15px 10px 5px; display: block; color: #444; }
        .utr-input { 
            width: calc(100% - 20px); margin: 0 10px; padding: 15px; border-radius: 10px; 
            border: 2px solid #ffc107; background: #fff9e6; /* Yellow tint */
            font-size: 16px; font-weight: bold; box-sizing: border-box; outline: none;
        }

        /* --- Naya Upload Button Style --- */
        .upload-btn-box {
            display: inline-flex; align-items: center; justify-content: center;
            background: #ffc107; color: #000; padding: 10px 20px; 
            border-radius: 8px; font-weight: bold; font-size: 14px;
            cursor: pointer; margin: 5px 10px; border: none;
        }
        #file-status { font-size: 12px; color: #28a745; font-weight: bold; display: none; margin-left: 5px; }

        .submit-btn { background: #ffc107; color: #000; border: none; width: calc(100% - 20px); margin: 20px 10px; padding: 16px; border-radius: 12px; font-weight: bold; font-size: 16px; }
        .qr-img { width: 200px; height: 200px; margin: 10px auto; display: block; }
    </style>
    </head>
    <body>
        <div class="header">
            <i class="bi bi-chevron-left" onclick="history.back()"></i>
            <span style="color:#f39c12; font-weight:bold;">DragonPay</span>
            <i class="bi bi-x-lg" onclick="location.href='/home'"></i>
        </div>

        <div class="amount-card">
            <div style="font-size:22px; font-weight:bold;">₹""" + str(amt) + """.00</div>
            <div style="font-size:12px; color:red;">Timer: <span id="timer">14:59</span></div>
        </div>

        <div class="method-bar">""" + mode + """ PAYMENT</div>

        {% if mode == 'UPI' %}
            {% if qr_url %}<img src="{{qr_url}}" class="qr-img">{% endif %}
            <div class="info-box">
                <div class="info-row"><span>UPI ID</span><span><b>""" + details + """</b> <i class="bi bi-copy copy-icon" onclick="copy('""" + details + """')"></i></span></div>
                <div class="info-row"><span>Payee</span><span><b>""" + hname + """</b></span></div>
            </div>
        {% else %}
            <div class="info-box">
                <div class="info-row"><span>Bank</span><span><b>""" + bname + """</b></span></div>
                <div class="info-row"><span>Acc No</span><span><b>""" + details + """</b> <i class="bi bi-copy copy-icon" onclick="copy('""" + details + """')"></i></span></div>
                <div class="info-row"><span>IFSC</span><span><b>""" + ifsc + """</b> <i class="bi bi-copy copy-icon" onclick="copy('""" + ifsc + """')"></i></span></div>
                <div class="info-row"><span>Holder</span><span><b>""" + hname + """</b></span></div>
            </div>
        {% endif %}

        <form id="mainForm" action="/submit_order" method="post">
            <span class="input-label">Enter 12-digit UTR No</span>
            <input name="utr" class="utr-input" placeholder="0000 0000 0000" required maxlength="12" inputmode="numeric">
            
            <span class="input-label">Upload Payment Screenshot</span>
            <div style="display: flex; align-items: center;">
                <div class="upload-btn-box" onclick="document.getElementById('proofImg').click()">
                    <i class="bi bi-camera-fill me-2"></i> Choose File
                </div>
                <span id="file-status">Selected ✅</span>
            </div>
            <input type="file" id="proofImg" style="display:none;" accept="image/*" required onchange="showSelected()">
            
            <input type="hidden" name="proof_url" id="proof_url">
            <input type="hidden" name="amt" value='""" + str(amt) + """'>
            <input type="hidden" name="reward" value='""" + str(reward) + """'>
            <input type="hidden" name="paid_to" value='""" + (details + " (" + bname + ")") + """'>

            <button type="submit" id="submitBtn" class="submit-btn">I HAVE PAID</button>
        </form>

        <script>
            function copy(t) { navigator.clipboard.writeText(t); alert("Copied!"); }
            
            function showSelected() {
                if(document.getElementById('proofImg').files.length > 0) {
                    document.getElementById('file-status').style.display = "inline";
                }
            }

            let timeLeft = 899;
            setInterval(() => {
                let m = Math.floor(timeLeft / 60); let s = timeLeft % 60;
                document.getElementById('timer').innerText = m + ":" + (s < 10 ? '0' : '') + s;
                if(timeLeft > 0) timeLeft--;
            }, 1000);

            document.getElementById('mainForm').onsubmit = async function(e) {
                e.preventDefault();
                const btn = document.getElementById('submitBtn');
                const file = document.getElementById('proofImg').files[0];
                btn.disabled = true; btn.innerHTML = "Submitting...";

                let formData = new FormData();
                formData.append("image", file);
                try {
                    let res = await fetch("https://api.imgbb.com/1/upload?key=b408d8b1ccbb6511571e440c49741180", {
                        method: "POST", body: formData
                    });
                    let data = await res.json();
                    if(data.success) {
                        document.getElementById('proof_url').value = data.data.url;
                        this.submit();
                    } else { alert("Upload Failed!"); btn.disabled = false; }
                } catch(err) { alert("Error!"); btn.disabled = false; }
            };
        </script>
    </body></html>
    """
    return render_template_string(html_content, mode=mode, qr_url=qr_url)



    
    

@app.route('/submit_order', methods=['POST'])
def submit_order():
    if 'user' not in session: return redirect('/')
    
    oid = "DRGN" + str(int(time.time())) # Unique Order ID
    utr = request.form.get('utr')
    amt = request.form.get('amt')
    proof = request.form.get('proof_url')  # ImgBB se aaya hua link
    paid_to = request.form.get('paid_to')  # Bank Name aur A/C Number
    reward = request.form.get('reward', 0)

    # Database mein save karna
    fb('PATCH', f"orders/{oid}", {
        "oid": oid,
        "phone": session['user'],
        "amt": amt,
        "utr": utr,
        "proof": proof,       # Screenshot Link
        "paid_to": paid_to,   # Target Account Details
        "status": "Pending",
        "type": "Buy",
        "reward": reward,
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    return redirect('/orders')
    
# --- PROFESSIONAL ADMIN PANEL ---

@app.route('/admin')
def admin_login_page():
    return render_template_string(f"""
    <html><head>{CSS}</head><body style="background:#121212"><div class="app-container d-flex align-items-center p-4">
        <div class="dragon-card w-100 p-4 shadow-lg text-center">
            <h2 class="fw-bold mb-4 text-danger">ADMIN PANEL  &#128736</h2>
            <form action="/admin/auth" method="post">
                <input type="password" name="pin" placeholder="Enter Admin PIN" class="form-control mb-4 py-3 rounded-3 text-center" required>
                <button class="btn btn-danger w-100 py-3 fw-bold rounded-3">ACCESS PANEL</button>
            </form>
        </div>
    </div></body></html>""")

@app.route('/admin/auth', methods=['POST'])
def admin_auth():
    if request.form.get('pin') == "8888":
        session['admin'] = True
        return redirect('/admin/dashboard')
    return "WRONG PIN! <a href='/admin'>Retry</a>"

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'): return redirect('/admin')
    all_o = fb('GET', 'orders') or {}
    bulk_upi = fb('GET', 'admin/bulk_upi') or {}
    bulk_bank = fb('GET', 'admin/bulk_bank') or {}
    
    # Filter pending orders
    p_buy = [v for k,v in all_o.items() if v.get('status') == 'Pending' and v.get('type') == 'Buy']
    p_sell = [v for k,v in all_o.items() if v.get('status') == 'Pending' and v.get('type') == 'Sell']
    
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="app-container p-3">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h4 class="fw-bold text-danger m-0">Admin Dashboard</h4>
            <a href="/logout" class="btn btn-sm btn-outline-dark">Exit</a>
        </div>
        
        <ul class="nav nav-tabs admin-nav mb-4 border-0 justify-content-between" id="adminTabs" role="tablist">
            <li class="nav-item" role="presentation"><button class="nav-link active" data-bs-toggle="tab" data-bs-target="#tab-buy" type="button">Buy Requests ({{{{p_buy|length}}}})</button></li>
            <li class="nav-item" role="presentation"><button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-sell" type="button">Sell Requests ({{{{p_sell|length}}}})</button></li>
            <li class="nav-item" role="presentation"><button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-gate" type="button">Gateways</button></li>
        </ul>

        <div class="tab-content">
            <div class="tab-pane fade show active" id="tab-buy">
                {{% for o in p_buy %}}
                <div class="dragon-card border-start border-warning border-4 shadow-sm fade-in">
                    <div class="row g-2">
                        <div class="col-7">
                            <span class="badge bg-dark mb-1">ID: {{{{o.oid}}}}</span><br>
                            <small class="text-muted">User: {{{{o.phone.replace(',','.')}}}}</small><br>
                            <b class="text-success fs-5">₹{{{{o.amt}}}}</b> 
                            <small class="text-primary fw-bold">UTR: {{{{o.utr}}}}</small>
                            <div class="mt-2 p-1 bg-light rounded border" style="font-size: 10px;">
                                <b>Paid To:</b> {{{{o.paid_to}}}}
                            </div>
                        </div>
                        <div class="col-5">
                            {{% if o.proof %}}
                            <img src="{{{{o.proof}}}}" class="proof-img-box" onclick="window.open('{{{{o.proof}}}}','_blank')" title="Click to zoom">
                            {{% else %}}
                            <div class="bg-light text-center py-4 rounded small text-danger">No Proof</div>
                            {{% endif %}}
                        </div>
                    </div>
                    <div class="d-flex gap-2 mt-3">
                        <a href="/admin/action/{{{{o.oid}}}}/Completed" class="btn btn-success btn-sm flex-grow-1 fw-bold py-2">APPROVE</a>
                        <button onclick="rejectWithMsg('{{{{o.oid}}}}')" class="btn btn-danger btn-sm flex-grow-1 fw-bold py-2">REJECT</button>
                    </div>
                </div>
                {{% endfor %}}
                {{% if not p_buy %}}<p class="text-center text-muted">No pending Buy orders.</p>{{% endif %}}
            </div>
            
            <div class="tab-pane fade" id="tab-sell">
                {{% for o in p_sell %}}
                <div class="dragon-card border-start border-primary border-4 shadow-sm fade-in">
                    <div class="d-flex justify-content-between">
                        <span><b>Sell Request</b><br><small class="text-muted">{{{{o.phone.replace(',','.')}}}}</small></span>
                        <b class="text-danger fs-5">&#8377;{{{{o.amt}}}}</b>
                    </div>
                    <div class="mt-2 p-2 bg-light rounded small border">
                        <b>Withdrawal Details:</b><br>{{{{o.w_info}}}}
                    </div>
                    <div class="d-flex gap-2 mt-3">
                        <a href="/admin/action/{{{{o.oid}}}}/Completed" class="btn btn-primary btn-sm flex-grow-1 fw-bold">MARK PAID</a>
                        <button onclick="rejectWithMsg('{{{{o.oid}}}}')" class="btn btn-danger btn-sm flex-grow-1 fw-bold py-2">REJECT & REFUND</button>
                    </div>
                </div>
                {{% endfor %}}
                {{% if not p_sell %}}<p class="text-center text-muted">No pending Sell orders.</p>{{% endif %}}
            </div>

            <div class="tab-pane fade" id="tab-gate">
                <div class="dragon-card bg-dark text-white p-3">
                    <h6 class="fw-bold text-warning mb-3">Gateway Manager</h6>
                    <div class="row g-2">
                        <div class="col-6"><button class="btn btn-primary btn-sm w-100" onclick="document.getElementById('upiForm').style.display='block';document.getElementById('bankForm').style.display='none'">+ UPI</button></div>
                        <div class="col-6"><button class="btn btn-warning btn-sm w-100" onclick="document.getElementById('bankForm').style.display='block';document.getElementById('upiForm').style.display='none'">+ Bank</button></div>
                    </div>
<div id="upiForm" style="display:none" class="mt-3 bg-white p-2 rounded text-dark border shadow-sm">
    <form id="qrUploadForm">
        <input id="q_name" class="form-control form-control-sm mb-1" placeholder="Holder Name" required>
        <input id="q_upi" class="form-control form-control-sm mb-1" placeholder="UPI ID" required>
        <label class="small fw-bold text-muted">Select QR Image File:</label>
        <input type="file" id="q_file" class="form-control form-control-sm mb-2" accept="image/*" required>
        <button type="submit" id="q_btn" class="btn btn-success btn-sm w-100 mt-1 fw-bold">UPLOAD & SAVE UPI</button>
    </form>
</div>

<script>
document.getElementById('qrUploadForm').onsubmit = async function(e) {{
    e.preventDefault();
    const btn = document.getElementById('q_btn');
    const file = document.getElementById('q_file').files[0];
    btn.disabled = true; 
    btn.innerHTML = "Uploading to ImgBB...";

    let formData = new FormData();
    formData.append("image", file);

    try {{
        let res = await fetch("https://api.imgbb.com/1/upload?key=b408d8b1ccbb6511571e440c49741180", {{
            method: "POST", body: formData
        }});
        let data = await res.json();
        if(data.success) {{
            let url = data.data.url;
            let name = document.getElementById('q_name').value;
            let upi = document.getElementById('q_upi').value;
            // Redirecting to python route with data
            window.location.href = "/admin/add_upi?name=" + name + "&upi_id=" + upi + "&qr_url=" + encodeURIComponent(url);
        }} else {{ alert("Upload Failed!"); btn.disabled = false; btn.innerHTML = "RETRY"; }}
    }} catch(err) {{ alert("Error!"); btn.disabled = false; }}
}};
</script>


                    <div id="bankForm" style="display:none" class="mt-3 bg-white p-2 rounded text-dark">
                        <form action="/admin/add_bank" method="post">
                            <input name="bank_name" class="form-control form-control-sm mb-1" placeholder="Bank Name" required>
                            <input name="name" class="form-control form-control-sm mb-1" placeholder="Holder Name" required>
                            <input name="acc_no" class="form-control form-control-sm mb-1" placeholder="Account No" required>
                            <input name="ifsc" class="form-control form-control-sm mb-1" placeholder="IFSC" required>
                            <button class="btn btn-success btn-sm w-100 mt-1">Save Bank</button>
                        </form>
                    </div>
                </div>
                
                <h6 class="fw-bold mt-4 small px-2">Active UPIs</h6>
                {{% for k,v in bulk_upi.items() %}}
                <div class="dragon-card d-flex justify-content-between py-2 align-items-center mb-2">
                    <span class="small">{{{{v.upi_id}}}} ({{{{v.name}}}})</span>
                    <a href="/admin/delete_gate/bulk_upi/{{{{k}}}}" class="text-danger px-2"><i class="bi bi-trash"></i></a>
                </div>
                {{% endfor %}}

                <h6 class="fw-bold mt-3 small px-2">Active Banks</h6>
                {{% for k,v in bulk_bank.items() %}}
                <div class="dragon-card d-flex justify-content-between py-2 align-items-center mb-2">
                    <span class="small">{{{{v.acc_no}}}} ({{{{v.name}}}})</span>
                    <a href="/admin/delete_gate/bulk_bank/{{{{k}}}}" class="text-danger px-2"><i class="bi bi-trash"></i></a>
                </div>
                {{% endfor %}}
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    
    <script>
    function rejectWithMsg(oid) {{
        let msg = prompt("Enter Rejection Reason:", "Wrong UTR Number");
        if (msg != null) {{
            window.location.href = "/admin/action/" + oid + "/Rejected?reason=" + encodeURIComponent(msg);
        }}
    }}
    </script>
    
    </body></html>""", p_buy=p_buy, p_sell=p_sell, bulk_upi=bulk_upi, bulk_bank=bulk_bank)



@app.route('/admin/add_upi')
def add_upi():
    if not session.get('admin'): return "Unauthorized"
    id = "UPI" + str(int(time.time()))
    # URL parameters se data capture karna
    data = {
        "name": request.args.get('name'), 
        "upi_id": request.args.get('upi_id'),
        "qr_url": request.args.get('qr_url', '') # ImgBB ka raw link yahan save hoga
    }
    fb('PATCH', f'admin/bulk_upi/{id}', data)
    return redirect('/admin/dashboard')


@app.route('/admin/add_bank', methods=['POST'])
def add_bank():
    if not session.get('admin'): return "Unauthorized"
    id = "BANK" + str(int(time.time()))
    fb('PATCH', f'admin/bulk_bank/{id}', {"bank_name": request.form.get('bank_name'), "name": request.form.get('name'), "acc_no": request.form.get('acc_no'), "ifsc": request.form.get('ifsc')})
    
    return redirect('/admin/dashboard')

@app.route('/admin/delete_gate/<type>/<id>')
def delete_gate(type, id):
    if not session.get('admin'): return "Unauthorized"
    fb('DELETE', f"admin/{type}/{id}")
    return redirect('/admin/dashboard')

@app.route('/admin/action/<oid>/<status>')
def admin_action(oid, status):
    if not session.get('admin'): return "Unauthorized"
    # Naya: Reason capture karne ke liye
    reason = request.args.get('reason', 'Verification Failed')
    
    order = fb('GET', f"orders/{oid}")
    if not order or order['status'] != 'Pending': return "Processed"
    user_id = order['phone']
    user = fb('GET', f"users/{user_id}")
    
    if status == 'Completed' and order['type'] == 'Buy':
        amt = float(order.get('amt', 0))
        rew = float(order.get('reward', 0))
        new_bal = float(user.get('balance', 0)) + amt + rew
        fb('PATCH', f"users/{user_id}", {"balance": new_bal})
    
    if status == 'Rejected' and order['type'] == 'Sell':
        new_bal = float(user.get('balance', 0)) + float(order['amt'])
        fb('PATCH', f"users/{user_id}", {"balance": new_bal})
        
    # Naya: Status ke saath Reason bhi save hoga
    fb('PATCH', f"orders/{oid}", {"status": status, "reason": reason})
    return redirect('/admin/dashboard')


@app.route('/logout')
def logout(): session.clear(); return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
