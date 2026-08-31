"""
Lightweight Zero-Dependency Local Web Server for Antigravity Metaphysics Dashboard
"""
import sys
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from pathlib import Path

repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "engine"))

from lunar_solar import calculate_time_coordinates, LOCAL_TZ
from mai_hoa import calculate_mai_hoa_from_time
from luc_hao import calculate_full_luc_hao
from formatter import format_divination_report
from bazi_engine import calculate_bazi, format_bazi_report
from tu_vi_engine import calculate_tu_vi_chart, format_tu_vi_report
from ha_lac_engine import calculate_ha_lac, format_ha_lac_report
from ky_mon_engine import calculate_ky_mon, format_ky_mon_report
from synthesis_engine import run_master_synthesis, format_master_synthesis_report

class MetaphysicsHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/calculate":
            params = parse_qs(parsed.query)
            dt_str = params.get("datetime", [None])[0]
            gender = int(params.get("gender", [1])[0])
            question = params.get("question", [""])[0]
            
            try:
                if dt_str:
                    dt = datetime.strptime(dt_str, "%Y-%m-%dT%H:%M").replace(tzinfo=LOCAL_TZ)
                else:
                    dt = datetime.now().replace(tzinfo=LOCAL_TZ)
            except Exception:
                dt = datetime.now().replace(tzinfo=LOCAL_TZ)
                
            # Compute all engines
            syn_data = run_master_synthesis(dt, question=question, gender=gender)
            syn_rep = format_master_synthesis_report(syn_data)
            
            tc = calculate_time_coordinates(dt)
            mh = calculate_mai_hoa_from_time(tc)
            lh = calculate_full_luc_hao(mh, tc)
            iching_rep = format_divination_report(tc, mh, lh, question)
            
            bz_data = calculate_bazi(dt, gender=gender)
            bazi_rep = format_bazi_report(bz_data)
            
            tv_data = calculate_tu_vi_chart(dt, gender=gender)
            tuvi_rep = format_tu_vi_report(tv_data)
            
            hl_data = calculate_ha_lac(dt, gender=gender)
            halac_rep = format_ha_lac_report(hl_data)
            
            km_data = calculate_ky_mon(dt)
            kymon_rep = format_ky_mon_report(km_data)
            
            res_payload = {
                "synthesis_report": syn_rep,
                "iching_report": iching_rep,
                "tuvi_report": tuvi_rep,
                "kymon_report": kymon_rep,
                "bazi_report": bazi_rep,
                "halac_report": halac_rep
            }
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(res_payload, ensure_ascii=False).encode("utf-8"))
            return
            
        # Serve static web files
        if parsed.path == "/" or parsed.path == "/index.html":
            html_file = repo_root / "web" / "index.html"
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html_file.read_bytes())
            return
            
        super().do_GET()

def start_server(port=8888):
    server = HTTPServer(("127.0.0.1", port), MetaphysicsHandler)
    print(f"\n=================================================================")
    print(f"  ANTIGRAVITY METAPHYSICS VISUAL DASHBOARD RUNNING")
    print(f"  Open in Browser: http://localhost:{port}")
    print(f"=================================================================\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    start_server(8888)
