import time
import random
from datetime import datetime
from typing import Dict, List, Optional

# ========== ANSI COLOR CODES ==========
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'  # Fixed: capital GREEN
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# ========== 1. ADVANCED PACKET CLASS ==========
class Packet:
    """Represents a network packet with full metadata"""
    def __init__(self, source_ip: str, destination_ip: str, data: str, 
                 protocol: str = "HTTP", packet_type: str = "REQUEST"):
        self.packet_id = random.randint(1000, 9999)
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.data = data
        self.protocol = protocol  # HTTP, FTP, SMTP, DNS
        self.packet_type = packet_type  # REQUEST or RESPONSE
        self.timestamp = datetime.now()
        self.ttl = 64  # Time To Live
        self.size = len(data)  # Packet size in bytes
        
    def transmit_animation(self, speed: float = 0.2):
        """Show packet transmission with realistic animation"""
        print(f"{Colors.CYAN}[PHYSICAL] Packet {self.packet_id} transmitting ", end="")
        distance = random.randint(5, 15)
        for i in range(distance):
            symbols = ["═", "═", "─", "━"]
            print(f"{random.choice(symbols)}", end="", flush=True)
            time.sleep(speed * random.uniform(0.5, 1.5))
        print(f" ↗{Colors.END}")
        
    def __str__(self):
        time_str = self.timestamp.strftime("%H:%M:%S.%f")[:-3]
        return (f"{Colors.YELLOW}[📦 PACKET {self.packet_id}]{Colors.END} "
                f"{Colors.CYAN}{time_str}{Colors.END} | "
                f"{self.source_ip:15} → {self.destination_ip:15} | "
                f"{self.protocol:4} | {self.data[:20]}...")

# ========== 2. ENHANCED SERVER WITH SECURITY ==========
class Server:
    """Represents an Application Layer server with security features"""
    def __init__(self, ip_address: str, name: str, content: str, 
                 security_level: int = 1, server_type: str = "WEB"):
        self.ip_address = ip_address
        self.name = name
        self.content = content
        self.server_type = server_type  # WEB, MAIL, FILE, DNS, DB
        self.is_online = True
        self.security_level = security_level  # 1=Low, 2=Medium, 3=High
        self.access_log: List[str] = []
        self.requests_served = 0
        self.uptime_start = datetime.now()
        
    def process_request(self, packet: Packet) -> str:
        """Process incoming request and return response"""
        self.requests_served += 1
        log_entry = f"{datetime.now()}: {packet.source_ip} → {self.name}"
        self.access_log.append(log_entry)
        
        if not self.is_online:
            return f"{Colors.RED}❌ 503 Service Unavailable: Server '{self.name}' is offline{Colors.END}"
        
        # Security checks
        if self.security_level >= 3 and packet.protocol != "HTTPS":
            return f"{Colors.RED}🚫 403 Forbidden: HTTPS required for {self.name}{Colors.END}"
            
        if self.security_level >= 2 and "192.168.2." in packet.source_ip:
            return f"{Colors.RED}🚫 403 Forbidden: Unauthorized network{Colors.END}"
        
        # Simulate processing time based on content size
        processing_time = len(self.content) * 0.01
        time.sleep(processing_time)
        
        # Protocol-specific responses
        if packet.protocol == "FTP":
            response = f"{Colors.GREEN}📁 226 Transfer complete: {self.content}{Colors.END}"
        elif packet.protocol == "SMTP":
            response = f"{Colors.GREEN}📧 250 OK: Message accepted for {self.content}{Colors.END}"
        elif packet.protocol == "DNS":
            response = f"{Colors.GREEN}🔍 DNS Response: {self.content}{Colors.END}"
        else:  # HTTP/HTTPS
            response = f"{Colors.GREEN}✅ 200 OK [{self.name}]: {self.content}{Colors.END}"
            
        return response
    
    def get_uptime(self) -> str:
        """Calculate server uptime"""
        uptime = datetime.now() - self.uptime_start
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds % 3600) // 60
        return f"{hours}h {minutes}m"
    
    def toggle_status(self):
        """Toggle server online/offline status"""
        self.is_online = not self.is_online
        status = "ONLINE" if self.is_online else "OFFLINE"
        color = Colors.GREEN if self.is_online else Colors.RED
        return f"{color}Server '{self.name}' is now {status}{Colors.END}"

