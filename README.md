# Advanced CLI File Manager

A professional-grade command-line interface tool built with Click and Rich, providing advanced file management capabilities with beautiful terminal output and intuitive user experience.

## 🎯 Project Overview

This CLI tool demonstrates advanced command-line application development using modern Python libraries. It combines powerful file management functionality with a rich, interactive terminal interface that rivals GUI applications.

## 🚀 Key Features

### 🎨 Rich Terminal Interface
- **Beautiful Output** - Rich formatting with colors, tables, and progress bars
- **Interactive Elements** - Progress indicators, confirmations, and prompts
- **Syntax Highlighting** - Code preview with automatic language detection
- **Tree Visualization** - Directory structure display with icons

### 📁 Advanced File Operations
- **Smart Listing** - Detailed file information with multiple sort options
- **File Analysis** - Hash calculation, size analysis, and statistics
- **Bulk Operations** - Copy, move, delete multiple files with progress tracking
- **Archive Management** - Create and extract ZIP/TAR archives
- **Directory Analysis** - Comprehensive statistics and insights

### 🛠️ Professional Features
- **Error Handling** - Graceful error management and user feedback
- **Permission Handling** - Proper handling of file system permissions
- **Cross-Platform** - Works on Windows, macOS, and Linux
- **Extensible Design** - Easy to add new commands and features

## 🔧 Installation

### Method 1: Direct Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run directly
python filemanager.py --help
```

### Method 2: Package Installation
```bash
# Install as a package
pip install -e .

# Use as system command
fm --help
filemanager --help
```

## 📚 Usage Examples

### Basic File Operations

#### List Directory Contents
```bash
# Simple listing
python filemanager.py list

# Detailed view with sorting
python filemanager.py list --details --sort size --path /home/user

# Show hidden files
python filemanager.py list --hidden
```

#### Directory Tree View
```bash
# Show directory structure
python filemanager.py tree

# Custom depth and show hidden
python filemanager.py tree --depth 5 --hidden --path /project
```

#### File Information & Analysis
```bash
# Calculate file hash
python filemanager.py hash document.pdf --algorithm sha256

# View file contents with syntax highlighting
python filemanager.py view script.py --lines 50

# Analyze directory statistics
python filemanager.py analyze --path /home/user/projects
```

### File Operations

#### Copy & Move Files
```bash
# Copy file
python filemanager.py copy source.txt destination.txt

# Copy directory recursively
python filemanager.py copy /source/dir /dest/dir --recursive

# Move files
python filemanager.py move old_name.txt new_name.txt
```

#### Archive Operations
```bash
# Create ZIP archive
python filemanager.py archive backup.zip file1.txt file2.txt folder/

# Create TAR.GZ archive
python filemanager.py archive project.tar.gz src/ docs/ --format tar.gz

# Extract archive
python filemanager.py extract backup.zip --destination /restore/path
```

#### Delete Operations
```bash
# Delete files (with confirmation)
python filemanager.py delete unwanted.txt temp.log

# Delete directory recursively
python filemanager.py delete old_project/ --recursive

# Force delete without confirmation
python filemanager.py delete *.tmp --force
```

## 🎨 Rich Interface Features

### Visual Elements
- **📊 Tables** - Formatted data display with headers and styling
- **🌳 Trees** - Hierarchical directory structure visualization
- **📦 Panels** - Information boxes with borders and titles
- **⏰ Progress Bars** - Real-time operation progress tracking
- **🎨 Syntax Highlighting** - Code preview with language detection

### Interactive Components
- **✅ Confirmations** - Safe operations with user confirmation
- **📝 Prompts** - Interactive input collection
- **🔄 Spinners** - Visual feedback for long operations
- **📊 Statistics** - Comprehensive data analysis and reporting

## 🏗️ Technical Architecture

### Command Structure
```
CLI Root
├── list        - Directory listing with options
├── tree        - Directory tree visualization  
├── hash        - File hash calculation
├── copy        - File/directory copying
├── move        - File/directory moving
├── delete      - File/directory deletion
├── archive     - Archive creation
├── extract     - Archive extraction
├── view        - File content viewing
└── analyze     - Directory analysis
```

### Core Components

#### FileManager Class
```python
class FileManager:
    """Core file operations with rich output"""
    
    def format_size(self, size_bytes):
        """Human-readable size formatting"""
    
    def get_file_info(self, path):
        """Comprehensive file metadata"""
    
    def calculate_hash(self, file_path, algorithm):
        """Secure hash calculation"""
    
    def list_directory(self, path, options):
        """Advanced directory listing"""
```

#### Click Command Framework
- **Argument Parsing** - Robust command-line argument handling
- **Option Validation** - Type checking and value validation  
- **Help Generation** - Automatic help documentation
- **Command Grouping** - Organized command structure

#### Rich Integration
- **Console Management** - Centralized output handling
- **Progress Tracking** - Visual operation feedback
- **Error Display** - Beautiful error formatting
- **Data Presentation** - Professional table and panel layouts

## 📊 Sample Outputs

### Directory Listing (Detailed View)
```
📂 Contents of: /home/user/project

