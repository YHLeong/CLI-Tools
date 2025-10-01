"""
Advanced CLI File Manager
A feature-rich command-line interface tool built with Click and Rich
for advanced file management and system utilities.
"""

import click
from rich.console import Console
from rich.table import Table
from rich.tree import Tree
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.text import Text
from pathlib import Path
import os
import shutil
import json
import hashlib
import mimetypes
from datetime import datetime
import stat
import subprocess
import sys
from typing import List, Dict, Optional
import zipfile
import tarfile

# Initialize Rich console
console = Console()

class FileManager:
    """Advanced file management operations with rich output"""
    
    def __init__(self):
        self.console = console
        self.current_path = Path.cwd()
    
    def format_size(self, size_bytes: int) -> str:
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f}PB"
    
    def get_file_info(self, path: Path) -> Dict:
        """Get detailed file information"""
        try:
            stat_info = path.stat()
            return {
                'name': path.name,
                'path': str(path),
                'size': stat_info.st_size,
                'size_formatted': self.format_size(stat_info.st_size),
                'modified': datetime.fromtimestamp(stat_info.st_mtime),
                'created': datetime.fromtimestamp(stat_info.st_ctime),
                'permissions': stat.filemode(stat_info.st_mode),
                'is_dir': path.is_dir(),
                'is_file': path.is_file(),
                'suffix': path.suffix.lower(),
                'mime_type': mimetypes.guess_type(str(path))[0] or 'unknown'
            }
        except (OSError, PermissionError) as e:
            return {'error': str(e), 'name': path.name}
    
    def calculate_hash(self, file_path: Path, algorithm: str = 'md5') -> str:
        """Calculate file hash"""
        hash_func = getattr(hashlib, algorithm.lower())()
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_func.update(chunk)
            return hash_func.hexdigest()
        except Exception as e:
            return f"Error: {e}"
    
    def list_directory(self, path: Path, show_hidden: bool = False, 
                      sort_by: str = 'name') -> List[Dict]:
        """List directory contents with detailed information"""
        try:
            items = []
            for item in path.iterdir():
                if not show_hidden and item.name.startswith('.'):
                    continue
                
                info = self.get_file_info(item)
                if 'error' not in info:
                    items.append(info)
            
            # Sort items
            if sort_by == 'size':
                items.sort(key=lambda x: x['size'], reverse=True)
            elif sort_by == 'modified':
                items.sort(key=lambda x: x['modified'], reverse=True)
            elif sort_by == 'type':
                items.sort(key=lambda x: (x['is_file'], x['suffix']))
            else:  # name
                items.sort(key=lambda x: (x['is_file'], x['name'].lower()))
            
            return items
        except PermissionError:
            console.print(f"[red]Permission denied: {path}[/red]")
            return []
    
    def display_directory_tree(self, path: Path, max_depth: int = 3, 
                              show_hidden: bool = False):
        """Display directory structure as a tree"""
        def add_tree_items(tree_node, current_path: Path, current_depth: int):
            if current_depth >= max_depth:
                return
            
            try:
                items = sorted(current_path.iterdir(), 
                             key=lambda x: (x.is_file(), x.name.lower()))
                
                for item in items:
                    if not show_hidden and item.name.startswith('.'):
                        continue
                    
                    if item.is_dir():
                        branch = tree_node.add(f"📁 [bold blue]{item.name}[/bold blue]")
                        add_tree_items(branch, item, current_depth + 1)
                    else:
                        icon = self.get_file_icon(item.suffix)
                        tree_node.add(f"{icon} {item.name}")
                        
            except PermissionError:
                tree_node.add("[red]Permission denied[/red]")
        
        tree = Tree(f"📁 [bold blue]{path.name or path}[/bold blue]")
        add_tree_items(tree, path, 0)
        console.print(tree)
    
    def get_file_icon(self, suffix: str) -> str:
        """Get icon for file type"""
        icons = {
            '.py': '🐍', '.js': '🟨', '.html': '🌐', '.css': '🎨',
            '.json': '📋', '.xml': '📄', '.txt': '📝', '.md': '📖',
            '.jpg': '🖼️', '.png': '🖼️', '.gif': '🖼️', '.svg': '🖼️',
            '.mp4': '🎬', '.mp3': '🎵', '.wav': '🎵', '.avi': '🎬',
            '.pdf': '📕', '.doc': '📘', '.docx': '📘', '.xls': '📗',
            '.zip': '📦', '.rar': '📦', '.7z': '📦', '.tar': '📦',
            '.exe': '⚙️', '.msi': '⚙️', '.deb': '⚙️', '.rpm': '⚙️'
        }
        return icons.get(suffix.lower(), '📄')