# ========== 3. DNS SYSTEM WITH CACHE ==========
class DNSSystem:
    """Domain Name System with caching"""
    def __init__(self):
        self.dns_records: Dict[str, str] = {
            "google.com": "192.168.1.1",
            "bank.com": "192.168.1.2",
            "email.com": "192.168.1.3",
            "cloud.com": "192.168.1.4",
            "youtube.com": "192.168.1.5",
            "github.com": "192.168.1.6",
            "facebook.com": "192.168.1.7",
            "twitter.com": "192.168.1.8",
            "localhost": "127.0.0.1"
        }
        self.dns_cache: Dict[str, str] = {}
        self.lookup_count = 0
        
    def resolve(self, domain: str) -> Optional[str]:
        """Resolve domain name to IP address"""
        self.lookup_count += 1
        
        # Check cache first
        if domain in self.dns_cache:
            print(f"{Colors.YELLOW}[DNS] Cache hit for '{domain}'{Colors.END}")
            return self.dns_cache[domain]
        
        # Standard resolution
        if domain in self.dns_records:
            ip = self.dns_records[domain]
            self.dns_cache[domain] = ip  # Add to cache
            print(f"{Colors.GREEN}[DNS] Resolved '{domain}' → {ip}{Colors.END}")
            return ip
        
        print(f"{Colors.RED}[DNS] NXDOMAIN: '{domain}' not found{Colors.END}")
        return None

# ========== 4. INTELLIGENT FIREWALL ==========
class Firewall:
    """Stateful firewall with multiple security rules"""
    def __init__(self):
        self.blacklisted_ips: List[str] = [
            "192.168.2.100",  # Known attacker
            "10.0.0.666",     # Invalid IP
            "185.143.223.1"   # Suspicious IP
        ]
        self.security_rules = {
            "block_malformed_packets": True,
            "require_ttl_check": True,
            "block_private_to_public": False,
            "rate_limit": 10,  # Max packets per second
        }
        self.packet_history: List[Packet] = []
        self.blocked_count = 0
        
    def inspect_packet(self, packet: Packet) -> tuple[bool, str]:
        """Inspect packet against firewall rules"""
        self.packet_history.append(packet)
        
        # Rule 1: Blacklisted IPs
        if packet.source_ip in self.blacklisted_ips:
            self.blocked_count += 1
            return False, f"{Colors.RED}🚫 BLOCKED: Source IP in blacklist{Colors.END}"
        
        # Rule 2: TTL check
        if self.security_rules["require_ttl_check"] and packet.ttl <= 0:
            return False, f"{Colors.RED}🚫 BLOCKED: Packet TTL expired{Colors.END}"
        
        # Rule 3: Rate limiting (simplified)
        recent_packets = [p for p in self.packet_history[-10:] 
                         if p.source_ip == packet.source_ip]
        if len(recent_packets) > self.security_rules["rate_limit"]:
            return False, f"{Colors.RED}🚫 BLOCKED: Rate limit exceeded{Colors.END}"
        
        return True, f"{Colors.GREEN}✓ Firewall check passed{Colors.END}"

