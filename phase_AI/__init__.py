from otree.api import *
from openai import OpenAI
import random

my_api_key = "API_KEY"
model_used = "gpt-5"


client = OpenAI(api_key = my_api_key)

class Group(BaseGroup):
    gpt_reason = models.LongStringField() 
    winner_type = models.StringField() 

def gpt_generate(participant_decision):
    generate_prompt = "prompt"

    response = client.chat.completions.create(
        model = model_used,
        messages = [
            {"role": "system", "content": generate_prompt},
            {"role": "user", "content": f"請針對以下受試者決策數字和實驗說明生成一個做出此決策的理由：{participant_decision}"}]
    )
    return response.choices[0].message.content

def gpt_judge(reason_a, reason_b):
    reasons = [("A", reason_a), ("B", reason_b)]
    random.shuffle(reasons)
    
    judge_prompt = f"""
    以下有兩個決策理由，請忽略其來源，僅針對『邏輯清晰度』與『說服力』進行評分。
    理由 1: {reasons[0][1]}
    理由 2: {reasons[1][1]}
    請僅回答『理由 1』或『理由 2』。
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": judge_prompt},
                  {"role": "user", "content": 請選擇你認為較清楚地說明決策思考過程的理由。請僅回答『理由 1』或『理由 2』。}]
    )
    result = response.choices[0].message.content
    
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