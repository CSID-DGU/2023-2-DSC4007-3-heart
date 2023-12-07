from flask import Flask,render_template
from flask import request, jsonify
#from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
#CORS(app)

API_KEY = os.getenv("api_key")

#chat gpt api불러오기
client = OpenAI(
    api_key = API_KEY
)

def chatcompletion(user_input):
    output = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=1,
        presence_penalty=0,
        frequency_penalty=0,
        max_tokens=2000,
        messages=[
            {"role": "user", "content": f"{user_input}."},
            {"role": "system", "content": "3줄로 요약해주기"},
            {"role": "system", "content": "한국어로 대답하고 존댓말로 대답하기"},
            {"role": "system", "content": "노인과 관련된 답변하기"}
        ]
    )

    print(output)
    chatgpt_output = output.choices[0].message.content#gpt 답변
    print(chatgpt_output)
    return chatgpt_output 

def chat(user_input):
    chatgpt_raw_output = chatcompletion(user_input)
    return chatgpt_raw_output 

def get_response(userText):
    return chat(userText)

@app.route("/")
def index():
    return render_template("index.html")

type=""
@app.route("/get")
def get_bot_response():
    global type
    userText = request.args.get('msg')
    options = ["1.생활지원", "2.주거지원", "3.건강의료", "4.고용,일자리", "5.돌봄","6.기타"]
    questions_and_answers = [{
            "question": "노인 목욕비 지원사업 지원 내용 알려주세요.",
            "answer": "연 50,000원(5,000원권*10매) [*10매 산출 = 분기별 3매+3분기(하절기) 1매] 입니다."
        },
        {
            "question": "저소득층 노인을 위한 치아 관련 지원제도가 있나요?",
            "answer": "네.'의료급여 노인틀니'는 만 65세 이상 의료급여수급권자가 대상이며, 신청방법은 치과 병의원에서 국민건강보험공단에전산 등록 제출하거나 치과 병의원에서 발급받은 틀니등록 신청서를 관할 시.군.구청 또는 읍.면.동에 방문하여 제출, 승인 후 틀니를 시술받습니다. 급여대상은 레진상 완전틀니, 금속상 완전틀니와 부분틀니이며 7년에 1회 지원됩니다. 틀니의 본인 부담은 입원,외래 구분없이 1종 수급권자는 5%, 2종 수급권자는 15%를 부담합니다."
        },
   
        {
            "question": "독거노인·장애인 응급안전안심서비스는 무엇인가요?",
            "answer": "독거노인과 장애인의 가정에 게이트웨이, 화재감지기 등을 설치하여 화재, 질병 등 응급상황 발생 시 119에 자동으로 신고하고 응급관리요원에게 알려 대상자가 응급상황에 신속하게 대처하는 지원 체계를 구축합니다."
        },
        {
            "question": "무료양로시설 신청 대상은 누구인가요?",
            "answer": "노인장기요양보험법 제15조에 따른 수급자 중 시설 급여 대상자 입니다."
            +"- 장기요양 1~2등급"
            +"- 장기요양 3~5등급자 중 불가피한 사유, 치매 등으로 등급판정위원회에서 시설급여 대상자로 판정을 받은 자"
        },
    
    
        {
            "question": "노인 틀니 지원 사업에 대해 알려주세요.",
            "answer": "만 65세 이상 의료급여 수급권자를 대상으로 하며, 치과에서 발급받은 신청서를 관할 구청 또는 동주민센터 방문하여 제출해주시면 됩니다."
        },
        {
            "question": "노인 무릎 인공관절수술 지원 대상 알려주세요.",
            "answer": "신청일 기준 만 60세 이상(1963년생 이상)으로, ①의료급여 1·2종 ②국민기초생활수급자 ③차상위계층 ④한부모가족이 기준이 됩니다. 대상질환은 건강보험급여 '인공관절치환술(슬관절)' 인정기준에 준하는 질환자입니다. 지원대상자 선정통보 전 발생한 수술비 등 비용은 지원 제외됩니다."
        },
        {
            "question": "노인일자리 사업 신청 방법 알려주세요.",
            "answer": "신분증 지참 후 노인일자리 사업 수행기관 6개소 또는 온라인(복지로)에서 신청하시면 됩니다."
        },
        {
            "question": "노인일자리 사업 접수는 어디에 해야하나요?",
            "answer": "부산사상시니어클럽 (302-2210) 백양대로768번길 63-6(덕포동), 사상구노인복지관 (325-7555) 가야대로196번길 51(학장동), 대한노인회 사상구지회 (305-3679) 사상로319번길 6(덕포동), 백양종합사회복지관 (305-4286) 모라로192번길 20-33(모라동), 사상구종합사회복지관 (314-8948) 백양대로 527(주례동), 학장종합사회복지관 (311-4017) 학감대로49번길 28-70(학장동)"
                +"다음과 같은 노인일자리 사업 수행기관 6개소 입니다."
        },
        {
            "question": "노인맞춤돌봄서비스의 서비스 대상을 자세히 알려주세요.",
            "answer": "만 65세 이상 국민기초생활보장수급자, 차상위계층 또는 기초연금 수급자로서 유사중복사업 자격에 해당되지 않는 자(다만, 시장,군수,구청장이 서비스가 필요하다고 인정하는 경우 예외적으로 제공 가능) 입니다."
                +"- 독거,조손,고령 부부 가구 노인 등 돌봄이 필요한 노인"
                +"- 신체적 기능 저하, 정신적 어려움(인지저하, 우울감 등) 등으로 돌봄이 필요한 노인"
                +"- 고독사 및 자살 위험이 높은 노인"
        },
        {
            "question": "노인맞춤돌봄서비스에서 제공되는 서비스는 무엇인가요?",
            "answer": "안전지원, 사회참여, 생활교육, 일상생활지원 같은 직접 서비스랑 민간후원 자원 연계 서비스를 제공하며, 개인별 조사와 상담을 통해 개인별 돌봄 욕구 및 필요정도에 따라 서비스 내용, 제공시간, 제공주기 등을 맞춤형으로 결정합니다."
        }
    
    ]
    
    
    if userText in options:
        type=userText
        return f"{userText}을 선택하셨습니다."
    elif "홍길동" in userText and "-" in userText:
        return f"신원확인 되었습니다. 궁금하신 사항을 구체적으로 말씀해주세요. "
    elif "홍길동" in userText and "-" not in userText:
        return f"잘못된 정보입니다. 다시 입력해주세요."
    elif userText in [qa["question"] for qa in questions_and_answers]:
        for qa in questions_and_answers:
            if qa["question"]==userText:
                return qa["answer"]
    else:
        return chatcompletion(userText)

if __name__ == "__main__":
    app.run(debug=True)