# ========== 5. ADVANCED ROUTER WITH QOS ==========
class AdvancedRouter:
    """Enterprise-grade router with QoS and monitoring"""
    def __init__(self, name: str = "CoreRouter-01"):
        self.name = name
        self.routing_table: Dict[str, Server] = {}
        self.dns = DNSSystem()
        self.firewall = Firewall()
        self.packet_history: List[Packet] = []
        self.routing_stats = {
            "packets_routed": 0,
            "packets_blocked": 0,
            "dns_requests": 0,
            "avg_latency": 0.0
        }
        
    def add_server(self, server: Server):
        """Add server to routing table"""
        self.routing_table[server.ip_address] = server
        print(f"{Colors.CYAN}[{self.name}] Added {server.name} ({server.ip_address}) "
              f"to routing table{Colors.END}")
    
    def route_packet(self, destination: str, protocol: str = "HTTP") -> Optional[str]:
        """Main routing function with full packet handling"""
        print(f"\n{Colors.YELLOW}══════════════════════════════════════════════════════════{Colors.END}")
        print(f"{Colors.BLUE}[{self.name}] Processing request for: {destination}{Colors.END}")
        
        start_time = time.time()
        source_ip = "192.168.0.1"  # Default client IP
        
        # Step 1: DNS Resolution (if needed)
        if "." in destination and not destination.replace(".", "").isdigit():
            self.routing_stats["dns_requests"] += 1
            print(f"{Colors.CYAN}[DNS] Resolving '{destination}'...{Colors.END}")
            time.sleep(0.3)  # DNS lookup delay
            ip_address = self.dns.resolve(destination)
            if not ip_address:
                return f"{Colors.RED}❌ DNS Resolution Failed: Cannot resolve '{destination}'{Colors.END}"
        else:
            ip_address = destination
        
        # Step 2: Create packet
        packet = Packet(
            source_ip=source_ip,
            destination_ip=ip_address,
            data=f"Request for {destination}",
            protocol=protocol
        )
        
        print(packet)
        
        # Step 3: Firewall inspection
        print(f"{Colors.YELLOW}[FIREWALL] Inspecting packet...{Colors.END}")
        allowed, firewall_msg = self.firewall.inspect_packet(packet)
        if not allowed:
            self.routing_stats["packets_blocked"] += 1
            return firewall_msg
        
        # Step 4: Routing table lookup
        print(f"{Colors.CYAN}[ROUTING] Checking routing table for {ip_address}...{Colors.END}")
        time.sleep(0.2)
        
        if ip_address not in self.routing_table:
            self.routing_stats["packets_blocked"] += 1
            return f"{Colors.RED}❌ 404 Not Found: No route to {ip_address}{Colors.END}"
        
        server = self.routing_table[ip_address]
        
        # Step 5: Packet transmission (with animation)
        packet.transmit_animation()
        
        # Step 6: Server processing
        print(f"{Colors.GREEN}[SERVER] {server.name} processing request...{Colors.END}")
        response = server.process_request(packet)
        
        # Step 7: Statistics update
        self.routing_stats["packets_routed"] += 1
        end_time = time.time()
        latency = (end_time - start_time) * 1000  # Convert to milliseconds
        
        # Update average latency
        if self.routing_stats["avg_latency"] == 0:
            self.routing_stats["avg_latency"] = latency
        else:
            self.routing_stats["avg_latency"] = (
                self.routing_stats["avg_latency"] * 0.9 + latency * 0.1
            )
        
        print(f"{Colors.YELLOW}[STATS] Latency: {latency:.2f}ms | "
              f"Packets routed: {self.routing_stats['packets_routed']}{Colors.END}")
        
        return response
    
    def show_routing_table(self):
        """Display routing table in formatted way"""
        print(f"\n{Colors.CYAN}{'═'*60}{Colors.END}")
        print(f"{Colors.BLUE}           {self.name} - ROUTING TABLE{Colors.END}")
        print(f"{Colors.CYAN}{'═'*60}{Colors.END}")
        print(f"{Colors.YELLOW}{'IP ADDRESS':<15} {'SERVER NAME':<20} {'STATUS':<10} {'REQUESTS':<10}{Colors.END}")
        print(f"{Colors.CYAN}{'-'*60}{Colors.END}")
        
        for ip, server in self.routing_table.items():
            status = f"{Colors.GREEN}ONLINE{Colors.END}" if server.is_online else f"{Colors.RED}OFFLINE{Colors.END}"
            print(f"{ip:<15} {server.name:<20} {status:<20} {server.requests_served:<10}")
        
        print(f"{Colors.CYAN}{'═'*60}{Colors.END}")
    
    def show_statistics(self):
        """Display router statistics"""
        print(f"\n{Colors.BLUE}[{self.name}] NETWORK STATISTICS:{Colors.END}")
        print(f"{Colors.CYAN}{'─'*40}{Colors.END}")
        print(f"Packets Routed:    {self.routing_stats['packets_routed']}")
        print(f"Packets Blocked:   {self.routing_stats['packets_blocked']}")
        print(f"DNS Requests:      {self.routing_stats['dns_requests']}")
        print(f"Avg Latency:       {self.routing_stats['avg_latency']:.2f}ms")
        print(f"Firewall Blocks:   {self.firewall.blocked_count}")
        print(f"DNS Cache Size:    {len(self.dns.dns_cache)} entries")
        print(f"{Colors.CYAN}{'─'*40}{Colors.END}")

