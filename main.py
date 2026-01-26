import requests, json, time, random
from flask import Flask, render_template_string, request, session, redirect, url_for
import time
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
# --- UI CSS (PREMIUM SCREENSHOT STYLE) ---

# --- FULL PREMIUM UI CSS ---
CSS = """
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
<style>
    :root { --dragon: #ffc107; --bg: #f8f9fa; }
    body { background: white; font-family: 'Segoe UI', Roboto, sans-serif; margin: 0; padding-bottom: 90px; }
    .app-container { max-width: 500px; margin: 0 auto; min-height: 100vh; background: white; position: relative; }
    
    .header-card { padding: 15px 20px; background: white; border-bottom: 1px solid #f1f1f1; }
    
    /* Compact Black Assets */
    .asset-label { color: #888; font-size: 10px; margin-top: 15px; font-weight: 700; text-transform: uppercase; }
    .asset-val { font-size: 20px; font-weight: 800; color: #000; margin-top: -5px; }
    .asset-val span { font-size: 11px; color: #999; }

    .banner-wrapper { margin: 10px; border-radius: 12px; overflow: hidden; height: 160px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .mySlides { display: none; width: 100%; height: 100%; object-fit: cover; }
    
    /* Compact Sliding Activity Bar */
    .activity-container { background: #fffcf0; margin: 0 10px 10px 10px; padding: 4px 0; border-radius: 15px; border: 1px solid #fdf2d0; overflow: hidden; display: flex; align-items: center; }
    .activity-label { background: #000; color: #fff; font-size: 8px; font-weight: 900; padding: 1px 6px; border-radius: 4px; margin-left: 5px; z-index: 2; white-space: nowrap; }
    .marquee-box { display: flex; overflow: hidden; width: 100%; }
    #marquee-content { display: flex; white-space: nowrap; animation: marquee 300s linear infinite; }
    .activity-item { font-size: 10px; color: #555; font-weight: 600; padding-left: 30px; display: flex; align-items: center; gap: 4px; }
    .activity-item b { color: #28a745; }
    
    @keyframes marquee { 0% { transform: translateX(0); } 100% { transform: translateX(-80%); } }

    .action-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; padding: 15px; text-align: center; }
    .grid-item { cursor: pointer; text-decoration: none; color: #444; font-size: 11px; font-weight: 600; }
    .grid-item i { font-size: 26px; color: var(--dragon); display: block; margin-bottom: 5px; }
    
    .trade-box { display: flex; gap: 12px; padding: 0 15px 15px 15px; }
    .t-card { flex: 1; padding: 15px; border-radius: 15px; position: relative; cursor: pointer; border: 1px solid #f0f0f0; }
    .buy-box { background: #fff9e6; color: #d4a017; border-color: #ffecb3; }
    .sell-box { background: #e6f9f0; color: #198754; border-color: #c8e6c9; }
    
    .nav-bottom { position: fixed; bottom: 0; width: 100%; max-width: 500px; background: white; display: flex; border-top: 1px solid #eee; padding: 10px 0; z-index: 1000; }
    .nav-item { flex: 1; text-align: center; color: #ccc; text-decoration: none; font-size: 11px; font-weight: 700; }
    .nav-item.active { color: var(--dragon); }
    .nav-item i { font-size: 22px; display: block; }
</style>
"""

import time, random

# --- UPDATED HOME ROUTE WITH SPIN ICON ---
@app.route('/home')
def home():
    if 'user' not in session: return redirect('/')
    u = fb('GET', f"users/{session['user']}")
    all_o = fb('GET', 'orders') or {}
    pending = [v for k,v in all_o.items() if v.get('phone') == session['user'] and v.get('status') == 'Pending']
    
    return render_template_string(f"""
    <html><head>{CSS}</head><body><div class="app-container">
        <div class="header-card d-flex justify-content-between align-items-center">
            <span class="fw-bold fs-5 text-warning">DragonPay</span>
            <i class="bi bi-gear fs-4" onclick="location.href='/profile'"></i>
        </div>
        
        <div class="px-3">
            <div class="asset-label">Net Balance</div>
            <div class="asset-val">{{{{u.balance}}}}.00 <span>DRB</span></div>
        </div>

        <div class="banner-wrapper">
            <img class="mySlides" src="https://i.ibb.co/hFwrgFCV/1769374734180.png">
            <img class="mySlides" src="https://i.ibb.co/V0HCtWVF/IMG-20260126-024034.png">
        </div>

        <div class="activity-container">
            <div class="activity-label">LIVE</div>
            <div class="marquee-box">
                <div id="marquee-content"></div>
            </div>
        </div>

        <div class="action-grid">
            <div class="grid-item" onclick="location.href='/lucky-spin'"><i class="bi bi-patch-check-fill" style="color:#FF4500;"></i><span>Lucky Spin</span></div>
            <div class="grid-item" onclick="location.href='/rules/buy'"><i class="bi bi-download"></i><span>Buy rules</span></div>
            <div class="grid-item" onclick="location.href='/rules/sell'"><i class="bi bi-upload" style="color:#6495ED;"></i><span>Sell rules</span></div>
            <div class="grid-item" onclick="window.location.href='https://t.me/Shinchain120'"><i class="bi bi-headset" style="color:#0dcaf0;"></i><span>Support</span></div>
        </div>

        <div class="trade-box">
            <div class="t-card buy-box" onclick="location.href='/buy'">
                <b>Buy DRB</b><br><small>Flexible</small>
            </div>
            <div class="t-card sell-box" onclick="location.href='/sell'">
                <b>Sell DRB</b><br><small>Fast</small>
            </div>
        </div>

        <div class="px-3" style="padding-bottom:100px;">
            <div class="fw-bold mb-2 small text-muted">ACTIVE ORDERS</div>
            {{% if pending %}}
                {{% for o in pending %}}
                <div class="p-3 border rounded-3 mb-2 d-flex justify-content-between align-items-center">
                    <div><div class="fw-bold" style="font-size:13px;">DRB {{{{o.type}}}}</div><small class="text-muted">{{{{o.time}}}}</small></div>
                    <div class="text-end"><div class="fw-bold">₹{{{{o.amt}}}}</div><span class="badge bg-warning text-dark" style="font-size:8px;">Processing</span></div>
                </div>
                {{% endfor %}}
            {{% else %}}
                <p class="text-center text-muted small mt-4">No active orders</p>
            {{% endif %}}
        </div>

        <div class="nav-bottom">
            <a href="/home" class="nav-item active"><i class="bi bi-house-door-fill"></i>Home</a>
            <a href="/orders" class="nav-item"><i class="bi bi-receipt"></i>Order</a>
            <a href="/profile" class="nav-item"><i class="bi bi-person-circle"></i>My</a>
        </div>
    </div>
    <script>
        let slideIndex = 0;
        function showSlides() {{
            let slides = document.getElementsByClassName("mySlides");
            for (let i = 0; i < slides.length; i++) slides[i].style.display = "none";
            slideIndex++; if (slideIndex > slides.length) slideIndex = 1;
            slides[slideIndex-1].style.display = "block";
            setTimeout(showSlides, 3000);
        }}
        showSlides();

        const marquee = document.getElementById('marquee-content');
        const prefixes = ["98", "91", "70", "88", "62", "81", "99", "77"];
        const actions = ["bought", "sold", "withdrew", "received bonus"];
        let activityHTML = "";
        for(let i=0; i<100; i++) {{
            let phone = prefixes[Math.floor(Math.random()*prefixes.length)] + "***" + Math.floor(10+Math.random()*90);
            let action = actions[Math.floor(Math.random()*actions.length)];
            let amount = Math.floor(Math.random()*20000) + 500;
            activityHTML += `<div class="activity-item">User ${{phone}} ${{action}} <b>₹${{amount}}</b></div>`;
        }}
        marquee.innerHTML = activityHTML + activityHTML;
    </script>
    </body></html>""", u=u, pending=pending)
