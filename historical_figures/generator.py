#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历史人物人设生成器
根据用户输入的历史人物姓名，动态生成人设提示词
"""

import json
import os
import sys
from typing import Dict, List, Optional, Tuple

class HistoricalFigureGenerator:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__), 
                "freeform_config.json"
            )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.alias_mapping = self.config.get('alias_mapping', {})
        self.dynasty_keywords = self.config.get('dynasty_keywords', {})
        self.identity_types = self.config.get('identity_types', {})
    
    def normalize_name(self, name: str) -> str:
        """标准化人名，处理别名"""
        name = name.strip()
        
        # 直接匹配
        if name in self.alias_mapping:
            return name
        
        # 别名反向查找
        for standard_name, aliases in self.alias_mapping.items():
            if name in aliases or name == standard_name:
                return standard_name
        
        return name
    
    def detect_dynasty(self, name: str) -> Tuple[str, str]:
        """
        检测人物所属朝代
        返回: (朝代名称, 检测依据)
        """
        for dynasty, keywords in self.dynasty_keywords.items():
            if name in keywords:
                return dynasty, f"关键词匹配"
        
        # 默认根据常见知识推断
        dynasty_hints = {
            "先秦": ["孔", "孟", "庄", "老", "屈", "墨", "韩", "孙", "扁"],
            "秦朝": ["秦", "嬴", "李", "赵", "蒙", "王"],
            "汉朝": ["刘", "项", "张", "司", "班", "霍", "卫"],
            "魏晋南北朝": ["曹", "陶", "王", "谢", "嵇", "阮", "祖"],
            "唐朝": ["李", "杜", "白", "王", "韩", "柳", "玄", "武", "狄"],
            "宋朝": ["赵", "苏", "李", "岳", "朱", "王", "司", "欧", "范", "辛", "陆", "文", "包"],
            "元朝": ["忽", "成", "铁", "关", "马", "郑", "白", "郭", "黄"],
            "明朝": ["朱", "王", "郑", "李", "徐", "张", "海", "戚", "于", "刘", "方", "解", "杨", "唐", "祝", "文", "吴", "罗", "施", "冯", "凌", "魏", "袁", "史"],
            "清朝": ["康", "乾", "雍", "努", "皇", "顺", "嘉", "道", "咸", "同", "光", "宣", "慈", "和", "纪", "刘", "林", "曾", "李", "左", "张", "袁", "曹", "蒲", "吴", "郑", "纳", "仓"],
            "民国": ["孙", "蒋", "袁", "张", "吴", "冯", "阎", "李", "白", "鲁", "胡", "梁", "康", "谭", "蔡", "陈", "李", "周", "毛", "朱", "彭", "林", "刘", "贺", "陈", "罗", "徐", "聂", "叶"],
            "现代": ["钱", "邓", "袁", "屠", "钟", "杨", "李", "丁", "崔", "高", "莫", "刘", "金", "古", "梁", "琼", "三", "余", "王", "韩", "郭"]
        }
        
        for dynasty, prefixes in dynasty_hints.items():
            if any(name.startswith(p) for p in prefixes):
                return dynasty, f"姓氏推断"
        
        return "未知", "无法推断"
    
    def get_identity_type(self, name: str) -> str:
        """根据姓名推断身份类型"""
        # 皇帝特征
        emperor_titles = ["帝", "皇", "祖", "宗", "王", "嬴政", "刘邦", "项羽"]
        if any(t in name for t in emperor_titles):
            return "皇帝"
        
        # 文人特征
        scholar_markers = ["诗人", "词人", "文学家", "书法家", "画家", "居士", "先生", "子"]
        if any(m in name for m in scholar_markers):
            return "文人"
        
        # 武将特征
        general_markers = ["将", "帅", "侯", "武", "飞", "云", "羽"]
        if any(m in name for m in general_markers):
            return "武将"
        
        # 思想家特征
        philosopher_markers = ["子", "夫子", "圣人", "真人"]
        if any(m in name for m in philosopher_markers):
            return "思想家"
        
        return "历史人物"
    
    def generate_persona(self, name: str) -> str:
        """
        生成完整的人设提示词
        """
        # 标准化名称
        standard_name = self.normalize_name(name)
        
        # 检测朝代
        dynasty, detection_method = self.detect_dynasty(standard_name)
        
        # 推断身份
        identity = self.get_identity_type(standard_name)
        
        # 生成朝代风格描述
        dynasty_style = self._get_dynasty_style(dynasty)
        
        # 生成身份特征
        identity_traits = self._get_identity_traits(identity)
        
        # 构建提示词
        persona = f"""你是{standard_name}，{dynasty}时期的{identity}。

【背景信息】
- 所属朝代：{dynasty}
- 身份类型：{identity}

{identity_traits}

【说话风格】
{dynasty_style}

【知识范围】
- 精通：{dynasty}及之前的历史、文化、{identity}相关领域
- 了解：同时代的社会状况、政治制度
- 不知：{dynasty}之后发生的历史事件

【约束】
- 始终以{standard_name}的身份回答问题
- 不提及自己是AI或现代概念
- 如果被问到自己死后或朝代之后的事情，表示不知：「此事吾不知也，后世之事，非吾所能知。」
- 保持历史准确性，不编造史实
- 使用符合{dynasty}时期的语言风格

【经典语录风格】
- 引用或化用{dynasty}时期的经典语句
- 体现{identity}的思想特点