@click.group()
@click.version_option(version='1.0.0')
@click.pass_context
def cli(ctx):
    """
    🚀 Advanced CLI File Manager
    
    A powerful command-line tool for file management and system utilities.
    Built with Click and Rich for an enhanced terminal experience.
    """
    ctx.ensure_object(dict)
    ctx.obj['file_manager'] = FileManager()

@cli.command()
@click.option('--path', '-p', default='.', help='Directory path to list')
@click.option('--hidden', '-a', is_flag=True, help='Show hidden files')
@click.option('--sort', '-s', type=click.Choice(['name', 'size', 'modified', 'type']), 
              default='name', help='Sort by field')
@click.option('--details', '-l', is_flag=True, help='Show detailed information')
@click.pass_context
def list(ctx, path: str, hidden: bool, sort: str, details: bool):
    """📂 List directory contents with rich formatting"""
    file_manager = ctx.obj['file_manager']
    target_path = Path(path).resolve()
    
    if not target_path.exists():
        console.print(f"[red]Error: Path '{path}' does not exist[/red]")
        return
    
    if not target_path.is_dir():
        console.print(f"[red]Error: '{path}' is not a directory[/red]")
        return
    
    console.print(f"\n[bold cyan]📂 Contents of: {target_path}[/bold cyan]\n")
    
    items = file_manager.list_directory(target_path, hidden, sort)
    
    if not items:
        console.print("[yellow]Directory is empty[/yellow]")
        return
    
    if details:
        # Create detailed table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Type", style="dim", width=4)
        table.add_column("Name", style="cyan", min_width=20)
        table.add_column("Size", style="green", justify="right")
        table.add_column("Modified", style="blue")
        table.add_column("Permissions", style="yellow")
        
        for item in items:
            icon = "📁" if item['is_dir'] else file_manager.get_file_icon(item['suffix'])
            name = f"[bold]{item['name']}[/bold]" if item['is_dir'] else item['name']
            size = "-" if item['is_dir'] else item['size_formatted']
            modified = item['modified'].strftime("%Y-%m-%d %H:%M")
            
            table.add_row(icon, name, size, modified, item['permissions'])
        
        console.print(table)
    else:
        # Simple grid layout
        columns = 3
        for i in range(0, len(items), columns):
            row_items = items[i:i+columns]
            row = []
            
            for item in row_items:
                icon = "📁" if item['is_dir'] else file_manager.get_file_icon(item['suffix'])
                style = "bold cyan" if item['is_dir'] else "white"
                row.append(f"{icon} [{style}]{item['name']}[/{style}]")
            
            console.print("  ".join(f"{item:<30}" for item in row))
    
    # Show summary
    total_items = len(items)
    total_dirs = sum(1 for item in items if item['is_dir'])
    total_files = total_items - total_dirs
    total_size = sum(item['size'] for item in items if not item['is_dir'])
    
    console.print(f"\n[dim]📊 Summary: {total_dirs} directories, "
                 f"{total_files} files, {file_manager.format_size(total_size)} total[/dim]")

@cli.command()
@click.option('--path', '-p', default='.', help='Directory path for tree view')
@click.option('--depth', '-d', default=3, help='Maximum tree depth')
@click.option('--hidden', '-a', is_flag=True, help='Show hidden files')
@click.pass_context
def tree(ctx, path: str, depth: int, hidden: bool):
    """🌳 Display directory structure as a tree"""
    file_manager = ctx.obj['file_manager']
    target_path = Path(path).resolve()
    
    if not target_path.exists():
        console.print(f"[red]Error: Path '{path}' does not exist[/red]")
        return
    
    if not target_path.is_dir():
        console.print(f"[red]Error: '{path}' is not a directory[/red]")
        return
    
    console.print(f"\n[bold cyan]🌳 Directory Tree (depth: {depth})[/bold cyan]\n")
    file_manager.display_directory_tree(target_path, depth, hidden)