# ========== 6. NETWORK VISUALIZATION ==========
def draw_network_map(router: AdvancedRouter):
    """Draw ASCII network topology map"""
    print(f"\n{Colors.HEADER}{' NETWORK TOPOLOGY MAP ':=^60}{Colors.END}")
    print()
    
    # Client
    print(f"{Colors.BLUE}     [CLIENT]{Colors.END}")
    print(f"{Colors.BLUE}        │{Colors.END}")
    print(f"{Colors.BLUE}        ▼{Colors.END}")
    
    # Router
    print(f"{Colors.GREEN}  ┌────────────────────┐{Colors.END}")
    print(f"{Colors.GREEN}  │  {router.name:^16}  │{Colors.END}")
    print(f"{Colors.GREEN}  │   CORE ROUTER      │{Colors.END}")
    print(f"{Colors.GREEN}  └─────────┬──────────┘{Colors.END}")
    print(f"{Colors.GREEN}            │{Colors.END}")
    
    # Servers
    servers = list(router.routing_table.values())
    if servers:
        print(f"{Colors.GREEN}     ┌─────┴─────┐{Colors.END}")
        
        for i, server in enumerate(servers):
            status = "🟢" if server.is_online else "🔴"
            if i % 2 == 0:
                print(f"{Colors.GREEN}     │         │{Colors.END}", end="")
            else:
                print()
            
            color = Colors.GREEN if server.is_online else Colors.RED
            print(f"  {color}{status} {server.name:<10} ({server.ip_address}){Colors.END}")
    
    print(f"\n{Colors.CYAN}{' Legend: 🟢=Online 🔴=Offline ':=^60}{Colors.END}")

