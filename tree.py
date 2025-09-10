#!/usr/bin/env python3
"""
tree.py - 以树状结构展示文件夹内容

作者: AI Assistant
版本: 1.0
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Optional, Tuple
import datetime
import stat

# 配置常量
VERSION = "1.0"
DEFAULT_ENCODING = "utf-8"

# 树形符号
PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "

# 文件类型图标
FILE_ICONS = {
    'directory': '📁',
    'file': '📄',
    'image': '🖼️',
    'video': '🎬',
    'audio': '🎵',
    'archive': '📦',
    'code': '💻',
    'text': '📝',
    'pdf': '📕',
    'excel': '📊',
    'word': '📝',
    'powerpoint': '📽️',
    'executable': '⚙️',
    'link': '🔗',
    'hidden': '👻'
}

# 文件扩展名映射
FILE_EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico'],
    'video': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
    'archive': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
    'code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php', '.rb', '.go'],
    'text': ['.txt', '.md', '.rst'],
    'pdf': ['.pdf'],
    'excel': ['.xls', '.xlsx'],
    'word': ['.doc', '.docx'],
    'powerpoint': ['.ppt', '.pptx'],
    'executable': ['.exe', '.msi', '.deb', '.rpm', '.app']
}

class Colors:
    """ANSI颜色代码"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    
    # 文本颜色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # 背景颜色
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

