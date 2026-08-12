#!/usr/bin/env python3
# E-Commerce Sales Insights System - local dashboard (Python standard library + SQLite).
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import sqlite3, html, csv, io, json, webbrowser, threading

ROOT=Path(__file__).resolve().parent
DB=ROOT/'database'/'ecsales.db'
PORT=8765

def db():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def money(x): return f"${(x or 0):,.2f}"
def pct(x): return f"{(x or 0):,.2f}%"

def esc(x): return html.escape(str(x))

def svg_line(points, w=760,h=240):
    if not points: return '<div class="empty">No data</div>'
    vals=[float(p[1] or 0) for p in points]; mn=min(vals); mx=max(vals); span=max(mx-mn,1)
    coords=[]
    for i,v in enumerate(vals):
        x=42+(w-70)*(i/max(len(vals)-1,1)); y=18+(h-55)*(1-(v-mn)/span); coords.append((x,y))
    poly=' '.join(f'{x:.1f},{y:.1f}' for x,y in coords)
    dots=''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3"><title>{esc(points[i][0])}: {money(vals[i])}</title></circle>' for i,(x,y) in enumerate(coords))
    return f'<svg viewBox="0 0 {w} {h}" class="chart"><line x1="42" y1="{h-35}" x2="{w-20}" y2="{h-35}"/><polyline points="{poly}"/>{dots}<text x="42" y="14">{money(mx)}</text><text x="42" y="{h-16}">{esc(points[0][0])}</text><text x="{w-120}" y="{h-16}">{esc(points[-1][0])}</text></svg>'

def svg_bars(rows, label_key, value_key, w=760,h=300):
    if not rows: return '<div class="empty">No data</div>'
    rows=list(rows)[:10]; vals=[float(r[value_key] or 0) for r in rows]; mx=max(max(vals),1)
    barh=(h-30)/len(rows)
    out=[f'<svg viewBox="0 0 {w} {h}" class="chart bars">']
    for i,(r,v) in enumerate(zip(rows,vals)):
        y=10+i*barh; bw=(w-245)*(v/mx)
        out.append(f'<text x="5" y="{y+barh*.62:.1f}">{esc(str(r[label_key])[:24])}</text><rect x="190" y="{y+3:.1f}" width="{bw:.1f}" height="{max(barh-7,5):.1f}" rx="4"><title>{esc(r[label_key])}: {money(v)}</title></rect><text x="{200+bw:.1f}" y="{y+barh*.62:.1f}">{money(v)}</text>')
    out.append('</svg>'); return ''.join(out)

