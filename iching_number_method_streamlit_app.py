import streamlit as st
from pathlib import Path

# 后天八卦映射表
BAGUA_MAP = {
    1: "乾", 2: "兑", 3: "离", 4: "震",
    5: "巽", 6: "坎", 7: "艮", 8: "坤"
}

# 完整的六十四卦映射表
HEXAGRAM_MAP = {
    # 乾宫八卦
    ("乾", "乾"): "乾为天",
    ("乾", "坤"): "天地否",
    ("乾", "坎"): "天水讼",
    ("乾", "离"): "天火同人",
    ("乾", "震"): "天雷无妄",
    ("乾", "艮"): "天山遁",
    ("乾", "巽"): "天风姤",
    ("乾", "兑"): "天泽履",
    
    # 坤宫八卦
    ("坤", "坤"): "坤为地",
    ("坤", "乾"): "地天泰",
    ("坤", "坎"): "地水师",
    ("坤", "离"): "地火明夷",
    ("坤", "震"): "地雷复",
    ("坤", "艮"): "地山谦",
    ("坤", "巽"): "地风升",
    ("坤", "兑"): "地泽临",
    
    # 坎宫八卦
    ("坎", "坎"): "坎为水",
    ("坎", "乾"): "水天需",
    ("坎", "坤"): "水地比",
    ("坎", "离"): "水火既济",
    ("坎", "震"): "水雷屯",
    ("坎", "艮"): "水山蹇",
    ("坎", "巽"): "水风井",
    ("坎", "兑"): "水泽节",
    
    # 离宫八卦
    ("离", "离"): "离为火",
    ("离", "乾"): "火天大有",
    ("离", "坤"): "火地晋",
    ("离", "坎"): "火水未济",
    ("离", "震"): "火雷噬嗑",
    ("离", "艮"): "火山旅",
    ("离", "巽"): "火风鼎",
    ("离", "兑"): "火泽睽",
    
    # 震宫八卦
    ("震", "震"): "震为雷",
    ("震", "乾"): "雷天大壮",
    ("震", "坤"): "雷地豫",
    ("震", "坎"): "雷水解",
    ("震", "离"): "雷火丰",
    ("震", "艮"): "雷山小过",
    ("震", "巽"): "雷风恒",
    ("震", "兑"): "雷泽归妹",
    
    # 艮宫八卦
    ("艮", "艮"): "艮为山",
    ("艮", "乾"): "山天大畜",
    ("艮", "坤"): "山地剥",
    ("艮", "坎"): "山水蒙",
    ("艮", "离"): "山火贲",
    ("艮", "震"): "山雷颐",
    ("艮", "巽"): "山风蛊",
    ("艮", "兑"): "山泽损",
    
    # 巽宫八卦
    ("巽", "巽"): "巽为风",
    ("巽", "乾"): "风天小畜",
    ("巽", "坤"): "风地观",
    ("巽", "坎"): "风水涣",
    ("巽", "离"): "风火家人",
    ("巽", "震"): "风雷益",
    ("巽", "艮"): "风山渐",
    ("巽", "兑"): "风泽中孚",
    
    # 兑宫八卦
    ("兑", "兑"): "兑为泽",
    ("兑", "乾"): "泽天夬",
    ("兑", "坤"): "泽地萃",
    ("兑", "坎"): "泽水困",
    ("兑", "离"): "泽火革",
    ("兑", "震"): "泽雷随",
    ("兑", "艮"): "泽山咸",
    ("兑", "巽"): "泽风大过"
}

# 八卦符号对应的Unicode字符
BAGUA_SYMBOLS = {
    "乾": "☰", "兑": "☱", "离": "☲", "震": "☳",
    "巽": "☴", "坎": "☵", "艮": "☶", "坤": "☷"
}

def normalize_number(num_str):
    """处理输入数字：忽略前导零，转换为整数"""
    if not num_str.strip():
        return 0
    num_str = num_str.lstrip('0')
    if not num_str:
        return 0
    try:
        return int(num_str)
    except ValueError:
        return 0

def calculate_trigram(num):
    """计算八卦符号"""
    remainder = num % 8
    return BAGUA_MAP[remainder if remainder != 0 else 8]

def calculate_yao(num):
    """计算爻位置"""
    remainder = num % 6
    return remainder if remainder != 0 else 6