# --- RULES ROUTES ---

@app.route('/rules/buy')
def buy_rules():
    if 'user' not in session: return redirect('/')
    return render_template_string(f"""
    <html><head>{CSS}
    <style>
        .rule-card {{ background: #fff9e6; border-left: 5px solid #ffc107; padding: 15px; border-radius: 8px; margin-bottom: 15px; }}
        .rule-title {{ font-weight: 800; color: #d4a017; font-size: 16px; margin-bottom: 5px; }}
        .rule-text {{ font-size: 13px; color: #555; line-height: 1.6; }}
    </style>
    </head>
    <body>
        <div class="app-container">
            <div class="header-card d-flex align-items-center">
                <i class="bi bi-chevron-left fs-4" onclick="location.href='/home'"></i>
                <b class="ms-3">DRB Purchase Rules</b>
            </div>
            
            <div class="p-3">
                <div class="rule-card">
                    <div class="rule-title">1. Minimum Purchase</div>
                    <div class="rule-text">Aap kam se kam 100 DRB kharid sakte hain. Har 1 DRB ki keemat ₹1 hai.</div>
                </div>
                
                <div class="rule-card">
                    <div class="rule-title">2. Payment Method</div>
                    <div class="rule-text">Sirf screen par dikhaye gaye UPI ID par hi payment karein. Har baar naya order lagane se pehle UPI ID check karein.</div>
                </div>

                <div class="rule-card">
                    <div class="rule-title">3. Screenshot Upload</div>
                    <div class="rule-text">Payment karne ke baad UTR number aur payment screenshot upload karna lazmi hai. Galat details par order reject ho jayega.</div>
                </div>

                <div class="rule-card">
                    <div class="rule-title">4. Processing Time</div>
                    <div class="rule-text">Aapka order 5 se 30 minutes ke andar approve kar diya jayega. Raat ke waqt thoda zyada samay lag sakta hai.</div>
                </div>

                <button class="btn btn-warning w-100 fw-bold py-3 mt-3" style="border-radius:12px;" onclick="location.href='/buy'">I UNDERSTAND, BUY NOW</button>
            </div>
        </div>
    </body></html>""")

@app.route('/rules/sell')
def sell_rules():
    if 'user' not in session: return redirect('/')
    return render_template_string(f"""
    <html><head>{CSS}
    <style>
        .rule-card {{ background: #e6f9f0; border-left: 5px solid #198754; padding: 15px; border-radius: 8px; margin-bottom: 15px; }}
        .rule-title {{ font-weight: 800; color: #198754; font-size: 16px; margin-bottom: 5px; }}
        .rule-text {{ font-size: 13px; color: #555; line-height: 1.6; }}
    </style>
    </head>
    <body>
        <div class="app-container">
            <div class="header-card d-flex align-items-center">
                <i class="bi bi-chevron-left fs-4" onclick="location.href='/home'"></i>
                <b class="ms-3">DRB Selling Rules</b>
            </div>
            
            <div class="p-3">
                <div class="rule-card">
                    <div class="rule-title">1. Minimum Withdrawal</div>
                    <div class="rule-text">Aap kam se kam 100 DRB sell karke apne bank ya UPI mein paisa le sakte hain.</div>
                </div>
                
                <div class="rule-card">
                    <div class="rule-title">2. Withdrawal Free </div>
                    <div class="rule-text">Din May Jitna Chahe Itna Buy Sell Kar Kar Earn Kar Sakte.</div>
                </div>

                <div class="rule-card">
                    <div class="rule-title">3. Account Details</div>
                    <div class="rule-text">Apni UPI ID aur Bank details dhyan se bharein. Agar details galat hui toh DragonPay zimmedar nahi hoga.</div>
                </div>

                <div class="rule-card">
                    <div class="rule-title">4. Payout Timing</div>
                    <div class="rule-text">Sell orders 1 se 24 ghante ke andar process kiye jaate hain. Bank holidays par deri ho sakti hai.</div>
                </div>

                <button class="btn btn-success w-100 fw-bold py-3 mt-3" style="border-radius:12px;" onclick="location.href='/sell'">I UNDERSTAND, SELL NOW</button>
            </div>
        </div>
    </body></html>""")
    
@app.route('/lucky-spin')
def lucky_spin():
    if 'user' not in session: return redirect('/')
    return render_template_string(f"""
    <html><head>{CSS}
    <style>
        .spin-page {{ text-align: center; padding: 40px 20px; }}
        .wheel-box {{ position: relative; width: 320px; height: 320px; margin: 30px auto; }}
        
        #wheel {{ 
            width: 100%; height: 100%; border-radius: 50%; border: 10px solid #ffc107;
            background: conic-gradient(
                #ffeb3b 0 45deg, #fffde7 45deg 90deg, 
                #ffeb3b 90deg 135deg, #fffde7 135deg 180deg, 
                #ffeb3b 180deg 225deg, #fffde7 225deg 270deg, 
                #ffeb3b 270deg 315deg, #fffde7 315deg 360deg
            );
            transition: transform 4s cubic-bezier(0.15, 0, 0.15, 1);
            position: relative; overflow: hidden;
            box-shadow: 0 0 25px rgba(255,193,7,0.5);
        }}
        
        /* Wheel Numbers - Slices par set kiye gaye hain */
        .num {{ position: absolute; width: 100%; height: 100%; top: 0; left: 0; font-weight: 900; color: #333; font-size: 22px; }}
        .num span {{ position: absolute; left: 50%; transform: translateX(-50%); top: 25px; }}
        
        /* Har number ko ghumakar slice ke beech mein laya gaya hai */
        .n1 {{ transform: rotate(22.5deg); }} .n2 {{ transform: rotate(67.5deg); }}
        .n3 {{ transform: rotate(112.5deg); }} .n4 {{ transform: rotate(157.5deg); }}
        .n5 {{ transform: rotate(202.5deg); }} .n6 {{ transform: rotate(247.5deg); }}
        .n7 {{ transform: rotate(292.5deg); }} .n8 {{ transform: rotate(337.5deg); }}

        /* Center GO Button - Image ki tarah */
        .wheel-center {{
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 80px; height: 80px; background: radial-gradient(circle, #ff5722, #bf360c);
            border-radius: 50%; border: 5px solid #fff; z-index: 30;
            display: flex; align-items: center; justify-content: center;
            color: white; font-weight: 900; font-size: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4); cursor: pointer;
            text-shadow: 1px 1px 2px #000;
        }}
        .wheel-center:active {{ transform: translate(-50%, -50%) scale(0.95); }}

        .wheel-pointer {{ 
            position: absolute; top: -25px; left: 50%; transform: translateX(-50%); 
            width: 0; height: 0; border-left: 20px solid transparent; 
            border-right: 20px solid transparent; border-top: 45px solid #d32f2f; 
            z-index: 40; filter: drop-shadow(0 3px 5px rgba(0,0,0,0.3));
        }}
        
        #statusMsg {{ min-height: 40px; }}
    </style>
    </head>
    <body style="background:#fff;">
        <div class="app-container">
            <div class="header-card d-flex align-items-center">
                <i class="bi bi-chevron-left fs-4" onclick="location.href='/home'"></i>
                <b class="ms-3">Lucky Event</b>
            </div>
            
            <div class="spin-page">
                <div class="wheel-box">
                    <div class="wheel-pointer"></div>
                    <div id="wheel">
                        <div class="num n1"><span>1</span></div><div class="num n2"><span>10</span></div>
                        <div class="num n3"><span>2</span></div><div class="num n4"><span>5</span></div>
                        <div class="num n5"><span>3</span></div><div class="num n6"><span>8</span></div>
                        <div class="num n7"><span>1</span></div><div class="num n8"><span>4</span></div>
                    </div>
                    <div class="wheel-center" id="spinBtn" onclick="doSpin()">GO</div>
                </div>
                
                <div id="statusMsg" class="mt-4">
                    <h4 class="fw-bold" style="color:#d4a017;">Spin & Win Real DRB!</h4>
                </div>
                <p class="text-muted small">Free chance every 24 hours</p>
            </div>
        </div>

        <script>
            function doSpin() {{
                const btn = document.getElementById('spinBtn');
                const wheel = document.getElementById('wheel');
                const msg = document.getElementById('statusMsg');
                
                // Click disable karo taaki baar-baar ghum na sake
                btn.style.pointerEvents = 'none';
                btn.style.opacity = '0.7';

                fetch('/add_spin_reward').then(r => r.json()).then(data => {{
                    if(data.status === 'success') {{
                        // Random rotation (min 5 rounds)
                        let finalDeg = 1800 + Math.floor(Math.random() * 360);
                        wheel.style.transform = "rotate(" + finalDeg + "deg)";
                        
                        setTimeout(() => {{
                            msg.innerHTML = "<div class='alert alert-success fw-bold animate__animated animate__bounceIn'>🔥 You Won " + data.prize + " DRB! 🔥</div>";
                            // 24 ghante baad hi button wapas aayega (backend handle kar raha hai)
                        }}, 4000);
                    }} else {{
                        alert(data.msg);
                        btn.style.pointerEvents = 'auto';
                        btn.style.opacity = '1';
                    }}
                }});
            }}
        </script>
    </body></html>""")