CSS='''
:root{--bg:#07111f;--panel:#0c1a2d;--panel2:#10223a;--text:#e8f0fb;--muted:#8ca2bd;--accent:#58d5ff;--accent2:#8c7cff;--good:#54e0a6;--warn:#ffc857;--bad:#ff758f;--line:#213650}*{box-sizing:border-box}body{margin:0;font-family:Inter,Segoe UI,Arial,sans-serif;background:radial-gradient(circle at 10% 0,#122846 0,#07111f 38%);color:var(--text)}a{color:inherit;text-decoration:none}.shell{display:grid;grid-template-columns:235px 1fr;min-height:100vh}.side{padding:28px 18px;border-right:1px solid var(--line);background:#081421e8;position:sticky;top:0;height:100vh}.brand{font-size:18px;font-weight:800;letter-spacing:.2px}.brand small{display:block;color:var(--accent);font-size:11px;margin-top:7px;text-transform:uppercase;letter-spacing:1.6px}.nav{margin-top:28px}.nav a{display:block;padding:11px 12px;margin:5px 0;border-radius:10px;color:var(--muted)}.nav a:hover,.nav a.on{background:var(--panel2);color:white}.main{padding:34px;max-width:1500px}.top{display:flex;justify-content:space-between;align-items:flex-start;gap:20px;margin-bottom:22px}.eyebrow{color:var(--accent);text-transform:uppercase;font-size:11px;letter-spacing:1.6px;font-weight:700}h1{font-size:30px;margin:5px 0 4px}h2{font-size:18px;margin:0}.sub{color:var(--muted);font-size:14px}.badge{border:1px solid #2b4966;background:#0e2034;padding:8px 11px;border-radius:999px;color:#b9cee4;font-size:12px}.filters{display:flex;gap:10px;flex-wrap:wrap;padding:14px;background:#0a1829;border:1px solid var(--line);border-radius:14px;margin-bottom:18px}.filters input,.filters select,.sqlbox textarea{background:#071421;border:1px solid #29415d;color:white;border-radius:8px;padding:9px 10px}.btn{background:linear-gradient(135deg,var(--accent),var(--accent2));border:0;color:#07111f;font-weight:800;padding:9px 14px;border-radius:8px;cursor:pointer}.grid{display:grid;gap:14px}.kpis{grid-template-columns:repeat(6,1fr);margin-bottom:14px}.card{background:linear-gradient(180deg,#0d1d31,#0a1728);border:1px solid var(--line);border-radius:15px;padding:17px;box-shadow:0 10px 34px #0002}.kpi .lab{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.8px}.kpi .val{font-size:25px;font-weight:800;margin-top:8px}.kpi .note{font-size:11px;color:#748ca8;margin-top:5px}.two{grid-template-columns:1.35fr 1fr}.three{grid-template-columns:repeat(3,1fr)}.section{margin-top:14px}.sectionhead{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}.chart{width:100%;height:auto;overflow:visible}.chart line{stroke:#2a4260}.chart polyline{fill:none;stroke:var(--accent);stroke-width:3}.chart circle{fill:var(--accent2);stroke:white;stroke-width:1}.chart text{fill:#8da3bd;font-size:11px}.bars rect{fill:url(#x);stroke:none}.bars rect{fill:#58d5ff}.tablewrap{overflow:auto;max-height:410px}table{width:100%;border-collapse:collapse;font-size:12px}th{text-align:left;color:#91a8c2;font-weight:700;background:#0d1c30;position:sticky;top:0}th,td{padding:10px;border-bottom:1px solid #1c3048;white-space:nowrap}.pill{display:inline-block;padding:3px 7px;border-radius:999px;background:#16324a;color:#9fdfff;font-size:10px}.good{color:var(--good)}.warn{color:var(--warn)}.bad{color:var(--bad)}.insight{border-left:3px solid var(--accent);padding:12px 14px;background:#0a1b2e;border-radius:0 10px 10px 0;color:#bdcce0;font-size:13px;line-height:1.5}.sqlbox textarea{width:100%;height:140px;font-family:Consolas,monospace;line-height:1.45}.footer{margin:28px 0 6px;color:#607894;font-size:11px}.empty{padding:40px;color:var(--muted);text-align:center}@media(max-width:1100px){.kpis{grid-template-columns:repeat(3,1fr)}.two,.three{grid-template-columns:1fr}.shell{grid-template-columns:1fr}.side{position:relative;height:auto}.nav{display:flex;flex-wrap:wrap}.main{padding:20px}}'''

NAV=[('overview','Overview'),('marketing','Marketing'),('products','Products'),('customers','Customers'),('operations','Operations'),('sql','SQL Lab')]

