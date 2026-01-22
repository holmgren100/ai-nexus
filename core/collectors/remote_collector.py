"""Remote data collector - syncs data from spoke servers via SSH"""
import paramiko
import os
from pathlib import Path
import subprocess

class RemoteCollector:
    """Collects data from remote spoke servers"""
    
    def __init__(self, host, user, ssh_key, paths):
        self.host = host
        self.user = user
        self.ssh_key = os.path.expanduser(ssh_key)
        self.paths = paths
        
    def test_connection(self):
        """Test SSH connection to spoke server"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=self.host,
                username=self.user,
                key_filename=self.ssh_key,
                timeout=10
            )
            
            # Test command
            stdin, stdout, stderr = ssh.exec_command('hostname')
            hostname = stdout.read().decode().strip()
            ssh.close()
            
            return True, hostname
        except Exception as e:
            return False, str(e)
    
    def sync_logs(self, local_dir):
        """Sync logs from spoke server"""
        local_dir = Path(local_dir)
        local_dir.mkdir(parents=True, exist_ok=True)
        
        remote_log = self.paths.get('logs', '/root/solbottrad/bot.log')
        local_log = local_dir / 'bot.log'
        
        # Use rsync for efficient sync
        cmd = [
            'rsync', '-avz',
            '-e', f'ssh -i {self.ssh_key} -o StrictHostKeyChecking=no',
            f'{self.user}@{self.host}:{remote_log}',
            str(local_log)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                # Get file size
                size_mb = local_log.stat().st_size / (1024 * 1024)
                return True, f"Synced {size_mb:.1f} MB"
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)
    
    def sync_data(self, local_dir):
        """Sync ML data from spoke server"""
        local_dir = Path(local_dir)
        local_dir.mkdir(parents=True, exist_ok=True)
        
        remote_data = self.paths.get('data', '/root/solbottrad/data/')
        
        # Sync entire data directory
        cmd = [
            'rsync', '-avz',
            '-e', f'ssh -i {self.ssh_key} -o StrictHostKeyChecking=no',
            '--include', '*.csv',
            '--include', '*.json',
            '--exclude', '*',
            f'{self.user}@{self.host}:{remote_data}',
            str(local_dir) + '/'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                # Count files
                files = list(local_dir.glob('*.csv')) + list(local_dir.glob('*.json'))
                return True, f"Synced {len(files)} files"
            else:
                return False, result.stderr
        except Exception as e:
            return False, str(e)
    
    def get_bot_status(self):
        """Get trading bot status from spoke server"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=self.host,
                username=self.user,
                key_filename=self.ssh_key,
                timeout=10
            )
            
            # Check service status
            stdin, stdout, stderr = ssh.exec_command('systemctl is-active solana-trading-bot')
            status = stdout.read().decode().strip()
            
            ssh.close()
            
            return status == "active", status
        except Exception as e:
            return False, str(e)
