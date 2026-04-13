#!/bin/bash
# 历史人物对话启动脚本

FIGURES_DIR="/Users/shimmer/.openclaw/workspace/historical_figures"
PERSONAS_DIR="$FIGURES_DIR/personas"

echo "🏛️  欢迎来到历史人物对话系统"
echo "================================"
echo ""

# 显示朝代选择
show_dynasties() {
    echo "请选择朝代："
    echo ""
    echo "  1) 唐朝 (618-907) - 盛世大唐，诗歌黄金时代"
    echo "  2) 宋朝 (960-1279) - 文化繁荣，理学兴起"
    echo "  3) 元朝 (1271-1368) - 疆域辽阔，戏曲兴盛"
    echo "  4) 明朝 (1368-1644) - 君主集权，海禁与开放并存"
    echo "  5) 清朝 (1644-1912) - 最后一个封建王朝"
    echo ""
}

# 显示人物选择
show_figures() {
    local dynasty=$1
    echo ""
    echo "【$dynasty】可选人物："
    echo ""
    
    case $dynasty in
        "唐朝")
            echo "  1) 李世民 - 唐太宗，贞观之治的开创者"
            echo "  2) 李白 - 诗仙，浪漫主义诗人"
            echo "  3) 杜甫 - 诗圣，现实主义诗人"
            echo "  4) 武则天 - 中国历史上唯一的女皇帝"
            echo "  5) 玄奘 - 西行取经，佛学大师"
            ;;
        "宋朝")
            echo "  1) 赵匡胤 - 宋太祖，杯酒释兵权"
            echo "  2) 苏轼 - 东坡居士，全才文人"
            echo "  3) 李清照 - 婉约词宗，千古第一才女"
            echo "  4) 岳飞 - 精忠报国，民族英雄"
            echo "  5) 朱熹 - 理学集大成者"
            ;;
        "元朝")
            echo "  1) 忽必烈 - 元世祖，元朝建立者"
            echo "  2) 关汉卿 - 元曲四大家之首"
            echo "  3) 郭守敬 - 天文水利专家"
            ;;
        "明朝")
            echo "  1) 朱元璋 - 明太祖，洪武之治"
            echo "  2) 王阳明 - 心学大师，知行合一"
            echo "  3) 郑和 - 七下西洋，航海家"
            echo "  4) 李时珍 - 《本草纲目》作者"
            echo "  5) 徐霞客 - 《徐霞客游记》作者"
            ;;
        "清朝")
            echo "  1) 康熙 - 清圣祖，平定三藩"
            echo "  2) 曹雪芹 - 《红楼梦》作者"
            echo "  3) 林则徐 - 虎门销烟，民族英雄"
            echo "  4) 曾国藩 - 晚清名臣，洋务运动领袖"
            ;;
    esac
    echo ""
}

# 获取人物ID
get_figure_id() {
    local dynasty=$1
    local choice=$2
    
    case $dynasty in
        "唐朝")
            case $choice in
                1) echo "lishimin" ;;
                2) echo "libai" ;;
                3) echo "dufu" ;;
                4) echo "wuzetian" ;;
                5) echo "xuanzang" ;;
            esac
            ;;
        "宋朝")
            case $choice in
                1) echo "zhaokuangyin" ;;
                2) echo "sushi" ;;
                3) echo "liqingzhao" ;;
                4) echo "yuefei" ;;
                5) echo "zhuxi" ;;
            esac
            ;;
        "元朝")
            case $choice in
                1) echo "hubilie" ;;
                2) echo "guanhanging" ;;
                3) echo "guoshoujing" ;;
            esac
            ;;
        "明朝")
            case $choice in
                1) echo "zhuyuanzhang" ;;
                2) echo "wangyangming" ;;
                3) echo "zhenghe" ;;
                4) echo "lishizhen" ;;
                5) echo "xuxiake" ;;
            esac
            ;;
        "清朝")
            case $choice in
                1) echo "kangxi" ;;
                2) echo "caoxueqin" ;;
                3) echo "linzexu" ;;
                4) echo "zengguofan" ;;
            esac
            ;;
    esac
}

# 获取人物名称
get_figure_name() {
    local dynasty=$1
    local choice=$2
    
    case $dynasty in
        "唐朝")
            case $choice in
                1) echo "李世民" ;;
                2) echo "李白" ;;
                3) echo "杜甫" ;;
                4) echo "武则天" ;;
                5) echo "玄奘" ;;
            esac
            ;;
        "宋朝")
            case $choice in
                1) echo "赵匡胤" ;;
                2) echo "苏轼" ;;
                3) echo "李清照" ;;
                4) echo "岳飞" ;;
                5) echo "朱熹" ;;
            esac
            ;;
        "元朝")
            case $choice in
                1) echo "忽必烈" ;;
                2) echo "关汉卿" ;;
                3) echo "郭守敬" ;;
            esac
            ;;
        "明朝")
            case $choice in
                1) echo "朱元璋" ;;
                2) echo "王阳明" ;;
                3) echo "郑和" ;;
                4) echo "李时珍" ;;
                5) echo "徐霞客" ;;
            esac
            ;;
        "清朝")
            case $choice in
                1) echo "康熙" ;;
                2) echo "曹雪芹" ;;
                3) echo "林则徐" ;;
                4) echo "曾国藩" ;;
            esac
            ;;
    esac
}

# 主流程
main() {
    while true; do
        show_dynasties
        read -p "请输入数字选择朝代 (1-5): " dynasty_choice
        
        case $dynasty_choice in
            1) dynasty="唐朝" ;;
            2) dynasty="宋朝" ;;
            3) dynasty="元朝" ;;
            4) dynasty="明朝" ;;
            5) dynasty="清朝" ;;
            *) 
                echo "无效选择，请重新输入"
                continue
                ;;
        esac
        
        show_figures "$dynasty"
        read -p "请输入数字选择人物: " figure_choice
        
        figure_id=$(get_figure_id "$dynasty" "$figure_choice")
        figure_name=$(get_figure_name "$dynasty" "$figure_choice")
        
        if [ -z "$figure_id" ]; then
            echo "无效选择，请重新输入"
            continue
        fi
        
        echo ""
        echo "✅ 您选择了【$dynasty】的 $figure_name"
        echo ""
        echo "正在启动对话..."
        echo ""
        echo "💡 提示："
        echo "   - 输入 '切换' 可以更换人物"
        echo "   - 输入 '退出' 结束对话"
        echo "   - 直接输入内容与历史人物对话"
        echo ""
        
        # 读取人物设定
        if [ -f "$PERSONAS_DIR/$figure_id.md" ]; then
            persona=$(cat "$PERSONAS_DIR/$figure_id.md")
            echo "=== 人物设定已加载 ==="
            echo ""
            echo "系统提示：你现在是以下的历史人物..."
            echo ""
        else
            echo "⚠️  人物设定文件不存在，使用默认设定"
            echo ""
        fi
        
        # 这里可以添加与OpenClaw的集成
        echo "📝 请直接在聊天窗口中与 $figure_name 对话"
        echo ""
        
        read -p "按回车键继续选择其他人物，或输入 '退出' 结束: " continue_choice
        if [ "$continue_choice" = "退出" ]; then
            echo ""
            echo "感谢使用历史人物对话系统，再见！"
            exit 0
        fi
        
        echo ""
    done
}

main
