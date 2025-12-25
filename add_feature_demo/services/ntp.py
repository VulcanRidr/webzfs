"""
NTP Configuration Service
Handles NTP (Network Time Protocol) configuration for both Linux and FreeBSD
"""
import subprocess
import platform
from pathlib import Path
from typing import Dict, List, Optional


class NTPService:
    """Service for managing NTP configuration across Linux and FreeBSD"""
    
    def __init__(self):
        self.os_type = self._detect_os()
        self.config_path = self._get_config_path()
        self.service_name = self._get_service_name()
    
    def _detect_os(self) -> str:
        """Detect the operating system"""
        system = platform.system().lower()
        if 'freebsd' in system:
            return 'freebsd'
        else:
            # Default to Linux - handles all Linux distributions
            return 'linux'
    
    def _get_config_path(self) -> Path:
        """Get NTP configuration file path based on OS"""
        if self.os_type == 'freebsd':
            return Path('/etc/ntp.conf')
        else:
            # Linux default
            return Path('/etc/ntp.conf')
    
    def _get_service_name(self) -> str:
        """Get NTP service name"""
        # Both Linux and FreeBSD use ntpd
        return 'ntpd'
    
    def get_status(self) -> Dict[str, any]:
        """Get NTP service status"""
        try:
            if self.os_type == 'linux':
                result = subprocess.run(
                    ['sudo', 'systemctl', 'status', self.service_name],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                is_running = result.returncode == 0
                output = result.stdout
            elif self.os_type == 'freebsd':
                result = subprocess.run(
                    ['sudo', 'service', self.service_name, 'status'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                is_running = 'is running' in result.stdout.lower()
                output = result.stdout
            else:
                is_running = False
                output = "Unsupported operating system"
            
            return {
                'running': is_running,
                'service_name': self.service_name,
                'output': output,
                'os_type': self.os_type
            }
        except Exception as e:
            return {
                'running': False,
                'service_name': self.service_name,
                'output': f"Error: {str(e)}",
                'os_type': self.os_type
            }
    
    def get_config(self) -> str:
        """Read current NTP configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error reading configuration: {str(e)}"
    
    def get_servers(self) -> List[str]:
        """Extract NTP servers from configuration"""
        servers = []
        try:
            config = self.get_config()
            for line in config.split('\n'):
                line = line.strip()
                if line.startswith('server ') or line.startswith('pool '):
                    parts = line.split()
                    if len(parts) >= 2:
                        servers.append(parts[1])
        except Exception:
            pass
        return servers
    
    def update_config(self, config_content: str) -> bool:
        """Update NTP configuration file"""
        try:
            # Write to temporary file first
            temp_path = Path('/tmp/ntp.conf.tmp')
            with open(temp_path, 'w') as f:
                f.write(config_content)
            
            # Copy to actual location with sudo
            result = subprocess.run(
                ['sudo', 'cp', str(temp_path), str(self.config_path)],
                capture_output=True,
                timeout=5
            )
            
            # Clean up temp file
            temp_path.unlink()
            
            return result.returncode == 0
        except Exception as e:
            print(f"Error updating config: {e}")
            return False
    
    def restart_service(self) -> bool:
        """Restart NTP service"""
        try:
            if self.os_type == 'linux':
                result = subprocess.run(
                    ['sudo', 'systemctl', 'restart', self.service_name],
                    capture_output=True,
                    timeout=10
                )
            elif self.os_type == 'freebsd':
                result = subprocess.run(
                    ['sudo', 'service', self.service_name, 'restart'],
                    capture_output=True,
                    timeout=10
                )
            else:
                return False
            
            return result.returncode == 0
        except Exception as e:
            print(f"Error restarting service: {e}")
            return False
    
    def enable_service(self) -> bool:
        """Enable NTP service to start on boot"""
        try:
            if self.os_type == 'linux':
                result = subprocess.run(
                    ['sudo', 'systemctl', 'enable', self.service_name],
                    capture_output=True,
                    timeout=5
                )
            elif self.os_type == 'freebsd':
                result = subprocess.run(
                    ['sudo', 'sysrc', f'{self.service_name}_enable=YES'],
                    capture_output=True,
                    timeout=5
                )
            else:
                return False
            
            return result.returncode == 0
        except Exception as e:
            print(f"Error enabling service: {e}")
            return False
    
    def get_time_info(self) -> Dict[str, str]:
        """Get current system time information"""
        try:
            # Get system time
            result = subprocess.run(
                ['date', '+%Y-%m-%d %H:%M:%S %Z'],
                capture_output=True,
                text=True,
                timeout=2
            )
            system_time = result.stdout.strip() if result.returncode == 0 else "Unknown"
            
            # Get NTP sync status using ntpq
            result = subprocess.run(
                ['ntpq', '-p'],
                capture_output=True,
                text=True,
                timeout=2
            )
            sync_status = result.stdout if result.returncode == 0 else "Not available"
            
            return {
                'system_time': system_time,
                'sync_status': sync_status
            }
        except Exception as e:
            return {
                'system_time': "Error",
                'sync_status': f"Error: {str(e)}"
            }
