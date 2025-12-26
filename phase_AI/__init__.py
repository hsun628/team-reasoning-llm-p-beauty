from otree.api import *
from openai import OpenAI
import random

client = OpenAI(api_key = "API_KEY")

class Group(BaseGroup):
    gpt_reason = models.LongStringField() # 儲存 GPT 生成的理由
    winner_type = models.StringField()    # 紀錄是 'Human' 還是 'AI' 贏了

def call_gpt_generate(prompt_text):
    """根據指令生成 AI 理由"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"請根據以下情境生成一個決策理由：{prompt_text}"}]
    )
    return response.choices[0].message.content

def call_gpt_judge(reason_a, reason_b):
    """擔任評審，判斷哪一個理由較清楚"""
    # 這裡使用隨機順序餵給 GPT，確保它不知道誰是玩家
    reasons = [("A", reason_a), ("B", reason_b)]
    random.shuffle(reasons)
    
    prompt = f"""
    以下有兩個決策理由，請忽略其來源，僅針對『邏輯清晰度』與『說服力』進行評分。
    理由 1: {reasons[0][1]}
    理由 2: {reasons[1][1]}
    請僅回答『理由 1』或『理由 2』哪一個更好，並給出一個簡短原因。
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "你是一個公正的實驗評審。"},
                  {"role": "user", "content": prompt}]
    )
    result = response.choices[0].message.content
    
    # 根據 GPT 的回答判定是 A 還是 B 贏
    if "理由 1" in result:
        return "Human" if reasons[0][0] == "A" else "AI"
    else:
        return "AI" if reasons[0][0] == "A" else "Human"

def set_payoffs(subsession):
    for group in subsession.get_groups():
        # 1. 取得該組隨機一位玩家的理由作為代表 (或根據你的邏輯挑選)
        representative_player = random.choice(group.get_players())
        human_reason = representative_player.reason
        
        # 2. GPT 生成自己的理由
        group.gpt_reason = call_gpt_generate("這是一個猜數字遊戲，目標是平均值的 2/3...")
        
        # 3. GPT 擔任評審進行盲測
        group.winner_type = call_gpt_judge(human_reason, group.gpt_reason)
        
        # 4. 根據勝負給予報酬 (範例：如果人類贏了，全組加分)
        for p in group.get_players():
            if group.winner_type == "Human":
                p.payoff += cu(50)