def get_hexagram_name(upper, lower):
    """根据上下卦获取六十四卦名称"""
    return HEXAGRAM_MAP.get((upper, lower), f"{upper}上{lower}下卦")

def generate_prompt(question, hexagram_name, moving_yao):
    """生成大模型解卦提示词"""
    return f"命主所问事情为「{question}」，{hexagram_name}卦第{moving_yao}爻意味着什么呢？请解卦。"

def display_result(num1_str, num2_str, num3_str, question):
    """显示计算结果"""
    # 处理输入并计算
    num1_val = normalize_number(num1_str)
    num2_val = normalize_number(num2_str)
    num3_val = normalize_number(num3_str)
    
    lower_trigram = calculate_trigram(num1_val)
    upper_trigram = calculate_trigram(num2_val)
    moving_yao = calculate_yao(num3_val)
    hexagram_name = get_hexagram_name(upper_trigram, lower_trigram)
    
    # 显示卦象
    col1, col2 = st.columns(2)
    col1.metric("下卦", f"{lower_trigram} {BAGUA_SYMBOLS[lower_trigram]}", 
               f"输入: {num1_str}")
    col2.metric("上卦", f"{upper_trigram} {BAGUA_SYMBOLS[upper_trigram]}", 
               f"输入: {num2_str}")
    
    st.metric("爻位置", f"第{moving_yao}爻", f"输入: {num3_str}")
    
    st.success(f"**六十四卦:** {hexagram_name}")
    
    # 生成并显示提示词
    prompt = generate_prompt(question, hexagram_name, moving_yao)
    st.divider()
    st.markdown("### 大模型解卦提示词")
    st.code(prompt, language="markdown")
    
    # 保存提示词到session state
    st.session_state.prompt = prompt
    
    # 添加复制按钮
    if st.button("复制提示词", key="copy_button"):
        # 使用JavaScript实现复制功能
        js = f"""
        <script>
        function copyToClipboard() {{
            const textArea = document.createElement('textarea');
            textArea.value = `{prompt}`;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            alert('提示词已复制到剪贴板！');
        }}
        copyToClipboard();
        </script>
        """
        st.components.v1.html(js, height=0)

def main():
    # 页面设置
    st.set_page_config(
        page_title="易经解卦应用",
        page_icon="☯️",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    # 初始化session state
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    if 'result_data' not in st.session_state:
        st.session_state.result_data = {}
    
    # 应用标题
    st.title("☯️ 易经解卦应用")
    st.markdown("《易经》是中国最古老、最深刻的哲学经典之一，通过数字输入预测吉凶，揭示事物发展规律。")
    
    # 分栏布局 - 左侧输入，右侧结果
    col_input, col_result = st.columns([1, 1])
    
    with col_input:
        # 输入区域
        with st.form("iching_form"):
            st.markdown("### 输入卦象数字")
            
            num1 = st.text_input("下卦数字", value="", 
                                help="此数字决定下卦，如123")
            num2 = st.text_input("上卦数字", value="", 
                                help="此数字决定上卦，如456")
            num3 = st.text_input("爻数字", value="", 
                                help="此数字决定爻位置，如789")
            
            question = st.text_area("求问事项", "",
                                  help="请清晰描述您想要求问的事情")
            
            submitted = st.form_submit_button("解卦")
            
            if submitted:
                st.session_state.submitted = True
                st.session_state.result_data = {
                    'num1': num1,
                    'num2': num2,
                    'num3': num3,
                    'question': question
                }
    
    # 使用说明放在下方
    with st.expander("使用说明", expanded=False):
        st.info("""
        **计算方法说明：**
        1. **下卦数字**：第一个三位数除以8的余数决定下卦
        2. **上卦数字**：第二个三位数除以8的余数决定上卦
        3. **爻数字**：第三个数除以6的余数决定爻位置
        4. **前导零处理**：如001视为1，000视为0
        5. **余数规则**：余数0视为8（卦）或6（爻）
        """)
    
    # 结果显示在右侧
    if st.session_state.submitted:
        with col_result:
            st.markdown("### 解卦结果")
            data = st.session_state.result_data
            display_result(data['num1'], data['num2'], data['num3'], data['question'])
    
    # 底部说明
    st.divider()
    st.markdown("""
    **关于易经解卦**  
    此应用基于《易经》原理，使用傅佩荣老师所授的数字卦预测方法。解卦结果仅供参考，
    具体应用需结合个人实际状况灵活理解。
    """)

if __name__ == "__main__":
    main()