# --- PYTHON SPIN LOGIC (THE BRAIN) ---
@app.route('/add_spin_reward')
def add_spin_reward():
    if 'user' not in session: return {"status": "error"}
    email = session['user']
    u = fb('GET', f"users/{email}")
    
    now = int(time.time())
    last = u.get('last_spin', 0)
    
    if (now - last) < 86400:
        rem = (86400 - (now - last)) // 3600
        return {"status": "wait", "msg": f"Wait {rem} hours for next spin!"}
    
    prize = random.randint(1, 10)
    new_bal = float(u.get('balance', 0)) + prize
    fb('PATCH', f"users/{email}", {"balance": new_bal, "last_spin": now})
    return {"status": "success", "prize": prize}


@app.route('/buy')
def buy():
    # Iske andar humne seedha CSS likh di hai, ab ye upar wali CSS se alag chalega
    return render_template_string(f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        <style>
            :root {{ --dragon: #ffc107; }}
            body {{ background: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding-bottom: 80px; }}
            .app-container {{ max-width: 500px; margin: 0 auto; min-height: 100vh; background: white; position: relative; }}
            
            /* Marketplace UI */
            .brand-title {{ font-size: 18px; font-weight: 800; }}
            .text-black {{ color: #222; }}
            .text-yellow {{ color: var(--dragon); }}

            .market-card {{ display: flex; align-items: center; justify-content: space-between; padding: 12px 15px; border-bottom: 1px solid #f2f2f2; }}
            .coin-circle {{ width: 38px; height: 38px; background: #f8f9fa; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 900; color: #b58d1d; font-size: 16px; border: 1px solid #eee; }}
            .amt-text {{ font-size: 17px; font-weight: 800; color: #222; margin: 0; }}
            .bank-badge {{ background: #0d6efd; color: white; font-size: 8px; padding: 1px 4px; border-radius: 3px; margin-left: 5px; vertical-align: middle; font-weight: 800; }}
            .reward-row {{ background: #fff5eb; color: #fd7e14; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px; display: inline-flex; align-items: center; gap: 4px; margin-top: 3px; }}
            .limit-tag {{ color: #aaa; font-size: 10px; font-weight: 500; margin-left: 5px; }}
            .btn-buy-yellow {{ background: var(--dragon); border: none; color: #222; padding: 6px 22px; border-radius: 20px; font-weight: 800; font-size: 12px; }}
            
            .pay-icons {{ display: flex; gap: 4px; margin-top: 5px; }}
            .pay-icons img {{ width: 14px; height: 14px; }}

            .filter-container {{ display: flex; background: #f1f1f1; border-radius: 25px; padding: 4px; margin: 10px 15px; }}
            .filter-btn {{ flex: 1; border: none; background: none; padding: 7px; font-size: 13px; font-weight: 700; color: #666; border-radius: 20px; }}
            .filter-btn.active {{ background: #0d6efd; color: white; }}

            .nav-bottom {{ position: fixed; bottom: 0; width: 100%; max-width: 500px; background: white; display: flex; border-top: 1px solid #eee; padding: 10px 0; }}
            .nav-item {{ flex: 1; text-align: center; color: #ccc; text-decoration: none; font-size: 11px; font-weight: 700; }}
            .nav-item.active {{ color: var(--dragon); }}
            .nav-item i {{ font-size: 22px; display: block; }}
        </style>
    </head>
    <body>
    <div class="app-container">
        <div class="p-3 d-flex align-items-center justify-content-between border-bottom">
            <div class="d-flex align-items-center">
                <i class="bi bi-chevron-left fs-5 me-3" onclick="location.href='/home'"></i>
                <div class="brand-title"><span class="text-black">DragonPay</span> <span class="text-yellow">Exchanger</span></div>
            </div>
            <i class="bi bi-arrow-clockwise fs-5 text-muted" onclick="generateData()"></i>
        </div>

        <div class="filter-container">
            <button class="filter-btn active" id="btn-small" onclick="switchCat('small')">Small Amount</button>
            <button class="filter-btn" id="btn-big" onclick="switchCat('big')">Big Amount</button>
        </div>
        
        <div id="market-list" class="px-1"></div>

        <div class="nav-bottom">
            <a href="/home" class="nav-item"><i class="bi bi-house-door"></i>Home</a>
            <a href="/orders" class="nav-item"><i class="bi bi-receipt"></i>Order</a>
            <a href="/profile" class="nav-item"><i class="bi bi-person-circle"></i>My</a>
        </div>

        <script>
            let currentCat = 'small';
            let marketData = [];

            function generateData() {{
                marketData = [];
                for(let i=0; i<10; i++){{
                    let isSmall = i < 5;
                    let amt = isSmall ? (Math.floor(Math.random()*19 + 1) * 100) : (Math.floor(Math.random()*480 + 20) * 100);
                    marketData.push({{ 
                        amt: amt, 
                        rew: (amt * (isSmall ? 0.05 : 0.03)).toFixed(0), 
                        cat: isSmall ? 'small' : 'big' 
                    }});
                }}
                renderList();
            }}

            function switchCat(cat) {{
                currentCat = cat;
                document.getElementById('btn-small').classList.toggle('active', cat === 'small');
                document.getElementById('btn-big').classList.toggle('active', cat === 'big');
                renderList();
            }}

            function renderList() {{
                const listDiv = document.getElementById('market-list');
                let html = '';
                marketData.filter(i => i.cat === currentCat).forEach(i => {{
                    html += `
                    <div class="market-card">
                        <div class="d-flex align-items-center">
                            <div class="coin-circle">A</div>
                            <div class="ms-1">
                                <p class="amt-text">₹${{i.amt}} <span class="bank-badge">BANK</span></p>
                                <div class="reward-row">
                                    <i class="bi bi-gift-fill"></i> Reward +₹${{i.rew}}
                                    <span class="limit-tag">Limit ${{i.amt}}-${{i.amt}}</span>
                                </div>
                                <div class="pay-icons">
                                    <img src="https://img.icons8.com/color/48/phone-pe.png">
                                    <img src="https://img.icons8.com/color/48/paytm.png">
                                    <img src="https://img.icons8.com/color/48/google-pay-india.png">
      
                                </div>
                            </div>
                        </div>
                        <button class="btn-buy-yellow" onclick="location.href='/pay_mode/${{i.amt}}?reward=${{i.rew}}'">Buy</button>
                    </div>`;
                }});
                listDiv.innerHTML = html;
            }}
            generateData();
            setInterval(generateData, 7000);
        </script>
    </div>
    </body>
    </html>""")






# ... [Baki routes same rahenge] ...


# --- ROUTES ---

# --- LOGIN & AUTH SECTION (FULLY UPDATED) ---

# --- UPDATED LOGIN & AUTH SECTION ---

@app.route('/')
def login():
    if 'user' in session: return redirect('/home')
    
    # Ultra Clean & Balanced Layout CSS
    CLEAN_CSS = """
    <style>
        :root { --dragon-yellow: #ffc107; --bg-gray: #f8f9fa; --text-dark: #212529; }
        body { background: #ffffff; font-family: 'Inter', -apple-system, sans-serif; margin: 0; display: flex; justify-content: center; color: var(--text-dark); }
        .app-container { width: 100%; max-width: 420px; min-height: 100vh; padding: 50px 25px; box-sizing: border-box; }
        
        /* Branding */
        .brand-header { font-size: 28px; font-weight: 800; margin-bottom: 35px; letter-spacing: -0.5px; }
        .text-black { color: #000; }
        .text-yellow { color: var(--dragon-yellow); }
        .sub-title { font-size: 22px; font-weight: 700; margin-bottom: 30px; }
        
        /* Inputs */
        .form-group { margin-bottom: 18px; position: relative; }
        .input-label { font-size: 13px; font-weight: 600; color: #666; margin-bottom: 6px; display: block; }
        .input-box { 
            background: #f4f6f8; border: 1.5px solid transparent; border-radius: 10px; 
            padding: 12px 15px; width: 100%; font-size: 14px; outline: none; 
            box-sizing: border-box; transition: all 0.2s;
        }
        .input-box:focus { border-color: var(--dragon-yellow); background: #fff; }

        /* Small & Balanced Buttons */
        .btn-stack { display: flex; flex-direction: column; gap: 12px; margin-top: 10px; }
        .btn-base { 
            border: none; border-radius: 10px; padding: 12px; font-weight: 700; 
            font-size: 15px; cursor: pointer; width: 100%; transition: opacity 0.2s;
        }
        .btn-black { background: #000; color: #fff; }
        .btn-yellow { background: var(--dragon-yellow); color: #000; }
        .btn-gray { background: #f0f0f0; color: #555; text-decoration: none; text-align: center; font-size: 14px; padding: 10px; }
        .btn-base:active { opacity: 0.8; }

        /* Forgot Password Link */
        .forgot-link { 
            float: right; color: var(--dragon-yellow); text-decoration: none; 
            font-size: 12px; font-weight: 600; cursor: pointer; margin-top: -2px;
        }
        
        .footer-text { text-align: center; margin-top: 25px; font-size: 13px; color: #888; }
        .reg-link { color: var(--dragon-yellow); text-decoration: none; font-weight: 700; }
        
        /* Popup Notification */
        #popup { 
            display: none; position: fixed; top: 25px; left: 50%; transform: translateX(-50%);
            background: #222; color: white; padding: 12px 20px; border-radius: 8px;
            font-size: 13px; z-index: 1000; text-align: center; width: 80%; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        }
    </style>
    """

    return render_template_string(f"""
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1.0">{CLEAN_CSS}</head>
    <body>
        <div id="popup"></div>
        <div class="app-container">
            <div class="brand-header"><span class="text-black">Dragon</span><span class="text-yellow">Pay</span></div>
            <div class="sub-title">Account Login</div>

            <form action="/auth" method="post">
                <div class="form-group">
                    <label class="input-label">Email Address</label>
                    <input type="email" name="email" id="userEmail" class="input-box" placeholder="example@gmail.com" required>
                </div>

                <div class="form-group">
                    <label class="input-label">Password</label>
                    <span class="forgot-link" onclick="handleForgot()">Forgot Password?</span>
                    <input type="password" name="pw" class="input-box" placeholder="Enter password" required>
                </div>

                <input type="hidden" name="ref_by" id="ref_input">

                <div class="btn-stack">
                    <button name="act" value="reg" class="btn-base btn-black">SIGN UP</button>
                    <button name="act" value="login" class="btn-base btn-yellow">Log In</button>
                    <a href="https://t.me/Shinchain120" class="btn-base btn-gray">Help Center</a>
                </div>
            </form>

            <div class="footer-text">
                Don't have an account? <a href="#" onclick="document.getElementById('userEmail').focus()" class="reg-link">Register Now</a>
            </div>
        </div>

        <script>
            function showPop(msg) {{
                let p = document.getElementById('popup');
                p.innerText = msg;
                p.style.display = 'block';
                setTimeout(() => p.style.display = 'none', 4000);
            }}

            function handleForgot() {{
                let email = document.getElementById('userEmail').value;
                if(!email) {{ alert("Please enter your email first."); return; }}
                
                fetch('/reset_password?email=' + email)
                .then(r => r.json())
                .then(data => {{
                    if(data.status === 'sent') {{
                        showPop("Check your spam folder. Reset link sent!");
                    }} else {{
                        showPop("Email not found. Please Sign Up first.");
                    }}
                }});
            }}
        </script>
    </body>
    </html>""")

@app.route('/reset_password')
def reset_password():
    email = request.args.get('email', '').replace('.', ',').lower()
    user = fb('GET', f"users/{email}")
    if user:
        # User mil gaya
        return {"status": "sent"}
    else:
        # User nahi mila
        return {"status": "not_found"}

@app.route('/auth', methods=['POST'])
def auth():
    email = request.form.get('email').replace('.', ',').lower()
    pw = request.form.get('pw')
    act = request.form.get('act')
    
    u = fb('GET', f"users/{email}")
    
    if act == 'reg':
        if u: return "Email already exists! <a href='/'>Back</a>"
        u = {
            "email": email, "password": pw, "balance": 0.0, 
            "uuid": "DP"+str(random.randint(1000,9999)),
            "ref_code": email[:4].upper()+str(random.randint(10,99)),
            "bank_acc":"", "upi_id":"", "bank_name":"", "ifsc":""
        }
        fb('PATCH', f"users/{email}", u)
    elif not u or u['password'] != pw:
        return "Invalid credentials! <a href='/'>Back</a>"
    
    session['user'] = email
    return redirect('/home')




@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if 'user' not in session: return redirect('/')
    u = fb('GET', f"users/{session['user']}")
    
    if request.method == 'POST':
        try:
            amt = int(request.form.get('amt', 0))
        except:
            amt = 0
            
        if amt > u.get('balance', 0): 
            return "<script>alert('Insufficient Balance!');window.location='/sell';</script>"
        if amt < 100 or amt % 100 != 0: 
            return "<script>alert('Enter amount in multiples of 100!');window.location='/sell';</script>"
        if not u.get('bank_acc') and not u.get('upi_id'): 
            return "<script>alert('Please add bank card first!');window.location='/profile';</script>"
        
        w_info = f"UPI: {u.get('upi_id')} | Bank: {u.get('bank_name')} | Acc: {u.get('bank_acc')} | IFSC: {u.get('ifsc')}"
        oid = "SELL" + str(int(time.time()))
        
        fb('PATCH', f"orders/{oid}", {
            "oid": oid, "phone": session['user'], "amt": amt, 
            "status": "Pending", "type": "Sell", 
            "time": time.strftime("%Y-%m-%d %H:%M"), 
            "utr": "Withdrawal", "w_info": w_info
        })
        fb('PATCH', f"users/{session['user']}", {"balance": u['balance'] - amt})
        return redirect('/orders')

    # CSS specifically designed for this premium look
    PAGE_CSS = """
    <style>
        :root { --dragon: #ffc107; --sell-green: #198754; }
        body { background: #fdfdfd; font-family: 'Segoe UI', sans-serif; margin: 0; }
        .app-container { max-width: 500px; margin: 0 auto; min-height: 100vh; background: white; padding-bottom: 80px; }
        
        /* Header */
        .top-nav { padding: 15px; display: flex; align-items: center; border-bottom: 1px solid #eee; background: white; }
        .top-nav h5 { margin: 0; font-weight: 800; font-size: 18px; margin-left: 15px; }
        
        /* Balance Card */
        .dragon-card { 
            background: linear-gradient(135deg, #198754 0%, #115c39 100%); 
            border-radius: 20px; padding: 25px; margin: 20px 15px; color: white;
            box-shadow: 0 10px 20px rgba(25, 135, 84, 0.2);
            position: relative; overflow: hidden;
        }
        .dragon-card::after {
            content: ''; position: absolute; right: -20px; top: -20px; 
            width: 100px; height: 100px; background: rgba(255,255,255,0.1); border-radius: 50%;
        }

        /* Form Controls */
        .form-group { padding: 0 15px; margin-top: 25px; }
        .form-label { font-size: 13px; font-weight: 700; color: #666; margin-bottom: 8px; display: block; }
        .input-wrapper { position: relative; }
        .input-wrapper span { position: absolute; left: 15px; top: 50%; transform: translateY(-50%); font-weight: 800; font-size: 18px; color: #222; }
        .form-control { 
            width: 100%; border: 2px solid #f0f0f0; border-radius: 15px; padding: 15px 15px 15px 40px;
            font-size: 18px; font-weight: 800; transition: 0.3s; color: #222;
        }
        .form-control:focus { border-color: var(--sell-green); outline: none; background: #f9fffb; }

        /* Button */
        .btn-main { 
            width: calc(100% - 30px); margin: 30px 15px; background: var(--dragon); border: none; 
            padding: 16px; border-radius: 15px; font-weight: 800; font-size: 16px;
            color: #222; box-shadow: 0 5px 15px rgba(255, 193, 7, 0.3); transition: 0.2s;
        }
        .btn-main:active { transform: scale(0.97); }

        /* Info Box */
        .info-box { margin: 0 15px; padding: 15px; background: #f8f9fa; border-radius: 12px; border-left: 4px solid var(--sell-green); }
        .info-box p { margin: 0; font-size: 12px; color: #666; line-height: 1.6; }
        
        /* Nav Fix */
        .nav-bottom { position: fixed; bottom: 0; width: 100%; max-width: 500px; background: white; display: flex; border-top: 1px solid #eee; padding: 10px 0; }
        .nav-item { flex: 1; text-align: center; color: #ccc; text-decoration: none; font-size: 11px; font-weight: 700; }
        .nav-item.active { color: var(--dragon); }
        .nav-item i { font-size: 22px; display: block; }
    </style>
    """

    return render_template_string(f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        {PAGE_CSS}
    </head>
    <body>
        <div class="app-container">
            <div class="top-nav">
                <i class="bi bi-chevron-left fs-4" onclick="location.href='/home'"></i>
                <h5>Sell Coins</h5>
            </div>

            <div class="dragon-card">
                <small class="opacity-75 fw-bold">Current Balance</small>
                <h1 class="fw-bold m-0 mt-1">₹{{{{u.balance}}}}.00</h1>
            </div>

            <form method="post">
                <div class="form-group">
                    <label class="form-label">Withdraw Amount (Multiples of 100)</label>
                    <div class="input-wrapper">
                        <span>₹</span>
                        <input name="amt" type="number" class="form-control" placeholder="0.00" required>
                    </div>
                </div>
                <button type="submit" class="btn-main">WITHDRAW NOW</button>
            </form>

            <div class="info-box">
                <p><b><i class="bi bi-shield-lock-fill"></i> Safety Note:</b><br>
                Please ensure your bank details/UPI ID is correct in your profile. 
                Withdrawals are usually processed within 15-30 minutes.</p>
            </div>

            <div class="nav-bottom">
                <a href="/home" class="nav-item"><i class="bi bi-house-door"></i>Home</a>
                <a href="/orders" class="nav-item"><i class="bi bi-receipt"></i>Order</a>
                <a href="/profile" class="nav-item"><i class="bi bi-person-circle"></i>My</a>
            </div>
        </div>
    </body>
    </html>""", u=u)


@app.route('/profile')
def profile():
    if 'user' not in session: return redirect('/')
    u = fb('GET', f"users/{session['user']}")
    if not u:
        session.clear()
        return redirect('/')

    # Fixed: Calculate time here and pass it to the template
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    # --- LUXURY GOLDEN PROFILE CSS ---
    PROFILE_CSS = """
    <style>
        :root { --premium-gold: #c5a059; --bg: #f5f6f8; --dark-text: #2c3e50; }
        body { background: var(--bg); font-family: 'Segoe UI', Roboto, sans-serif; margin: 0; }
        .app-container { max-width: 500px; margin: 0 auto; min-height: 100vh; background: var(--bg); padding-bottom: 100px; }
        
        .header-bg { 
            background: #b68d60; 
            padding: 30px 20px 60px 20px;
            display: flex; align-items: center;
            color: white;
        }
        .profile-img { 
            width: 80px; height: 80px; 
            border-radius: 50%; object-fit: cover;
            border: 3px solid rgba(255,255,255,0.3);
            margin-right: 15px;
        }
        .user-info h4 { margin: 0; font-weight: 700; font-size: 22px; text-transform: uppercase; }
        .vip-badge { 
            background: linear-gradient(90deg, #f3d498, #c5a059);
            color: white; font-size: 10px; font-weight: 800;
            padding: 2px 8px; border-radius: 12px; margin-left: 5px;
            vertical-align: middle;
        }
        .uid-tag { 
            background: rgba(255,255,255,0.2); font-size: 12px; 
            padding: 2px 10px; border-radius: 20px; margin-top: 8px; display: inline-block;
        }
        .balance-section { 
            margin: -40px 15px 20px 15px; 
            background: white; border-radius: 15px; padding: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        }
        .total-label { color: #95a5a6; font-size: 13px; font-weight: 600; }
        .balance-amt { font-size: 28px; font-weight: 800; color: #2c3e50; display: block; margin-top: 5px; }
        .action-card {
            background: white; margin: 0 15px 12px 15px; 
            border-radius: 12px; padding: 15px;
            display: flex; align-items: center; text-decoration: none; color: var(--dark-text);
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }
        .icon-box {
            width: 40px; height: 40px; border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 20px; margin-right: 15px;
        }
        .edit-box {
            display: none; background: #fff; margin-top: 10px;
            padding: 15px; border-radius: 10px; border: 1px dashed #ddd;
        }
        .form-control { border-radius: 10px; padding: 10px; margin-bottom: 10px; border: 1px solid #eee; }
        .save-btn { background: #b68d60; color: white; border: none; width: 100%; padding: 10px; border-radius: 10px; font-weight: 700; }
        .logout-link { color: #e74c3c; text-align: center; display: block; margin-top: 30px; font-weight: 700; text-decoration: none; }
        .nav-bottom { position: fixed; bottom: 0; width: 100%; max-width: 500px; background: white; display: flex; border-top: 1px solid #eee; padding: 12px 0; }
        .nav-item { flex: 1; text-align: center; color: #bdc3c7; text-decoration: none; font-size: 11px; font-weight: 700; }
        .nav-item.active { color: #b68d60; }
        .nav-item i { font-size: 22px; display: block; }
    </style>
    """

    return render_template_string(f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        {PROFILE_CSS}
    </head>
    <body>
        <div class="app-container">
            <div class="header-bg">
                <img src="https://i.pravatar.cc/150?u={{{{u.get('uuid', '123')}}}}" class="profile-img">
                <div class="user-info">
                    <h4>{{{{u.get('email', 'User').split('@')[0]}}}} <span class="vip-badge">VIP2</span></h4>
                    <div class="uid-tag">UID | {{{{u.get('uuid', '1859308')}}}} <i class="bi bi-copy ms-1"></i></div>
                    <div style="font-size: 10px; margin-top: 5px; opacity: 0.8;">Last login: {{{{current_time}}}}</div>
                </div>
            </div>

            <div class="balance-section">
                <span class="total-label">Total balance</span>
                <span class="balance-amt">₹{{{{u.get('balance', 0)}}}}.00 <i class="bi bi-arrow-repeat ms-2 fs-5 opacity-50"></i></span>
            </div>

            <a href="https://t.me/DragonpayEc" class="action-card">
                <div class="icon-box" style="background: #e3f2fd; color: #1976d2;"><i class="bi bi-telegram"></i></div>
                <div style="flex:1"><b>Telegram Join Chanel</b><br><small class="text-muted">Click to join help center</small></div>
                <i class="bi bi-chevron-right text-muted"></i>
            </a>

            <div class="px-3 mb-2 small fw-bold text-muted text-uppercase">Withdrawal Settings</div>
            
            <div class="action-card d-block">
                <div class="d-flex align-items-center" onclick="document.getElementById('upiBox').style.display='block'">
                    <div class="icon-box" style="background: #f0fdf4; color: #16a34a;"><i class="bi bi-qr-code-scan"></i></div>
                    <div style="flex:1"><b>UPI Address</b><br><small class="text-muted">{{{{u.get('upi_id', 'Not Linked')}}}}</small></div>
                    <i class="bi bi-pencil-square text-muted"></i>
                </div>
                <div id="upiBox" class="edit-box">
                    <form action="/update_profile" method="post">
                        <input name="upi_id" class="form-control" placeholder="example@upi" value="{{{{u.get('upi_id', '')}}}}">
                        <button class="save-btn">Update UPI</button>
                    </form>
                </div>
            </div>

            <div class="action-card d-block">
                <div class="d-flex align-items-center" onclick="document.getElementById('bankBox').style.display='block'">
                    <div class="icon-box" style="background: #fff7ed; color: #ea580c;"><i class="bi bi-bank"></i></div>
                    <div style="flex:1"><b>Bank Account</b><br><small class="text-muted">{{{{u.get('bank_acc', 'Not Linked')}}}}</small></div>
                    <i class="bi bi-pencil-square text-muted"></i>
                </div>
                <div id="bankBox" class="edit-box">
                    <form action="/update_profile" method="post">
                        <input name="bank_name" class="form-control" placeholder="Bank Name">
                        <input name="bank_acc" class="form-control" placeholder="Account Number">
                        <input name="ifsc" class="form-control" placeholder="IFSC Code">
                        <button class="save-btn">Update Bank</button>
                    </form>
                </div>
            </div>

            <a href="/logout" class="logout-link"><i class="bi bi-power"></i> Log Out Account</a>

            <div class="nav-bottom">
                <a href="/home" class="nav-item"><i class="bi bi-house-door"></i>Home</a>
                <a href="/orders" class="nav-item"><i class="bi bi-receipt"></i>Orders</a>
                <a href="/profile" class="nav-item active"><i class="bi bi-person-circle"></i>My</a>
            </div>
        </div>
    </body>
    </html>""", u=u, current_time=current_time)



@app.route('/orders')
def orders():
    if 'user' not in session: return redirect('/')
    all_o = fb('GET', 'orders') or {}
    my_o = [v for k,v in all_o.items() if v.get('phone') == session['user']]
    buys = [o for o in my_o if o['type'] == 'Buy'][::-1]
    sells = [o for o in my_o if o['type'] == 'Sell'][::-1]
    
    # --- MODERN ORDERS CSS ---
    ORDERS_CSS = """
    <style>
        :root { --dragon: #ffc107; --bg: #f8f9fa; }
        body { background: var(--bg); font-family: 'Segoe UI', Roboto, sans-serif; margin: 0; }
        .app-container { max-width: 500px; margin: 0 auto; min-height: 100vh; background: var(--bg); padding-bottom: 80px; }
        
        /* Header & Tabs */
        .history-header { background: white; padding: 20px 15px; border-bottom: 1px solid #eee; position: sticky; top: 0; z-index: 100; }
        .nav-pills .nav-link { color: #666; font-weight: 700; font-size: 14px; border: 1px solid transparent; }
        .nav-pills .nav-link.active { background: #0d6efd !important; color: white !important; }

        /* Small Modern Cards */
        .order-card { 
            background: white; border-radius: 12px; padding: 12px 15px; 
            margin-bottom: 10px; border: 1px solid #f0f0f0; transition: 0.2s;
        }
        .order-card:active { transform: scale(0.98); background: #fdfdfd; }
        .amt-text { font-size: 16px; font-weight: 800; color: #222; }
        .time-text { font-size: 11px; color: #999; }
        
        /* Modal Receipt Style */
        .modal-content { border-radius: 20px; border: none; overflow: hidden; }
        .receipt-body { padding: 25px 20px; }
        .detail-row { 
            display: flex; justify-content: space-between; 
            padding: 8px 0; border-bottom: 1px dashed #f0f0f0; 
            font-size: 14px;
        }
        .detail-row:last-child { border-bottom: none; }
        .detail-label { color: #7f8c8d; font-weight: 500; }
        .detail-value { color: #2c3e50; font-weight: 700; text-align: right; }
        
        .rejection-box {
            background: #fff5f5; border: 1.5px dashed #ff8282;
            border-radius: 12px; padding: 15px; margin-top: 15px;
        }

        /* Status Badges */
        .badge-sm { padding: 4px 10px; border-radius: 8px; font-size: 10px; font-weight: 800; text-transform: uppercase; }
        .st-Completed { background: #e6fcf5; color: #0ca678; }
        .st-Rejected { background: #fff5f5; color: #fa5252; }
        .st-Pending { background: #fff9db; color: #f08c00; }

        /* Bottom Nav */
        .nav-bottom { position: fixed; bottom: 0; width: 100%; max-width: 500px; background: white; display: flex; border-top: 1px solid #eee; padding: 10px 0; }
        .nav-item { flex: 1; text-align: center; color: #ccc; text-decoration: none; font-size: 11px; font-weight: 700; }
        .nav-item.active { color: var(--dragon); }
        .nav-item i { font-size: 22px; display: block; }
    </style>
    """

    return render_template_string(f"""
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
        {ORDERS_CSS}
    </head>
    <body>
        <div class="app-container">
            <div class="history-header">
                <h5 class="fw-bold mb-3"><i class="bi bi-chevron-left me-2" onclick="history.back()"></i> Transaction History</h5>
                <ul class="nav nav-pills nav-justified bg-light p-1 rounded-pill">
                    <li class="nav-item"><button class="nav-link active rounded-pill" data-bs-toggle="pill" data-bs-target="#b-logs">BUY</button></li>
                    <li class="nav-item"><button class="nav-link rounded-pill" data-bs-toggle="pill" data-bs-target="#s-logs">SELL</button></li>
                </ul>
            </div>

            <div class="tab-content p-3">
                <div class="tab-pane fade show active" id="b-logs">
                    {{% for o in buys %}}
                    <div class="order-card d-flex justify-content-between align-items-center" onclick='showDet({{{{o|tojson}}}})'>
                        <div>
                            <div class="amt-text text-success">+ ₹{{{{o.amt}}}}</div>
                            <div class="time-text">{{{{o.time}}}}</div>
                        </div>
                        <span class="badge-sm st-{{{{o.status}}}}">{{{{o.status}}}}</span>
                    </div>
                    {{% endfor %}}
                </div>
                
                <div class="tab-pane fade" id="s-logs">
                    {{% for o in sells %}}
                    <div class="order-card d-flex justify-content-between align-items-center" onclick='showDet({{{{o|tojson}}}})'>
                        <div>
                            <div class="amt-text text-danger">- ₹{{{{o.amt}}}}</div>
                            <div class="time-text">{{{{o.time}}}}</div>
                        </div>
                        <span class="badge-sm st-{{{{o.status}}}}">{{{{o.status}}}}</span>
                    </div>
                    {{% endfor %}}
                </div>
            </div>

            <div id="detModal" class="modal fade" tabindex="-1">
                <div class="modal-dialog modal-dialog-centered px-4">
                    <div class="modal-content shadow-lg">
                        <div class="receipt-body">
                            <h5 class="fw-bold text-center mb-4">Transaction Details</h5>
                            <div id="detBody"></div>
                            <button class="btn btn-dark w-100 mt-4 rounded-3 py-3 fw-bold" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="nav-bottom">
                <a href="/home" class="nav-item"><i class="bi bi-house-door"></i>Home</a>
                <a href="/orders" class="nav-item active"><i class="bi bi-receipt"></i>Order</a>
                <a href="/profile" class="nav-item"><i class="bi bi-person-circle"></i>My</a>
            </div>
        </div>

        <script>
            function showDet(o){{
                let statusClass = 'st-' + o.status;
                let html = `
                    <div class="detail-row"><span class="detail-label">Order ID</span><span class="detail-value">${{o.oid}}</span></div>
                    <div class="detail-row"><span class="detail-label">Type</span><span class="detail-value text-uppercase">${{o.type}}</span></div>
                    <div class="detail-row"><span class="detail-label">Amount</span><span class="detail-value text-success" style="font-size:18px">₹${{o.amt}}</span></div>
                    <div class="detail-row"><span class="detail-label">Reward</span><span class="detail-value text-primary">₹${{o.reward || 0}}</span></div>
                    <div class="detail-row"><span class="detail-label">Status</span><span class="badge-sm ${{statusClass}}">${{o.status}}</span></div>
                    <div class="detail-row"><span class="detail-label">Date</span><span class="detail-value" style="font-size:12px;">${{o.time}}</span></div>
                    <div class="detail-row"><span class="detail-label">UTR/Ref</span><span class="detail-value text-truncate" style="max-width:140px;">${{o.utr || 'N/A'}}</span></div>
                `;

                if(o.status === 'Rejected') {{
                    html += `
                    <div class="rejection-box">
                        <small class="text-danger fw-bold d-block mb-1"><i class="bi bi-exclamation-triangle-fill"></i> REJECTION REASON:</small>
                        <span class="text-dark fw-bold" style="font-size:15px;">${{o.reason || 'Verification Failed'}}</span>
                    </div>`;
                }}

                document.getElementById('detBody').innerHTML = html;
                new bootstrap.Modal(document.getElementById('detModal')).show();
            }}
        </script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>""", buys=buys, sells=sells)


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

# --- FULL UPDATED ADMIN DASHBOARD WITH FIXED IMAGE CSS ---

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'): return redirect('/admin')
    all_o = fb('GET', 'orders') or {}
    bulk_upi = fb('GET', 'admin/bulk_upi') or {}
    bulk_bank = fb('GET', 'admin/bulk_bank') or {}
    
    # Filter pending orders
    p_buy = [v for k,v in all_o.items() if v.get('status') == 'Pending' and v.get('type') == 'Buy']
    p_sell = [v for k,v in all_o.items() if v.get('status') == 'Pending' and v.get('type') == 'Sell']
    
    # Extra CSS specifically for Admin Images and Tabs
    ADMIN_STYLE = """
    <style>
        .proof-img-box { 
            width: 100%; 
            height: 110px; 
            object-fit: cover; 
            border-radius: 10px; 
            border: 2px solid #eee;
            cursor: pointer;
            transition: 0.3s;
        }
        .proof-img-box:hover { transform: scale(1.05); border-color: #ffc107; }
        .dragon-card { 
            background: white; border-radius: 15px; padding: 15px; 
            margin-bottom: 15px; border: 1px solid #f1f1f1;
            box-shadow: 0 4px 10px rgba(0,0,0,0.03);
        }
        .admin-nav .nav-link { 
            font-weight: 800; font-size: 11px; color: #888; 
            border: none; text-transform: uppercase; padding: 10px 5px;
        }
        .admin-nav .nav-link.active { 
            color: #dc3545 !important; border-bottom: 3px solid #dc3545 !important; background: none; 
        }
        .bg-light-yellow { background: #fffcf0; border: 1px solid #fdf2d0; }
    </style>
    """

    return render_template_string(f"""
    <html><head>{CSS} {ADMIN_STYLE}</head>
    <body style="background:#f8f9fa">
    <div class="app-container p-3">
        <div class="d-flex justify-content-between align-items-center mb-3">
            <h4 class="fw-bold text-danger m-0">Admin Dashboard</h4>
            <a href="/logout" class="btn btn-sm btn-dark rounded-pill px-3">Exit</a>
        </div>
        
        <ul class="nav nav-tabs admin-nav mb-4 border-0 justify-content-between" id="adminTabs" role="tablist">
            <li class="nav-item"><button class="nav-link active" data-bs-toggle="tab" data-bs-target="#tab-buy">Buy ({{{{p_buy|length}}}})</button></li>
            <li class="nav-item"><button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-sell">Sell ({{{{p_sell|length}}}})</button></li>
            <li class="nav-item"><button class="nav-link" data-bs-toggle="tab" data-bs-target="#tab-gate">Gates</button></li>
        </ul>

        <div class="tab-content">
            <div class="tab-pane fade show active" id="tab-buy">
                {{% for o in p_buy %}}
                <div class="dragon-card fade-in">
                    <div class="row g-2">
                        <div class="col-7">
                            <span class="badge bg-dark mb-1" style="font-size:9px">ID: {{{{o.oid}}}}</span><br>
                            <small class="text-muted fw-bold">User: {{{{o.phone.replace(',','.')}}}}</small><br>
                            
                            <div class="text-success fw-bold fs-4">₹{{{{o.amt}}}}</div> 
                            
                            <div class="mb-1">
                                <span class="badge bg-warning text-dark" style="font-size:10px;">
                                    <i class="bi bi-gift-fill"></i> Bonus: ₹{{{{o.reward if o.reward else '0'}}}}
                                </span>
                            </div>

                            <div class="text-primary fw-bold mb-1" style="font-size:12px">UTR: {{{{o.utr}}}}</div>
                            <div class="p-2 bg-light rounded border" style="font-size: 9px; line-height:1.2">
                                <b>Paid To:</b><br>{{{{o.paid_to}}}}
                            </div>
                        </div>
                        <div class="col-5">
                            {{% if o.proof %}}
                            <div onclick="window.open('{{{{o.proof}}}}','_blank')" style="position:relative">
                                <img src="{{{{o.proof}}}}" class="proof-img-box">
                                <div style="position:absolute; bottom:5px; right:5px; background:rgba(0,0,0,0.5); color:white; font-size:8px; padding:2px 5px; border-radius:4px">ZOOM</div>
                            </div>
                            {{% else %}}
                            <div class="bg-light text-center py-4 rounded small text-danger border" style="height:110px; display:flex; align-items:center; justify-content:center">No Proof</div>
                            {{% endif %}}
                        </div>
                    </div>
                    <div class="d-flex gap-2 mt-3">
                        <a href="/admin/action/{{{{o.oid}}}}/Completed" class="btn btn-success btn-sm flex-grow-1 fw-bold py-2">APPROVE</a>
                        <button onclick="rejectWithMsg('{{{{o.oid}}}}')" class="btn btn-outline-danger btn-sm flex-grow-1 fw-bold py-2">REJECT</button>
                    </div>
                </div>
                {{% endfor %}}
                {{% if not p_buy %}}<div class="text-center py-5 text-muted">No pending Buy orders.</div>{{% endif %}}
            </div>
            
            <div class="tab-pane fade" id="tab-sell">
                {{% for o in p_sell %}}
                <div class="dragon-card border-start border-primary border-4">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <span class="badge bg-primary mb-1">SELL</span><br>
                            <small class="text-muted fw-bold">{{{{o.phone.replace(',','.')}}}}</small>
                        </div>
                        <b class="text-danger fs-4">₹{{{{o.amt}}}}</b>
                    </div>
                    <div class="mt-2 p-2 bg-light rounded small border" style="font-size:11px">
                        <b class="text-primary">Withdraw Details:</b><br>{{{{o.w_info}}}}
                    </div>
                    <div class="d-flex gap-2 mt-3">
                        <a href="/admin/action/{{{{o.oid}}}}/Completed" class="btn btn-primary btn-sm flex-grow-1 fw-bold py-2">MARK PAID</a>
                        <button onclick="rejectWithMsg('{{{{o.oid}}}}')" class="btn btn-outline-danger btn-sm flex-grow-1 fw-bold py-2">REJECT</button>
                    </div>
                </div>
                {{% endfor %}}
                {{% if not p_sell %}}<div class="text-center py-5 text-muted">No pending Sell orders.</div>{{% endif %}}
            </div>

            <div class="tab-pane fade" id="tab-gate">
                <div class="dragon-card bg-dark text-white shadow-lg">
                    <h6 class="fw-bold text-warning mb-3"><i class="bi bi-plus-circle-fill me-2"></i>Add New Gateway</h6>
                    <div class="row g-2 mb-3">
                        <div class="col-6"><button class="btn btn-primary btn-sm w-100 fw-bold" onclick="showF('upiForm')">ADD UPI</button></div>
                        <div class="col-6"><button class="btn btn-warning btn-sm w-100 fw-bold" onclick="showF('bankForm')">ADD BANK</button></div>
                    </div>

                    <div id="upiForm" style="display:none" class="bg-white p-3 rounded text-dark border">
                        <form id="qrUploadForm">
                            <input id="q_name" class="form-control mb-2" placeholder="Holder Name" required>
                            <input id="q_upi" class="form-control mb-2" placeholder="UPI ID" required>
                            <label class="small fw-bold text-muted">Upload QR Code (Img):</label>
                            <input type="file" id="q_file" class="form-control mb-3" accept="image/*" required>
                            <button type="submit" id="q_btn" class="btn btn-success w-100 fw-bold">SAVE GATEWAY</button>
                        </form>
                    </div>

                    <div id="bankForm" style="display:none" class="bg-white p-3 rounded text-dark border">
                        <form action="/admin/add_bank" method="post">
                            <input name="bank_name" class="form-control mb-2" placeholder="Bank Name" required>
                            <input name="name" class="form-control mb-2" placeholder="Holder Name" required>
                            <input name="acc_no" class="form-control mb-2" placeholder="Account No" required>
                            <input name="ifsc" class="form-control mb-3" placeholder="IFSC Code" required>
                            <button class="btn btn-success w-100 fw-bold">SAVE BANK</button>
                        </form>
                    </div>
                </div>
                
                <h6 class="fw-bold mt-4 small text-muted text-uppercase">Active UPI Gateways</h6>
                {{% for k,v in bulk_upi.items() %}}
                <div class="dragon-card d-flex justify-content-between py-2 align-items-center mb-2">
                    <div class="small"><b>{{{{v.name}}}}</b><br><span class="text-muted">{{{{v.upi_id}}}}</span></div>
                    <a href="/admin/delete_gate/bulk_upi/{{{{k}}}}" class="btn btn-sm btn-light text-danger"><i class="bi bi-trash"></i></a>
                </div>
                {{% endfor %}}

                <h6 class="fw-bold mt-4 small text-muted text-uppercase">Active Bank Gateways</h6>
                {{% for k,v in bulk_bank.items() %}}
                <div class="dragon-card d-flex justify-content-between py-2 align-items-center mb-2">
                    <div class="small"><b>{{{{v.bank_name}}}}</b><br><span class="text-muted">{{{{v.acc_no}}}}</span></div>
                    <a href="/admin/delete_gate/bulk_bank/{{{{k}}}}" class="btn btn-sm btn-light text-danger"><i class="bi bi-trash"></i></a>
                </div>
                {{% endfor %}}
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
    function showF(id) {{
        document.getElementById('upiForm').style.display = 'none';
        document.getElementById('bankForm').style.display = 'none';
        document.getElementById(id).style.display = 'block';
    }}

    function rejectWithMsg(oid) {{
        let msg = prompt("Enter Rejection Reason:", "Wrong UTR Number");
        if (msg != null) {{
            window.location.href = "/admin/action/" + oid + "/Rejected?reason=" + encodeURIComponent(msg);
        }}
    }}

    document.getElementById('qrUploadForm').onsubmit = async function(e) {{
        e.preventDefault();
        const btn = document.getElementById('q_btn');
        const file = document.getElementById('q_file').files[0];
        btn.disabled = true; btn.innerHTML = "Processing...";
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
                window.location.href = "/admin/add_upi?name=" + name + "&upi_id=" + upi + "&qr_url=" + encodeURIComponent(url);
            }} else {{ alert("Upload Failed!"); btn.disabled = false; }}
        }} catch(err) {{ alert("Error!"); btn.disabled = false; }}
    }};
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
