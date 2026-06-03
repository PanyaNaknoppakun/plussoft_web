import http.server
import ssl
import os

PORT = 8000
# ค้นหาไฟล์ cert ในโฟลเดอร์เดียวกับสคริปต์
base_dir = os.path.dirname(os.path.abspath(__file__))
cert_file = os.path.join(base_dir, "server.crt")
key_file = os.path.join(base_dir, "server.key")

# สร้าง HTTPServer
httpd = http.server.HTTPServer(('0.0.0.0', PORT), http.server.SimpleHTTPRequestHandler)

# ตรวจสอบการมีอยู่ของไฟล์ SSL Certificate เพื่อเปลี่ยนเป็น HTTP อัตโนมัติหากไม่มีไฟล์
if os.path.exists(cert_file) and os.path.exists(key_file):
    try:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=cert_file, keyfile=key_file)
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        print(f"Secure server started on HTTPS: https://localhost:{PORT}")
    except Exception as e:
        print(f"Failed to initialize SSL: {e}. Falling back to HTTP...")
        print(f"Server started on HTTP: http://localhost:{PORT}")
else:
    print("SSL Certificate files not found. Starting in HTTP mode...")
    print(f"Server started on HTTP: http://localhost:{PORT}")

# เริ่มเซิร์ฟเวอร์
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped.")
    httpd.shutdown()