def layout(page,title,subtitle,body):
    nav=''.join(f'<a class="{"on" if page==p else ""}" href="/?page={p}">{n}</a>' for p,n in NAV)
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{esc(title)}</title><style>{CSS}</style></head><body><div class="shell"><aside class="side"><div class="brand">E-Commerce Insights<small>SQL Analytics System</small></div><div class="nav">{nav}</div></aside><main class="main"><div class="top"><div><div class="eyebrow">Portfolio Analytics Project</div><h1>{esc(title)}</h1><div class="sub">{esc(subtitle)}</div></div><div class="badge">SQLite • SQL • Python • Local Dashboard</div></div>{body}<div class="footer">E-Commerce Sales Insights System • synthetic portfolio dataset • built for local execution without a database server</div></main></div></body></html>'''

def qdict(qs): return {k:v[0] for k,v in qs.items() if v}
def where(filters, alias='os'):
    clauses=['1=1']; args=[]
    if filters.get('start'): clauses.append(f'{alias}.order_date >= ?'); args.append(filters['start'])
    if filters.get('end'): clauses.append(f'{alias}.order_date <= ?'); args.append(filters['end'])
    if filters.get('channel'):
        clauses.append(f'{alias}.channel_id = ?'); args.append(filters['channel'])
    if filters.get('country'):
        clauses.append(f'{alias}.ship_country = ?'); args.append(filters['country'])
    return ' AND '.join(clauses), args

def filterbar(filters):
    c=db(); channels=c.execute('SELECT channel_id,channel_name FROM channels').fetchall(); countries=c.execute('SELECT DISTINCT ship_country FROM orders ORDER BY 1').fetchall(); c.close()
    chopts='<option value="">All channels</option>'+''.join(f'<option value="{r[0]}" {"selected" if filters.get("channel")==str(r[0]) else ""}>{esc(r[1])}</option>' for r in channels)
    coopts='<option value="">All countries</option>'+''.join(f'<option {"selected" if filters.get("country")==r[0] else ""}>{esc(r[0])}</option>' for r in countries)
    return f'''<form class="filters"><input type="hidden" name="page" value="overview"><input type="date" name="start" value="{esc(filters.get('start','2026-01-01'))}"><input type="date" name="end" value="{esc(filters.get('end','2026-06-30'))}"><select name="channel">{chopts}</select><select name="country">{coopts}</select><button class="btn">Apply filters</button></form>'''

def table(rows):
    rows=list(rows)
    if not rows:return '<div class="empty">No rows</div>'
    cols=rows[0].keys(); h='<div class="tablewrap"><table><thead><tr>'+''.join(f'<th>{esc(c)}</th>' for c in cols)+'</tr></thead><tbody>'
    for r in rows:h+='<tr>'+''.join(f'<td>{esc(r[c] if r[c] is not None else "-")}</td>' for c in cols)+'</tr>'
    return h+'</tbody></table></div>'

def overview(filters):
    c=db(); wh,args=where(filters)
    k=c.execute(f'''SELECT COUNT(*) orders, SUM(order_revenue) revenue, AVG(order_revenue) aov, SUM(units) units, SUM(gross_profit) profit, 100.0*SUM(gross_profit)/SUM(order_revenue) margin FROM v_order_summary os WHERE {wh}''',args).fetchone()
    cust=c.execute(f'SELECT COUNT(DISTINCT customer_id) FROM v_order_summary os WHERE {wh}',args).fetchone()[0]
    trend=c.execute(f'''SELECT strftime('%Y-%m',order_date) month, SUM(order_revenue) revenue FROM v_order_summary os WHERE {wh} GROUP BY 1 ORDER BY 1''',args).fetchall()
    prod=c.execute(f'''SELECT p.product_name, ROUND(SUM(ol.line_revenue),2) revenue FROM v_order_lines_paid ol JOIN products p ON p.product_id=ol.product_id JOIN v_order_summary os ON os.order_id=ol.order_id WHERE {wh} GROUP BY p.product_id ORDER BY revenue DESC LIMIT 8''',args).fetchall()
    geo=c.execute(f'''SELECT ship_region, COUNT(*) orders, ROUND(SUM(order_revenue),2) revenue FROM v_order_summary os WHERE {wh} GROUP BY ship_region ORDER BY revenue DESC LIMIT 8''',args).fetchall()
    recent=c.execute(f'''SELECT order_id,order_date,ship_country,ROUND(order_revenue,2) revenue,units FROM v_order_summary os WHERE {wh} ORDER BY order_date DESC,order_id DESC LIMIT 12''',args).fetchall(); c.close()
    kpis=f'''<div class="grid kpis"><div class="card kpi"><div class="lab">Net Revenue</div><div class="val">{money(k['revenue'])}</div><div class="note">Paid orders only</div></div><div class="card kpi"><div class="lab">Orders</div><div class="val">{k['orders']:,}</div><div class="note">Completed purchases</div></div><div class="card kpi"><div class="lab">AOV</div><div class="val">{money(k['aov'])}</div><div class="note">Revenue / orders</div></div><div class="card kpi"><div class="lab">Gross Profit</div><div class="val">{money(k['profit'])}</div><div class="note">Before marketing & shipping</div></div><div class="card kpi"><div class="lab">Margin</div><div class="val">{pct(k['margin'])}</div><div class="note">Gross profit / revenue</div></div><div class="card kpi"><div class="lab">Customers</div><div class="val">{cust:,}</div><div class="note">Unique buyers</div></div></div>'''
    body=filterbar(filters)+kpis+f'''<div class="grid two"><div class="card"><div class="sectionhead"><h2>Revenue Trend</h2><span class="pill">Monthly</span></div>{svg_line([(r['month'],r['revenue']) for r in trend])}</div><div class="card"><div class="sectionhead"><h2>Top Products</h2><span class="pill">By revenue</span></div>{svg_bars(prod,'product_name','revenue')}</div></div><div class="grid two section"><div class="card"><div class="sectionhead"><h2>Regional Performance</h2></div>{table(geo)}</div><div class="card"><div class="sectionhead"><h2>Recent Paid Orders</h2></div>{table(recent)}</div></div>'''
    return layout('overview','Executive Overview','Revenue, profitability, customers and product performance at a glance.',body)

def marketing():
    c=db(); rows=c.execute('''SELECT channel_name, SUM(sessions) sessions, SUM(conversions) conversions, ROUND(100.0*SUM(conversions)/SUM(sessions),2) conversion_pct, ROUND(SUM(revenue),2) revenue, ROUND(SUM(spend),2) spend, ROUND(SUM(revenue)/NULLIF(SUM(spend),0),2) roas, ROUND(SUM(spend)/NULLIF(SUM(new_customers),0),2) cac FROM v_channel_daily GROUP BY channel_name ORDER BY roas DESC''').fetchall()
    trend=c.execute('''SELECT strftime('%Y-%m',order_date) month, ROUND(SUM(spend),2) spend FROM v_channel_daily GROUP BY 1 ORDER BY 1''').fetchall(); c.close()
    body=f'''<div class="grid two"><div class="card"><div class="sectionhead"><h2>Channel Revenue</h2><span class="pill">Attribution</span></div>{svg_bars(rows,'channel_name','revenue')}</div><div class="card"><div class="sectionhead"><h2>Marketing Spend Trend</h2></div>{svg_line([(r['month'],r['spend']) for r in trend])}</div></div><div class="card section"><div class="sectionhead"><h2>ROAS, CAC & Conversion</h2></div>{table(rows)}</div><div class="insight section">Use ROAS to compare revenue efficiency, CAC to assess acquisition economics, and conversion rate to diagnose funnel quality. A channel can have strong revenue but weak efficiency if spend is disproportionately high.</div>'''
    return layout('marketing','Marketing Performance','Channel efficiency across traffic, conversion, revenue, spend, ROAS and CAC.',body)

def products():
    c=db(); rows=c.execute('''SELECT p.product_name,c.category_name,SUM(ol.quantity) units,ROUND(SUM(ol.line_revenue),2) revenue,ROUND(SUM(ol.gross_profit),2) gross_profit,ROUND(100.0*SUM(ol.gross_profit)/SUM(ol.line_revenue),2) margin_pct FROM v_order_lines_paid ol JOIN products p ON p.product_id=ol.product_id JOIN categories c ON c.category_id=p.category_id GROUP BY p.product_id ORDER BY revenue DESC''').fetchall()
    cats=c.execute('''SELECT c.category_name,ROUND(SUM(ol.line_revenue),2) revenue,ROUND(SUM(ol.gross_profit),2) gross_profit FROM v_order_lines_paid ol JOIN products p ON p.product_id=ol.product_id JOIN categories c ON c.category_id=p.category_id GROUP BY c.category_id ORDER BY revenue DESC''').fetchall()
    inv=c.execute('''WITH x AS (SELECT MAX(snapshot_date) dt FROM inventory_snapshots) SELECT p.product_name,i.stock_on_hand,i.reorder_level,CASE WHEN i.stock_on_hand<=i.reorder_level THEN 'REORDER' ELSE 'OK' END stock_flag FROM inventory_snapshots i JOIN x ON i.snapshot_date=x.dt JOIN products p ON p.product_id=i.product_id ORDER BY stock_flag DESC,stock_on_hand LIMIT 15''').fetchall(); c.close()
    body=f'''<div class="grid two"><div class="card"><h2>Category Revenue</h2>{svg_bars(cats,'category_name','revenue')}</div><div class="card"><h2>Top Product Revenue</h2>{svg_bars(rows,'product_name','revenue')}</div></div><div class="grid two section"><div class="card"><div class="sectionhead"><h2>Product Profitability</h2></div>{table(rows[:20])}</div><div class="card"><div class="sectionhead"><h2>Inventory Risk</h2></div>{table(inv)}</div></div>'''
    return layout('products','Product & Inventory Insights','Merchandising performance, profitability and stock-risk monitoring.',body)

def customers():
    c=db(); top=c.execute('''SELECT customer_name,country,paid_orders,lifetime_revenue,avg_order_value,first_order_date,last_order_date FROM v_customer_lifetime_value WHERE paid_orders>0 ORDER BY lifetime_revenue DESC LIMIT 20''').fetchall()
    rep=c.execute('''WITH x AS (SELECT customer_id,COUNT(*) n FROM v_order_summary GROUP BY customer_id) SELECT COUNT(*) buyers,SUM(CASE WHEN n>=2 THEN 1 ELSE 0 END) repeat_buyers,ROUND(100.0*SUM(CASE WHEN n>=2 THEN 1 ELSE 0 END)/COUNT(*),2) repeat_rate FROM x''').fetchone()
    cohort=c.execute('''WITH f AS (SELECT customer_id,MIN(order_date) first_dt FROM v_order_summary GROUP BY customer_id), r AS (SELECT f.customer_id,f.first_dt,MAX(CASE WHEN julianday(o.order_date)>julianday(f.first_dt) AND julianday(o.order_date)<=julianday(f.first_dt)+30 THEN 1 ELSE 0 END) rep FROM f LEFT JOIN v_order_summary o ON o.customer_id=f.customer_id GROUP BY f.customer_id) SELECT strftime('%Y-%m',first_dt) cohort_month,COUNT(*) customers,SUM(rep) repeat_30d,ROUND(100.0*SUM(rep)/COUNT(*),2) repeat_30d_pct FROM r GROUP BY 1 ORDER BY 1''').fetchall(); c.close()
    body=f'''<div class="grid three"><div class="card kpi"><div class="lab">Purchasing Customers</div><div class="val">{rep['buyers']}</div></div><div class="card kpi"><div class="lab">Repeat Buyers</div><div class="val">{rep['repeat_buyers']}</div></div><div class="card kpi"><div class="lab">Repeat Rate</div><div class="val">{pct(rep['repeat_rate'])}</div></div></div><div class="grid two section"><div class="card"><h2>30-Day Cohort Retention</h2>{table(cohort)}</div><div class="card"><h2>High-Value Customers</h2>{table(top)}</div></div>'''
    return layout('customers','Customer & Cohort Analytics','Customer value, repeat purchasing and early-retention behavior.',body)

def operations():
    c=db(); ship=c.execute('''SELECT courier,COUNT(*) delivered_shipments,ROUND(AVG(julianday(delivered_at)-julianday(shipped_at)),2) avg_delivery_days,ROUND(100.0*SUM(CASE WHEN date(delivered_at)>promised_delivery_date THEN 1 ELSE 0 END)/COUNT(*),2) late_delivery_pct FROM shipping WHERE shipping_status='DELIVERED' GROUP BY courier ORDER BY late_delivery_pct''').fetchall()
    ret=c.execute('''SELECT reason,COUNT(*) returns,ROUND(SUM(refund_amount),2) refund_value FROM returns GROUP BY reason ORDER BY refund_value DESC''').fetchall()
    pay=c.execute('''SELECT method,COUNT(*) transactions,ROUND(SUM(paid_amount),2) amount FROM payments GROUP BY method ORDER BY amount DESC''').fetchall(); c.close()
    body=f'''<div class="grid two"><div class="card"><h2>Courier Performance</h2>{table(ship)}</div><div class="card"><h2>Return Reasons</h2>{svg_bars(ret,'reason','refund_value')}</div></div><div class="grid two section"><div class="card"><h2>Refund Impact</h2>{table(ret)}</div><div class="card"><h2>Payment Mix</h2>{table(pay)}</div></div>'''
    return layout('operations','Operations & Refunds','Shipping service levels, return drivers, refunds and payment behavior.',body)

def sqllab(qs):
    library={
      'Marketing ROAS': "SELECT channel_name, ROUND(SUM(revenue),2) AS revenue, ROUND(SUM(spend),2) AS spend, ROUND(SUM(revenue)/NULLIF(SUM(spend),0),2) AS roas FROM v_channel_daily GROUP BY channel_name ORDER BY roas DESC;",
      'Top Products': "SELECT p.product_name, ROUND(SUM(ol.line_revenue),2) AS revenue, SUM(ol.quantity) AS units FROM v_order_lines_paid ol JOIN products p ON p.product_id=ol.product_id GROUP BY p.product_id ORDER BY revenue DESC LIMIT 10;",
      'Top Customers': "SELECT customer_name, country, paid_orders, lifetime_revenue, avg_order_value FROM v_customer_lifetime_value WHERE paid_orders>0 ORDER BY lifetime_revenue DESC LIMIT 15;",
      'Category Performance': "SELECT c.category_name, ROUND(SUM(ol.line_revenue),2) AS revenue, ROUND(SUM(ol.gross_profit),2) AS gross_profit FROM v_order_lines_paid ol JOIN products p ON p.product_id=ol.product_id JOIN categories c ON c.category_id=p.category_id GROUP BY c.category_id ORDER BY revenue DESC;",
      'Shipping Performance': "SELECT courier, COUNT(*) AS shipments, ROUND(AVG(julianday(delivered_at)-julianday(shipped_at)),2) AS avg_delivery_days FROM shipping WHERE shipping_status='DELIVERED' GROUP BY courier ORDER BY avg_delivery_days;",
      'Refund Analysis': "SELECT reason, COUNT(*) AS returns, ROUND(SUM(refund_amount),2) AS refund_value FROM returns GROUP BY reason ORDER BY refund_value DESC;"
    }
    picked=qs.get('example',['Marketing ROAS'])[0]
    query=qs.get('query',[library.get(picked,library['Marketing ROAS'])])[0]; result=''; meta=''
    if 'query' in qs:
        import time
        st=query.strip().lower()
        if not (st.startswith('select') or st.startswith('with')) or ';' in st[:-1]:
            result='<div class="insight bad">SQL Lab is read-only. Use one SELECT or WITH query.</div>'
        else:
            try:
                t=time.perf_counter(); c=db(); cur=c.execute(query); rows=cur.fetchmany(200); c.close(); ms=(time.perf_counter()-t)*1000
                result=table(rows); meta=f'<div class="insight good">Query executed successfully in {ms:.2f} ms - {len(rows)} row(s) displayed - maximum 200 rows</div>'
            except Exception as e: result=f'<div class="insight bad">{esc(e)}</div>'
    opts=''.join(f'<option {"selected" if picked==k else ""}>{esc(k)}</option>' for k in library)
    js=json.dumps(library)
    empty='<div class="insight">Choose a prepared query or write your own SELECT/WITH statement. The result is calculated from the local SQLite database when you click Run Query.</div>'
    body=f'''<div class="card sqlbox"><div class="sectionhead"><h2>Interactive SQL Workspace</h2><span class="pill">Live SQLite execution - Read only</span></div><div class="filters" style="margin-bottom:12px"><label class="sub">Query Library&nbsp;</label><select id="example">{opts}</select><button type="button" class="btn" onclick="loadExample()">Load Example</button><button type="button" class="badge" onclick="document.getElementById('query').value=''">Clear</button></div><form><input type="hidden" name="page" value="sql"><textarea id="query" name="query" spellcheck="false">{esc(query)}</textarea><div style="margin-top:10px"><button class="btn">Run Query</button></div></form><script>const examples={js};function loadExample(){{document.getElementById('query').value=examples[document.getElementById('example').value]||'';}}</script></div>{meta}<div class="card section">{result or empty}</div>'''
    return layout('sql','SQL Lab','Write or modify SQL and execute it live against the project database.',body)

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        u=urlparse(self.path); qs=parse_qs(u.query); page=qs.get('page',['overview'])[0]
        if u.path=='/export/orders.csv':
            c=db(); rows=c.execute('SELECT * FROM v_order_summary ORDER BY order_date').fetchall();
            sio=io.StringIO(); w=csv.writer(sio); w.writerow(rows[0].keys() if rows else []); w.writerows([tuple(r) for r in rows]); c.close(); data=sio.getvalue().encode()
            self.send_response(200); self.send_header('Content-Type','text/csv'); self.send_header('Content-Disposition','attachment; filename=order_summary.csv'); self.end_headers(); self.wfile.write(data); return
        if page=='marketing': out=marketing()
        elif page=='products': out=products()
        elif page=='customers': out=customers()
        elif page=='operations': out=operations()
        elif page=='sql': out=sqllab(qs)
        else: out=overview(qdict(qs))
        data=out.encode(); self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def log_message(self,*a): pass

if __name__=='__main__':
    url=f'http://127.0.0.1:{PORT}'
    print('\nE-Commerce Sales Insights System')
    print('Dashboard:',url)
    print('Press Ctrl+C to stop.\n')
    threading.Timer(0.8, lambda:webbrowser.open(url)).start()
    ThreadingHTTPServer(('127.0.0.1',PORT),H).serve_forever()