@cli.command()
@click.argument('file_path')
@click.option('--algorithm', '-a', default='md5', 
              type=click.Choice(['md5', 'sha1', 'sha256', 'sha512']),
              help='Hash algorithm to use')
@click.pass_context
def hash(ctx, file_path: str, algorithm: str):
    """🔐 Calculate file hash"""
    file_manager = ctx.obj['file_manager']
    target_path = Path(file_path)
    
    if not target_path.exists():
        console.print(f"[red]Error: File '{file_path}' does not exist[/red]")
        return
    
    if not target_path.is_file():
        console.print(f"[red]Error: '{file_path}' is not a file[/red]")
        return
    
    console.print(f"\n[bold cyan]🔐 Calculating {algorithm.upper()} hash...[/bold cyan]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Hashing file...", total=None)
        hash_value = file_manager.calculate_hash(target_path, algorithm)
    
    file_info = file_manager.get_file_info(target_path)
    
    panel = Panel(
        f"[bold white]File:[/bold white] {target_path.name}\n"
        f"[bold white]Size:[/bold white] {file_info['size_formatted']}\n"
        f"[bold white]{algorithm.upper()}:[/bold white] [green]{hash_value}[/green]",
        title=f"🔐 File Hash ({algorithm.upper()})",
        border_style="green"
    )
    
    console.print(panel)

@cli.command()
@click.argument('source')
@click.argument('destination')
@click.option('--recursive', '-r', is_flag=True, help='Copy directories recursively')
@click.option('--force', '-f', is_flag=True, help='Overwrite existing files')
@click.pass_context
def copy(ctx, source: str, destination: str, recursive: bool, force: bool):
    """📋 Copy files or directories"""
    source_path = Path(source)
    dest_path = Path(destination)
    
    if not source_path.exists():
        console.print(f"[red]Error: Source '{source}' does not exist[/red]")
        return
    
    if dest_path.exists() and not force:
        if not Confirm.ask(f"Destination '{destination}' exists. Overwrite?"):
            console.print("[yellow]Operation cancelled[/yellow]")
            return
    
    try:
        if source_path.is_file():
            console.print(f"[cyan]📋 Copying file: {source} → {destination}[/cyan]")
            shutil.copy2(source_path, dest_path)
        elif source_path.is_dir() and recursive:
            console.print(f"[cyan]📋 Copying directory: {source} → {destination}[/cyan]")
            if dest_path.exists():
                shutil.rmtree(dest_path)
            shutil.copytree(source_path, dest_path)
        elif source_path.is_dir():
            console.print("[red]Error: Use --recursive flag to copy directories[/red]")
            return
        
        console.print("[green]✅ Copy completed successfully[/green]")
        
    except Exception as e:
        console.print(f"[red]Error during copy: {e}[/red]")

@cli.command()
@click.argument('source')
@click.argument('destination')
@click.pass_context
def move(ctx, source: str, destination: str):
    """🔄 Move/rename files or directories"""
    source_path = Path(source)
    dest_path = Path(destination)
    
    if not source_path.exists():
        console.print(f"[red]Error: Source '{source}' does not exist[/red]")
        return
    
    if dest_path.exists():
        if not Confirm.ask(f"Destination '{destination}' exists. Overwrite?"):
            console.print("[yellow]Operation cancelled[/yellow]")
            return
    
    try:
        console.print(f"[cyan]🔄 Moving: {source} → {destination}[/cyan]")
        shutil.move(str(source_path), str(dest_path))
        console.print("[green]✅ Move completed successfully[/green]")
        
    except Exception as e:
        console.print(f"[red]Error during move: {e}[/red]")

