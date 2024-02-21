from flask import Flask, render_template, request, jsonify
import nmap
import ipaddress
import proxmoxer
import cProfile


app = Flask(__name__)

 
# List to store scan results
scanned_results = []

# Function to run NMAP scan and fetch resolvable IPs
def run_nmap_scan(ip_range, scanned_results):
    try:

        nm = nmap.PortScanner()
        arguments = '-R -v -sn'
        nm.scan(hosts=ip_range, arguments=arguments)

        results = []
        for host in nm.all_hosts():
            results.append({
                'hostname': nm[host].hostname() if nm[host].hostname() else 'N/A',
                'ip': host,
                'status': 'up' if nm[host]['status']['state'] == 'up' else 'down'
            })
        # Sort the results based on IP address
        results = sorted(results, key=lambda x: ipaddress.IPv4Address(x['ip']))

        # Update scanned_results directly (modify in-place)
        scanned_results.clear()
        scanned_results.extend(results)
        return results

    except Exception as e:
        print(f"Error in run_nmap_scan: {str(e)}")
        return []

# Main function
def main():
    app.run(debug=True)

# Route for handling the scan request
@app.route('/')
def index():
    return render_template('index.html', scanned_results=scanned_results)

@app.route('/scan', methods=['POST'])
def scan():
    try:
        ip_range = request.json['ip_range']

        # Run NMAP scan and store the results in the scanned_results list
        results = run_nmap_scan(ip_range, scanned_results)
        return jsonify(results)

    except Exception as e:
        print(f"Error in scan: {str(e)}")
        return jsonify({'error': str(e)})
# cProfile main (comment out when not needed)
#if __name__ == '__main__':
#    cProfile.run('main()', sort='cumulative')

if __name__ == '__main__':
    app.run(debug=True)
