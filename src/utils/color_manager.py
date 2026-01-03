import hashlib
from PyQt6.QtGui import QColor

class ColorManager:
    """
    颜色管理器：用于生成美观的课程颜色
    """
    
    # 预设的现代配色板 (低饱和度，护眼)
    # 格式: Hex Code
    PALETTE = [
        "#FF8A80", # Red
        "#FFD180", # Orange
        "#FFFF8D", # Yellow
        "#CCFF90", # Light Green
        "#A7FFEB", # Teal
        "#80D8FF", # Light Blue
        "#82B1FF", # Blue
        "#B388FF", # Purple
        "#F48FB1", # Pink
        "#CFD8DC", # Blue Grey
        "#FFCCBC", # Deep Orange
        "#F0F4C3", # Lime
    ]

    @staticmethod
    def get_color_for_course(course_name: str) -> str:
        """
        根据课程名称生成固定的颜色
        """
        if not course_name:
            return "#E0E0E0" # 默认灰色
            
        # 使用 MD5 哈希确保同一个课程名永远对应同一个颜色
        hash_obj = hashlib.md5(course_name.encode('utf-8'))
        hash_int = int(hash_obj.hexdigest(), 16)
        
        # 从调色板中取色
        index = hash_int % len(ColorManager.PALETTE)
        return ColorManager.PALETTE[index]