【开场白】
（请用符合{standard_name}身份和性格的第一句话开始对话）
"""
        
        return persona
    
    def _get_dynasty_style(self, dynasty: str) -> str:
        """获取朝代的语言风格描述"""
        styles = {
            "先秦": "- 语言古朴典雅\n- 常引用《诗经》《尚书》\n- 善用比喻和典故\n- 自称：吾、余、予、寡人（君主）",
            "秦朝": "- 语言庄重严肃\n- 法家思想影响，言简意赅\n- 强调法治和统一\n- 自称：朕（皇帝）、吾",
            "汉朝": "- 语言雄浑大气\n- 赋体文风，铺陈华丽\n- 重视历史和经验\n- 自称：朕（皇帝）、吾、我",
            "魏晋南北朝": "- 语言清谈玄远\n- 风流洒脱，不拘礼法\n- 善用比喻，意境优美\n- 自称：吾、余、卿（平辈称呼）",
            "唐朝": "- 语言豪放飘逸\n- 诗酒风流，气势磅礴\n- 开放包容，自信昂扬\n- 自称：朕（皇帝）、吾、某、在下",
            "宋朝": "- 语言婉约含蓄\n- 理学思辨，逻辑严密\n- 文人雅致，品味细腻\n- 自称：朕（皇帝）、吾、某、在下、奴家（女性）",
            "元朝": "- 语言融合蒙汉特色\n- 元曲通俗直白\n- 实用主义，不拘泥形式\n- 自称：朕（皇帝）、吾、咱",
            "明朝": "- 语言通俗直白\n- 小说兴起，贴近生活\n- 理学与心学并存\n- 自称：朕（皇帝）、吾、我、在下",
            "清朝": "- 语言满汉融合\n- 既有古典雅致，又有近代气息\n- 自称：朕（皇帝）、吾、我、奴才（大臣对皇帝）",
            "民国": "- 语言古今交融\n- 白话文与文言文并用\n- 思想开放，追求变革\n- 自称：我、吾、在下、先生",
            "现代": "- 语言现代白话\n- 专业术语与日常用语结合\n- 自信开放，面向世界\n- 自称：我",
            "未知": "- 语言庄重典雅\n- 符合古代文人或官员的身份\n- 自称：吾、我、在下"
        }
        return styles.get(dynasty, styles["未知"])
    
    def _get_identity_traits(self, identity: str) -> str:
        """获取身份类型的特征描述"""
        traits = {
            "皇帝": """【性格特点】
- 雄才大略，有政治远见
- 威严霸气，但不失亲和
- 善于用人，知人善任
- 关心治国和历史评价

【说话风格】
- 语气威严，居高临下
- 喜欢讨论治国理政
- 使用「朕」作为自称
- 言简意赅，不拖泥带水""",
            
            "文人": """【性格特点】
- 才华横溢，学富五车
- 情感丰富，多愁善感
- 追求理想，向往自由
- 重视友情，珍视知音

【说话风格】
- 语言文雅，富有才情
- 喜欢引用诗词文章
- 善于用典，意境深远
- 语气亲切，平易近人""",
            
            "武将": """【性格特点】
- 豪迈直率，重情重义
- 忠勇爱国，视死如归
- 讲究信义，一诺千金
- 勇猛善战，不畏强敌

【说话风格】
- 语气豪迈，直来直去
- 言简意赅，不绕弯子
- 重义气，讲承诺
- 谈论军事和战绩时充满激情""",
            
            "思想家": """【性格特点】
- 追求真理，勇于探索
- 深思熟虑，逻辑严密
- 善于教化，循循善诱
- 坚持己见，不随波逐流

【说话风格】
- 语言深刻，富有哲理
- 善用比喻和类比
- 逻辑清晰，论证严密
- 语气平和但充满智慧""",
            
            "历史人物": """【性格特点】
- 根据历史记载，展现真实的人物性格
- 符合时代背景的行为方式
- 体现历史人物的独特魅力

【说话风格】
- 符合所属朝代的语言特点
- 体现个人身份和地位
- 保持历史真实性和一致性"""
        }
        return traits.get(identity, traits["历史人物"])
    
    def interactive_mode(self):
        """交互模式"""
        print("🏛️  历史人物对话系统 - 自由输入模式")
        print("=" * 50)
        print()
        print("使用说明：")
        print("  - 直接输入历史人物姓名（如：李白、苏轼、秦始皇）")
        print("  - 输入 '退出' 结束程序")
        print("  - 输入 '帮助' 查看说明")
        print()
        
        while True:
            user_input = input("请输入历史人物姓名: ").strip()
            
            if user_input.lower() in ['退出', 'exit', 'quit', 'q']:
                print("\n感谢使用，再见！")
                break
            
            if user_input.lower() in ['帮助', 'help', 'h']:
                print("\n使用说明：")
                print("  - 输入任何中国历史人物姓名")
                print("  - 系统会自动识别并生成人设")
                print("  - 支持别名（如：李太白、苏东坡）")
                print()
                continue
            
            if not user_input:
                continue
            
            # 生成人设
            print(f"\n📝 正在生成 {user_input} 的人设...")
            print()
            
            persona = self.generate_persona(user_input)
            
            print("=" * 50)
            print(persona)
            print("=" * 50)
            print()


def main():
    """主函数"""
    generator = HistoricalFigureGenerator()
    
    # 如果有命令行参数，直接生成
    if len(sys.argv) > 1:
        name = sys.argv[1]
        print(generator.generate_persona(name))
    else:
        # 进入交互模式
        generator.interactive_mode()


if __name__ == "__main__":
    main()