@cli.command()
@click.argument('paths', nargs=-1)
@click.option('--recursive', '-r', is_flag=True, help='Delete directories recursively')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation')
@click.pass_context
def delete(ctx, paths: tuple, recursive: bool, force: bool):
    """🗑️ Delete files or directories"""
    if not paths:
        console.print("[red]Error: No paths specified[/red]")
        return
    
    for path_str in paths:
        path = Path(path_str)
        
        if not path.exists():
            console.print(f"[yellow]Warning: '{path_str}' does not exist[/yellow]")
            continue
        
        if not force:
            if not Confirm.ask(f"Delete '{path_str}'?", default=False):
                console.print(f"[yellow]Skipped: {path_str}[/yellow]")
                continue
        
        try:
            if path.is_file():
                path.unlink()
                console.print(f"[green]✅ Deleted file: {path_str}[/green]")
            elif path.is_dir() and recursive:
                shutil.rmtree(path)
                console.print(f"[green]✅ Deleted directory: {path_str}[/green]")
            elif path.is_dir():
                console.print(f"[red]Error: Use --recursive flag to delete directories: {path_str}[/red]")
            
        except Exception as e:
            console.print(f"[red]Error deleting {path_str}: {e}[/red]")

@cli.command()
@click.argument('archive_path')
@click.argument('files', nargs=-1)
@click.option('--format', '-f', type=click.Choice(['zip', 'tar', 'tar.gz']), 
              default='zip', help='Archive format')
@click.pass_context
def archive(ctx, archive_path: str, files: tuple, format: str):
    """📦 Create archives from files/directories"""
    if not files:
        console.print("[red]Error: No files specified[/red]")
        return
    
    archive_file = Path(archive_path)
    
    console.print(f"[cyan]📦 Creating {format} archive: {archive_path}[/cyan]")
    
    try:
        if format == 'zip':
            with zipfile.ZipFile(archive_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file_path in files:
                    path = Path(file_path)
                    if path.exists():
                        if path.is_file():
                            zf.write(path, path.name)
                        elif path.is_dir():
                            for file in path.rglob('*'):
                                if file.is_file():
                                    zf.write(file, file.relative_to(path.parent))
                        console.print(f"[green]  ✅ Added: {file_path}[/green]")
                    else:
                        console.print(f"[yellow]  ⚠️  Skipped: {file_path} (not found)[/yellow]")
        
        elif format in ['tar', 'tar.gz']:
            mode = 'w:gz' if format == 'tar.gz' else 'w'
            with tarfile.open(archive_file, mode) as tf:
                for file_path in files:
                    path = Path(file_path)
                    if path.exists():
                        tf.add(path, path.name)
                        console.print(f"[green]  ✅ Added: {file_path}[/green]")
                    else:
                        console.print(f"[yellow]  ⚠️  Skipped: {file_path} (not found)[/yellow]")
        
        console.print(f"[green]✅ Archive created: {archive_path}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error creating archive: {e}[/red]")

@cli.command()
@click.argument('archive_path')
@click.option('--destination', '-d', default='.', help='Extraction destination')
@click.pass_context
def extract(ctx, archive_path: str, destination: str):
    """📂 Extract archives"""
    archive_file = Path(archive_path)
    dest_dir = Path(destination)
    
    if not archive_file.exists():
        console.print(f"[red]Error: Archive '{archive_path}' does not exist[/red]")
        return
    
    console.print(f"[cyan]📂 Extracting: {archive_path} → {destination}[/cyan]")
    
    try:
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_file, 'r') as zf:
                zf.extractall(dest_dir)
        elif archive_path.endswith(('.tar', '.tar.gz', '.tgz')):
            with tarfile.open(archive_file, 'r:*') as tf:
                tf.extractall(dest_dir)
        else:
            console.print("[red]Error: Unsupported archive format[/red]")
            return
        
        console.print("[green]✅ Extraction completed successfully[/green]")
        
    except Exception as e:
        console.print(f"[red]Error extracting archive: {e}[/red]")

