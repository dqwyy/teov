import json
import requests
from pathlib import Path

# 输入和输出文件路径（与脚本同目录）
INPUT_FILE = Path("teov-zh.json")
OUTPUT_FILE = Path("teov-zh.update.json")

# API 地址模板
API_URL_TEMPLATE = "https://api.vtbs.moe/v1/detail/{}"

def fetch_follower(uid: str) -> float | None:
    """从 API 获取指定 uid 的粉丝数（原始整数），失败返回 None"""
    url = API_URL_TEMPLATE.format(uid)
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if "follower" in data:
                return float(data["follower"])
        return None
    except Exception:
        return None

def convert_to_wan(follower_int: float) -> float:
    """将整数粉丝数转换为万，四舍五入保留一位小数"""
    return round(follower_int / 10000.0, 1)

def main():
    # 读取原始 JSON
    if not INPUT_FILE.exists():
        print(f"错误：输入文件 {INPUT_FILE} 不存在")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    bili_list = data.get("bili", [])
    updated_count = 0
    for item in bili_list:
        uid = item.get("uid")
        if not uid:
            continue

        new_follower_int = fetch_follower(uid)
        if new_follower_int is not None:
            new_follower_wan = convert_to_wan(new_follower_int)
            item["follower"] = new_follower_wan
            updated_count += 1
            print(f"更新 {item['name']} (UID:{uid}): {new_follower_wan} 万")
        else:
            print(f"未收录或更新失败，保留原值: {item['name']} (UID:{uid})")

    # 将 bili 列表按 follower 降序排序
    bili_list.sort(key=lambda x: x["follower"], reverse=True)
    data["bili"] = bili_list
    data["count"] = len(bili_list)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent='\t')  # 使用 tab 缩进

    print(f"更新完成。共处理 {len(bili_list)} 条记录，成功更新 {updated_count} 条。")
    print(f"结果已保存至 {OUTPUT_FILE}")
    # 等待用户按键后退出
    input("按回车键退出...")

if __name__ == "__main__":
    main()