class FileInfo:
    """文件信息类"""
    def __init__(self, path: Path, is_last: bool = False, prefix: str = ""):
        self.path = path
        self.is_last = is_last
        self.prefix = prefix
        self.name = path.name
        self.is_dir = path.is_dir()
        self.is_hidden = self.name.startswith('.') if sys.platform != 'win32' else self._is_hidden_windows()
        self.size = self._get_size()
        self.mod_time = datetime.datetime.fromtimestamp(path.stat().st_mtime)
        self.file_type = self._get_file_type()
        self.permissions = self._get_permissions()
        
    def _is_hidden_windows(self) -> bool:
        """检查Windows隐藏文件"""
        try:
            return bool(os.stat(self.path).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
        except:
            return False
    
    def _get_size(self) -> str:
        """获取文件大小（格式化）"""
        if self.is_dir:
            return ""
        
        try:
            size_bytes = self.path.stat().st_size
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if size_bytes < 1024.0:
                    return f"{size_bytes:.1f}{unit}"
                size_bytes /= 1024.0
            return f"{size_bytes:.1f}PB"
        except:
            return "N/A"
    
    def _get_file_type(self) -> str:
        """获取文件类型"""
        if self.is_dir:
            return 'directory'
        
        if self.path.is_symlink():
            return 'link'
        
        ext = self.path.suffix.lower()
        
        for file_type, extensions in FILE_EXTENSIONS.items():
            if ext in extensions:
                return file_type
        
        return 'file'
    
    def _get_permissions(self) -> str:
        """获取文件权限"""
        try:
            st = self.path.stat()
            return stat.filemode(st.st_mode)
        except:
            return "??????????"

class TreeGenerator:
    """树形结构生成器"""
    
    def __init__(self, 
                 show_hidden: bool = False,
                 max_depth: Optional[int] = None,
                 show_size: bool = False,
                 show_date: bool = False,
                 show_permissions: bool = False,
                 use_colors: bool = True,
                 use_icons: bool = True,
                 include_patterns: Optional[List[str]] = None,
                 exclude_patterns: Optional[List[str]] = None):
        self.show_hidden = show_hidden
        self.max_depth = max_depth
        self.show_size = show_size
        self.show_date = show_date
        self.show_permissions = show_permissions
        self.use_colors = use_colors and self._supports_color()
        self.use_icons = use_icons
        self.include_patterns = include_patterns or []
        self.exclude_patterns = exclude_patterns or []
        self.total_dirs = 0
        self.total_files = 0
        
    def _supports_color(self) -> bool:
        """检查终端是否支持颜色"""
        if sys.platform == 'win32':
            return os.environ.get('TERM_PROGRAM') == 'vscode' or os.environ.get('WT_SESSION') is not None
        return True
    
    def _colorize(self, text: str, color: str) -> str:
        """给文本添加颜色"""
        if not self.use_colors:
            return text
        return f"{color}{text}{Colors.RESET}"
    
    def _get_icon(self, file_type: str) -> str:
        """获取文件类型图标"""
        if not self.use_icons:
            return ""
        return FILE_ICONS.get(file_type, '📄')
    
    def _should_include(self, path: Path) -> bool:
        """检查是否应该包含该文件/目录"""
        name = path.name
        
        # 检查隐藏文件
        if not self.show_hidden and name.startswith('.'):
            return False
        
        # 检查包含模式
        if self.include_patterns:
            if not any(pattern in name for pattern in self.include_patterns):
                return False
        
        # 检查排除模式
        if self.exclude_patterns:
            if any(pattern in name for pattern in self.exclude_patterns):
                return False
        
        return True
    
    def _format_file_info(self, file_info: FileInfo) -> str:
        """格式化文件信息"""
        parts = []
        
        # 图标和名称
        icon = self._get_icon(file_info.file_type)
        name = file_info.name
        
        # 颜色处理
        if file_info.is_dir:
            name = self._colorize(name, Colors.BLUE + Colors.BOLD)
        elif file_info.is_hidden:
            name = self._colorize(name, Colors.DIM)
        elif file_info.file_type == 'executable':
            name = self._colorize(name, Colors.GREEN)
        elif file_info.file_type == 'link':
            name = self._colorize(name, Colors.CYAN)
        
        name_part = f"{icon} {name}" if icon else name
        parts.append(name_part)
        
        # 添加额外信息
        if self.show_size and file_info.size:
            parts.append(self._colorize(f"[{file_info.size}]", Colors.YELLOW))
        
        if self.show_date:
            date_str = file_info.mod_time.strftime("%Y-%m-%d %H:%M")
            parts.append(self._colorize(f"[{date_str}]", Colors.CYAN))
        
        if self.show_permissions:
            parts.append(self._colorize(f"[{file_info.permissions}]", Colors.MAGENTA))
        
        return " ".join(parts)
    
    def _generate_tree(self, directory: Path, prefix: str = "", depth: int = 0) -> List[str]:
        """递归生成树形结构"""
        if self.max_depth is not None and depth > self.max_depth:
            return []
        
        entries = []
        try:
            # 获取目录内容
            paths = sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
            
            # 过滤文件
            filtered_paths = [p for p in paths if self._should_include(p)]
            
            for i, path in enumerate(filtered_paths):
                is_last = i == len(filtered_paths) - 1
                
                # 创建文件信息
                file_info = FileInfo(path, is_last, prefix)
                
                # 更新统计
                if path.is_dir():
                    self.total_dirs += 1
                else:
                    self.total_files += 1
                
                # 生成当前行的前缀
                connector = ELBOW if is_last else TEE
                current_prefix = prefix + connector
                
                # 添加当前条目
                formatted_info = self._format_file_info(file_info)
                entries.append(f"{current_prefix} {formatted_info}")
                
                # 递归处理子目录
                if path.is_dir() and not path.is_symlink():
                    extension = SPACE_PREFIX if is_last else PIPE_PREFIX
                    entries.extend(self._generate_tree(path, prefix + extension, depth + 1))
                    
        except PermissionError:
            entries.append(f"{prefix}{ELBOW} {self._colorize('【权限拒绝】', Colors.RED)}")
        except Exception as e:
            entries.append(f"{prefix}{ELBOW} {self._colorize(f'【错误: {e}】', Colors.RED)}")
        
        return entries
    
    def generate(self, root_path: Path) -> str:
        """生成完整的树形结构"""
        self.total_dirs = 0
        self.total_files = 0
        
        # 根目录信息
        root_info = FileInfo(root_path)
        icon = self._get_icon('directory')
        root_name = self._colorize(root_path.name, Colors.BLUE + Colors.BOLD)
        root_display = f"{icon} {root_name}" if icon else root_name
        
        lines = [root_display]
        
        # 生成树形结构
        tree_lines = self._generate_tree(root_path)
        lines.extend(tree_lines)
        
        # 添加统计信息
        lines.append("")
        lines.append(self._colorize(f"📊 统计信息:", Colors.BOLD))
        lines.append(f"  目录: {self.total_dirs}")
        lines.append(f"  文件: {self.total_files}")
        lines.append(f"  总计: {self.total_dirs + self.total_files}")
        
        return "\n".join(lines)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="以树状结构展示文件夹内容",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                    # 显示当前目录
  %(prog)s /path/to/dir       # 显示指定目录
  %(prog)s -a                 # 显示隐藏文件
  %(prog)s -L 2               # 限制深度为2层
  %(prog)s -s                 # 显示文件大小
  %(prog)s -d                 # 显示修改日期
  %(prog)s -p                 # 显示权限
  %(prog)s --no-color         # 禁用颜色输出
  %(prog)s --no-icons         # 禁用图标
  %(prog)s -i "*.py" "*.md"   # 只显示包含这些模式的文件
  %(prog)s -e "*.pyc" "__pycache__"  # 排除这些模式的文件
        """
    )
    
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='要显示的目录路径 (默认: 当前目录)'
    )
    
    parser.add_argument(
        '-a', '--all',
        action='store_true',
        help='显示所有文件，包括隐藏文件'
    )
    
    parser.add_argument(
        '-L', '--level',
        type=int,
        metavar='N',
        help='限制显示的层级深度'
    )
    
    parser.add_argument(
        '-s', '--size',
        action='store_true',
        help='显示文件大小'
    )
    
    parser.add_argument(
        '-d', '--date',
        action='store_true',
        help='显示文件修改日期'
    )
    
    parser.add_argument(
        '-p', '--permissions',
        action='store_true',
        help='显示文件权限'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='禁用颜色输出'
    )
    
    parser.add_argument(
        '--no-icons',
        action='store_true',
        help='禁用图标'
    )
    
    parser.add_argument(
        '-i', '--include',
        nargs='+',
        metavar='PATTERN',
        help='只显示包含指定模式的文件'
    )
    
    parser.add_argument(
        '-e', '--exclude',
        nargs='+',
        metavar='PATTERN',
        help='排除包含指定模式的文件'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'%(prog)s {VERSION}'
    )
    
    args = parser.parse_args()
    
    # 验证路径
    root_path = Path(args.path).expanduser().resolve()
    
    if not root_path.exists():
        print(f"错误: 路径 '{root_path}' 不存在", file=sys.stderr)
        sys.exit(1)
    
    if not root_path.is_dir():
        print(f"错误: 路径 '{root_path}' 不是目录", file=sys.stderr)
        sys.exit(1)
    
    # 创建生成器
    generator = TreeGenerator(
        show_hidden=args.all,
        max_depth=args.level,
        show_size=args.size,
        show_date=args.date,
        show_permissions=args.permissions,
        use_colors=not args.no_color,
        use_icons=not args.no_icons,
        include_patterns=args.include,
        exclude_patterns=args.exclude
    )
    
    try:
        # 生成并输出树形结构
        tree_output = generator.generate(root_path)
        print(tree_output)
    except KeyboardInterrupt:
        print("\n操作被用户中断", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()