"""
强智教务系统通用导入器 - 智能穿透版 v2 (Auto-Layout Edition)

核心更新：
1. [表头侦测]: 自动识别"星期日"开头还是"星期一"开头，自动识别是否有节次列。
2. [Iframe 穿透]: 保持了之前的 Iframe 穿透能力。
3. [积分寻址]: 保持了积分算法定位表格的能力。
"""

import re
import uuid
import logging
from typing import List, Tuple, Optional

from bs4 import BeautifulSoup, Tag

try:
    from .base_importer import BaseImporter
    from ..models.course_base import CourseBase
    from ..models.course_detail import CourseDetail
    from ..models.week_type import WeekType
    from ..utils.color_manager import ColorManager
except ImportError:
    from importers.base_importer import BaseImporter
    from models.course_base import CourseBase
    from models.course_detail import CourseDetail
    from models.week_type import WeekType
    from utils.color_manager import ColorManager

logger = logging.getLogger(__name__)

class FrameDetectedError(ValueError):
    def __init__(self, message, inner_url):
        super().__init__(message)
        self.inner_url = inner_url

class QiangZhiImporter(BaseImporter):

    def __init__(
        self,
        school_name: str = "通用强智系统",
        sunday_first: bool = False, # 默认值，会被自动侦测覆盖
        first_col_is_header: bool = False, # 默认值，会被自动侦测覆盖
        split_pattern: str = r'-{10,}',
        table_id: str = 'kbtable',
        cell_class: str = 'kbcontent',
        week_pattern: str = r'([\d\-,]+)\(周\)',
        section_pattern: str = r'\[(\d+)-(\d+)节\]',
        teacher_title: str = '老师',
        location_title: str = '教室',
        week_section_title: str = '周次(节次)',
        odd_week_keyword: str = '单周',
        even_week_keyword: str = '双周',
        exclude_courses: List[str] = None
    ):
        self.school_name = school_name
        self.sunday_first = sunday_first
        self.first_col_is_header = first_col_is_header
        self.split_pattern = split_pattern
        self.table_id = table_id
        self.cell_class = cell_class
        self.week_pattern = week_pattern
        self.section_pattern = section_pattern
        self.teacher_title = teacher_title
        self.location_title = location_title
        self.week_section_title = week_section_title
        self.odd_week_keyword = odd_week_keyword
        self.even_week_keyword = even_week_keyword
        self.exclude_courses = exclude_courses or ["教学资料", ""]
        self.color_manager = ColorManager()

    def get_supported_formats(self) -> List[str]:
        return ['.html', '.htm']

    def get_importer_name(self) -> str:
        return self.school_name

    def _check_iframe_trap(self, soup: BeautifulSoup) -> Optional[str]:
        # 1. 检查是否存在包含 'xskb' 或 'list.do' 的 iframe
        iframe = soup.find('iframe', src=re.compile(r'xskb|list\.do', re.IGNORECASE))
        if iframe:
            return iframe.get('src')
        # 2. 检查是否有 id="Frame1" (南华大学特定)
        frame1 = soup.find(id="Frame1")
        if frame1 and frame1.name == 'iframe':
            return frame1.get('src')
        return None

    def _calculate_table_score(self, element: Tag) -> int:
        score = 0
        text = element.get_text()

        if "星期" in text: score += 10
        if "节次" in text: score += 10

        week_matches = re.findall(r'\d+-\d+\(周\)', text)
        score += len(week_matches) * 5

        section_matches = re.findall(r'\[\d+-\d+节\]', text)
        score += len(section_matches) * 5

        if element.get('id') == self.table_id:
            score += 50

        if len(text) < 50: score = 0
        return score

    def _find_best_table(self, soup: BeautifulSoup) -> Optional[Tag]:
        candidates = []
        tables = soup.find_all('table')
        for tbl in tables:
            score = self._calculate_table_score(tbl)
            if score > 0: candidates.append((score, tbl))

        if not candidates:
            divs = soup.find_all('div')
            for d in divs:
                if len(d.get_text()) > 200:
                    score = self._calculate_table_score(d)
                    if score > 20: candidates.append((score, d))

        candidates.sort(key=lambda x: x[0], reverse=True)
        if candidates: return candidates[0][1]
        return None

    def _autodetect_layout(self, table: Tag):
        """
        [新增] 自动分析表格表头，确定列偏移和星期顺序
        解决"星期错位"问题的核心逻辑
        """
        rows = table.find_all('tr')
        header_row = None

        # 1. 寻找包含"星期"的表头行
        for row in rows:
            text = row.get_text()
            if "星期" in text or "周一" in text:
                header_row = row
                break

        if not header_row:
            return # 没找到表头，维持默认设置

        # 2. 分析列结构
        cells = header_row.find_all(['th', 'td'])
        col_texts = [cell.get_text(strip=True) for cell in cells]

        idx_sun = -1
        idx_mon = -1

        for i, text in enumerate(col_texts):
            if "星期日" in text or "周日" in text:
                idx_sun = i
            elif "星期一" in text or "周一" in text:
                idx_mon = i

        # 3. 判定首列是否为表头 (偏移量)
        # 如果星期一/星期日出现的索引 > 0，说明前面有占位列(如"节次")
        valid_indices = [i for i in [idx_sun, idx_mon] if i >= 0]
        if valid_indices:
            first_day_idx = min(valid_indices)
            if first_day_idx > 0:
                self.first_col_is_header = True
                logger.info(f"[{self.school_name}] 自动修正: 检测到首列为表头列")
            else:
                self.first_col_is_header = False

        # 4. 判定星期顺序 (南华是星期日开头)
        if idx_sun != -1 and idx_mon != -1:
            if idx_sun < idx_mon:
                self.sunday_first = True
                logger.info(f"[{self.school_name}] 自动修正: 检测到星期日排在星期一之前")
            else:
                self.sunday_first = False

    def validate(self, content: str) -> Tuple[bool, str]:
        if not content or not content.strip():
            return False, "内容为空"

        content = content.replace('\u3000', ' ')
        try:
            soup = BeautifulSoup(content, 'html.parser')
        except:
            soup = BeautifulSoup(content, 'lxml')

        if self._check_iframe_trap(soup):
            return False, "检测到Iframe陷阱"

        if not self._find_best_table(soup):
            return False, "未找到有效的课表结构"

        return True, ""

    def parse(self, content: str) -> Tuple[List[CourseBase], List[CourseDetail]]:
        content = content.replace('\u3000', ' ')
        try:
            soup = BeautifulSoup(content, 'html.parser')
        except:
            soup = BeautifulSoup(content, 'lxml')

        inner_url = self._check_iframe_trap(soup)
        if inner_url:
            raise FrameDetectedError("检测到外层框架，请加载内部课表 URL", inner_url)

        table = self._find_best_table(soup)
        if not table:
            raise ValueError("无法定位课表数据")

        # [关键步骤] 解析数据前，先自动侦测布局
        self._autodetect_layout(table)

        course_bases, course_details = [], []
        name_to_id = {}

        rows = table.find_all('tr')
        if not rows: return [], []

        for row in rows:
            td_cells = row.find_all(['td', 'th'])
            if len(td_cells) < 2: continue

            for col_idx, cell in enumerate(td_cells):
                # 跳过表头列 (根据自动侦测结果)
                if self.first_col_is_header and col_idx == 0:
                    continue

                self._process_cell(cell, col_idx, course_bases, course_details, name_to_id)

        return course_bases, course_details

    def _process_cell(self, cell, col_idx, course_bases, course_details, name_to_id):
        detail_div = cell.find('div', class_=self.cell_class)
        if not detail_div:
            divs = cell.find_all('div')
            for d in divs:
                if d.get_text(strip=True):
                    detail_div = d
                    break

        if not detail_div or not detail_div.get_text(strip=True):
            return

        raw_html = str(detail_div)
        segments = re.split(self.split_pattern, raw_html)

        for segment in segments:
            self._parse_segment(segment, col_idx, course_bases, course_details, name_to_id)

    def _parse_segment(self, segment_html, col_idx, course_bases, course_details, name_to_id):
        seg_soup = BeautifulSoup(segment_html, 'html.parser')
        all_text_list = [t.strip() for t in seg_soup.get_text("|").split("|") if t.strip()]
        if not all_text_list: return

        course_name = all_text_list[0]
        course_name = re.sub(r'\s*\(.*?\)$', '', course_name).strip()
        course_name = course_name.replace('&nbsp;', '')
        if course_name in self.exclude_courses: return

        teacher = ""
        location = ""
        week_sec_text = ""

        fonts = seg_soup.find_all('font')
        if fonts:
            for f in fonts:
                title = f.get('title', '')
                text_val = f.get_text(strip=True)
                if title == self.teacher_title: teacher = text_val
                elif title == self.location_title: location = text_val
                elif title == self.week_section_title: week_sec_text = text_val
        else:
            teacher = self._extract_field_from_text(all_text_list, self.teacher_title)
            location = self._extract_field_from_text(all_text_list, self.location_title)
            week_sec_text = self._extract_field_from_text(all_text_list, self.week_section_title)

        sec_match = re.search(self.section_pattern, week_sec_text)
        if not sec_match: return
        start_sec = int(sec_match.group(1))
        end_sec = int(sec_match.group(2))
        step = end_sec - start_sec + 1

        week_ranges = self._parse_complex_weeks(week_sec_text)
        if not week_ranges: return

        if course_name not in name_to_id:
            course_id = str(uuid.uuid4())
            name_to_id[course_name] = course_id
            course_color = self.color_manager.get_color_for_course(course_name)
            course_bases.append(CourseBase(name=course_name, course_id=course_id, color=course_color))
        else:
            course_id = name_to_id[course_name]

        # 计算星期几 (使用自动侦测后的参数)
        day_of_week = self._calculate_day_of_week(col_idx)
        week_type = self._detect_week_type(segment_html)

        for w_start, w_end in week_ranges:
            detail = CourseDetail(
                course_id=course_id, teacher=teacher, location=location,
                day_of_week=day_of_week, start_section=start_sec, step=step,
                start_week=w_start, end_week=w_end, week_type=week_type
            )
            course_details.append(detail)

    def _calculate_day_of_week(self, col_idx: int) -> int:
        effective_idx = col_idx
        # 如果侦测到有表头列，减去偏移
        if self.first_col_is_header and effective_idx > 0:
            effective_idx -= 1

        # 如果侦测到是星期日开头
        if self.sunday_first:
            # 0(Sun)->7, 1(Mon)->1, ...
            return effective_idx if effective_idx != 0 else 7
        else:
            # 0(Mon)->1, 1(Tue)->2...
            return effective_idx + 1

    def _extract_field_from_text(self, text_list: List[str], field_name: str) -> str:
        try:
            if field_name in text_list:
                idx = text_list.index(field_name)
                if idx + 1 < len(text_list): return text_list[idx + 1]
        except: pass
        return ""

    def _detect_week_type(self, text: str) -> WeekType:
        if self.odd_week_keyword in text: return WeekType.ODD_WEEK
        if self.even_week_keyword in text: return WeekType.EVEN_WEEK
        return WeekType.EVERY_WEEK

    def _parse_complex_weeks(self, text: str) -> List[Tuple[int, int]]:
        match = re.search(self.week_pattern, text)
        if not match: return []
        raw_weeks = match.group(1)
        ranges = []
        for part in raw_weeks.split(','):
            part = part.strip()
            if not part: continue
            if '-' in part:
                try:
                    s, e = part.split('-')
                    if s.isdigit() and e.isdigit(): ranges.append((int(s), int(e)))
                except: continue
            elif part.isdigit():
                ranges.append((int(part), int(part)))
        return ranges