┏━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Type ┃ Name               ┃ Size     ┃ Modified         ┃ Permissions ┃
┡━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 🐍   │ main.py           │ 2.4KB    │ 2024-01-01 15:30│ -rw-r--r--    │
│ 📁   │ src               │ -        │ 2024-01-01 14:20│ drwxr-xr-x    │
│ 📋   │ requirements.txt  │ 156B     │ 2024-01-01 12:00│ -rw-r--r--    │
└──────┴────────────────────┴──────────┴──────────────────┴─────────────┘

📊 Summary: 1 directories, 2 files, 2.6KB total
```

### Directory Tree View
```
🌳 Directory Tree (depth: 3)

📁 project
├── 🐍 main.py
├── 📋 requirements.txt
├── 📁 src
│   ├── 🐍 __init__.py
│   ├── 🐍 utils.py
│   └── 📁 modules
│       ├── 🐍 parser.py
│       └── 🐍 formatter.py
└── 📁 tests
    ├── 🐍 test_main.py
    └── 🐍 test_utils.py
```

### File Hash Calculation
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                🔐 File Hash (SHA256)             ┃
┠───────────────────────────────────────────────────┨
┃ File: document.pdf                                ┃
┃ Size: 1.2MB                                       ┃
┃ SHA256: a1b2c3d4e5f6...                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

### Directory Analysis
```
📊 Directory Analysis Summary

┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Metric             ┃ Value      ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ 📁 Total Directories │ 15        │
│ 📄 Total Files      │ 247       │
│ 💾 Total Size       │ 15.3MB    │
│ 📊 Average File Size │ 63.4KB    │
└────────────────────┴────────────┘
```

## 💼 Professional Applications

This CLI tool demonstrates skills valuable for:

### DevOps & System Administration
- **File Management** - Automated file operations and maintenance
- **System Monitoring** - Directory analysis and space management
- **Backup Operations** - Archive creation and data management
- **Script Integration** - Command-line automation capabilities

### Software Development
- **Project Management** - Code organization and file operations
- **Build Tools** - Integration with development workflows  
- **Deployment Scripts** - Automated file deployment and management
- **Development Tools** - Enhanced terminal productivity

### Data Engineering
- **File Processing** - Bulk file operations and transformations
- **Data Migration** - File movement and organization
- **Archive Management** - Data compression and extraction
- **Quality Assurance** - File integrity verification

## 🔧 Customization & Extension

### Adding New Commands
```python
@cli.command()
@click.argument('target')
@click.option('--option', help='Command option')
def new_command(target, option):
    """New command description"""
    # Implementation here
    pass
```

### Custom File Operations
```python
def custom_operation(self, path: Path) -> Dict:
    """Add custom file analysis"""
    # Custom logic here
    return results
```

### Rich Formatting Extensions
```python
# Custom progress bars
with Progress(SpinnerColumn(), TextColumn(...)) as progress:
    task = progress.add_task("Processing...", total=100)

# Custom tables and panels
table = Table(title="Custom Data")
panel = Panel(content, title="Results")
```

## 📚 Learning Outcomes

### CLI Development Mastery
- **Click Framework** - Professional command-line interface development
- **Argument Parsing** - Robust input handling and validation
- **Help Systems** - Automatic documentation generation
- **Error Handling** - User-friendly error management

### Rich Terminal Applications
- **Advanced Formatting** - Colors, tables, progress bars, panels
- **Interactive Elements** - Prompts, confirmations, real-time updates
- **Cross-Platform** - Consistent appearance across operating systems
- **Performance** - Efficient rendering and resource management

### File System Operations
- **Path Manipulation** - Modern Python pathlib usage
- **Permission Handling** - Secure file system operations
- **Error Recovery** - Graceful handling of file system errors
- **Cross-Platform** - OS-independent file operations

## 🚀 Advanced Features

### Planned Enhancements
- [ ] **Plugin System** - Extensible architecture for custom commands
- [ ] **Configuration Files** - User preferences and settings
- [ ] **Network Operations** - Remote file management capabilities  
- [ ] **Database Integration** - File metadata storage and querying
- [ ] **Compression Options** - Advanced archive formats and settings
- [ ] **Parallel Processing** - Multi-threaded file operations
- [ ] **Watch Mode** - Real-time directory monitoring
- [ ] **Integration APIs** - Programmatic access to file operations

### Performance Optimizations
- **Lazy Loading** - Efficient handling of large directories
- **Caching** - Intelligent metadata caching
- **Streaming** - Memory-efficient large file processing
- **Parallel Operations** - Concurrent file processing

---

*This CLI tool showcases advanced command-line application development skills suitable for DevOps, system administration, and software engineering roles.*