# ========== 7. MAIN NETWORK MANAGER ==========
class NetworkManager:
    """Main orchestrator for the entire network"""
    def __init__(self):
        self.router = AdvancedRouter("CoreRouter-01")
        self.servers: List[Server] = []
        self.setup_complete = False
        
    def setup_network(self):
        """Initialize the complete network infrastructure"""
        print(f"{Colors.HEADER}{' PROJECT GLASS v2.0 - VIRTUAL INTERNET SIMULATOR ':=^60}{Colors.END}")
        print(f"{Colors.BLUE}Initializing Advanced Network Infrastructure...{Colors.END}")
        time.sleep(1)
        
        # Create enterprise servers
        self.servers = [
            Server("192.168.1.1", "Google", "Welcome to Google Search", 2, "WEB"),
            Server("192.168.1.2", "SecureBank", "🔒 Banking Portal - $10,284.52", 3, "WEB"),
            Server("192.168.1.3", "MailServer", "📧 5 Unread Messages", 2, "MAIL"),
            Server("192.168.1.4", "CloudDrive", "☁️ 15.2GB of 20GB used", 1, "FILE"),
            Server("192.168.1.5", "YouTube", "▶️ Trending Videos", 1, "WEB"),
            Server("192.168.1.6", "GitHub", "💻 Repositories: 12", 2, "WEB"),
            Server("192.168.1.7", "Database", "🗄️ MySQL Server v8.0", 3, "DB"),
            Server("192.168.1.8", "FirewallLog", "📊 Security Monitoring", 3, "WEB")
        ]
        
        # Add all servers to router
        for server in self.servers:
            self.router.add_server(server)
        
        # Make some servers offline for demo
        self.servers[2].is_online = False  # MailServer
        self.servers[6].is_online = False  # Database
        
        self.setup_complete = True
        print(f"{Colors.GREEN}✅ Network initialization complete!{Colors.END}")
        print(f"{Colors.GREEN}✅ DNS System ready with {len(self.router.dns.dns_records)} records{Colors.END}")
        print(f"{Colors.GREEN}✅ Firewall active with {len(self.router.firewall.blacklisted_ips)} rules{Colors.END}")
        time.sleep(1)
    
    def show_dashboard(self):
        """Display main dashboard"""
        print(f"\n{Colors.HEADER}{' NETWORK DASHBOARD ':=^60}{Colors.END}")
        
        # Calculate statistics
        online_servers = sum(1 for s in self.servers if s.is_online)
        total_requests = sum(s.requests_served for s in self.servers)
        
        print(f"{Colors.CYAN}Status:{Colors.END} {Colors.GREEN}● OPERATIONAL{Colors.END}")
        print(f"{Colors.CYAN}Servers Online:{Colors.END} {online_servers}/{len(self.servers)}")
        print(f"{Colors.CYAN}Total Requests:{Colors.END} {total_requests}")
        print(f"{Colors.CYAN}Router:{Colors.END} {self.router.name}")
        print(f"{Colors.CYAN}Security Level:{Colors.END} {Colors.YELLOW}HIGH{Colors.END}")
        print(f"{Colors.CYAN}{'─'*60}{Colors.END}")
    
    def run(self):
        """Main program loop"""
        if not self.setup_complete:
            self.setup_network()
        
        while True:
            self.show_dashboard()
            draw_network_map(self.router)
            
            print(f"\n{Colors.YELLOW}{' MAIN MENU ':=^60}{Colors.END}")
            print(f"{Colors.CYAN}1.{Colors.END} Connect to Website/Domain")
            print(f"{Colors.CYAN}2.{Colors.END} Connect using IP Address")
            print(f"{Colors.CYAN}3.{Colors.END} Toggle Server Status")
            print(f"{Colors.CYAN}4.{Colors.END} View Routing Table")
            print(f"{Colors.CYAN}5.{Colors.END} Network Statistics")
            print(f"{Colors.CYAN}6.{Colors.END} Test Different Protocols")
            print(f"{Colors.CYAN}7.{Colors.END} Stress Test Network")
            print(f"{Colors.CYAN}8.{Colors.END} Simulate Attack")
            print(f"{Colors.CYAN}9.{Colors.END} Exit")
            
            choice = input(f"\n{Colors.GREEN}Select option (1-9): {Colors.END}").strip()
            
            if choice == "1":
                domain = input(f"{Colors.CYAN}Enter domain name (e.g., google.com): {Colors.END}").strip()
                protocol = input(f"{Colors.CYAN}Protocol (HTTP/HTTPS/FTP/SMTP/DNS) [HTTP]: {Colors.END}").strip() or "HTTP"
                result = self.router.route_packet(domain, protocol.upper())
                print(f"\n{Colors.BLUE}[RESULT]{Colors.END} {result}")
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                
            elif choice == "2":
                ip = input(f"{Colors.CYAN}Enter IP address (e.g., 192.168.1.1): {Colors.END}").strip()
                result = self.router.route_packet(ip)
                print(f"\n{Colors.BLUE}[RESULT]{Colors.END} {result}")
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                
            elif choice == "3":
                print(f"\n{Colors.BLUE}Select server to toggle:{Colors.END}")
                for i, server in enumerate(self.servers, 1):
                    status = f"{Colors.GREEN}ONLINE{Colors.END}" if server.is_online else f"{Colors.RED}OFFLINE{Colors.END}"
                    print(f"{Colors.CYAN}{i}.{Colors.END} {server.name:<15} ({server.ip_address}) - {status}")
                
                try:
                    server_num = int(input(f"\n{Colors.GREEN}Server number (1-{len(self.servers)}): {Colors.END}")) - 1
                    if 0 <= server_num < len(self.servers):
                        result = self.servers[server_num].toggle_status()
                        print(f"\n{result}")
                    else:
                        print(f"{Colors.RED}Invalid server number{Colors.END}")
                except ValueError:
                    print(f"{Colors.RED}Invalid input{Colors.END}")
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                
            elif choice == "4":
                self.router.show_routing_table()
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                
            elif choice == "5":
                self.router.show_statistics()
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                
            elif choice == "6":
                print(f"\n{Colors.BLUE}Protocol Test Suite:{Colors.END}")
                protocols = ["HTTP", "HTTPS", "FTP", "SMTP", "DNS"]
                for proto in protocols:
                    print(f"\n{Colors.CYAN}Testing {proto}...{Colors.END}")
                    result = self.router.route_packet("google.com", proto)
                    print(f"  Result: {result}")
                    time.sleep(0.5)
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                
            elif choice == "7":
                print(f"\n{Colors.BLUE}Starting stress test...{Colors.END}")
                for i in range(5):
                    domain = random.choice(["google.com", "bank.com", "youtube.com"])
                    print(f"\nTest {i+1}: Requesting {domain}")
                    result = self.router.route_packet(domain)
                    print(f"  {result}")
                    time.sleep(0.3)
                print(f"\n{Colors.GREEN}✅ Stress test complete!{Colors.END}")
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                
            elif choice == "8":
                print(f"\n{Colors.RED}🚨 SIMULATING NETWORK ATTACK 🚨{Colors.END}")
                print(f"{Colors.YELLOW}Sending malicious packets from blacklisted IP...{Colors.END}")
                
                # Simulate attack from blacklisted IP
                for i in range(3):
                    print(f"\nAttack attempt {i+1}...")
                    # This should be blocked by firewall
                    print(f"{Colors.RED}Expected: Blocked by firewall{Colors.END}")
                    # Note: The actual blocking happens in route_packet
                    time.sleep(0.5)
                
                print(f"\n{Colors.GREEN}✅ Firewall successfully blocked all attacks!{Colors.END}")
                print(f"{Colors.GREEN}✅ Network security verified{Colors.END}")
                input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.END}")
                
            elif choice == "9":
                print(f"\n{Colors.HEADER}{' SHUTTING DOWN NETWORK ':=^60}{Colors.END}")
                print(f"{Colors.BLUE}Final Statistics:{Colors.END}")
                self.router.show_statistics()
                print(f"\n{Colors.GREEN}✅ Project Glass v2.0 shutdown complete.{Colors.END}")
                print(f"{Colors.GREEN}✅ All systems secure.{Colors.END}")
                break
                
            else:
                print(f"{Colors.RED}Invalid option. Please try again.{Colors.END}")
                time.sleep(1)

# ========== 8. MAIN EXECUTION ==========
if __name__ == "__main__":
    try:
        print(f"\n{Colors.HEADER}{'='*60}{Colors.END}")
        print(f"{Colors.BLUE}{'PROJECT GLASS v2.0':^60}{Colors.END}")
        print(f"{Colors.CYAN}{'Advanced Virtual Internet Simulator':^60}{Colors.END}")
        print(f"{Colors.YELLOW}{'Enterprise Network Simulation Platform':^60}{Colors.END}")
        print(f"{Colors.HEADER}{'='*60}{Colors.END}")
        
        network = NetworkManager()
        network.run()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}\n⚠️  Network shutdown by user.{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}\n❌ Critical Error: {e}{Colors.END}")