@cli.command()
@click.argument('file_path')
@click.option('--lines', '-n', default=10, help='Number of lines to display')
@click.option('--syntax', '-s', help='Syntax highlighting language')
@click.pass_context
def view(ctx, file_path: str, lines: int, syntax: Optional[str]):
    """👁️ View file contents with syntax highlighting"""
    file = Path(file_path)
    
    if not file.exists():
        console.print(f"[red]Error: File '{file_path}' does not exist[/red]")
        return
    
    if not file.is_file():
        console.print(f"[red]Error: '{file_path}' is not a file[/red]")
        return
    
    try:
        with open(file, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Auto-detect syntax if not specified
        if not syntax:
            suffix = file.suffix.lower()
            syntax_map = {
                '.py': 'python', '.js': 'javascript', '.html': 'html',
                '.css': 'css', '.json': 'json', '.xml': 'xml',
                '.yaml': 'yaml', '.yml': 'yaml', '.sql': 'sql',
                '.sh': 'bash', '.bat': 'batch', '.md': 'markdown'
            }
            syntax = syntax_map.get(suffix, 'text')
        
        # Truncate if too many lines
        lines_in_content = content.count('\n') + 1
        if lines < lines_in_content:
            content_lines = content.split('\n')
            content = '\n'.join(content_lines[:lines])
            truncated = True
        else:
            truncated = False
        
        syntax_obj = Syntax(content, syntax, theme="monokai", line_numbers=True)
        
        panel = Panel(
            syntax_obj,
            title=f"👁️ {file.name}" + (f" (first {lines} lines)" if truncated else ""),
            border_style="cyan"
        )
        
        console.print(panel)
        
        if truncated:
            console.print(f"[dim]... showing first {lines} of {lines_in_content} lines[/dim]")
    
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")

@cli.command()
@click.option('--path', '-p', default='.', help='Directory to analyze')
@click.pass_context
def analyze(ctx, path: str):
    """📊 Analyze directory statistics"""
    file_manager = ctx.obj['file_manager']
    target_path = Path(path).resolve()
    
    if not target_path.exists():
        console.print(f"[red]Error: Path '{path}' does not exist[/red]")
        return
    
    console.print(f"[bold cyan]📊 Analyzing: {target_path}[/bold cyan]")
    
    # Collect statistics
    total_files = 0
    total_dirs = 0
    total_size = 0
    file_types = {}
    largest_files = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Scanning files...", total=None)
        
        for item in target_path.rglob('*'):
            try:
                if item.is_file():
                    total_files += 1
                    size = item.stat().st_size
                    total_size += size
                    
                    # Track file types
                    ext = item.suffix.lower() or 'no extension'
                    file_types[ext] = file_types.get(ext, 0) + 1
                    
                    # Track largest files
                    largest_files.append((item, size))
                    
                elif item.is_dir():
                    total_dirs += 1
                    
            except (PermissionError, OSError):
                continue
    
    # Sort and limit largest files
    largest_files.sort(key=lambda x: x[1], reverse=True)
    largest_files = largest_files[:10]
    
    # Create summary table
    summary_table = Table(title="📊 Directory Analysis Summary", show_header=True)
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="white")
    
    summary_table.add_row("📁 Total Directories", f"{total_dirs:,}")
    summary_table.add_row("📄 Total Files", f"{total_files:,}")
    summary_table.add_row("💾 Total Size", file_manager.format_size(total_size))
    summary_table.add_row("📊 Average File Size", 
                         file_manager.format_size(total_size // total_files) if total_files > 0 else "0B")
    
    console.print(summary_table)
    
    # File types table
    if file_types:
        types_table = Table(title="📂 File Types Distribution", show_header=True)
        types_table.add_column("Extension", style="cyan")
        types_table.add_column("Count", style="green", justify="right")
        types_table.add_column("Percentage", style="yellow", justify="right")
        
        sorted_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:15]
        
        for ext, count in sorted_types:
            percentage = (count / total_files) * 100 if total_files > 0 else 0
            types_table.add_row(ext, f"{count:,}", f"{percentage:.1f}%")
        
        console.print(types_table)
    
    # Largest files table
    if largest_files:
        large_table = Table(title="📋 Largest Files", show_header=True)
        large_table.add_column("File", style="cyan")
        large_table.add_column("Size", style="green", justify="right")
        
        for file_path, size in largest_files:
            relative_path = file_path.relative_to(target_path)
            large_table.add_row(str(relative_path), file_manager.format_size(size))
        
        console.print(large_table)

if __name__ == '__main__':
    cli()