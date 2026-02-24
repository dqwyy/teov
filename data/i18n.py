import json
import copy

teo_translation_map = {
	"女": "姿娘",
	"男": "打埠",
	"杂谈": "鋸弦",
	"游戏": "遊戲",
	"绘画": "畵畵",
	"(个人势)": "(家己)"
}

en_translation_map = {
	"女": "Female",
	"男": "Male",
	"杂谈": "Chat",
	"游戏": "Game",
	"唱歌": "Sing",
	"绘画": "Draw",
	"(个人势)": "(Indie)",
	"、": ", "
}

def translate_text(text: str, trans_map: dict) -> str:
	"""
	对文本进行全局子串替换翻译。
	按键长度降序替换，避免短键错误覆盖长键。
	"""
	if not isinstance(text, str):
		return text
	items = sorted(trans_map.items(), key=lambda x: len(x[0]), reverse=True)
	for old, new in items:
		text = text.replace(old, new)
	return text

def main():
	input_file = "teov-zh.json"
	teo_output = "teov-teo.json"
	en_output = "teov-en.json"

	# 读取原始 JSON
	with open(input_file, 'r', encoding='utf-8') as f:
		data = json.load(f)

	# 深拷贝两份，分别用于潮州话和英文翻译
	data_teo = copy.deepcopy(data)
	data_en = copy.deepcopy(data)

	# 翻译潮州话版本
	for item in data_teo.get("bili", []):
		for field in ["gender", "content", "affiliation"]:
			if field in item:
				item[field] = translate_text(item[field], teo_translation_map)

	with open(teo_output, 'w', encoding='utf-8') as f:
		json.dump(data_teo, f, ensure_ascii=False, indent=2, separators=(',', ': '))

	# 翻译英文版本
	for item in data_en.get("bili", []):
		for field in ["gender", "content", "affiliation"]:
			if field in item:
				item[field] = translate_text(item[field], en_translation_map)

	with open(en_output, 'w', encoding='utf-8') as f:
		json.dump(data_en, f, ensure_ascii=False, indent=2, separators=(',', ': '))

	print(f"翻译完成：已生成 {teo_output}（潮州话）和 {en_output}（英文）")
	input("按回车键退出...")  # 等待用户按键后退出

if __name__ == "__main__":
	main()